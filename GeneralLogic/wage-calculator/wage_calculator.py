import json
from classes import Employee, Job, TimePunch
from datetime import datetime, timedelta

jobs = []

def main():
    file = open('input.json')

    data = json.load(file)

    employees = []
    timePunches = []

    for i in data['jobMeta']:
        job = Job(i.get('job'), i.get('rate'), i.get('benefitsRate'))
        jobs.append(job)

    id = 0
    for i in data['employeeData']:
        
        employee = Employee(id, i.get('employee'), 0, 0, 0)
        employees.append(employee)

        for j in i['timePunch']:
            start = datetime.strptime(j.get('start'), '%Y-%m-%d %H:%M:%S')
            end = datetime.strptime(j.get('end'), '%Y-%m-%d %H:%M:%S')
            punch = TimePunch(id, j.get('job'), start, end)
            timePunches.append(punch)
        
        id += 1

    y = 1
    for employee in employees:
        x = 1
        
        print('employee ' + str(y))
        y += 1
        for punch in timePunches:
            if punch.employee == employee.id:
                hours = calculateShiftTime(punch.start, punch.end)
                timeCategory = checkIfOvertime(hours, employee.timeWorked)

                if timeCategory != 'R':
                    calculateExtraHours()

                employee.timeWorked += hours
                employee.wageTotal += calculateWage(punch.job, hours, timeCategory)
                
                print(x)
                x += 1  
        

    file.close()


def calculateShiftTime(start,end):
        difference = end - start
        hours = difference / timedelta(hours=1)
        
        return hours
        

def calculateWage(jobType, hoursWorked, timeCategory):
    wageEarned = 0
    benefitEarned = 0
    overtimeRate = 1.5
    doubletimeRate = 2

    for i in jobs:
        if i.name == jobType:
            if timeCategory == 'R':
                wageEarned = hoursWorked * i.rate

            elif timeCategory == 'O':
                wageEarned = hoursWorked * i.rate * overtimeRate

            else:
                wageEarned = hoursWorked * i.rate * doubletimeRate

            benefitEarned = hoursWorked * i.benefitsRate
            return wageEarned


def checkIfOvertime(hours, totalHoursWorked):
    newTotal = totalHoursWorked + hours
    regularCap = 40
    overtimeCap = 48

    if newTotal > regularCap:
        calculateExtraHours(newTotal)
        if newTotal > overtimeCap:
            return ('D')
        else:
            return ('O')
    else:
        return ('R')
    

def calculateExtraHours(newTotal):

    return



if __name__ == "__main__":
    main()