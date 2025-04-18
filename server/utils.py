from datetime import datetime

# Log events to a file with timestamps
def log_event(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("chat_logs.txt", "a") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")
