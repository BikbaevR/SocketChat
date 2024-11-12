from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import Dict, List
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

connections: Dict[str, List[WebSocket]] = {}
app.mount("/static", StaticFiles(directory="templates"), name="static")

@app.get("/")
async def get():
    html_content = Path("templates/index.html").read_text(encoding="utf-8")
    return HTMLResponse(content=html_content)

@app.websocket("/ws/{chat_name}")
async def websocket_endpoint(websocket: WebSocket, chat_name: str):
    await websocket.accept()
    if chat_name not in connections:
        connections[chat_name] = []
    connections[chat_name].append(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            for connection in connections[chat_name]:
                await connection.send_text(data)
    except WebSocketDisconnect:
        connections[chat_name].remove(websocket)
