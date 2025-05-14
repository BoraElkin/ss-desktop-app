# PyWebview launcher for the FastAPI app
# Starts the FastAPI server and opens a native window to the web UI

import webview
import subprocess
import time
import sys
import os

# Path to the minimal UI HTML file
ui_html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../ui/index.html'))

# Start FastAPI server as a subprocess
server = subprocess.Popen([
    sys.executable, "-m", "uvicorn", "src.main:app", "--host", "127.0.0.1", "--port", "8000"
])

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