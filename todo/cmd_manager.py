# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from .todo import Todo
from .utility import RecordIsNotFoundError, datetime_filter
from datetime import datetime
import time


class TodoActionDispatcher(object):
    
    def _init_action(self):
        """
        Initial todo table action
        """
        Todo.drop_table()

    def _add_action(self, args):
        """
        Add todo action

        Parameters
        ----------
        args : argparse.Namespace
            An Namespace object of argparse use to storing attributes. 
        """
        text = vars(args)['add-text']
        Todo(context=text, id=self.generate_next_id()).save()
        print('Task has been added successfully.')
        result = Todo.find_all({'flag': False})
        self._print_and_check_result(result)
    
    def _delete_action(self, args):
        """
        Delete todo action

        Parameters
        ----------
        args : argparse.Namespace
            An Namespace object of argparse use to storing attributes. 
        """
        id = vars(args)['del-task-id']
        result = Todo(id=id).remove()
        if result:
            print('Task {} is deleted successfully.'.format(id))
        else:
            raise RecordIsNotFoundError('This id of task not exist.')    

    def _update_action(self, args):
        """
        Update todo action

        Parameters
        ----------
        args : argparse.Namespace
            An Namespace object of argparse use to storing attributes.  
        """

        id = vars(args)['update_task_id']
        text = vars(args)['update_task_text']
        result = Todo(id=id, context=text, update_at=time.time()).update()
        if result:
            print('The Context of task {} has changed to "{}".'.format(id, text))
        else:
            raise RecordIsNotFoundError('This id of task not exist.')

    def _show_action(self, args):
        """
        Show todo action
        
        Parameters
        ----------
        args : argparse.Namespace
            An Namespace object of argparse use to storing attributes.  
        """
        if vars(args)['complete']:
            result = Todo.find_all({"flag" : True})
            self._print_and_check_result(result)

        elif vars(args)['incomplete']:
            result = Todo.find_all({"flag": False})
            self._print_and_check_result(result)

        elif vars(args)['all']:
            result = Todo.find_all()
            self._print_and_check_result(result)

    def _complete_action(self, args):
        """
        Complete todo action
        
        Parameters
        ----------
        args : argparse.Namespace
            An Namespace object of argparse use to storing attributes.  
        """
        id = vars(args)['complete-task-id']
        result = Todo(id=id, flag=True, update_at=time.time()).update()
        if result:
            print('Task {} complete.'.format(id))
        else:
            raise RecordIsNotFoundError('This id of task not exist.')

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

    def generate_next_id(self):
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


class CmdLineParser(object):

    def __init__(self, argv, dispatcher):
        self.dispatcher = dispatcher
        self.parser = ArgumentParser(description='Todo list manager')
        self.subparsers = self.parser.add_subparsers(
            help='sub-command of Todo List manager help')
        self.option_command_init()
        self.subcommand_add()
        self.subcommand_delete()
        self.subcommand_update()
        self.subcommand_show()
        self.subcommand_complete()
        self.args = self.parser.parse_args(argv)

    def option_command_init(self):
        """
        Create `--init` option of todo cli.
        """
        self.parser.add_argument('--init', action='store_true',
                          help='Initialize table of the database.')
        self.parser.set_defaults(dispatch=self.dispatcher._init_action)

    def subcommand_add(self):
        """
        Create `add` subcommand of todo cli.
        """
        parser_add = self.subparsers.add_parser(
            'add', help='Add a task to the todo list')
        parser_add.add_argument('add-text', type=str,
                                help='Add a task using this context.')
        parser_add.set_defaults(dispatch=self.dispatcher._add_action)

    def subcommand_delete(self):
        """
        Create `delete` subcommand of todo cli.
        """
        parser_delete = self.subparsers.add_parser(
            'delete', help='Delete a task in the todo list.')
        parser_delete.add_argument('del-task-id', type=int,
                                   help='The task id you want to delete.')
        parser_delete.set_defaults(dispatch=self.dispatcher._delete_action)

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
        parser_update.set_defaults(dispatch=self.dispatcher._update_action)

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
        parser_show.set_defaults(dispatch=self.dispatcher._show_action)

    def subcommand_complete(self):
        """
        Create `complete` subcommand of todo cli.
        """
        parser_complete = self.subparsers.add_parser(
            'complete', help='Mark a task as complete.')
        parser_complete.add_argument('complete-task-id', type=int,
                                     help='The task id you want complete.')
        parser_complete.set_defaults(dispatch=self.dispatcher._complete_action)
    