# Ripple: Simple WebSocket Chat App

This is a basic real-time chat app using FastAPI and WebSockets.  
Users can join with a name, send public and private messages, and see who’s typing.

## Features

- Real-time chat with WebSocket
- "User is typing..." indicator
- Private messages using [whisper]
- Built with FastAPI + HTML/JS

## How to Run

1. Install FastAPI and Uvicorn
2. Run: `uvicorn server.main:app --reload`
3. Open your browser: `http://127.0.0.1:8000`

## Project Files

- `server/` — the backend (FastAPI)
- `client/` — Python client
- `static/index.html` — frontend
