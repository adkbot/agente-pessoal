
from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn
import asyncio
import json
import base64
import os
import cv2
import numpy as np
from dotenv import load_dotenv

# Import AgentCore (Multimodal)
from agent_core import AgentCore
import vision_utils

# Load Env
load_dotenv()

# Initialize FastAPI
app = FastAPI(title="AntiGravity Agent Portal")

# Setup Templates
templates = Jinja2Templates(directory="templates")

# --- VISION MONKEYPATCH ---
# Store the latest frame received from the User's Browser
latest_frame_bgr = None

def patched_capturar_tela_cv():
    """Patched version of vision_utils.capturar_tela_cv that returns the WS frame."""
    global latest_frame_bgr
    if latest_frame_bgr is not None:
        return latest_frame_bgr.copy()
    else:
        # Return black image if no stream yet to prevent errors
        return np.zeros((720, 1280, 3), dtype=np.uint8)

# Apply Patch
print("🔧 Applying Monkeypatch to vision_utils.capturar_tela_cv...")
vision_utils.capturar_tela_cv = patched_capturar_tela_cv
# --------------------------

# Global Agent Instance
agent: AgentCore = None
agent_loop_task = None

@app.on_event("startup")
async def startup_event():
    global agent
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in env!")
        return

    # Callback placeholders
    agent = AgentCore(api_key=api_key)
    print("🚀 AgentCore Initialized inside Server")

@app.on_event("shutdown")
async def shutdown_event():
    if agent:
        agent.stop()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "system_name": "AntiGravity Agent"})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global latest_frame_bgr
    await websocket.accept()
    
    # Update Agent Callbacks to route to this WebSocket
    async def send_text_to_client(text):
        try:
            await websocket.send_json({"type": "agent_message", "text": text})
        except:
            pass
            
    async def send_status_to_client(status):
        try:
            await websocket.send_json({"type": "system_status", "status": status})
        except:
            pass
            
    async def send_skill_log(log):
         try:
            await websocket.send_json({"type": "skill_log", "log": log})
         except:
            pass

    if agent:
        agent.on_text = lambda t: asyncio.create_task(send_text_to_client(t))
        agent.on_status = lambda s: asyncio.create_task(send_status_to_client(s))
        agent.on_skill_log = lambda l: asyncio.create_task(send_skill_log(l))

    # Start Agent Logic Background Task if not running
    if agent and not agent.running:
        asyncio.create_task(agent.run_with_reconnect())

    # Task to stream Audio Output from Agent -> WebSocket
    async def stream_audio_output():
        try:
            while True:
                audio_data = await agent.audio_output_queue.get()
                # Send as binary
                await websocket.send_bytes(audio_data)
        except Exception as e:
            print(f"Audio output stream ended: {e}")

    audio_task = asyncio.create_task(stream_audio_output())

    try:
        await websocket.send_json({"type": "system_status", "status": "Connected to Cloud Agent ☁️"})
        
        while True:
            # Handle messages
            message = await websocket.receive()
            
            if "text" in message:
                try:
                    data = json.loads(message["text"])
                    if data.get("type") == "command":
                        cmd = data.get("text")
                        print(f"Command received: {cmd}")
                        await agent.send_text(cmd)
                except json.JSONDecodeError:
                    pass
            
            elif "bytes" in message:
                data = message["bytes"]
                if len(data) > 0:
                    msg_type = data[0] 
                    payload = data[1:]
                    
                    if msg_type == 0: # Audio
                        struct = {"data": payload, "mime_type": "audio/pcm"}
                        if not agent.audio_input_queue.full():
                             agent.audio_input_queue.put_nowait(struct)
                             
                    elif msg_type == 1: # Video (JPEG)
                        # 1. Update Global Frame for Skills (OCR/VisionTools)
                        try:
                            nparr = np.frombuffer(payload, np.uint8)
                            img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                            if img_np is not None:
                                latest_frame_bgr = img_np
                        except Exception as e:
                            print(f"Frame decode error: {e}")

                        # 2. Send to AgentCore for Gemini Vision
                        # AgentCore expects base64 string
                        b64_img = base64.b64encode(payload).decode('utf-8')
                        if not agent.screen_input_queue.full():
                            agent.screen_input_queue.put_nowait(b64_img)

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WS Error: {e}")
    finally:
        audio_task.cancel()
        # Don't stop the agent, it might be persistent (or stop it if single user)
        # For now, let's keep running to avoid cold starts, or stop to save resources.
        pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
