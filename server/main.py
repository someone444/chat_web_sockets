from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

static_path = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/ping")
async def ping():
    return {"status": "ok"}

@app.get("/")
async def get():
    html_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    with open(html_path, "r") as f:
        return HTMLResponse(f.read())

# --- WebSocket Chat Management ---
clients = {}  # Maps username -> websocket

async def broadcast_user_list():
    user_list = "USER_LIST:" + ",".join(clients.keys())
    for ws in clients.values():
        await ws.send_text(user_list)

async def broadcast_typing_status():
    typing_status = "false"  # Default to no one typing
    for ws in clients.values():
        await ws.send_text(f"[typing]:{typing_status}")

@app.websocket("/ws/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()

    # Receive username on connection
    username = await websocket.receive_text()

    if username in clients:
        await websocket.send_text("Username already taken. Refresh and try a different name.")
        await websocket.close()
        return

    clients[username] = websocket
    await broadcast_user_list()

    try:
        while True:
            message = await websocket.receive_text()

            # Handle typing notification
            if message.startswith("/typing"):
                typing_status = message.split(" ")[1]  # "true" or "false"
                if typing_status == "true":
                    await websocket.send_text(f"[typing] {username} is typing...")
                else:
                    await websocket.send_text(f"[typing] {username} has stopped typing.")
                continue

            # --- /list command ---
            if message == "/list":
                await websocket.send_text("Online users: " + ", ".join(clients.keys()))
                continue

            # --- /whisper command ---
            if message.startswith("/whisper"):
                try:
                    rest = message[len("/whisper"):].strip()
                    target_name, whisper_msg = rest.split(":", 1)
                    target_name = target_name.strip()
                    whisper_msg = whisper_msg.strip()

                    if target_name.lower() == username.lower():
                        await websocket.send_text("[whisper] Server: You can't whisper to yourself.")
                        continue

                    matched_name = next((name for name in clients if name.lower() == target_name.lower()), None)
                    if matched_name:
                        target_ws = clients[matched_name]
                        sender_msg = f"[whisper] {username}: {whisper_msg}"
                        await target_ws.send_text(sender_msg)
                        await websocket.send_text(sender_msg)
                    else:
                        await websocket.send_text(f"[whisper] Server: User '{target_name}' not found.")
                except ValueError:
                    await websocket.send_text("[whisper] Server: Invalid format. Use /whisper target: message")
                continue

            # --- Broadcast normal message ---
            for name, client_ws in clients.items():
                await client_ws.send_text(f"{username}: {message}")

    except WebSocketDisconnect:
        del clients[username]
        await broadcast_user_list()
