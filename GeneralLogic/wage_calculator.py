import json

file = open('input.json')

data = json.load(file)

for i in data['jobMeta']:
    print(i.get('rate'))

file.close()