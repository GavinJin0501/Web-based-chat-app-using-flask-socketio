from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_socketio import SocketIO, send
import json
from datetime import datetime
import check_db     # our library for dealing with our database
import chat_utils   # our library for making standard message

CLIENT_NAME_TO_ID = {}  # { username: socketio_id }
USERS = []      # For ajax update online user info
GROUPS = []     # For ajax update group chat info

app = Flask(__name__)
app.config["SERECT_KEY"] = "GavinAndAlan"
app.secret_key = "my secret key"
socket = SocketIO(app, cors_allowed_origins='*')

# Initialize database connection
# check_db.drop_table()
check_db.user_table_initialization()


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
        print(username)
        post = "Hello Hello"
        return render_template('home.html', username=username, post=post)
    else:
        flash("Don't cheat! Login first!")
        return redirect(url_for("initial"))


@socket.on("message")
def handle_message(msg):
    msg = json.loads(msg)

    # Type 1: Socket, when client is authorized and connected to the server via socket.io
    if msg["Type"] == "Socket":
        user_id = msg["Id"]
        username = msg["Username"]
        CLIENT_NAME_TO_ID[username] = user_id
        if username not in USERS:
            USERS.append(username)
        print("User '%s':'%s' has connected to the server." % (user_id, msg["Username"]))
        print(CLIENT_NAME_TO_ID)
        print(USERS)
        chat_utils.print_segment()

        content = "Hello, everyone. I am in."
        curr_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        to_send = "%s %s: %s" % (curr_time, username, content)
        send(to_send, broadcast=True)

    elif msg["Type"] == "Post":
        # print(msg)
        content = msg["Content"]
        username = msg["From"]

        curr_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        to_send = "%s %s: %s" % (curr_time, username, content)
        # to = socketio.room. Can we do multiple rooms at the same time?
        send(to_send, to=CLIENT_NAME_TO_ID["Alan"])

    # # Type 2: Private message {"Type": "Private Chat", "From": username1, "To": username2, "Content": xxx, "Time": xxx}
    # elif msg["Type"] == "Private Chat":
    #     from_user = msg["From"]
    #     to_user = msg["To"]
    #     content = msg["Content"]
    #     time = msg["Time"]
    #
    #     id =
    #     check_db.update_history()
    #
    # # Type 3: Group message {"Type": "Group Chat", "From": username, "To": group_name, "Content": xxx, "Time": xxx}
    # elif msg["Type"] == "Group Chat":
    #     pass


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
        chat_utils.print_segment()
    return redirect('/')


# @app.route('/getMyInfo', methods=["POST"])
# def sendInfo():
#
#     return jsonify(username=session.get("Username", "None"))


if __name__ == "__main__":
    socket.run(app, debug=True)
    # socket.run(app, host="172.20.10.9", port=5000, debug=True)
