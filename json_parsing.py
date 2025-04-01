import json

string_as_json_format = '{"answer":"Hello, User"}'
obj = json.loads(string_as_json_format)
key = '2'

if key in obj:
    print(obj[key])
else:
    print(f"Key  {key} doesn't belong to json")
