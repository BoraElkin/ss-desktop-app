from fastapi import FastAPI, Response, HTTPException, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import time
from typing import List, Dict
from .screenshotter import list_windows, screenshot_window, activate_window
import pyautogui

app = FastAPI(root_path="/api/v1")
start_time = time.time()

class Bounds(BaseModel):
    x: int
    y: int
    width: int
    height: int

class Window(BaseModel):
    id: str
    title: str
    bounds: Bounds

class AutomateAction(BaseModel):
    x: int
    y: int
    text: str = ""

class AutomateRequest(BaseModel):
    window_id: str
    actions: List[AutomateAction]

@app.get("/health")
def health():
    uptime = int(time.time() - start_time)
    return JSONResponse({"status": "ok", "uptime_seconds": uptime})

@app.get("/windows", response_model=List[Window])
def get_windows():
    return list_windows()

@app.get("/windows/{window_id}/screenshot")
def get_window_screenshot(window_id: str):
    try:
        png_bytes = screenshot_window(window_id)
        return Response(content=png_bytes, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Window not found or screenshot failed: {e}")

@app.post("/automate")
def automate(req: AutomateRequest):
    try:
        activate_window(req.window_id)
        time.sleep(0.5)
        for action in req.actions:
            pyautogui.moveTo(action.x, action.y)
            pyautogui.click()
            if action.text:
                pyautogui.typewrite(action.text)
            # Log the action
            with open("dtop_automation.log", "a") as logf:
                logf.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} window_id={req.window_id} x={action.x} y={action.y} text={action.text}\n")
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Automation failed: {e}") 