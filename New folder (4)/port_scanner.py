#!/usr/bin/env python3
"""
Simple TCP Port Scanner with banner grabbing and multithreading.
"""

import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Tuple, List

# --- Config / ANSI colors for nicer terminal output ---
OPEN_COLOR = "\033[92m"   # green
CLOSE_COLOR = "\033[91m"  # red
RESET = "\033[0m"

# --- Helper: resolve hostname to IP ---
def resolve_host(host: str) -> str:
    try:
        return socket.gethostbyname(host)
    except Exception:
        return host  # assume it's already an IP or return as-is

# --- Get banner (attempts to read initial data from an open socket) ---
def get_banner(sock: socket.socket) -> str:
    try:
        sock.settimeout(1.0)
        banner = sock.recv(1024)
        return banner.decode(errors="ignore").strip()
    except Exception:
        return ""

# --- Scan a single port; return tuple (port, is_open, service_name, banner) ---
def scan_port(ip: str, port: int, timeout: float = 1.0) -> Tuple[int, bool, str, str]:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((ip, port))
        if result == 0:
            # Port open
            try:
                service = socket.getservbyport(port, "tcp")
            except Exception:
                service = "unknown"
            banner = get_banner(sock)
            sock.close()
            return (port, True, service, banner)
        else:
            sock.close()
            return (port, False, "", "")
    except Exception:
        try:
            sock.close()
        except Exception:
            pass
        return (port, False, "", "")

# --- Pretty print results ---
def print_results(results: List[Tuple[int, bool, str, str]]):
    print("\nScan results:")
    print(f"{'PORT':<8}{'STATUS':<10}{'SERVICE':<15}{'BANNER'}")
    print("-" * 60)
    for port, is_open, service, banner in sorted(results, key=lambda x: x[0]):
        status = f"{OPEN_COLOR}OPEN{RESET}" if is_open else f"{CLOSE_COLOR}CLOSED{RESET}"
        service_display = service if service else "-"
        banner_display = banner if banner else "-"
        print(f"{port:<8}{status:<10}{service_display:<15}{banner_display}")

# --- Main scan function: spawn threads and track progress ---
def port_scan(target: str, start_port: int, end_port: int, max_workers: int = 100):
    ip = resolve_host(target)
    ports = range(start_port, end_port + 1)
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_port = {executor.submit(scan_port, ip, p): p for p in ports}

        total = len(ports)
        done = 0
        for future in as_completed(future_to_port):
            port_result = future.result()
            results.append(port_result)
            done += 1
            # dynamic progress (overwrites same line)
            sys.stdout.write(f"\rScanned {done}/{total} ports")
            sys.stdout.flush()

    print()  # newline after progress
    print_results(results)

# --- Entry point ---
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python port_scanner.py <target> <start_port> <end_port>")
        print("Example: python port_scanner.py 127.0.0.1 1 1024")
        sys.exit(1)

    tgt = sys.argv[1]
    sp = int(sys.argv[2])
    ep = int(sys.argv[3])

    # Choose max_workers depending on the range size; keep it reasonable to avoid resource strain
    range_size = ep - sp + 1
    mw = 200 if range_size > 1000 else 100

    print(f"Starting scan on {tgt} (ports {sp} to {ep})")
    port_scan(tgt, sp, ep, max_workers=mw)
