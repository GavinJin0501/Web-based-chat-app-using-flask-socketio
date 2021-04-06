# Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, flash
import json
import random
import check_db

# Initialize the app from Flask
app = Flask(__name__)

# Define a route to hello function
@app.route('/')
def hello():
    return render_template('index.html')

# Define route for login
@app.route('/login')
def login():
    return render_template('login.html')


# Define route for register
@app.route('/register')
def register():
    return render_template('register.html')


# Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    # grabs information from the forms
    username = request.form['username']
    password = request.form['password']

    table = check_db.load_table()

    if username not in table or table[username] != password:
        # returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('login.html', error=error)
    else:
        # creates a session for the the user
        # session is a built in
        session['username'] = username
        return redirect(url_for('home'))


# Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    # grabs information from the forms
    username = request.form['username']
    password = request.form['password']

    if not len(password) >= 4:
        flash("Password length must be at least 4 characters")
        return redirect(request.url)

    # open JSON file to check
    table = check_db.load_table()

    if username in table:
        # If user exists
        error = "This username already exists"
        return render_template('register.html', error=error)
    else:
        table[username] = password
        check_db.write_table(table)
        flash("You are logged in")
        return render_template('index.html')


# @app.route('/home')
# def home():
#     username = session['username']
#     cursor = conn.cursor();
#     query = "SELECT ts, blog_post FROM blog WHERE username = \'{}\' ORDER BY ts DESC"
#     cursor.execute(query.format(username))
#     data1 = cursor.fetchall()
#     cursor.close()
#     return render_template('home.html', username=username, posts=data1)
#
#
# @app.route('/post', methods=['GET', 'POST'])
# def post():
#     username = session['username']
#     cursor = conn.cursor();
#     blog = request.form['blog']
#     query = "INSERT INTO blog (blog_post, username) VALUES(\'{}\', \'{}\')"
#     cursor.execute(query.format(blog, username))
#     conn.commit()
#     cursor.close()
#     return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')


app.secret_key = 'some key that you will never guess'
# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
