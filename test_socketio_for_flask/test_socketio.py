from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_socketio import SocketIO, send, join_room, leave_room
import json
from datetime import datetime
import check_db  # our library for dealing with our database

CLIENT_NAME_TO_ID = {}  # { username: socketio_id }
USERS = []  # For ajax update online user info
GROUPS = {"general": []}  # For ajax update group chat info

app = Flask(__name__)
app.config["SERECT_KEY"] = "GavinAndAlan"
app.secret_key = "my secret key"
socket = SocketIO(app, cors_allowed_origins='*')

# Initialize database
check_db.drop_table()
check_db.user_table_initialization()
check_db.history_table_initialization('general')


# 1. initial page
@app.route("/")
def initial():
    return render_template("index.html")


# 2.1 login page
@app.route('/login')
def login():
    return render_template('login.html')


# 2.2 login authorize
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if username in USERS:
            error = 'User "%s" has already logged in!' % username
            return render_template('login.html', error=error)

        data = check_db.login_check(username, password)

        if data:
            return redirect(url_for('home', username=username))
        else:
            error = 'Invalid login or username'
            return render_template('login.html', error=error)


# 3.1 register page
@app.route('/register')
def register():
    return render_template('register.html')


# 3.2 register authorize
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    username = request.form['username']
    password = request.form['password']

    data = check_db.register_check(username)

    if data:
        error = "This user already exists"
        return render_template('register.html', error=error)
    else:
        # session["Username"] = username
        check_db.register(username, password)
        return redirect(url_for('home', username=username))


# 4. home page
@app.route('/home', defaults={'username': ""})
@app.route('/home/<string:username>', endpoint='home')
def home(username):
    # if "Username" in session:
    if username != "":
        # username = session["Username"]
        # print("Test session:", username)
        # print(username)
        post = "Hello Hello"
        return render_template('home.html', username=username, post=post)
    else:
        flash("Don't cheat! Login first!")
        return redirect(url_for("initial"))


@socket.on("message")
def handle_message(msg):
    msg = json.loads(msg)

    # Type 1: Connect, when client is authorized and connected to the server via socket.io. Put into the general channel
    if msg["Type"] == "Connect":
        user_id = msg["Id"]
        username = msg["Username"]
        if username not in CLIENT_NAME_TO_ID:
            USERS.append(username)
            GROUPS['general'].append(username)
        CLIENT_NAME_TO_ID[username] = user_id
        print("New User '%s' has connected to the server." % username)
        # print(CLIENT_NAME_TO_ID)
        # print(USERS)
        check_db.print_segment()

        # give the history
        history = check_db.get_history('general')
        print(history)
        # send(history, to=CLIENT_NAME_TO_ID[username])

        content = "Hello, everyone. I am in."
        curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # to_send = "%s %s: %s" % (curr_time, username, content)
        msg["Content"] = content
        msg["Time"] = curr_time
        for each in GROUPS['general']:
            send(json.dumps(msg), to=CLIENT_NAME_TO_ID[each])

    # Type 2: Send information to others.
    elif msg["Type"] == "Send":
        # print(msg)
        content = msg["Content"]
        username = msg["From"]
        to = msg["To"]

        curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # to_send = "%s %s: %s" % (curr_time, username, content)
        check_db.update_history(to, username, curr_time, content)
        # to = socketio.room. Can we do multiple rooms at the same time?
        msg["Time"] = curr_time
        for each in GROUPS[to]:
            if each != username:
                send(json.dumps(msg), to=CLIENT_NAME_TO_ID[each])

    # Type 3: Join a private/group chat. msg = {"Type": "Join", "Chat": "Private/Group", "From": username, "To": xxx}
    elif msg["Type"] == "Join":
        pass


@app.route('/logout', defaults={'username': ""})
@app.route('/logout/<string:username>')
def logout(username):
    if username != "":
        if username not in USERS:
            return redirect('/')
        print(username)
        USERS.remove(username)
        del CLIENT_NAME_TO_ID[username]
        print(CLIENT_NAME_TO_ID)
        print(USERS)
        check_db.print_segment()
    return redirect('/')

# @app.route('/getMyInfo', methods=["POST"])
# def sendInfo():
#
#     return jsonify(username=session.get("Username", "None"))


if __name__ == "__main__":
    socket.run(app, debug=True)
    # socket.run(app, host="172.20.10.9", port=5000, debug=True)
