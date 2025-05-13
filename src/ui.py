import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import requests
import os

API_BASE = "http://127.0.0.1:8000/api/v1"
LOG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app.log"))

def fetch_health():
    try:
        r = requests.get(f"{API_BASE}/health", timeout=1)
        if r.status_code == 200:
            return True, r.json().get("uptime_seconds", 0)
    except Exception:
        pass
    return False, 0

def read_local_logs():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r", encoding="utf-8", errors="replace") as f:
        return [line.strip() for line in f if line.strip()]

def refresh():
    health, uptime = fetch_health()
    if health:
        status_var.set("UP")
        status_label.config(bg="green", fg="white")
        uptime_var.set(str(uptime))
    else:
        status_var.set("DOWN")
        status_label.config(bg="red", fg="white")
        uptime_var.set("-")
    logs = read_local_logs()
    log_box.config(state='normal')
    log_box.delete(1.0, tk.END)
    log_box.insert(tk.END, "\n".join(logs))
    log_box.config(state='disabled')

def periodic_refresh():
    refresh()
    root.after(2000, periodic_refresh)

root = tk.Tk()
root.title("Server Monitor")

tk.Label(root, text="Server Status:").grid(row=0, column=0, sticky="e")
status_var = tk.StringVar(value="UNKNOWN")
status_label = tk.Label(root, textvariable=status_var, width=8, bg="gray", fg="white")
status_label.grid(row=0, column=1, sticky="w")

tk.Label(root, text="Uptime:").grid(row=1, column=0, sticky="e")
uptime_var = tk.StringVar(value="-")
tk.Label(root, textvariable=uptime_var).grid(row=1, column=1, sticky="w")

tk.Label(root, text="Request Log:").grid(row=2, column=0, columnspan=2, sticky="w")
log_box = ScrolledText(root, width=80, height=15, state='disabled')
log_box.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

tk.Button(root, text="Refresh", command=refresh).grid(row=4, column=0, pady=5)
tk.Button(root, text="Exit", command=root.destroy).grid(row=4, column=1, pady=5)

refresh()
periodic_refresh()
root.mainloop() 