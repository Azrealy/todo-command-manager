from argparse import ArgumentParser
import sys

class CmdLineParser(ArgumentParser):
    
    def __init__(self, argv):
        super(CmdLineParser, self).__init__(description='Todo list manager')
        self.add_argument('--init', action='store_true', help='Initialize table of the database.')
        self.subparsers = self.add_subparsers(help='sub-command of Todo List manager help')
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
        parser_add = self.subparsers.add_parser('add', help='Add a task to the todo list')
        parser_add.add_argument('add-text', type=str, help='Add a task using this context.')

    def subcommand_delete(self):
        """
        Create `delete` subcommand of todo cli.
        """
        parser_delete = self.subparsers.add_parser('delete', help='Delete a task in the todo list.')
        parser_delete.add_argument('del-task-id', type=int,
                                help='The task id you want to delete.')
                                
    def subcommand_update(self):
        """
        Create `update` subcommand of todo cli.
        With two require options `--update-task-id` and `--update-task-text`
        use to update task.
        """
        parser_update = self.subparsers.add_parser('update', help='Update a task to the todo list.')
        parser_update.add_argument('-i', '--update-task-id', type=int, required=True,
                                help='The task id you want to update.')
        parser_update.add_argument('-t', '--update-task-text', type=str, required=True,
                                help='The context of task you want update.')

    def subcommand_show(self):
        """
        Create `show` subcommand of todo cli.
        """
        parser_show = self.subparsers.add_parser('show', help='Show the todo list.')
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
        parser_complete = self.subparsers.add_parser('complete', help='Mark a task as complete.')
        parser_complete.add_argument('complete-task-id', type=int,
                                    help='The task id you want complete.')


    def execute_sql_by_command(self, todo):
        """
        Depends command line args to execute sql.

        Parameters
        ----------
        todo : TodoList
            Instance of TodoList Class.
        """

        if self.dict_args['init']:
            todo.destory_todo_list()
            print('Todo list initailized succussfully.')

        elif 'add-text' in self.dict_args:
            text = self.dict_args['add-text']
            todo.add_task(text)
            print('Task has been added scucessfully.')
            result = todo.show_todo_list_by_status(completed=False)
            for r in result:
                print(str(r[0]) + ' | ' + str(r[1]))

        elif 'del-task-id' in self.dict_args:
            id = self.dict_args['del-task-id']
            todo.delete_task_by_id(id)
            print('Task {} is deleted sucessfully.'.format(self.dict_args['del-task-id']))

        elif 'update_task_id' in self.dict_args:
            id = self.dict_args['update_task_id']
            text = self.dict_args['update_task_text']
            todo.update_task_by_id(id, text)
            print('The Context of task {} has changed to "{}".'.format(id, text))

        elif 'complete-task-id'in self.dict_args:
            id = self.dict_args['complete-task-id']
            todo.complete_task_by_id(index=id)
            print('Task {} complete.'.format(id))

        elif 'complete' in self.dict_args and self.dict_args['complete']:
            result = todo.show_todo_list_by_status(completed=True)
            self._print_and_check_result(result)

        elif 'incomplete' in self.dict_args and self.dict_args['incomplete']:
            result = todo.show_todo_list_by_status(completed=False)
            self._print_and_check_result(result)

        elif 'all' in self.dict_args and self.dict_args['all']:
            result = todo.show_todo_list()
            self._print_and_check_result(result)

    def _print_and_check_result(self, result):
        """
        Check the task lines from DB

        Parameters:
        -----------
        result : list
            List of task column.
        """
        if result:
            for r in result:
                print(str(r[0]) + ' | ' + str(r[1]))
        else:
            print('No task exist.')
