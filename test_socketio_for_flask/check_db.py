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


def drop_table():
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = """DROP TABLE Users"""
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()


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


def get_history(id):
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS \'{}\'(
                        from        VARCHAR(10),
                        time        DATETIME,
                        message     VARCHAR(256))"""
    cursor.execute(query.format(id))
    conn.commit()

    query = """SELECT * FROM \'{}\'"""
    cursor.execute(query.format(id))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def update_history(id, from_name, time, message):
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS \'{}\'(
                            from        VARCHAR(10),
                            time        DATETIME,
                            message     VARCHAR(256))"""
    cursor.execute(query.format(id))
    conn.commit()

    query  = """INSERT INTO \'{}\'
                VALUES (\'{}\', \'{}\', \'{}\')"""
    cursor.execute(query.format(id, from_name, time, message))
    conn.commit()
    cursor.close()
    conn.close()
    return
