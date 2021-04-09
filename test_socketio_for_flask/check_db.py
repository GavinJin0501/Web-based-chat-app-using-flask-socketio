import json
import sqlite3


# def load_table():
#     file = open("check_list.json", "r")
#     table = json.loads(file.read())
#     file.close()
#     return table
#
#
# def write_table(table):
#     with open("check_list.json", "w") as file:
#         file.write(json.dumps(table))


def user_table_initialization():
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS Users(
                    username    VARCHAR(10) PRIMARY KEY,
                    password    VARCHAR(15))"""
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()
    return


def login_check(username, password):
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = "SELECT * FROM Users WHERE username = \'{}\' and password = \'{}\'"
    cursor.execute(query.format(username, password))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def register_check(username):
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = "SELECT * FROM Users WHERE username = \'{}\'"
    cursor.execute(query.format(username))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def register(username, password):
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = "INSERT INTO Users VALUES(\'{}\', \'{}\')"
    cursor.execute(query.format(username, password))
    conn.commit()
    cursor.close()
    conn.close()
    return
