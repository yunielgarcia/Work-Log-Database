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


# INPUT FUNCTIONALITY FOR NEW ENTRIES


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


def enter_searching_option(field):
    """
    Receives and validate input data
    :return: date (string)
    """
    valid_data = False
    # used to keep track of the values and change them in other scopes
    input_data = {field: ''}

    tasks_entries = Task.select()
    date_set = set()  # this way we guarantee no repeated elements.
    for task in tasks_entries:
        if field == 'date':
            date_set.add(task.date)
        elif field == 'employee_name':
            date_set.add(task.employee_name)
    set_length = len(date_set)

    while not valid_data:
        print("Select from options below" + "\n")
        order_list = list(range(1, (set_length + 1)))
        option_list = list(date_set)
        field_option_selected = input(print_options(order_list, option_list))
        if re.match('\d+', field_option_selected) and int(field_option_selected) < (set_length + 1):
            # it's gotta be a number no greater than the options max number\
            input_data[field] = option_list[(int(field_option_selected) - 1)]
            valid_data = True
            clean_scr()
        elif field_option_selected in option_list:
            # then the user enter the value for the entry i.e Name , date , etc
            input_data[field] = field_option_selected
            valid_data = True
            clean_scr()

    return find_tasks_by_field(field, input_data[field])


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


# Accessing the database


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
    elif field == 'employee_name':
        tasks = Task.select().where(Task.employee_name == field_value)
        return tasks
    elif field == 'time_spent':
        tasks = Task.select().where(Task.time_spent == field_value)
        return tasks
    elif field == 'search_str':
        tasks = Task.select().where((Task.title.contains(field_value)) |
                                    (Task.notes.contains(field_value)))
        return tasks
