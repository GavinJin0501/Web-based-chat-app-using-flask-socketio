from flask import Flask, render_template
from flask_socketio import SocketIO, send
import os
import json

app = Flask(__name__)

app.config["SERECT_KEY"] = "GavinAndAlan"
app.secret_key = "my secret key"
socket = SocketIO(app, cors_allowed_origins='*')

@app.route('/')
def home():
    return render_template("index.html")

@socket.on('message')
def handle_message(msg):
    msg = json.loads(msg)
    if msg["Type"] == "connect":
        print("User '%s' has connected!" % msg["id"])
    elif msg["Type"] == "image":
        socket.send(json.dumps(msg), broadcast=True)
        print("Successfully broadcast forwarding!")



if __name__ == "__main__":
    socket.run(app, debug=True)