from fastapi import WebSocket, WebSocketDisconnect
from server.clients import clients
from server.utils import log_event
from server.dashboard import get_dashboard_stats


# Handle new WebSocket connections and messages
async def handle_websocket(websocket: WebSocket):
    await websocket.accept()
    username = None

    try:
        # Request username from client
        await websocket.send_text("Enter your username:")
        username = await websocket.receive_text()

        # Add client to the clients list
        clients[websocket] = username
        log_event(f"{username} has joined the chat.")
        await broadcast_message(f"{username} has joined the chat.", sender=websocket)

        while True:
            message = await websocket.receive_text()
            if message.lower() == "/exit":
                break  # Disconnect the user

            # Handle /whisper command
            if message.startswith("/whisper "):
                parts = message.split(" ", 2)
                if len(parts) < 3:
                    await websocket.send_text("Usage: /whisper <username> <message>")
                    continue

                target_username = parts[1]
                private_message = parts[2]

                # Find recipient websocket
                target_ws = None
                for ws, uname in clients.items():
                    if uname == target_username:
                        target_ws = ws
                        break

                if target_ws:
                    await target_ws.send_text(f"{username} (whisper): {private_message}")
                    await websocket.send_text(f"You (to {target_username}): {private_message}")
                    log_event(f"{username} whispered to {target_username}: {private_message}")
                else:
                    await websocket.send_text(f"User '{target_username}' not found or not online.")
                continue

            # Normal public message
            await broadcast_message(f"{username}: {message}", sender=websocket)
            log_event(f"{username}: {message}")

    except WebSocketDisconnect:
        if websocket in clients:
            username = clients.pop(websocket)
            log_event(f"{username} has disconnected.")
            await broadcast_message(f"{username} has left the chat.", sender=None)

    finally:
        await websocket.close()



# Broadcast a message to all clients
async def broadcast_message(message: str, sender: WebSocket = None):
    for client in clients.keys():
        if client != sender:
            await client.send_text(message)
