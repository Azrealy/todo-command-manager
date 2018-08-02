from .cmd_parser import CmdLineParser
from .todo import TodoList, RecordIsNotFoundError
import sys

def main():
    """
    Main() function execute todo cli.
    """
    try:
        todo_list = TodoList('file:/tmp/data.db')
        if len(sys.argv[1:]) < 1:
            print('too few arguments.')
        else:
            cmd_parser = CmdLineParser(sys.argv[1:])
            cmd_parser.execute_sql_by_command(todo_list)
            todo_list.conn.commit()

    except RecordIsNotFoundError as e:
        todo_list.conn.rollback()
        print(e)