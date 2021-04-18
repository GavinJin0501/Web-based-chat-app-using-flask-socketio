import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


PASSWORD_HASH = "sha256"


def drop_table():
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = """DROP TABLE IF EXISTS `Users`"""
    cursor.execute(query)
    conn.commit()
    query = """DROP TABLE IF EXISTS `general`"""
    cursor.execute(query)
    conn.commit()
    query = """DROP TABLE IF EXISTS `Groups`"""
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


def group_table_initialization():
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS `Groups`(
                        `group_name`      VARCHAR(20) PRIMARY KEY,
                        `group_leader`    VARCHAR(10))"""
    cursor.execute(query)
    conn.commit()
    query = """INSERT INTO `Groups`
               VALUES (\'{}\', \'{}\')"""
    cursor.execute(query.format("general", "king_jjy"))
    conn.commit()
    cursor.close()
    conn.close()


def login_check(username, password):
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = "SELECT * FROM `Users` WHERE `username` = \'{}\'"
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
    cursor.execute(query.format(username))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def register(username, password):
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = "INSERT INTO `Users` VALUES(\'{}\', \'{}\')"
    cursor.execute(query.format(username, generate_password_hash(password, PASSWORD_HASH)))
    conn.commit()
    cursor.close()
    conn.close()
    return


def history_table_initialization(id):
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS \'{}\'(
                            `from`        VARCHAR(10),
                            `time`        DATETIME,
                            `message`     VARCHAR(256))"""
    cursor.execute(query.format(id))
    conn.commit()
    cursor.close()
    conn.close()


def get_history(id):
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = """SELECT * FROM \'{}\'"""
    cursor.execute(query.format(id))
    data = []
    for each in cursor.fetchall():
        data.append(each[1] + " " + each[0] + ": " + each[2])
    # print(data)
    cursor.close()
    conn.close()
    return data


def update_history(id, from_name, time, message):
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = """INSERT INTO \'{}\'
               VALUES (\'{}\', \'{}\', \'{}\')"""
    message = message.replace("\'", "\"")
    cursor.execute(query.format(id, from_name, time, message))
    conn.commit()
    cursor.close()
    conn.close()
    return


def get_groups():
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = "SELECT * FROM Groups"
    cursor.execute(query.format())
    groups = cursor.fetchall()
    cursor.close()
    conn.close()
    return groups


def update_groups(group_name, username):
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = "INSERT INTO `Groups` VALUES(\'{}\', \'{}\')"
    cursor.execute(query.format(group_name, username))
    conn.commit()
    cursor.close()
    conn.close()
    return


def check_group_leader(group_name, username):
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = "SELECT * FROM \'{}\' WHERE group_name = \'{}\' AND group_leader = \'{}\'"
    cursor.execute(query.format(group_name, username))
    status = cursor.fetchall()
    cursor.close()
    conn.close()
    return status != []


def delete_group_chat(group_name):
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = "DROP TABLE \'{}\'"
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
