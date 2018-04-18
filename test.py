import unittest
from unittest.mock import patch

import utils
from task import Task
import work_log_database


class UtilsTests(unittest.TestCase):
    def setUp(self):
        self.menu_order = ['a)', 'b)']
        self.menu_options = [
            ' Add new entry',
            ' Search in existing entries']
        self.test_task = Task('01/01/2000',
                              'tester',
                              99,
                              'test notes',
                              'Tester')
        self.init_db()

    def test_save_task(self):
        new_task = Task('01/01/2000',
                        'tester',
                        99999,
                        'test notes',
                        'Tester')
        work_log_database.save_entry(new_task)
        saved_task = Task.get(Task.time_spent == 99999)
        # import pdb;pdb.set_trace()
        assert(new_task == saved_task)

    def test_menu_option_list(self):
        self.assertEqual((len(utils.SEARCHING_CRITERIA_ORDER)), (len(utils.SEARCHING_CRITERIA)))

    def test_menu_list_format(self):
        menu = utils.print_options(self.menu_order, self.menu_options)
        expected_menu = 'a) -  Add new entry\nb) -  Search in existing entries\n'
        self.assertEqual(menu, expected_menu)

    def test_find_task_by_field_date(self):
        tasks = utils.find_tasks_by_field('date', self.test_task.date)
        self.assertEqual(self.test_task.date, tasks[0].date)

    def test_find_task_by_field_time_spent(self):
        tasks = utils.find_tasks_by_field('time_spent', self.test_task.time_spent)
        # import pdb; pdb.set_trace()
        self.assertEqual(self.test_task.time_spent, tasks[0].time_spent)

    def test_find_task_by_field_search_str(self):
        tasks = utils.find_tasks_by_field('search_str', 'tes')
        # import pdb; pdb.set_trace()
        self.assertTrue('tes' in tasks[0].title or
                        'tes' in tasks[0].notes)

    def test_enter_date(self):
        user_input = [
            '12/12/1212'
        ]
        with patch('builtins.input', side_effect=user_input):
            date = utils.enter_date()
        self.assertEqual(date, '12/12/1212')

    def test_enter_title(self):
        user_input = [
            'task_title'
        ]
        with patch('builtins.input', side_effect=user_input):
            date = utils.enter_title()
        self.assertEqual(date, 'task_title')

    def test_enter_time(self):
        user_input = [
            '99',
        ]
        with patch('builtins.input', side_effect=user_input):
            time = utils.enter_searching_time()
        self.assertEqual(int(time), 99)

    def init_db(self):
        work_log_database.initialize()
        self.delete_data()
        Task.create(date=self.test_task.date,
                    title=self.test_task.title,
                    time_spent=self.test_task.time_spent,
                    notes=self.test_task.notes,
                    employee_name=self.test_task.employee_name)

    def delete_data(self):
        """Deletes test task creater for every test case"""
        Task.delete().where(Task.title == 'tester').execute()


if __name__ == '__main__':
    unittest.main()
