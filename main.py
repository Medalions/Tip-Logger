import consts
from datetime import date


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

        if assertion.upper() == "Y":
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
        if assertion.upper() == "Y":
            return tip


def getMonthData(month, year):
    if isinstance(month, int):
        month = consts.MONTHS[month]
    with open(f"{consts.PRIMARY_DIR_PATH}{month}{year}.csv", "r") as file:
        contents = file.readlines()
    return contents


def log(date_worked, hours, tip):
    month = consts.MONTHS[date_worked.month]
    try:
        file_contents = getMonthData(month, date_worked.year)
    except FileNotFoundError:
        dirs = [consts.PRIMARY_DIR_PATH, consts.SECONDARY_DIR_PATH]

        file = open(f"{dirs[0]}{month}{date_worked.year}.csv", "w")
        file.write(f"{date_worked.day},{hours},{tip},\n")
        file.close()

        backup = open(f"{dirs[1]}{month}{date_worked.year}.csv", "w")
        backup.write(f"{date_worked.day},{hours},{tip},\n")
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
    for index, line in enumerate(file_contents):
        separated = line.split(",")
        day = int(separated[0])

        if day < date_worked.day:
            continue

        if day == date_worked.day:
            separated[1] = hours
            separated[2] = tip
            new_line = ",".join(separated)
            file_contents[index] = new_line
            break

        if day > date_worked.day:
            new_line = f"{date_worked.day},{hours},{tip},\n"
            file_contents.insert(index, new_line)
            break

        if index == len(file_contents)-1:
            file_contents.append(f"{date_worked.day},{hours},{tip},\n")

    dirs = [consts.PRIMARY_DIR_PATH, consts.SECONDARY_DIR_PATH]

    file = open(f"{dirs[0]}{month}{date_worked.year}.csv", "w")
    file.writelines(file_contents)
    file.close()

    backup = open(f"{dirs[1]}{month}{date_worked.year}.csv", "w")
    backup.writelines(file_contents)
    backup.close()

    return


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


'''
Currently this range function will ignore days that don't exist and continue,
but not months. If a month doesn't exist, it errors and I am not in the mood
to fix it right now
'''
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

            for line in month_data:
                separated = line.split(",")
                if month == start_month and int(separated[0]) < start.day:
                    continue
                if month == end_month and int(separated[0]) > end.day:
                    break
                range_total.append(line)
    return range_total


def report():
    date_worked, shift_length = getDate()
    tip = getTip()
    log(date_worked, shift_length, tip)


def tipRange():
    start, end = getRangeInput()
    range_list = dataRange(start, end)
    tips = [int(line.split(",")[2]) for line in range_list]
    total = sum(tips)
    print(f"You made a total of ${total}")


if __name__ == "__main__":
    options = set(str(i+1) for i in range(2))
    selection = None

    print("Select what you would like to do: ")
    while selection not in options:
        selection = input(consts.OPTIONS)

        match selection:
            case "1":
                report()
            case "2":
                tipRange()
            case _:
                print("Error in selection, please reinput")
