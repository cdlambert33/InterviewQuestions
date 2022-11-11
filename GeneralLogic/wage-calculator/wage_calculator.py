import json
from functions import *


def main():
    input = open('input.json')
    data = json.load(input)
    values = loadData(data)   
    input.close()     

    employees = values[0]
    timePunches = values[1]

    finalData = []
        
    for employee in employees:
        timeWorked = 0

        for punch in timePunches:
            if punch.employee == employee.employee:
                currentShiftHours = calculateShiftTime(punch.start, punch.end)

                newTotal = timeWorked + currentShiftHours

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
        
        
        results = cleanUpNumbers(employee)
        finalData.append(formatData(results))

        print(vars(results))

    with open('output.json', 'w') as outfile:
        json_data = json.dumps(finalData, indent=2)
        outfile.write(json_data)
        
    outfile.close()


if __name__ == "__main__":
    main()