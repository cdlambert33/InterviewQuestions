import json

file = open('input.json')

data = json.load(file)

jobProperties = {}
employees = {}
timePunches = {}

for i in data['jobMeta']:
    print(i.get('rate'))

file.close()