import json
from classes import Employee, Job, TimePunch
from datetime import datetime, timedelta
from decimal import Decimal, getcontext

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

    for i in data['employeeData']:
        
        employee = Employee(i.get('employee'), 0, 0, 0, 0, 0)
        employees.append(employee)

        for j in i['timePunch']:
            start = datetime.strptime(j.get('start'), '%Y-%m-%d %H:%M:%S')
            end = datetime.strptime(j.get('end'), '%Y-%m-%d %H:%M:%S')
            punch = TimePunch(employee.employee, j.get('job'), start, end)
            timePunches.append(punch)
        
        
    for employee in employees:
        timeWorked = 0

        for punch in timePunches:
            if punch.employee == employee.employee:
                currentShiftHours = calculateShiftTime(punch.start, punch.end)

                newTotal = timeWorked + currentShiftHours

                """timeCategory = checkTimeCategory(currentShiftHours, newTotal)"""

                timeWorked += currentShiftHours
                job = punch.job

                if newTotal < regularCap:
                    employee.wageTotal += calculateRegularWage(job, currentShiftHours)
                    employee.regular += currentShiftHours
                    employee.benefitTotal += calculateBenefits(job, currentShiftHours)

                else:
                    extraHours = calculateExtraHours(newTotal, currentShiftHours)
                    employee.wageTotal += calculateExtraWage(punch.job, extraHours)
                    employee.overtime += extraHours.get('overtime')
                    employee.doubletime += extraHours.get('doubletime')
                    employee.benefitTotal += calculateExtraBenefits(job, extraHours)
                    employee.regular = regularCap
        
        cleanResults = cleanUpNumbers(employee)

        print(vars(cleanResults))

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

            if extraHours.get('regular') > 0:
                wageEarned += extraHours.get('regular') * i.rate

            if extraHours.get('overtime') > 0:
                wageEarned += extraHours.get('overtime') * i.rate * overtimeRate

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
    regular = 0
    overtime = 0
    doubletime = 0

    totalBeforeCurrentShift = newTotal - currentShiftHours

    if totalBeforeCurrentShift > regularCap:
        overtime = currentShiftHours
    else:
        overtime = newTotal - regularCap
        regular = currentShiftHours - overtime

    if newTotal > overtimeCap:
        doubletime = newTotal - overtimeCap
        overtime = overtime - doubletime


    extraHours = {
        "overtime": overtime,
        "doubletime": doubletime,
        "regular": regular
    }

    return extraHours


def calculateBenefits(job, hours):
    benefits = 0
    
    for i in jobs:
        if i.name == job:
            benefits += i.benefitsRate * hours
    return benefits

def calculateExtraBenefits(job, extraHours):
    benefits = 0
    for i in jobs:
        if i.name == job:
            if extraHours.get('regular') > 0:
                benefits += i.benefitsRate * extraHours.get('regular')

            if extraHours.get('overtime') > 0:
                benefits += i.benefitsRate * extraHours.get('overtime')

            if extraHours.get('doubletime') > 0:
                benefits += i.benefitsRate * extraHours.get('doubletime')

    return benefits


def cleanUpNumbers(employee):
    employee.regular = str(round(Decimal(employee.regular), 4))
    employee.overtime = str(round(Decimal(employee.overtime), 4))
    employee.doubletime = str(round(Decimal(employee.doubletime), 4))
    employee.wageTotal = str(round(Decimal(employee.wageTotal), 4))
    employee.benefitTotal = str(round(Decimal(employee.benefitTotal), 4))

    return employee


if __name__ == "__main__":
    main()