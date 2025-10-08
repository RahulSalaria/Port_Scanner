# Port Scanner

**Project:** Port Scanner Using Python
**Author:** Inlighn Tech (student implementation)

---

## Overview

A simple, multithreaded TCP port scanner written in Python that detects open ports, attempts banner grabbing, and prints a formatted results table. Designed for learning socket programming, multithreading, and basic reconnaissance techniques.

**Important — Legal & Ethical Notice:**
Only scan systems you own or have explicit permission to scan. Unauthorized scanning may be illegal and unethical.

---

## Features

* TCP port scanning using `socket.connect_ex()`
* Banner grabbing via `recv()` when possible
* Multithreaded scanning with `concurrent.futures.ThreadPoolExecutor`
* Dynamic progress counter
* Pretty-printed terminal table with ANSI color output
* Optional CSV and JSON export (example provided)
* No external dependencies — uses Python standard library

---

## Prerequisites

* Python 3.7+ (works with 3.8, 3.9, 3.10, etc.)
* Basic terminal (recommended Linux/macOS/Windows Terminal/PowerShell)
* Network access to the target you intend to scan

---

## Files

* `port_scanner.py` — main scanner script
* `README.md` — project documentation (this file)

PowerShell:

```powershell
python .\port_scanner.py 127.0.0.1 1 1024 | Tee-Object -FilePath scan_output.txt

```

Notes:

* `OPEN` appears in green, `CLOSED` appears in red in ANSI-capable terminals.
* `BANNER` may be empty for services that do not send data immediately (HTTP often requires a request).


## Troubleshooting

* If most ports show `CLOSED`: that is normal. Only a few services are usually exposed.
* If output contains escape sequences like `\x1b[92m`, use a terminal that supports ANSI colors or strip color codes when writing to files.
* If scans seem slow, adjust `max_workers` to a reasonable number (e.g., 100–200) or increase timeouts for slow networks.
