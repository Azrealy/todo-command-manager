# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from .todo import Todo
from .utility import RecordIsNotFoundError
from datetime import datetime
import time


class CmdLineParser(ArgumentParser):

    def __init__(self, argv):
        super(CmdLineParser, self).__init__(description='Todo list manager')
        Todo.create_table()
        self.add_argument('--init', action='store_true',
                          help='Initialize table of the database.')
        self.subparsers = self.add_subparsers(
            help='sub-command of Todo List manager help')
        self.subparsers._parser_class = ArgumentParser
        self.subcommand_add()
        self.subcommand_delete()
        self.subcommand_update()
        self.subcommand_show()
        self.subcommand_complete()
        self.dict_args = vars(self.parse_args(argv))

    def subcommand_add(self):
        """
        Create `add` subcommand of todo cli.
        """
        parser_add = self.subparsers.add_parser(
            'add', help='Add a task to the todo list')
        parser_add.add_argument('add-text', type=str,
                                help='Add a task using this context.')

    def subcommand_delete(self):
        """
        Create `delete` subcommand of todo cli.
        """
        parser_delete = self.subparsers.add_parser(
            'delete', help='Delete a task in the todo list.')
        parser_delete.add_argument('del-task-id', type=int,
                                   help='The task id you want to delete.')

    def subcommand_update(self):
        """
        Create `update` subcommand of todo cli.
        With two require options `--update-task-id` and `--update-task-text`
        use to update task.
        """
        parser_update = self.subparsers.add_parser(
            'update', help='Update a task to the todo list.')
        parser_update.add_argument('-i', '--update-task-id', type=int, required=True,
                                   help='The task id you want to update.')
        parser_update.add_argument('-t', '--update-task-text', type=str, required=True,
                                   help='The context of task you want update.')

    def subcommand_show(self):
        """
        Create `show` subcommand of todo cli.
        """
        parser_show = self.subparsers.add_parser(
            'show', help='Show the todo list.')
        parser_show.add_argument('-c', '--complete', action='store_true', default=False,
                                 help='Show complete task list.')
        parser_show.add_argument('-i', '--incomplete', action='store_true', default=False,
                                 help='Show incomplete task list.')
        parser_show.add_argument('-a', '--all', action='store_true', default=False,
                                 help='Show all tasks.')

    def subcommand_complete(self):
        """
        Create `complete` subcommand of todo cli.
        """
        parser_complete = self.subparsers.add_parser(
            'complete', help='Mark a task as complete.')
        parser_complete.add_argument('complete-task-id', type=int,
                                     help='The task id you want complete.')

    def execute_sql_by_command(self):
        """
        Depends on command line args to manipulate DB.
        """
        if self.dict_args['init']:
            Todo.drop_table()
            print('Todo list initialized successfully.')

        elif 'add-text' in self.dict_args:
            text = self.dict_args['add-text']
            Todo(context=text, id=generate_next_id()).save()
            print('Task has been added successfully.')
            result = Todo.find_all({'flag': False})
            self._print_and_check_result(result)

        elif 'del-task-id' in self.dict_args:
            id = self.dict_args['del-task-id']
            result = Todo(id=id).remove()
            if result:
                print('Task {} is deleted successfully.'.format(self.dict_args['del-task-id']))
            else:
                raise RecordIsNotFoundError('This id of task not exist.')

        elif 'update_task_id' in self.dict_args:
            id = self.dict_args['update_task_id']
            text = self.dict_args['update_task_text']
            result = Todo(id=id, context=text, update_at=time.time()).update()
            if result:
                print('The Context of task {} has changed to "{}".'.format(id, text))
            else:
                raise RecordIsNotFoundError('This id of task not exist.')

        elif 'complete-task-id'in self.dict_args:
            id = self.dict_args['complete-task-id']
            result = Todo(id=id, flag=True, update_at=time.time()).update()
            if result:
                print('Task {} complete.'.format(id))
            else:
                raise RecordIsNotFoundError('This id of task not exist.')

        elif 'complete' in self.dict_args and self.dict_args['complete']:
            result = Todo.find_all({"flag" : True})
            self._print_and_check_result(result)

        elif 'incomplete' in self.dict_args and self.dict_args['incomplete']:
            result = Todo.find_all({"flag": False})
            self._print_and_check_result(result)

        elif 'all' in self.dict_args and self.dict_args['all']:
            result = Todo.find_all()
            self._print_and_check_result(result)

    def _print_and_check_result(self, result):
        """
        Check the task lines from DB

        Parameters:
        -----------
        result : list(todo) or None
            A list of todo dict.
        """
        if result:
            for r in result:
                print('{} | {} (Created At: {}, Updated At: {})'.format(
                    str(r.id), r.context, 
                    datetime_filter(r.created_at),
                    '' if r.update_at == 0.0 else datetime_filter(r.update_at)
                ))
        else:
            print('No task exist.')
    
def generate_next_id():
    """
    Generate the next id column

    Returns:
    --------
    id : int
        Return the Highest id plus one,
        if table is empty return 1.
    """
    todo = Todo.find_all(order_by='id desc', size=1)
    if todo:
        return int(todo[0].id) + 1
    else:
        return 1

def datetime_filter(stored_time):
    """
    Filter datetime

    Parameters
    ----------
    stored_time : time.time object
        Time stored in DB
    
    Returns
    -------
    message : str
        Message of elapsed time
    """
    delta = int(time.time() - stored_time)
    if delta < 60:
        return u'1 mins ago'
    if delta < 3600:
        return u'%s mins ago' % (delta // 60)
    if delta < 86400:
        return u'%s hours ago' % (delta // 3600)
    if delta < 604800:
        return u'%s days ago' % (delta // 86400)
    dt = datetime.fromtimestamp(stored_time)
    return u'%s year %s month %s day ago' % (dt.year, dt.month, dt.day)
