#!/usr/bin/env python3
import argparse
import json
import socket
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from modules.scanner import COMMON_PORTS, scan_ports
from modules.service_detect import detect_services
from modules.dns import analyze_dns
from modules.http_audit import audit_http
from modules.tls import audit_tls
from modules.findings import analyze_findings
from modules.score import score_findings
from modules.export import save_json
from modules.html_report import save_html
from modules.history import record

BASE = Path(__file__).resolve().parent
REPORTS = BASE / "reports"
DEFAULT_PORTS = list(COMMON_PORTS)

def banner():
    print("""
╔══════════════════════════════════════╗
║          🛡️  CYBERLAB               ║
║   Authorized Security Assessment     ║
╚══════════════════════════════════════╝
""")

def valid_target(target):
    if not target or len(target) > 253:
        return False
    try:
        socket.getaddrinfo(target, None)
        return True
    except socket.gaierror:
        return False

def host_available(host):
    try:
        r = subprocess.run(["ping", "-c", "1", "-W", "1", host], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=3)
        return r.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False

def prompt_target():
    while True:
        target = input("Target (authorized host): ").strip()
        if valid_target(target): return target
        print("[!] Invalid/unresolvable target.")

def port_scan(host):
    results = scan_ports(host, DEFAULT_PORTS)
    print(f"\n[*] TCP scan: {host}\n" + "-" * 55)
    for r in results:
        if r["state"] == "OPEN": print(f"[OPEN] {r['port']:<5} {r['service']}")
    print("-" * 55)
    print(f"[+] Complete: {sum(r['state']=='OPEN' for r in results)} open")
    return results

def full_assessment(host):
    started = time.perf_counter()
    ports = scan_ports(host, DEFAULT_PORTS)
    open_ports = [r["port"] for r in ports if r["state"] == "OPEN"]
    services = detect_services(host, open_ports)
    findings = analyze_findings(open_ports, services)
    http = audit_http(host, 80) if 80 in open_ports else {"available": False}
    tls = audit_tls(host, 443) if 443 in open_ports else {"available": False}
    dns = analyze_dns(host, 53) if 53 in open_ports else {"available": False}
    score = score_findings(findings, http, tls)
    duration = round(time.perf_counter() - started, 2)
    data = {"tool":"CyberLab","version":"1.0","target":host,"timestamp":datetime.now().isoformat(timespec="seconds"),"duration_seconds":duration,"ports":ports,"open_ports":open_ports,"services":services,"findings":findings,"http_audit":http,"tls_audit":tls,"dns":dns,"score":score}
    print("\n" + "=" * 72 + "\nCYBERLAB SECURITY ASSESSMENT\n" + "=" * 72)
    for r in ports: print(f"{r['port']:<7} {r['state']:<8} {r['service']}")
    print("-" * 72)
    for f in findings:
        print(f"[{f['severity']}] {f['title']} (TCP/{f['port']})\n  {f['recommendation']}")
    print("-" * 72)
    if http.get("available"):
        print("[*] HTTP security-header audit")
        for k,v in http.get("headers",{}).items(): print(f"{k:<24} {v}")
    print(f"\nSECURITY SCORE: {score['score']}/100  Grade: {score['grade']}\nDuration: {duration}s")
    REPORTS.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = save_json(data, REPORTS / f"scan_{stamp}.json")
    html_path = save_html(data, REPORTS / f"scan_{stamp}.html")
    record(data)
    print(f"\n📄 Report saved: {json_path}\n🌐 HTML report saved: {html_path}\n[+] Assessment complete.")
    return data

def main():
    parser = argparse.ArgumentParser(description="CyberLab — authorized security assessment toolkit")
    parser.add_argument("--target", help="Authorized target host/IP")
    parser.add_argument("--scan", action="store_true", help="Run TCP scan")
    parser.add_argument("--assess", action="store_true", help="Run full assessment")
    args = parser.parse_args()
    if args.target and (args.scan or args.assess):
        if not valid_target(args.target): print("[!] Invalid/unresolvable target."); return 2
        full_assessment(args.target) if args.assess else port_scan(args.target)
        return 0
    banner()
    while True:
        print("""
[1] Host availability
[2] TCP port scan
[3] Service detection
[4] Full security assessment
[5] DNS analysis
[6] HTTP header audit
[7] TLS audit
[8] Scan history
[9] Exit
""")
        choice = input("CyberLab > ").strip()
        if choice == "1":
            host=prompt_target(); print(f"[+] {host}: {'ONLINE' if host_available(host) else 'OFFLINE'}")
        elif choice == "2": port_scan(prompt_target())
        elif choice == "3":
            host=prompt_target(); open_ports=[r["port"] for r in scan_ports(host,DEFAULT_PORTS) if r["state"]=="OPEN"]
            for r in detect_services(host,open_ports): print(f"{r['port']:<6} {r['details']}")
        elif choice == "4": full_assessment(prompt_target())
        elif choice == "5": print(json.dumps(analyze_dns(prompt_target(),53),indent=2))
        elif choice == "6": print(json.dumps(audit_http(prompt_target(),80),indent=2))
        elif choice == "7": print(json.dumps(audit_tls(prompt_target(),443),indent=2))
        elif choice == "8": print(json.dumps(record(None,read_only=True),indent=2))
        elif choice == "9": print("Goodbye."); return 0
        else: print("[!] Invalid option.")

if __name__ == "__main__": sys.exit(main())
