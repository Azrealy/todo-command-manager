# -*- coding: utf-8 -*-
from unittest.mock import Mock, patch, call
import pytest
import sqlite3
from todo.todo import Todo
import argparse
from todo.cmd_manager import CmdLineParser


def test_add_subcommand_with_set_context():
    with patch('todo.cmd_manager.CmdLineParser._add_action') as mock_add_action:
        parser = CmdLineParser(['add', 'hello'])
        assert vars(parser.args) == {
            'add-text': 'hello',
            'init': False,
            'execute_cmd': mock_add_action,
            'file_path': None
        }


def test_add_subcommand_without_set_context():
    with pytest.raises(SystemExit):
        mock_execute_cmder = Mock()
        CmdLineParser(['add'])


def test_delete_subcommand_with_set_args():
    with patch('todo.cmd_manager.CmdLineParser._delete_action') as mock_delete_action:
        parser = CmdLineParser(['delete', '1'])
        assert vars(parser.args) == {
            'del-task-id': 1, 
            'init': False,
            'execute_cmd': mock_delete_action,
            'file_path': None
        }


def test_delete_subcommand_without_set_args():
    
    with pytest.raises(SystemExit):
        CmdLineParser(['delete'])


def test_update_subcommand_with_set_args():
    with patch('todo.cmd_manager.CmdLineParser._update_action') as mock_update_action:
        parser = CmdLineParser(['update', '-i', '1', '-t', 'Hello'])
        assert vars(parser.args) == {
            'init': False,
            'update_task_id': 1,
            'update_task_text': 'Hello',
            'execute_cmd': mock_update_action,
            'file_path': None
        }


def test_update_subcommand_without_set_right_args():
    with pytest.raises(SystemExit):
        CmdLineParser(['update'])
    
    with pytest.raises(SystemExit):
        CmdLineParser(['update', '-i', '-t'])
    
    with pytest.raises(SystemExit):
        CmdLineParser(['update', '-i', '1'])
    
    with pytest.raises(SystemExit):
        CmdLineParser(['update', '-i', '1', '-t'])
    
    with pytest.raises(SystemExit):
        CmdLineParser(['update', '-t', 'hello'])


def test_show_subcommand_set_option():

    with patch('todo.cmd_manager.CmdLineParser._show_action') as mock_show_action:

        parser = CmdLineParser(['show', '-c'])

        assert vars(parser.args) == {
            'all': False,
            'complete': True,
            'incomplete': False,
            'init': False,
            'execute_cmd': mock_show_action,
            'file_path': None
        }

        parser = CmdLineParser(['show', '-i'])
        assert vars(parser.args) == {
            'all': False,
            'complete': False,
            'incomplete': True,
            'init': False,
            'execute_cmd': mock_show_action,
            'file_path': None
        }

        parser = CmdLineParser(['show', '-a'])
        assert vars(parser.args) == {
            'all': True,
            'complete': False,
            'incomplete': False,
            'init': False,
            'execute_cmd': mock_show_action,
            'file_path': None
        }


def test_complete_subcommand_set_args():
    with patch('todo.cmd_manager.CmdLineParser._complete_action') as mock_complete_action:
        parser = CmdLineParser(['complete', '1'])
        assert vars(parser.args) == {
            'complete-task-id': 1,
            'init': False,
            'execute_cmd': mock_complete_action,
            'file_path': None
        }


def test_complete_subcommand_withou_set_args():

    with pytest.raises(SystemExit):
        CmdLineParser(['complete'])
