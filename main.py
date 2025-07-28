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


def report():
    date_worked, shift_length = getDate()
    tip = getTip()
    log(date_worked, shift_length, tip)


def getMonthFile(month, year):
    if isinstance(month, int):
        month = consts.MONTHS[month]
    with open(f"{month}{year}.csv", "r") as file:
        contents = file.readlines()
    return contents


def log(date_worked, hours, tip):
    month = consts.MONTHS[date_worked.month]
    try:
        file_contents = getMonthFile(month, date_worked.year)
    except FileNotFoundError:
        file = open(f"{month}{date_worked.year}.csv", "w")
        file.write(f"{date_worked.day},{hours},{tip}\n")
        file.close()
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
    for line, index in enumerate(file_contents):
        separated = ",".split(line)

        if separated[0] < date_worked.day:
            continue

        if separated[0] == date_worked.day:
            separated[1] = hours
            separated[2] = tip
            new_line = ",".join(separated)
            file_contents[index] = new_line
            break

        if separated[0] > date_worked.day:
            new_line = f"{date_worked.day},{hours},{tip}"
            file_contents.insert(index, new_line)
            break

        if index == len(file_contents)-1:
            file_contents.append(f"{date_worked.day},{hours},{tip}")

    file = open(f"{month}{date_worked.year}.csv", "w")
    file.writelines(file_contents)
    file.close()
    return


if __name__ == "__main__":
    report()
