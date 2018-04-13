import datetime
from peewee import *

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
    employee_name = utils.enter_employee_name()

    # create instance
    task = Task(date=task_date,
                title=task_title,
                time_spent=task_time_spent,
                employee_name=employee_name,
                notes=task_notes)
    # call to save it
    save_entry(task)


def save_entry(task):
    """
    Saves the task in the csv file
    :param task:
    :return:
    """
    if isinstance(task, Task):
        Task.create(date=task.date,
                    title=task.title,
                    time_spent=task.time_spent,
                    notes=task.notes,
                    employee_name=task.employee_name,
                    )
        utils.clean_scr()
        input("Task saved. Press enter to return to the menu")
        utils.clean_scr()
    else:
        print("Couldn't save. Data is corrupted.")


# SEARCHING FUNCTIONALITY
def print_tasks(tasks):
    """Displays result tasks by exact date"""
    if not tasks:
        input("No tasks found. Press enter to return")
        utils.clean_scr()
    else:
        for task in tasks:
            print("Date: " + task.date)
            print("Title: " + task.title)
            print("Time Spent: {0.time_spent}".format(task))
            if task.notes:
                print("Notes : " + task.notes)
            print("-" * 40)
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


def get_by_string():
    str_w = input("Enter word or part of if: ")
    tasks = utils.find_tasks_by_word(str_w)
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
        if search_option == 'e':
            utils.clean_scr()
            loop_search = False
        elif search_option == 'a':
            utils.clean_scr()
            get_by_exact_date()
        elif search_option == 'b':
            utils.clean_scr()
            get_by_time()
        elif search_option == 'c':
            utils.clean_scr()
            get_by_string()
        elif search_option == 'd':
            utils.clean_scr()
            get_by_time()
        elif search_option == 'e':
            utils.clean_scr()
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


def initialize():
    db = SqliteDatabase('logs.db')
    with db.connection_context():
        db.create_tables([Task], safe=True)


if __name__ == "__main__":
    initialize()
    execute()
