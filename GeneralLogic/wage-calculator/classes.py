class Job:
    
    def __init__(self, name, rate, benefitsRate):
        self.name = name
        self.rate = rate
        self.benefitsRate = benefitsRate


class TimePunch:
    def __init__(self, job, start, end):
        self.job = job
        self.start = start
        self.end = end

class Employee:
    def __init__(self, employee, timePunch):
        self.employee = employee
        self.timePunch = timePunch