import os
import re
import datetime
import csv

OPTIONS_ORDER = ['a', 'b', 'c']
OPTIONS_TEXT = [
    ') Add new entry',
    ') Search in existing entries',
    ') Quit program'
]

SEARCHING_CRITERIA_ORDER = ['a', 'b', 'c', 'd', 'e', 'f']
SEARCHING_CRITERIA = [
    ') Exact Date',
    ') Range of Dates',
    ') Exact Search',
    ') Time Spent',
    ') Regex Pattern',
    ') Return to Menu',
]


def clean_scr():
    """Clear the screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_options(order_list, option_list):
    """
    Creates a menu to be printed
    :return: menu (string)
    """
    menu = ''
    for order, text in zip(order_list, option_list):
        menu += (order + text + '\n')
    return menu


# INPUT FUNCTIONALITY


def enter_date():
    """
    Receives and validate input data
    :return: date (string)
    """
    valid_data = False
    # used to keep track of the values and change them in other scopes
    input_data = {'date': ''}

    while not valid_data:
        input_data['date'] = input("Date of the task" + "\n" + "Please use DD/MM/YYYY format: ")
        if re.match('\d{2}/\d{2}/\d{4}', input_data['date']):
            try:
                datetime.datetime.strptime(input_data['date'], '%d/%m/%Y')
            except ValueError:
                clean_scr()
                input("Enter a valid date. Press enter to try again.")
            else:
                valid_data = True
                clean_scr()

    return input_data['date']


def enter_title():
    """
    Receives and validate input data
    :return: title (string)
    """
    valid_data = False
    # used to keep track of the values and change them in other scopes
    input_data = {'title': ''}

    while not valid_data:
        input_data['title'] = input("Title of the task: ")
        if re.match('[\w]+', input_data['title']):
            valid_data = True
            clean_scr()

    return input_data['title']


def enter_notes():
    """
    Receives and returns input data
    :return: notes (string)
    """
    return input("Notes (Optional): ")


def enter_time_spent():
    """
    Receives and validate input data
    :return: time_spent (string)
    """
    valid_data = False
    # used to keep track of the values and change them in other scopes
    input_data = {'time_spent': ''}

    while not valid_data:
        input_data['time_spent'] = input("Time spent on task (rounded minutes) : ")
        if re.match('\d+', input_data['time_spent']):
            valid_data = True
            clean_scr()

    return input_data['time_spent']


# SEARCHING FUNCTIONALITY


def enter_searching_date_range():
    """
    Receives and validate input data for date range
    :return: dt_start, dt_end (Datetime Obj)
    """
    valid_data = False
    valid_second = False
    # used to keep track of the values and change them in other scopes
    input_data = {'dt_start': '', 'dt_end': ''}

    while not valid_data:
        input_data['dt_start'] = input("Enter the starting date" + "\n" + "Please use DD/MM/YYYY format: ")
        if re.match('\d{2}/\d{2}/\d{4}', input_data['dt_start']):
            try:
                datetime.datetime.strptime(input_data['dt_start'], '%d/%m/%Y')
            except ValueError:
                clean_scr()
                input("Enter a valid date. Press enter to try again.")
            else:
                # If no error with first date, let's get the second date
                while not valid_second:
                    input_data['dt_end'] = input("Enter the ending date" + "\n" + "Please use DD/MM/YYYY format: ")
                    if re.match('\d{2}/\d{2}/\d{4}', input_data['dt_end']):
                        try:
                            datetime.datetime.strptime(input_data['dt_end'], '%d/%m/%Y')
                        except ValueError:
                            clean_scr()
                            input("Enter a valid ending date. Press enter to try again.")
                        else:
                            # out of the two whiles
                            valid_second = True
                            valid_data = True
                            clean_scr()
    return input_data


def enter_searching_date():
    """
    Receives and validate input data
    :return: date (string)
    """
    valid_data = False
    # used to keep track of the values and change them in other scopes
    input_data = {'date': ''}

    while not valid_data:
        input_data['date'] = input("Enter the date" + "\n" + "Please use DD/MM/YYYY format: ")
        if re.match('\d{2}/\d{2}/\d{4}', input_data['date']):
            try:
                datetime.datetime.strptime(input_data['date'], '%d/%m/%Y')
            except ValueError:
                clean_scr()
                input("Enter a valid date. Press enter to try again.")
            else:
                valid_data = True
                clean_scr()
    return input_data['date']


def enter_searching_time():
    """
    Receives and validate input data
    :return: time (string)
    """
    valid_data = False
    # used to keep track of the values and change them in other scopes
    input_data = {'time': ''}

    while not valid_data:
        input_data['time'] = input("Enter the time spent your are interested in (min)")
        if re.match('\d+', input_data['time']):
            valid_data = True
            clean_scr()
        else:
            input("Enter valid minutes value.")

    return input_data['time']


# Accessing the csv file


def find_tasks_by_field(field, field_value):
    """
    Opens and reads csv file and collect matching task according to search param
    :param field: key to search for
    :param field_value: value to compare that field
    :return: list of task with matching criteria
    """
    tasks = []
    try:
        open('log.csv', 'r')
    except IOError:
        print("Couldn't open the file.")
    else:
        with open('log.csv', newline='') as csvfile:
            task_reader = csv.DictReader(csvfile, delimiter=',')
            rows = list(task_reader)
            for row in rows:
                if row[field] == field_value:
                    tasks.append(row)
            return tasks


def find_tasks_by_date_range(dt_start, dt_end):
    """
    Opens and reads csv file and collect matching task according to search param
    :param dt_start: datetime object
    :param  dt_end: datetime object
    :return: list of task with match dates
    """
    tasks = []
    try:
        open('log.csv', 'r')
    except IOError:
        print("Couldn't open the file.")
    else:
        with open('log.csv', newline='') as csvfile:
            task_reader = csv.DictReader(csvfile, delimiter=',')
            rows = list(task_reader)

            # Work around to keep track of a value.
            # Scope behavior won't let change immutable var
            # That's why the use of list here
            current = []
            for row in rows:
                try:
                    datetime.datetime.strptime(row['date'], '%d/%m/%Y')
                except ValueError:
                    pass
                else:
                    # the current value will be always on index 0 of current list above
                    current.insert(0, datetime.datetime.strptime(row['date'], '%d/%m/%Y'))

                # current[0] == datetime object for current row
                if dt_end >= current[0] >= dt_start:
                    tasks.append(row)

            return tasks


def find_tasks_by_word(str_w):
    tasks = []
    try:
        open('log.csv', 'r')
    except IOError:
        print("Couldn't open the file.")
    else:
        with open('log.csv', newline='') as csvfile:
            task_reader = csv.DictReader(csvfile, delimiter=',')
            rows = list(task_reader)
            for row in rows:
                # if re.match(str_w, row['title']) or re.match(str_w, row['notes']):
                if row['title'].lower().__contains__(str_w.lower()) or row['notes'].lower().__contains__(str_w.lower()):
                    tasks.append(row)
            return tasks


def find_tasks_by_pattern(ptrn):
    """Looks for a match for the pattern entered in the title and the notes.
    If any that task is selected for display.
    :param ptrn to match on name or notes
    :return list of task that passed the matching criteria
    """
    tasks = []
    try:
        open('log.csv', 'r')
    except IOError:
        print("Couldn't open the file.")
    else:
        with open('log.csv', newline='') as csvfile:
            task_reader = csv.DictReader(csvfile, delimiter=',')
            rows = list(task_reader)
            for row in rows:
                if re.match(ptrn, row['title']) or re.match(ptrn, row['notes']):
                    tasks.append(row)
            return tasks


