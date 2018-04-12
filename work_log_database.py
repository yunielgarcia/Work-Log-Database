import os
import csv
import datetime

import utils
from task import Task


def add_entry_data():
    """
    Collects and validates data needed to create a task.
    Creates Task instance.
    Call to save in csv
    """
    task_date = utils.enter_date()
    task_title = utils.enter_title()
    task_time_spent = utils.enter_time_spent()
    task_notes = utils.enter_notes()

    # create instance
    task = Task(task_date, task_title, task_time_spent, task_notes)
    # call to save it
    save_entry(task)


def save_entry(task):
    """
    Saves the task in the csv file
    :param task:
    :return:
    """
    try:
        open('log.csv', 'a')
    except IOError:
        print("Couldn't open the file.")
    else:
        if isinstance(task, Task):
            with open('log.csv', 'a') as csvfile:
                fieldnames = vars(task).keys()
                task_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # only if file is empty write headers
                if os.stat("log.csv").st_size == 0:
                    task_writer.writeheader()

                task_writer.writerow(vars(task))
                utils.clean_scr()
                input("Task added. Press enter to return to the menu")
                utils.clean_scr()
        else:
            print("Couldn't save. Data is corrupted.")


# SEARCHING FUNCTIONALITY
def print_tasks(tasks_list):
    """Displays result tasks by exact date"""
    if len(tasks_list) == 0:
        input("No tasks found. Press enter to return")
        utils.clean_scr()
    else:
        for task in tasks_list:
            print("Date: " + task['date'])
            print("Title: " + task['title'])
            print("Time Spent: " + task['time_spent'])
            print("Notes : " + task['notes'])
            if len(tasks_list) > 1:

                print("-"*40)
        input("\n" + "Press enter to return to search menu")
        utils.clean_scr()


def get_by_exact_date():
    """Retrieve result tasks by exact date"""
    desire_date = utils.enter_searching_date()
    tasks = utils.find_tasks_by_field('date', desire_date)
    print_tasks(tasks)


def get_by_time():
    """Retrieve result tasks by exact time"""
    desire_time = utils.enter_searching_time()
    tasks = utils.find_tasks_by_field('time_spent', desire_time)
    print_tasks(tasks)


def get_by_range():
    """Retrieve result tasks by date range"""
    range_dict = utils.enter_searching_date_range()

    # create both datetime obj out of dict
    dt_start = datetime.datetime.strptime(range_dict['dt_start'], '%d/%m/%Y')
    dt_end = datetime.datetime.strptime(range_dict['dt_end'], '%d/%m/%Y')

    # let's make a validation for that range
    if dt_start > dt_end:
        # Do all again, range is wrong
        print("Starting date {starting} is greater than ending date {ending}".format(starting=dt_start, ending=dt_end))
        get_by_range()
    else:
        tasks = utils.find_tasks_by_date_range(dt_start, dt_end)
        print_tasks(tasks)


def get_by_string():
    str_w = input("Enter word or part of if: ")
    tasks = utils.find_tasks_by_word(str_w)
    print_tasks(tasks)


def get_by_regex():
    regex = input("Enter your regular expression: ")
    tasks = utils.find_tasks_by_pattern(regex)
    print_tasks(tasks)


def search_tasks():
    """
    Starts the looping over the search actions.
    Once done, it falls back to main menu loop actions
    :return:
    """
    loop_search = True
    while loop_search:
        print("Do you want to search by:" + "\n")
        search_option = input(utils.print_options(utils.SEARCHING_CRITERIA_ORDER, utils.SEARCHING_CRITERIA))
        if search_option == 'f':
            utils.clean_scr()
            loop_search = False
        elif search_option == 'a':
            utils.clean_scr()
            get_by_exact_date()
        elif search_option == 'b':
            utils.clean_scr()
            get_by_range()
        elif search_option == 'c':
            utils.clean_scr()
            get_by_string()
        elif search_option == 'd':
            utils.clean_scr()
            get_by_time()
        elif search_option == 'e':
            utils.clean_scr()
            get_by_regex()
        else:
            utils.clean_scr()
            print('Please select a letter option.')


# main function
def execute():
    loop = True
    while loop:
        print("\n" + "What would you like to do: " + "\n")
        main_option = input(utils.print_options(utils.OPTIONS_ORDER, utils.OPTIONS_TEXT))
        if main_option == 'c':
            utils.clean_scr()
            print('Thanks.')
            loop = False
        elif main_option == 'a':
            utils.clean_scr()
            add_entry_data()
        elif main_option == 'b':
            utils.clean_scr()
            search_tasks()
        else:
            print('Please select a letter option.')


if __name__ == "__main__":
    execute()
