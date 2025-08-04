# Standard Libraries
import filecmp
from sys import exit
from datetime import date, timedelta
import matplotlib.pyplot as plt

# Custom modules
import consts
from Day import Day

dirs = [consts.PRIMARY_DIR_PATH, consts.SECONDARY_DIR_PATH]


def getDate():
    while True:
        chosen_date = input("Input the date in yyyymmdd format: ")
        hours = input("Input length of shift in hours: ")
        try:
            choice = date.fromisoformat(chosen_date)
            hours = int(hours)
        except ValueError:
            print("Date or hours not accepted, please reinput")
            continue

        assertion = input(f"Correct date is {consts.MONTHS[choice.month]} " +
                          f"{choice.day}, {choice.year}? (y/n) ")

        if assertion.upper() == "Y" or assertion.upper() == "YES":
            return choice, hours


def getTip():
    while True:
        tip = input("Input tip amount rounded down to nearest dollar: ")
        try:
            tip = int(tip)
        except ValueError:
            print("Invalid input, please reinput")
            continue

        assertion = input(f"Correct amount is ${tip}? (y/n) ")
        if assertion.upper() == "Y" or assertion.upper() == "YES":
            return tip


def getMonthData(month, year):
    if isinstance(month, int):
        month = consts.MONTHS[month]
    try:
        with open(f"{dirs[0]}{month}{year}.csv", "r") as file:
            contents = file.readlines()
    except FileNotFoundError:
        return []

    month_str = str(consts.INV_MONTHS[month])
    if len(month_str) == 1:
        month_str = "0" + month_str

    data = list()
    for line in contents:
        separated = line.split(",")
        day = separated[0]
        if len(day) == 1:  # Iso formate requires 2 digit day and month values
            day = "0" + day

        hours = int(separated[1])
        tip = int(separated[2])

        iso = date.fromisoformat(str(year) + month_str + day)
        data.append(Day(iso, hours, tip))

    return data


def getRangeInput():
    print("What range is the data spanning?")
    while True:
        try:
            start = date.fromisoformat(input("Starting date? yyyymmdd "))
            end = date.fromisoformat(input("ending date? yyyymmdd "))
            if start > end:
                start, end = end, start
            if start == end:
                print("Please give different dates")
                continue
            break
        except ValueError:
            print("Date(s) not accepted, please reinput")
            continue
    return start, end


def getLastWeek():
    today = date.today()
    days_ago = 6 if today.weekday() == 0 else today.weekday() - 1
    end = today - timedelta(days=days_ago)
    start = end - timedelta(days=6)
    return start, end


def getLastMonth():
    end = date.today() - timedelta(days=date.today().day)
    start = end - timedelta(end.day - 1)
    return start, end


def log(date_worked, hours, tip):
    workday = Day(date_worked, hours, tip)
    try:
        file_contents = getMonthData(workday.month(), workday.year())
    except FileNotFoundError:
        file = open(f"{dirs[0]}{workday.month()}{workday.year()}.csv", "w")
        file.write(workday.toCSV())
        file.close()

        backup = open(f"{dirs[1]}{workday.month()}{workday.year()}.csv", "w")
        backup.write(workday.toCSV())
        backup.close()
        return

    """
    This for loop below is meant to keep the files that hold the
    data organized. It goes over each line in the month and reads
    the day. If the day is before the one trying to be written, it
    continues. If the days are the same, it overwrites the data with
    the new one. If it hits a day that comes after the one being input,
    it inserts the data. Else, if every day in the file came before the
    input, it just appends it at the end
    """
    for index, shift in enumerate(file_contents):
        if shift.day() < workday.day():
            continue

        if shift.day() == workday.day():
            file_contents[index] = workday
            break

        if shift.day() > workday.day():
            file_contents.insert(index, workday)
            break

        if index == len(file_contents)-1:
            file_contents.append(workday)

    CSV_lines = [shift.toCSV() for shift in file_contents]
    writeToFiles(CSV_lines, workday)
    return


def writeToFiles(contents, workday):
    file = f"{dirs[0]}{workday.month()}{workday.year()}.csv"
    backup = f"{dirs[1]}{workday.month()}{workday.year()}.csv"

    if not filecmp.cmp(file, backup, shallow=False):
        print("Error, the main file and backup file are not identical")
        exit(1)

    file = open(file, "w")
    file.writelines(contents)
    file.close()

    backup = open(backup, "w")
    backup.writelines(contents)
    backup.close()


def dataRange(start, end):
    start_month = consts.MONTHS[start.month]
    end_month = consts.MONTHS[end.month]
    range_total = []

    if end.year > start.year:
        # Oh boy, can't wait to do this!
        pass
    else:
        num_months = end.month-start.month

        for i in range(num_months+1):
            month = consts.MONTHS[start.month+i]
            month_data = getMonthData(month, start.year)

            for shift in month_data:
                if shift.month() == start_month and shift.day() < start.day:
                    continue
                if shift.month() == end_month and shift.day() > end.day:
                    break
                range_total.append(shift)
    return range_total


def report():
    date_worked, shift_length = getDate()
    tip = getTip()
    log(date_worked, shift_length, tip)


def tipRange(start, end):
    shifts = dataRange(start, end)
    if start.month == end.month:
        days = [shift.day() for shift in shifts]
    else:  # This branch is confusing, but it cleans up axis vars in plot
        days = [shift.date() for shift in shifts]

    tips = [shift.tip for shift in shifts]
    hours = [shift.hours for shift in shifts]
    wage = (sum(tips)/sum(hours))+consts.BASE_WAGE

    print(f"You made a total of ${sum(tips)}")
    print(f"Approximate wage = ${wage:.2f}/hour")
    plot_trend(days, tips)


def reportWeek():
    start, end = getLastWeek()
    shifts = dataRange(start, end)

    tips = [shift.tip for shift in shifts]
    hours = [shift.hours for shift in shifts]
    total = sum(tips)
    wage = (sum(tips)/sum(hours))+consts.BASE_WAGE

    print(f"Total tips last week: {total}")
    print(f"Approximate wage = ${wage:.2f}/hour")
    if total < 400:
        print("Not enough last week")
    else:
        print("After $350 in savings and $50 to credit cards, " +
              f"you have ${total-400} for yourself")
    plot_trend(shifts, tips, is_week=True)


def reportMonth():
    start, end = getLastMonth()
    shifts = dataRange(start, end)

    days = [shift.day() for shift in shifts]
    tips = [shift.tip for shift in shifts]
    hours = [shift.hours for shift in shifts]
    wage = (sum(tips)/sum(hours))+consts.BASE_WAGE

    print(f"Last month, you made a total of ${sum(tips)}")
    print(f"Approximate wage = ${wage:.2f}/hour")
    plot_trend(days, tips)


def plot_trend(days, tips, is_week=False):
    if is_week:
        indices = [day.weekday() for day in days]
        plt.xlabel("Weekday")
    else:
        indices = [str(day) for day in days]
        plt.xlabel("Day")

    plt.ylabel("Tip Amount")
    plt.plot(indices, tips)
    plt.show()


def main():
    options = set(str(i+1) for i in range(4))
    selection = None

    print("Select what you would like to do: ")
    while selection not in options:
        selection = input(consts.OPTIONS)

        match selection:
            case "1":
                report()
            case "2":
                start, end = getRangeInput()
                tipRange(start, end)
            case "3":
                reportWeek()
            case "4":
                reportMonth()
            case _:
                print("Error in selection, please reinput")


if __name__ == "__main__":
    main()
