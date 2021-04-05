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

s = '{"Name": "Gavin", "Age":18}'
print(type(json.loads(s)))
