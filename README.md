# Screenshot-Automate Desktop App

A FastAPI-based backend for desktop window automation and screenshotting, designed for integration with a web frontend and AI-driven workflows.

---

## Features

- **Health check endpoint**
- **List open user-facing windows** (filtered for relevance)
- **Take screenshots of any open window**
- **Automate mouse clicks and typing in any window**
- **(Planned) Retrieve automation logs**

---

## API Endpoints

### 1. `GET /api/v1/health`
**Description:**  
Returns the health status and uptime of the server.

**Response:**
```json
{
  "status": "ok",
  "uptime_seconds": 123
}
```

---

### 2. `GET /api/v1/windows`
**Description:**  
Lists all open, user-facing windows with their IDs, titles, and bounds.

**Response:**
```json
[
  {
    "id": "394",
    "title": "Notes Test",
    "bounds": { "x": 100, "y": 100, "width": 800, "height": 600 }
  },
  ...
]
```

---

### 3. `GET /api/v1/windows/{window_id}/screenshot`
**Description:**  
Returns a PNG screenshot of the specified window's client area.

**Response:**  
- `image/png` binary data

---

### 4. `POST /api/v1/automate`
**Description:**  
Automates actions (mouse clicks and typing) in a specified window.

**Request Body:**
```json
{
  "window_id": "394",
  "actions": [
    { "x": 600, "y": 200, "text": "Hello World" }
  ]
}
```
- Brings the window to the front.
- For each action: moves mouse, clicks, and types text if provided.

**Response:**
```json
{ "status": "ok" }
```

---

### 5. `GET /api/v1/logs?limit=N` *(Planned)*
**Description:**  
Returns the last N log entries from the automation log.

---

## Setup & Requirements

- **Python 3.8+**
- **macOS or Windows** (cross-platform support)
- **Dependencies:**  
  - `fastapi`
  - `uvicorn`
  - `pygetwindow`
  - `pyautogui`
  - `mss`
  - `pydantic`
  - `pywebview`

Install dependencies:
```sh
pip install -r requirements.txt
```

---

## Running the Server and UI

```sh
python src/ui.py
```

- This will start the FastAPI backend and open a native desktop window to the web UI.
- The backend runs at `http://127.0.0.1:8000`.
- The UI is served at `http://127.0.0.1:8000/ui/index.html` (not file://).
- The UI and API must be served from the same origin for full functionality.

---

## Project Structure

```
/dtop-app
  /src
    main.py         # FastAPI backend
    ui.py           # PyWebview launcher
    ...
  /ui               # Frontend HTML/JS for the UI
  requirements.txt
  README.md
```

---

## Notes

- **macOS:**  
  - Grant Accessibility permissions to your terminal or Python app for automation to work.
  - Some system UI windows are filtered out for a cleaner window list.
- **Window IDs:**  
  - IDs may change if you close/reopen windows. Always fetch the latest list before automating.
- **Automation:**  
  - Coordinates are absolute screen positions. Use screenshots to determine the correct values.

---

## Contributing

- Keep code simple and DRY.
- Avoid code duplication and unnecessary mocking.
- Keep files under 200–300 lines; refactor as needed.
- Do not add stubbing or fake data to dev/prod code.

---

## License

MIT 
