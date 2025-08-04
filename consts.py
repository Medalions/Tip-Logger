BASE_WAGE = 2.13

DAYS = ["Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"]

MONTHS = [None,
          "January",
          "February",
          "March",
          "April",
          "May",
          "June",
          "July",
          "August",
          "September",
          "October",
          "November",
          "December"]

# This is a dict where I put the month's name to get its numeric value
INV_MONTHS = {v: k for k, v in enumerate(MONTHS)}

# To Change upon implementation
PRIMARY_DIR_PATH = "./"
SECONDARY_DIR_PATH = "./backup/"

OPTIONS = '''
(1) Report tip
(2) View summed tips
(3) View last week
(4) View last month
'''
