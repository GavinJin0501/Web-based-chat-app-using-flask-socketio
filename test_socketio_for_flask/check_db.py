import sqlite3
import hashlib


def drop_table():
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = """DROP TABLE `Users`"""
    cursor.execute(query)
    conn.commit()
    query = """DROP TABLE `general`"""
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()


def user_table_initialization():
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS `Users`(
                    `username`    VARCHAR(10) PRIMARY KEY,
                    `password`    VARCHAR(40))"""
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()


def login_check(username, password):
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = "SELECT * FROM `Users` WHERE `username` = \'{}\' and `password` = \'{}\'"
    cursor.execute(query.format(username, password))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


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
    cursor.execute(query.format(username, password))
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
        data.append(each[2]+" "+each[0]+": "+each[3])
    data.append("Above is the history")
    # print(data)
    cursor.close()
    conn.close()
    return data


def update_history(id, from_name, time, message):
    conn = sqlite3.connect("system_database.db")
    cursor = conn.cursor()
    query = """INSERT INTO \'{}\'
               VALUES (\'{}\', \'{}\', \'{}\')"""
    cursor.execute(query.format(id, from_name, time, message))
    conn.commit()
    cursor.close()
    conn.close()
    return


def print_segment():
    print("============================================")
    return