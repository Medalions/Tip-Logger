import consts


class Day:
    def __init__(self, shift, hours, tip):
        self.shift = shift
        self.hours = hours
        self.tip = tip

    def year(self):
        return self.shift.year

    def month(self):
        return consts.MONTHS[self.shift.month]

    def day(self):
        return self.shift.day

    def toCSV(self):
        data = [str(self.day()), str(self.hours), str(self.tip), "\n"]
        return ",".join(data)

    def date(self):
        month = str(self.shift.month)
        if len(month) == 1:
            month = "0" + month
        return month + "/" + str(self.day())

    def weekday(self):
        return consts.DAYS[self.shift.weekday()]
