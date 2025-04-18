import websocket
import threading

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Connection closed")

def on_open(ws):
    print("Connection established")

    # Send messages
    while True:
        msg = input("Enter message: ")
        if msg.lower() == "/exit":
            ws.close()
            break
        ws.send(msg)

if __name__ == "__main__":
    ws_url = "ws://127.0.0.1:8000/ws/chat"
    ws = websocket.WebSocketApp(ws_url, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
