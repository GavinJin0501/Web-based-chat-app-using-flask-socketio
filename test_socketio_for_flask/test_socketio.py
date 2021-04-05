from flask import Flask, render_template
from flask_socketio import SocketIO, send


app = Flask(__name__)
app.config["SERECT_KEY"] = "gavinandalan"
socket = SocketIO(app, cors_allowed_origins='*')

@app.route("/")
def home():
    return render_template("index.html")

@socket.on("message")
def handle_message(msg):
    print("From: " + msg)
    send(msg, broadcast=True)


if __name__ == "__main__":
    socket.run(app, debug=True)