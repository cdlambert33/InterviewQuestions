import json
from classes import Employee, Job, TimePunch

file = open('input.json')

data = json.load(file)

jobs = []
employees = []
timePunches = []

for i in data['jobMeta']:
    job = Job(i.get('job'),i.get('rate'),i.get('benefitsRate'))
    jobs.append(job)

for i in data['employeeData']:
    employee = Employee(i.get('employee'),i.get('timePunch'))
    employees.append(employee)

file.close()