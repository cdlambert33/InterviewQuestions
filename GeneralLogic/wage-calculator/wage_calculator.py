import json
from classes import Employee, Job, TimePunch
from datetime import datetime, timedelta

jobs = []
regularCap = 40
overtimeCap = 48
previousOvertime = 0


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
                currentShiftHours = calculateShiftTime(punch.start, punch.end)

                newTotal = employee.timeWorked + currentShiftHours

                """timeCategory = checkTimeCategory(currentShiftHours, newTotal)"""

                employee.timeWorked += currentShiftHours

                if newTotal < regularCap:
                    employee.wageTotal += calculateRegularWage(punch.job, currentShiftHours)

                else:
                    extraHours = calculateExtraHours(newTotal, currentShiftHours)
                    employee.wageTotal += calculateExtraWage(punch.job, extraHours)

                
                
                print(x)
                x += 1  
        

    file.close()


def calculateShiftTime(start,end):
        difference = end - start
        currentShiftHours = difference / timedelta(hours=1)
        
        return currentShiftHours
        

def calculateRegularWage(jobType, currentShiftHours):
    wageEarned = 0

    for i in jobs:
        if i.name == jobType:
            wageEarned = currentShiftHours * i.rate

            return wageEarned

def calculateExtraWage(jobType, extraHours):
    wageEarned = 0
    overtimeRate = 1.5
    doubletimeRate = 2

    for i in jobs:
        if i.name == jobType:

            wageEarned += extraHours.get('overtime') * i.rate * overtimeRate
            
            if extraHours.get('underRegularCap') > 0:
                wageEarned += extraHours.get('underRegularCap') * i.rate

            if extraHours.get('doubletime') > 0:
                wageEarned += extraHours.get('doubletime') * i.rate * doubletimeRate

            return wageEarned


def checkTimeCategory(newTotal):
    
    if newTotal > regularCap:
        if newTotal > overtimeCap:
            return ('D')
        else:
            return ('O')
    else:
        return ('R')
    

def calculateExtraHours(newTotal, currentShiftHours):
    extraHoursDifference = overtimeCap - regularCap

    overtime = newTotal - regularCap
    doubletime = 0

    if overtime > extraHoursDifference:
        doubletime = overtime - extraHoursDifference
        overtime = overtime - doubletime

    underRegularCap = currentShiftHours - overtime

    extraHours = {
        "overtime": overtime,
        "doubletime": doubletime,
        "underRegularCap": underRegularCap
    }

    return extraHours



if __name__ == "__main__":
    main()