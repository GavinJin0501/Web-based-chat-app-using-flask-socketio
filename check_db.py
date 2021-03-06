import sqlite3
import json
from werkzeug.security import generate_password_hash, check_password_hash

PASSWORD_HASH = "sha256"


def get_json_groups():
    try:
        with open("/groups.json", "r") as file:
            GROUPS = json.load(file)
    except:
        GROUPS = {'general': []}
        file = open("groups.json", "w")
        file.write(json.dumps(GROUPS))
        file.close()
    return GROUPS


def update_json_groups(new):
    file = open("groups.json", "w")
    file.write(json.dumps(new))
    file.close()
    return


def drop_table():
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = """DROP TABLE IF EXISTS `Users`"""
    cursor.execute(query)
    conn.commit()
    query = """DROP TABLE IF EXISTS `general`"""
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()


def user_table_initialization():
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS `Users`(
                    `username`    VARCHAR(10) PRIMARY KEY,
                    `password`    VARCHAR(80))"""
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()


def login_check(username, password):
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = "SELECT * FROM `Users` WHERE `username` = \'{}\'"
    username = username.replace("\'", "\'\'")
    cursor.execute(query.format(username))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    if not data:
        return False
    return check_password_hash(data[0][1], password)


def register_check(username):
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = "SELECT * FROM `Users` WHERE `username` = \'{}\'"
    username = username.replace("\'", "\'\'")
    cursor.execute(query.format(username))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def register(username, password):
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = "INSERT INTO `Users` VALUES(\'{}\', \'{}\')"
    username = username.replace("\'", "\'\'")
    cursor.execute(query.format(username, generate_password_hash(password, PASSWORD_HASH)))
    conn.commit()
    cursor.close()
    conn.close()
    return


def history_table_initialization(id):
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS [{}](
                            `from`        VARCHAR(10),
                            `time`        DATETIME,
                            `message`     VARCHAR(256) DEFAULT "",
                            `image`       BLOB DEFAULT "")"""
    cursor.execute(query.format(id))
    conn.commit()
    cursor.close()
    conn.close()


def get_history(id):
    # (from, time, message, image)
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = """SELECT * FROM [{}]"""
    cursor.execute(query.format(id))
    # data = []
    # for each in cursor.fetchall():
    #     data.append(each[1] + " " + each[0] + ": " + each[2])
    # print(data)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def update_history(id, from_name, time, message, image=""):
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = """INSERT INTO [{}]
               VALUES (\'{}\', \'{}\', \'{}\', \'{}\')"""
    message = message.replace("\'", "\'\'")
    cursor.execute(query.format(id, from_name, time, message, image))
    conn.commit()
    cursor.close()
    conn.close()
    return


def delete_group_chat(group_name):
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = "DROP TABLE [{}]"
    cursor.execute(query.format(group_name))
    conn.commit()
    cursor.close()
    conn.close()
    return


def print_segment():
    print("============================================")
    return


def private_db_naming(from_name, to_name):
    if from_name > to_name:
        return from_name + "_" + to_name
    else:
        return to_name + "_" + from_name
