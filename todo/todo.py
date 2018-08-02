# -*- coding: utf-8 -*-
from .model import Model
import argparse
from functools import wraps

class RecordIsNotFoundError(Exception):
    """
    Record is not found.
    """
    pass

def check_task_exist(method):
    """
    Decorator for TodoList class methods that check whether exists
    the task.

    Notes:
    ------
    ..note:: This decorator should be used at the method which have
             the index argument. Because we use id of the task to
             check existence.
    """
    @wraps(method)
    def wrapper(self, index, *args):
        check = self.select(table_name = self.table_name, id = index)
        if check.fetchall():
            return method(self, index, *args)
        else:
            raise RecordIsNotFoundError('This id of task not exist.')

    return wrapper

class TodoList(Model):
    """
    Todo List manager
    """
    def __init__(self, data_file):
        """
        Inherit the model class
        """
        values = ['id INTEGER NOT NULL PRIMARY KEY',
                  'context TEXT NOT NULL',
                  'completed boolean NOT NULL']
        super(TodoList, self).__init__(data_file)
        self.table_name = 'todo_list'
        self.create_table(self.table_name, values)
        

    def _get_greatest_id(self):
        """
        Use select all SQL statement
        get greatest id of todo list table.

        Returns
        -------
        id : int
            If todo list is empty return 0,
            else return the max id of todo list.
        """
        cursor = self.select_all(self.table_name, option = 'order by id desc')
        result = cursor.fetchone()
        cursor.close()
        if result:
            return result[0]
        else:
            return 0

    def show_todo_list_by_status(self, completed):
        """
        Show the tasks using task status.
    
        Parameters
        ----------
        completed : bool
            Completed status of task.

        Returns
        -------
        result : list
            List of task column.
        """
        cursor = self.select(table_name = self.table_name, completed = completed)
        result = cursor.fetchall()
        cursor.close()
        return result 


    def show_todo_list(self):
        """
        Show the all tasks in todo list.

        Returns
        -------
        result : list
            List of task column.
        """
        cursor = self.select_all(table_name = self.table_name)
        result = cursor.fetchall()
        cursor.close()
        return result

    def add_task(self, context):
        """
        Add task to todo list.

        Parameters
        ----------
        context : str
            Context of task
        """
        id = self._get_greatest_id() + 1
        cursor = self.insert(self.table_name, id=id, context=context, completed = False)
        cursor.close()

    @check_task_exist
    def complete_task_by_id(self, index):
        """
        Change the task status using task ID

        Parameters
        ----------
        index : int
            ID of task
        """
        set_values = {'completed': True}
        cursor = self.update_item(table_name = self.table_name,
                                  set_values = set_values,
                                  id=index)
        cursor.close()

    @check_task_exist
    def update_task_by_id(self, index, context):
        """
        Update the task context using task ID

        Parameters
        ----------
        index : int
            ID of task
        context : str
            New context of task
        """
        set_values = {'context': context}
        cursor = self.update_item(table_name = self.table_name,
                                  set_values = set_values,
                                  id=index)
        cursor.close()

    @check_task_exist
    def delete_task_by_id(self, index):
        """
        Delete the task using task ID

        Parameters
        ----------
        index : int
            ID of task
        """
        cursor = self.delete_item(table_name = self.table_name, id=index)
        cursor.close()

    def destory_todo_list(self):
        """
        Drop the todo list table
        """
        cursor = self.drop_table(self.table_name)
        cursor.close()
