from datetime import datetime


def content_format(msg, username):
    curr_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    to_send = "%s %s: %s" % (curr_time, username, msg)
    return to_send


def print_segment():
    print("============================================")
    return

def name_format(from_name, to_name):
    pass

def password_encryption(password, serect_key):
    pass


def password_decryption(password, serect_key):
    pass