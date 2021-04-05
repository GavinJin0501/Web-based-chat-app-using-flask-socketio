import json

# d = {}
# json_data = json.dumps(d)
#
# file = open("check_list.json", "w")
# file.write(json_data)
# file.close()

# file = open("check_list.json", "r")
# json_data = json.loads(file.read())
# print(json_data)
# print(type(json_data))

name = "Gavin"
s = {"Name": name, "Age":18}
print(json.loads(json.dumps(s)))
