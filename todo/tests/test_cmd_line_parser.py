# -*- coding: utf-8 -*-
from unittest.mock import Mock, patch, call
import pytest
import sqlite3
from todo.todo import Todo
import argparse
from todo.cmd_manager import CmdLineParser


def test_add_subcommand_with_set_context():
    mock_dispatcher = Mock()
    mock_add_action = Mock()
    mock_dispatcher._add_action = mock_add_action 
    parser = CmdLineParser(['add', 'hello'], mock_dispatcher)
    assert vars(parser.args) == {
        'add-text': 'hello',
        'init': False,
        'dispatch': mock_add_action
    }


def test_add_subcommand_without_set_context():
    
    with pytest.raises(SystemExit):
        mock_dispatcher = Mock()
        CmdLineParser(['add'], mock_dispatcher)


def test_delete_subcommand_with_set_args():
    mock_dispatcher = Mock()
    mock_delete_action = Mock()
    mock_dispatcher._delete_action = mock_delete_action 
    parser = CmdLineParser(['delete', '1'], mock_dispatcher)
    assert vars(parser.args) == {
        'del-task-id': 1, 
        'init': False,
        'dispatch': mock_delete_action
    }


def test_delete_subcommand_without_set_args():
    
    with pytest.raises(SystemExit):
        mock_dispatcher = Mock()
        CmdLineParser(['delete'], mock_dispatcher)


def test_update_subcommand_with_set_args():
    mock_dispatcher = Mock()
    mock_update_action = Mock()
    mock_dispatcher._update_action = mock_update_action 
    parser = CmdLineParser(['update', '-i', '1', '-t', 'Hello'], mock_dispatcher)
    assert vars(parser.args) == {
        'init': False,
        'update_task_id': 1,
        'update_task_text': 'Hello',
        'dispatch': mock_update_action
    }


def test_update_subcommand_without_set_right_args():
    mock_dispatcher = Mock()
    with pytest.raises(SystemExit):
        CmdLineParser(['update'], mock_dispatcher)
    
    with pytest.raises(SystemExit):
        CmdLineParser(['update', '-i', '-t'], mock_dispatcher)
    
    with pytest.raises(SystemExit):
        CmdLineParser(['update', '-i', '1'], mock_dispatcher)
    
    with pytest.raises(SystemExit):
        CmdLineParser(['update', '-i', '1', '-t'], mock_dispatcher)
    
    with pytest.raises(SystemExit):
        CmdLineParser(['update', '-t', 'hello'], mock_dispatcher)


def test_show_subcommand_set_option():
    mock_dispatcher = Mock()
    mock_show_action = Mock()
    mock_dispatcher._show_action = mock_show_action 
    parser = CmdLineParser(['show', '-c'], mock_dispatcher)
    assert vars(parser.args) == {
        'all': False,
        'complete': True,
        'incomplete': False,
        'init': False,
        'dispatch': mock_show_action
    }

    parser = CmdLineParser(['show', '-i'], mock_dispatcher)
    assert vars(parser.args) == {
        'all': False,
        'complete': False,
        'incomplete': True,
        'init': False,
        'dispatch': mock_show_action
    }

    parser = CmdLineParser(['show', '-a'], mock_dispatcher)
    assert vars(parser.args) == {
        'all': True,
        'complete': False,
        'incomplete': False,
        'init': False,
        'dispatch': mock_show_action
    }


def test_complete_subcommand_set_args():
    mock_dispatcher = Mock()
    mock_complete_action = Mock()
    mock_dispatcher._complete_action = mock_complete_action 
    
    parser = CmdLineParser(['complete', '1'], mock_dispatcher)
    assert vars(parser.args) == {
        'complete-task-id': 1,
        'init': False,
        'dispatch': mock_complete_action
    }


def test_complete_subcommand_withou_set_args():
    mock_dispatcher = Mock()

    with pytest.raises(SystemExit):
        CmdLineParser(['complete'], mock_dispatcher)
