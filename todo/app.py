# -*- coding: utf-8 -*-
from .cmd_manager import CmdLineParser
from .utility import RecordIsNotFoundError
from .todo import Todo
from .utility import SQLConnection
import sys


def main():
    """
    Main function execute todo cli.
    """
    try:
        if len(sys.argv) == 1:
            CmdLineParser(['-h'])
        else:
            parser = CmdLineParser(sys.argv[1:])
            path = vars(parser.args)['file_path']
            if path:
                SQLConnection.initialize(path)
            Todo.create_table()
            parser.args.execute_cmd()

    except RecordIsNotFoundError as e:
        # As usually Unix programs does, `todo` cmd use exit code 2 for
        # command line syntax errors and 1 for all other kinds of errors.
        print(str(e), file=sys.stderr)
        sys.exit(2)
        
    except Exception:
        print('Failed to execute todo command...', file=sys.stderr)
        sys.exit(1)
