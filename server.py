
from fastapi import FastAPI, WebSocket, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn
import asyncio
import json
import os
from main import AntiGravitySystem

# Initialize System
system = AntiGravitySystem()

# Initialize FastAPI
app = FastAPI(title="AntiGravity Agent Portal")

# Setup Templates
templates = Jinja2Templates(directory="templates")

# Store active connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "system_name": system.config['system']['name']})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        await websocket.send_text(json.dumps({"type": "system_status", "status": "connected", "message": "AntiGravity Agent Connected"}))
        while True:
            data = await websocket.receive_text()
            # Process command through system
            # In a real scenario, this would route to system.process_input() and capture output
            # For now, we'll just echo back that we received it
            
            print(f"📥 Web Command: {data}")
            
            # Simple command processing simulation for the web interface
            response = {"type": "command_response", "status": "received", "command": data}
            
            # If it looks like a command the system can handle
            try:
                # We can asynchronously run the process_input
                # But process_input currently prints to stdout. 
                # Ideally we'd redirect that output to the websocket.
                # For this step, we just acknowledge.
                pass 
            except Exception as e:
                response["status"] = "error"
                response["error"] = str(e)
                
            await websocket.send_text(json.dumps(response))
            
    except Exception as e:
        print(f"WebSocket Error: {e}")
    finally:
        manager.disconnect(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
