from classes import Employee, Job, TimePunch
from datetime import timedelta, datetime
from decimal import Decimal

jobs = []
regularCap = 40
overtimeCap = 48


def loadData(data):
    employees = []
    timePunches = []
    values = []

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

    values.append(employees)
    values.append(timePunches)

    return values


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


def formatData(results):
    finalResults = {
            'employee': results.employee,
            'regular': results.regular,
            'overtime': results.overtime,
            'doubletime': results.doubletime,
            'wageTotal': results.wageTotal,
            'benefitTotal': results.benefitTotal
        }
    resultsDict = {
        finalResults['employee']: finalResults
    }

    return resultsDict