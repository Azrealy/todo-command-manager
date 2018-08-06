# -*- coding: utf-8 -*-
from .cmd_parser import CmdLineParser
from .utility import RecordIsNotFoundError
import sys


def main():
    """
    Main() function execute todo cli.
    """
    try:
        if len(sys.argv[1:]) < 1:
            print('too few arguments.')
        else:
            cmd_parser = CmdLineParser(sys.argv[1:])
            cmd_parser.execute_sql_by_command()
    except RecordIsNotFoundError as e:
        print(str(e), file=sys.stderr)

