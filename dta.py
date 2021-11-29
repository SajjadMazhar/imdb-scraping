import json

a = {1:"sajjad", "age":23, "languages":["Python", "JavaScript"], "tuple":(3,4,5,6)}



content = json.dumps(a)
print(content)
d=json.loads(content)
print(d)


# with open("new.json", 'w') as f:
#     json.dump(a, f, indent=4)




