<div align="center">

# 📡 Network Packet Analyzer

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![Scapy](https://img.shields.io/badge/Library-Scapy-orange?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

> A Python-based network packet sniffer that captures and analyzes live network traffic — logging IP addresses, protocols, TCP flags, HTTP requests, and DNS queries for educational and lab use.

⚠️ **For educational and authorized lab use only.**

</div>

---

## 📸 Overview

This tool uses the **Scapy** library to intercept and dissect network packets in real time. It identifies key packet metadata including source/destination IPs, transport protocols, HTTP activity, and DNS lookups — logging everything to a rotating log file for later review.

---

## ✨ Features

### 🔍 Packet Analysis
- Captures **IP packets** with source/destination IPs and ports
- Identifies transport protocols: **TCP, UDP, ICMP, IGMP, OSPF**
- Extracts **TCP flags** (SYN, ACK, FIN, RST, etc.)

### 🌐 Protocol-Specific Inspection
| Protocol | Details Captured |
|---|---|
| **HTTP** | Host, path, and request method |
| **DNS** | Query name from DNS question records |
| **TCP** | Flags, source/destination ports |
| **UDP** | Source/destination ports |

### 📝 Logging
- All captured packets saved to `packet_capture_log.txt`
- **Auto-rotating logs** — rotates at 5MB to prevent disk bloat
- Timestamped entries for every packet
- Simultaneous console and file output

### ⚙️ Flexible Options
- Select from available **network interfaces** interactively
- Set a **packet count limit** or run indefinitely
- Apply **BPF filters** (e.g. `tcp port 80`) for targeted capture
- Graceful stop with `Ctrl+C`

---

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- Scapy library
- **Root / Administrator privileges** (required for raw packet capture)

### Installation

```bash
# Clone the repository
git clone https://github.com/sekere01/network-packet-analyzer.git

# Navigate into the directory
cd network-packet-analyzer

# Install dependencies
pip install scapy
```

### Running the Tool

**Linux / macOS** (requires sudo):
```bash
sudo python3 sniffer.py
```

**Windows** (run terminal as Administrator):
```bash
python sniffer.py
```

---

## 📖 Usage

### Interactive Mode
Simply run the script and select your network interface from the list:
```bash
sudo python3 sniffer.py
```

### Command-Line Arguments
```bash
sudo python3 sniffer.py [OPTIONS]
```

| Argument | Description | Example |
|---|---|---|
| `-i`, `--interface` | Network interface to sniff | `-i eth0` |
| `-c`, `--count` | Number of packets to capture (`0` = unlimited) | `-c 100` |
| `-f`, `--filter` | BPF filter expression | `-f "tcp port 80"` |

### Examples
```bash
# Capture 50 packets on eth0
sudo python3 sniffer.py -i eth0 -c 50

# Capture only HTTP traffic
sudo python3 sniffer.py -i eth0 -f "tcp port 80"

# Capture DNS queries only
sudo python3 sniffer.py -i eth0 -f "udp port 53"

# Unlimited capture on all interfaces
sudo python3 sniffer.py -i eth0
```

---

## 📄 Sample Output

```
[2026-03-01 14:23:11] IP Packet:
    Source: 192.168.1.5:54321
    Destination: 8.8.8.8:53
    Protocol: UDP
    [!] DNS Query:
        Query: www.example.com.

[2026-03-01 14:23:12] IP Packet:
    Source: 192.168.1.5:49200
    Destination: 93.184.216.34:80
    Protocol: TCP
    TCP Flags: S
    [!] HTTP Request:
        Host: www.example.com
        Path: /index.html
        Method: GET
```

---

## 📁 Project Structure

```
network-packet-analyzer/
│
├── sniffer.py                  # Main application file
├── packet_capture_log.txt      # Auto-generated capture log
└── README.md                   # Project documentation
```

---

## ⚠️ Ethical Use & Legal Notice

> This tool is intended **strictly for educational purposes** and authorized network environments such as personal lab setups.
>
> - ✅ Use on networks you **own or have explicit permission** to test
> - ✅ Use in isolated **lab/VM environments**
> - ❌ Do NOT use on public, corporate, or any network without written authorization
>
> Unauthorized packet sniffing may violate the **Computer Fraud and Abuse Act (CFAA)**, **GDPR**, and equivalent laws worldwide. Only packet **metadata** is logged — full payloads are not captured to minimize privacy risk.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to open an issue or submit a pull request.
