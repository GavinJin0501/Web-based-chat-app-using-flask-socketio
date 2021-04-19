from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_socketio import SocketIO, send
import json
from datetime import datetime
import check_db  # our library for dealing with our database

CLIENT_NAME_TO_ID = {}  # { username: socketio_id }
USERS = []  # For ajax update online user info
GROUPS = {}  # For ajax update group chat info

app = Flask(__name__)
app.config["SERECT_KEY"] = "GavinAndAlan"
app.secret_key = "my secret key"
socket = SocketIO(app, cors_allowed_origins='*')

# Initialize database
check_db.drop_table()
check_db.user_table_initialization()
check_db.group_table_initialization()
check_db.history_table_initialization('general')

# Initialize GROUPS
for each in check_db.get_groups():  # each = (group_name, group_leader)
    GROUPS[each[0]] = []


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
        if username in CLIENT_NAME_TO_ID:
            error = 'User "%s" has already logged in!' % username
            return render_template('login.html', error=error)

        login_success = check_db.login_check(username, password)

        if login_success:
            USERS.append(username)
            # GROUPS['general'].append(username)
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
    elif len(password) < 6 or len(password) > 12:
        error = "password length is invalid: [6,12]"
        return render_template('register.html', error=error)
    else:
        USERS.append(username)
        # GROUPS['general'].append(username)
        check_db.register(username, password)
        return redirect(url_for('home', username=username))


# 4. home page
@app.route('/home', defaults={'username': ""})
@app.route('/home/<string:username>', endpoint='home')
def home(username):
    if username != "":
        if username not in USERS:
            flash("Don't cheat! Login first!")
            return redirect(url_for("initial"))
        for k in GROUPS:
            if username in GROUPS[k]:
                flash("Don't cheat! Login first!")
                return redirect(url_for("initial"))
        post = "Hello Hello"
        return render_template('home.html', username=username, post=post)
    else:
        flash("Don't cheat! Login first!")
        return redirect(url_for("initial"))


@app.route('/get-user-list', methods=['POST'])
def get_user_list():
    return jsonify(userlist=USERS)


@app.route('/get-group-list', methods=['POST'])
def get_group_list():
    return jsonify(grouplist=GROUPS)


@socket.on("message")
def handle_message(msg):
    msg = json.loads(msg)

    # Type 1: Connect, when client is authorized and connected to the server via socket.io. Put into the general channel
    # msg = {"Type": "Connect", "Id": user_socket.io_id, "Username": username}
    if msg["Type"] == "Connect":
        user_id = msg["Id"]
        username = msg["Username"]
        CLIENT_NAME_TO_ID[username] = user_id
        GROUPS['general'].append(username)
        print("New User '%s' has connected to the server." % username)
        print(msg)
        # print(CLIENT_NAME_TO_ID)
        # print(USERS)
        check_db.print_segment()

        content = "Hello, everyone. I am in."
        curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg["Content"] = content
        msg["Time"] = curr_time
        # print("Boradcast to everyone in the general channel")
        for each in GROUPS['general']:
            send(json.dumps(msg), to=CLIENT_NAME_TO_ID[each])

    # Type 2: Send information to others.
    # msg = {"Type": "Send", "From": from_user, "To": destination, "Content": content, "Chat": private/group}
    # -> May need a state: group/private
    elif msg["Type"] == "Send":
        print(msg)
        content = msg["Content"]
        from_name = msg["From"]
        to_name = msg["To"]

        curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg["Time"] = curr_time

        # case 1: to a group
        if msg["Chat"] == "group":
            check_db.update_history(to_name, from_name, curr_time, content)
            for each in GROUPS[to_name]:
                if each != from_name and CLIENT_NAME_TO_ID.get(each, False):
                    send(json.dumps(msg), to=CLIENT_NAME_TO_ID[each])
        # case 2: to a private user
        else:
            check_db.update_history(check_db.private_db_naming(from_name, to_name), from_name, curr_time, content)
            # only forward the msg if the destination user is online:
            if CLIENT_NAME_TO_ID.get(to_name, False):
                send(json.dumps(msg), to=CLIENT_NAME_TO_ID[to_name])

    # Type 3: Join a private/group chat.
    # msg = {"Type": "Join", "Chat": "Private/Group", "From": username, "To": xxx, "Current": xxx， "Deputy": 0/1}
    elif msg["Type"] == "Join":
        # print(msg)
        from_name = msg["From"]
        to_name = msg["To"]
        print(msg["To"] + "and" + msg["From"])
        if msg["Chat"] == "private":  # to_name is a user name
            check_db.history_table_initialization(check_db.private_db_naming(from_name, to_name))
            history = check_db.get_history(check_db.private_db_naming(from_name, to_name))
            if history and msg["Deputy"] == 0:
                send(json.dumps({"Type": 'history', "Content": history}), to=CLIENT_NAME_TO_ID[from_name])
        elif msg["Chat"] == "group":  # to_name is a group name
            history = check_db.get_history(to_name)
            if history and msg["Deputy"] == 0:
                # print("send history from join request from" + from_name + " to " + to_name)
                send(json.dumps({"Type": 'history', "Content": history}), to=CLIENT_NAME_TO_ID[from_name])
            if from_name not in GROUPS[to_name]:
                GROUPS[to_name].append(from_name)
        # may need to send a notification msg to those involved...

    # Type 4: Create a group chat. msg = {"Type": "Create", "Name": group_name, "From": username}
    elif msg["Type"] == "Create":
        group_name = msg["Name"]
        from_name = msg["From"]
        if group_name in GROUPS:
            # Error, name already used
            print("Group name already exists")
            pass
        else:
            check_db.update_groups(group_name, from_name)
            check_db.history_table_initialization(group_name)
            GROUPS[group_name] = [from_name]
            print("Group created successfully")

    # Type 5: Delete a group chat. msg = {"Type": Delete", "Name": group_name, "From": username}
    elif msg["Type"] == "Delete":
        group_name = msg["Name"]
        from_name = msg["From"]
        # Check if the from_name is the group_leader of this group
        status = check_db.check_group_leader(group_name, from_name)
        if status:  # group leader can delete the group
            del GROUPS[group_name]
            check_db.delete_group_chat(group_name)
        else:       # others can not delete the group
            pass


@app.route('/logout', defaults={'username': ""})
@app.route('/logout/<string:username>', methods=["Get"])
def logout(username):
    if username != "":
        if username not in CLIENT_NAME_TO_ID or username not in USERS:
            return redirect('/')
        print("User '%s' logs out." % username)
        USERS.remove(username)
        CLIENT_NAME_TO_ID.pop(username, None)
        # del CLIENT_NAME_TO_ID[username]
        for k in GROUPS:
            try:
                # print(GROUPS[k])
                GROUPS[k].remove(username)
            except:
                continue
        print(CLIENT_NAME_TO_ID)
        print(USERS)
        print(GROUPS)
        check_db.print_segment()
    return redirect('/')


if __name__ == "__main__":
    socket.run(app, debug=True)
    # socket.run(app, host="172.20.10.9", port=5000, debug=True)
