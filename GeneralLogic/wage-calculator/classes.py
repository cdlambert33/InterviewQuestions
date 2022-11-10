class Employee:
    def __init__(self, employee, timePunch):
        self.employee = employee
        self.timePunch = timePunch


class Job:
    def __init__(self, job, rate, benefitsRate):
        self.job = job
        self.rate = rate
        self.benefitsRate = benefitsRate


class TimePunch:
    def __init__(self, job, start, end):
        self.job = job
        self.start = start
        self.end = end

