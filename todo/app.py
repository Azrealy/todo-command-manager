# -*- coding: utf-8 -*-
from .cmd_manager import CmdLineParser
from .utility import RecordIsNotFoundError
from .todo import Todo
from .utility import SQLConnection
import sys


def main():
    """
    Main() function execute todo cli.
    """
    try:
        if len(sys.argv[1:]) < 1:
            print('too few arguments.')
        else:
            parser = CmdLineParser(sys.argv[1:])
            path = vars(parser.args)['file_path']
            if path:
                SQLConnection.initialize(path)
            Todo.create_table()
            parser.args.execute_action()

    except RecordIsNotFoundError as e:
        print(str(e), file=sys.stderr)

