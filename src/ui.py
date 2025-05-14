#!/usr/bin/env python3
# PyWebview launcher for the FastAPI app
# Starts the FastAPI server and opens a native window to the web UI

import sys
import os

# Set working directory to project root (parent of src/) and ensure it's in sys.path
APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if APP_ROOT not in sys.path:
    sys.path.insert(0, APP_ROOT)
os.chdir(APP_ROOT)

import webview
import subprocess
import time

if getattr(sys, 'frozen', False):
    # Running as a PyInstaller bundle
    BUNDLE_DIR = sys._MEIPASS
    SRC_PATH = os.path.join(BUNDLE_DIR, 'src')
    PYTHON_EXECUTABLE = '/usr/bin/python3'
    CWD = BUNDLE_DIR
else:
    # Running in dev mode
    APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SRC_PATH = os.path.join(APP_ROOT, 'src')
    PYTHON_EXECUTABLE = sys.executable
    CWD = APP_ROOT

# Prepare environment for subprocess to ensure src is importable
env = os.environ.copy()
env['PYTHONPATH'] = os.path.dirname(SRC_PATH) + os.pathsep + env.get('PYTHONPATH', '')

# Path to the minimal UI HTML file
ui_html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../ui/index.html'))

# Start FastAPI server as a subprocess
server = subprocess.Popen([
    PYTHON_EXECUTABLE, "-m", "uvicorn", "src.main:app", "--host", "127.0.0.1", "--port", "8000"
], cwd=CWD, env=env)  # Set cwd to project root and pass env

try:
    # Wait for the server to start
    time.sleep(2)
    # Open the webview window to the served UI
    webview.create_window("Server Monitor", "http://127.0.0.1:8000/ui/index.html")
    webview.start()
finally:
    # When the window is closed, terminate the server
    server.terminate()
    server.wait() 