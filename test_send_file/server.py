from flask import Flask, render_template
from flask_socketio import SocketIO, send
import json, os

app = Flask(__name__)

app.config["SERECT_KEY"] = "GavinAndAlan"
app.secret_key = os.getenv("SECRET_KEY")
socket = SocketIO(app, cors_allowed_origins='*')


@app.route('/')
def home():
    return render_template("index.html")


@socket.on('message')
def handle_message(msg):
    msg = json.loads(msg)
    print("Received message")
    if msg["Type"] == "connect":
        print("User '%s' has connected!" % msg["id"])
    elif msg["Type"] == "image":
        send(json.dumps(msg), broadcast=True)
        print("Successfully broadcast forwarding!")


if __name__ == "__main__":
    socket.run(app, debug=True, host="172.20.10.9", port=5000)