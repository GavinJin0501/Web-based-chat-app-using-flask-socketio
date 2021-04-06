import json


def load_table():
    file = open("check_list.json", "r")
    table = json.loads(file.read())
    file.close()
    return table


def write_table(table):
    with open("check_list.json", "w") as file:
        file.write(json.dumps(table))
