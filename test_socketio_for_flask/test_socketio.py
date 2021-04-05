from flask import Flask, render_template
from flask_socketio import SocketIO, send
import json

UNAUTH_CLIENT_SOCKETS = []     # [ client socketio id ]
AUTH_CLIENT_SOCKETS = []       # [ client socketio id ]
GROUPS = {}                    # { group_id/group_name: [members] }


app = Flask(__name__)
app.config["SERECT_KEY"] = "GavinAndAlan"
socket = SocketIO(app, cors_allowed_origins='*')


@app.route("/")
def home():
    return render_template("index.html")


@socket.on("message")
def handle_message(msg):
    msg = json.loads(msg)
    print(msg)
    print(type(msg))
    send(msg, broadcast=True)


if __name__ == "__main__":
    socket.run(app, debug=True)