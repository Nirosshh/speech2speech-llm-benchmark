
"""
Minimal Flask + Socket.IO stub to show real-time events and threaded queues.
Evidence of real-time pipeline structure.
"""
import queue, threading, time
from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
socketio = SocketIO(app, cors_allowed_origins="*")

audio_q = queue.Queue()
text_q = queue.Queue()

def asr_worker():
    while True:
        time.sleep(0.2)
        text_q.put("hello ")
        socketio.emit("partial_transcript", {"text": "hello "})

def llm_worker():
    while True:
        txt = text_q.get()
        for token in ["hi", ", ", "how ", "can ", "I ", "help?"]:
            time.sleep(0.15)
            socketio.emit("llm_token", {"token": token})
        socketio.emit("llm_done", {"ok": True})

@socketio.on("connect")
def on_connect():
    emit("connected", {"ok": True})

def main():
    threading.Thread(target=asr_worker, daemon=True).start()
    threading.Thread(target=llm_worker, daemon=True).start()
    socketio.run(app, host="0.0.0.0", port=5001)

if __name__ == "__main__":
    main()
