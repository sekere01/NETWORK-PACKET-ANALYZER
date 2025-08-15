#!/usr/bin/env python3
"""
NETWORK PACKET SNIFFER - FOR EDUCATIONAL PURPOSES ONLY

Output will be saved to packet_capture_log.txt in the same directory
as this script. Only metadata is logged (no full payloads for privacy).
"""

from scapy.all import *
from scapy.layers import http
import argparse
import textwrap
from datetime import datetime
import os

# Constants
LOG_FILE = "packet_capture_log.txt"
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5MB max log size

def init_log_file():
    """Initialize log file with header"""
    header = (
        "PACKET CAPTURE LOG - EDUCATIONAL USE ONLY\n"
        f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        "==========================================\n\n"
    )
    with open(LOG_FILE, "w") as f:
        f.write(header)

def write_to_log(entry):
    """Write entry to log file with size management"""
    # Rotate log if it gets too large
    if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > MAX_LOG_SIZE:
        rotate_log()
    
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")

def rotate_log():
    """Rotate log file keeping previous version"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"packet_capture_log_{timestamp}.txt"
    os.rename(LOG_FILE, backup_file)
    print(f"\n[!] Log rotated to {backup_file}")
    init_log_file()

def get_interface():
    """Get available network interfaces"""
    interfaces = get_if_list()
    print("Available interfaces:")
    for i, iface in enumerate(interfaces, 1):
        print(f"{i}. {iface}")
    selection = int(input("Select interface number: ")) - 1
    return interfaces[selection]

def packet_callback(packet):
    """Process each captured packet and log to file"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = ""
    
    # IP Packet Analysis
    if packet.haslayer(IP):
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        protocol = packet[IP].proto
        
        log_entry += f"[{timestamp}] IP Packet:\n"
        log_entry += f"    Source: {src_ip}:{packet.sport if hasattr(packet, 'sport') else 'N/A'}\n"
        log_entry += f"    Destination: {dst_ip}:{packet.dport if hasattr(packet, 'dport') else 'N/A'}\n"
        log_entry += f"    Protocol: {get_protocol_name(protocol)}\n"
        
        # TCP/UDP Analysis
        if packet.haslayer(TCP):
            log_entry += f"    TCP Flags: {packet[TCP].flags}\n"
        elif packet.haslayer(UDP):
            log_entry += "    UDP Packet\n"
    
    # HTTP Analysis
    if packet.haslayer(http.HTTPRequest):
        http_layer = packet[http.HTTPRequest]
        log_entry += "    [!] HTTP Request:\n"
        log_entry += f"        Host: {http_layer.Host.decode()}\n"
        log_entry += f"        Path: {http_layer.Path.decode()}\n"
        log_entry += f"        Method: {http_layer.Method.decode()}\n"
    
    # DNS Analysis
    elif packet.haslayer(DNS):
        log_entry += "    [!] DNS Query:\n"
        if packet.haslayer(DNSQR):  # DNS Question Record
            log_entry += f"        Query: {packet[DNSQR].qname.decode()}\n"
    
    # Write to log and print to console
    if log_entry:
        write_to_log(log_entry)
        print(log_entry.strip())  # Also show in console

def get_protocol_name(proto_num):
    """Convert protocol number to name"""
    protocols = {
        1: "ICMP",
        6: "TCP",
        17: "UDP",
        2: "IGMP",
        89: "OSPF"
    }
    return protocols.get(proto_num, f"Unknown ({proto_num})")

def main():
    print(__doc__)  # Show ethical disclaimer
    init_log_file()
    
    # Argument parsing
    parser = argparse.ArgumentParser(description='Network Packet Sniffer - Educational Use Only')
    parser.add_argument('-i', '--interface', help='Network interface to sniff')
    parser.add_argument('-c', '--count', type=int, default=0, 
                       help='Number of packets to capture (0 for unlimited)')
    parser.add_argument('-f', '--filter', default='', 
                       help='BPF filter (e.g., "tcp port 80")')
    args = parser.parse_args()
    
    interface = args.interface if args.interface else get_interface()
    
    print(f"\n[+] Starting packet capture on {interface}")
    print(f"[+] Filter: {args.filter if args.filter else 'None'}")
    print(f"[+] Logging to: {os.path.abspath(LOG_FILE)}")
    print("[+] Press Ctrl+C to stop\n")
    
    try:
        sniff(iface=interface,
              prn=packet_callback,
              count=args.count,
              filter=args.filter,
              store=0)
    except KeyboardInterrupt:
        print("\n[!] Capture stopped by user")
        write_to_log(f"\n[Capture stopped by user at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
    except PermissionError:
        print("[ERROR] Requires root/admin privileges. Try running with sudo/Admin.")
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        write_to_log(f"[ERROR] {str(e)}")

if __name__ == "__main__":
    main()