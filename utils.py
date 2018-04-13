import os
import re
import datetime
import csv
from peewee import *

from task import Task

OPTIONS_ORDER = ['a)', 'b)', 'c)']
OPTIONS_TEXT = [
    ' Add new entry',
    ' Search in existing entries',
    ' Quit program'
]

SEARCHING_CRITERIA_ORDER = ['a)', 'b)', 'c)', 'd)', 'e)']
SEARCHING_CRITERIA = [
    ' Exact Date',
    ' Time Spent',
    ' Employee\'s Name',
    ' Exact Search',
    ' Return to Menu',
]

db = SqliteDatabase('logs.db')


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
        menu += (str(order) + ' - ' + text + '\n')
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


def enter_employee_name():
    """
    Receives and validate input data
    :return: title (string)
    """
    valid_data = False
    # used to keep track of the values and change them in other scopes
    input_data = {'employee_name': ''}

    while not valid_data:
        input_data['employee_name'] = input("Employee's Name: ")
        if re.match('[\w]+', input_data['employee_name']):
            valid_data = True
            clean_scr()

    return input_data['employee_name']


def enter_notes():
    """
    Receives and returns input data
    :return: notes (string)
    """
    notes = input("Notes (Optional): ")
    clean_scr()
    return notes


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


def enter_searching_date():
    """
    Receives and validate input data
    :return: date (string)
    """
    valid_data = False
    # used to keep track of the values and change them in other scopes
    input_data = {'date': ''}

    tasks_entries = Task.select()
    date_set = set()  # this way we guarantee no repeated elements.
    for task in tasks_entries:
        date_set.add(task.date)
    set_length = len(date_set)

    while not valid_data:
        print("Select the date" + "\n")
        order_list = list(range(1, (set_length + 1)))
        option_list = list(date_set)
        date_option_selected = input(print_options(order_list, option_list))
        if re.match('\d+', date_option_selected) and int(date_option_selected) < (set_length + 1):
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
    Opens and reads database and collect matching task according to search param
    :param field: key to search for
    :param field_value: value to compare that field
    :return: list of task with matching criteria
    """
    if field == 'date':
        tasks = Task.select().where(Task.date == field_value)
        return tasks
    if field == 'employee_name':
        tasks = Task.select().where(Task.employee_name == field_value)
        return tasks
    if field == 'time_spent':
        tasks = Task.select().where(Task.time_spent == field_value)
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
