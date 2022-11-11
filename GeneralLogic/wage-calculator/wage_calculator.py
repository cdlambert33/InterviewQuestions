import json
import jsonpickle
from functions import *


def main():
    input = open('input.json')
    data = json.load(input)
    values = loadData(data)   
    input.close()     

    employees = values[0]
    timePunches = values[1]

    results = {}
    allResults = []
    finalResults = {}
        
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
        
        
        results = cleanUpNumbers(employee)
        """finalResult = jsonpickle.encode(cleanedResult)"""
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
        allResults.append(resultsDict)

        print(vars(results))

    with open('output.json', 'w') as outfile:
        """for i in allResults:"""
        json_data = json.dumps(allResults, indent=2)
        outfile.write(json_data)
        

    outfile.close()


if __name__ == "__main__":
    main()