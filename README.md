# CyberLab

CyberLab is a root-free, Termux-friendly **authorized security assessment toolkit**.

## Features

- TCP port discovery
- Service probing
- DNS resolution checks
- HTTP security-header audit
- TLS inspection
- Rule-based findings and transparent risk scoring
- JSON and HTML reports
- Scan history
- Interactive menu
- Command-line mode
- Standard-library Python

## Run

```bash
cd ~/CyberLab
python3 cyberlab.py
```

CLI examples:

```bash
python3 cyberlab.py --target 192.168.1.1 --scan
python3 cyberlab.py --target 192.168.1.1 --assess
```

Only test systems and networks you own or have explicit permission to assess.
