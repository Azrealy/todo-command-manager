# -*- coding: utf-8 -*-
from .cmd_manager import CmdLineParser, TodoActionDispatcher
from .utility import RecordIsNotFoundError
from .todo import Todo
import sys


def main():
    """
    Main() function execute todo cli.
    """
    try:
        Todo.create_table()
        if len(sys.argv[1:]) < 1:
            print('too few arguments.')
        else:
            parser = CmdLineParser(sys.argv[1:], TodoActionDispatcher())
            parser.args.dispatch(parser.args)

    except RecordIsNotFoundError as e:
        print(str(e), file=sys.stderr)

