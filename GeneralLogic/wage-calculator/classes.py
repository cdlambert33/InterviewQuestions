class Job:
    
    def __init__(self, name, rate, benefitsRate):
        self.name = name
        self.rate = rate
        self.benefitsRate = benefitsRate


class TimePunch:
    def __init__(self, employee, job, start, end):
        self.employee = employee
        self.job = job
        self.start = start
        self.end = end

class Employee:
    def __init__(self, id, employee, timeWorked, regular, overtime, doubletime, wageTotal, benefitTotal):
        self.id = id
        self.employee = employee
        self.timeWorked = timeWorked
        self.regular = regular
        self.overtime = overtime
        self.doubletime = doubletime
        self.wageTotal = wageTotal
        self.benefitTotal = benefitTotal
