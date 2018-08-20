# -*- coding: utf-8 -*-
from unittest.mock import Mock, patch, call
import pytest
import sqlite3
import argparse
from todo.cmd_manager import CmdLineParser
from todo.todo import Todo


def test_init_action():
    with patch('todo.cmd_manager.Todo') as mock_todo:
        parser = CmdLineParser(['--init'])
        parser._init_action()
        assert mock_todo.drop_table.call_count == 1


def test_add_action():
    with patch('todo.cmd_manager.Todo') as mock_todo:
        with patch(
            'todo.cmd_manager.CmdLineParser.generate_next_id') as mock_id:
            mock_id.return_value = 10
            CmdLineParser(['add', 'test text'])._add_action()
            assert mock_todo.call_args == call(text='test text', id=10)
            assert mock_todo.return_value.save.call_count == 1
            assert mock_todo.find_all.call_args == call({'is_completed': False})


def test_delete_action():
    with patch('todo.cmd_manager.Todo') as mock_todo:
        CmdLineParser(['delete', '1'])._delete_action()
        assert mock_todo.call_args == call(id=1)
        assert mock_todo.return_value.remove.call_count == 1


def test_update_action():
    with patch('todo.cmd_manager.Todo') as mock_todo:
        with patch('todo.cmd_manager.time.time') as mock_time:
            mock_time.return_value = 10.102
            CmdLineParser(['update', '-i', '1', '-t', 'new text'])._update_action()
            assert mock_todo.call_args == call(
                text='new text',
                id=1,
                update_at=10.102
            )
            assert mock_todo.return_value.update.call_count == 1


def test_complete_action():
    with patch('todo.cmd_manager.Todo') as mock_todo:
        with patch('todo.cmd_manager.time.time') as mock_time:
            mock_time.return_value = 1010.1010
            CmdLineParser(['complete', '10'])._complete_action()
            assert mock_todo.call_args == call(
                is_completed=True,
                id=10,
                update_at=1010.1010
            )
            assert mock_todo.return_value.update.call_count == 1


def test_show_action_when_choice_complete():
    with patch('todo.cmd_manager.Todo') as mock_todo:
        CmdLineParser(['show', '-c'])._show_action()
        assert mock_todo.find_all.call_args == call(
            {'is_completed': True}
        )


def test_show_action_when_choice_incomplete():
    with patch('todo.cmd_manager.Todo') as mock_todo:
        CmdLineParser(['show', '-i'])._show_action()
        assert mock_todo.find_all.call_args == call(
            {'is_completed': False}
        )


def test_show_action_when_choice_all():
    with patch('todo.cmd_manager.Todo') as mock_todo:
        CmdLineParser(['show', '-a'])._show_action()
        assert mock_todo.find_all.call_args == call()


def test_generate_next_id():
    
    with patch('todo.cmd_manager.Todo') as mock_todo:
        mock_todo.find_all.return_value = [Todo(id=8)]
        result = CmdLineParser([]).generate_next_id()
        assert mock_todo.find_all.call_args == call(order_by='id desc', size=1)
        assert result == 9
        mock_todo.find_all.return_value = None
        result = CmdLineParser([]).generate_next_id()
        assert result == 1
