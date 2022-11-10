import json
from classes import Employee, Job, TimePunch
from datetime import datetime, timedelta


def main():
    file = open('input.json')

    data = json.load(file)

    jobs = []
    employees = []
    timePunches = []

    for i in data['jobMeta']:
        job = Job(i.get('job'), i.get('rate'), i.get('benefitsRate'))
        jobs.append(job)

    for i in data['employeeData']:
        id = 0
        employee = Employee(id, i.get('employee'), 0, 0, 0)
        employees.append(employee)

        for j in i['timePunch']:
            start = datetime.strptime(j.get('start'), '%Y-%m-%d %H:%M:%S')
            end = datetime.strptime(j.get('end'), '%Y-%m-%d %H:%M:%S')
            punch = TimePunch(id, j.get('job'), start, end)
            timePunches.append(punch)
        
        id += 1


    for employee in employees:
        for punch in timePunches:
            getTime(punch.start, punch.end)
            

    file.close()


def getTime(start,end):
        difference = end - start
        
        return


if __name__ == "__main__":
    main()