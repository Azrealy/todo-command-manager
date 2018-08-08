# -*- coding: utf-8 -*-
from unittest.mock import Mock, patch, call
import pytest
import sqlite3
import argparse
from todo.cmd_manager import TodoActionDispatcher
from todo.todo import Todo


def test_init_action():
    with patch('todo.cmd_manager.Todo') as mock_todo:
        TodoActionDispatcher()._init_action()
        assert mock_todo.drop_table.call_count == 1


def test_add_action():
    with patch('todo.cmd_manager.Todo') as mock_todo:
        with patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(**{'add-text': 'add-test'})) as mock_args:
            with patch(
                'todo.cmd_manager.TodoActionDispatcher.generate_next_id') as mock_id:
                mock_id.return_value = 10
                TodoActionDispatcher()._add_action(mock_args.return_value)
                assert mock_todo.call_args == call(context='add-test', id=10)
                assert mock_todo.return_value.save.call_count == 1
                assert mock_todo.find_all.call_args == call({'flag': False})


def test_delete_action():
    with patch('todo.cmd_manager.Todo') as mock_todo:
        with patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(**{'del-task-id': 12})) as mock_args:
            TodoActionDispatcher()._delete_action(mock_args.return_value)
            assert mock_todo.call_args == call(id=12)
            assert mock_todo.return_value.remove.call_count == 1


def test_update_action():
    with patch('todo.cmd_manager.Todo') as mock_todo:
        with patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(
                **{'update_task_id': 12,'update_task_text': 'update-text'})) as mock_args:
            with patch('todo.cmd_manager.time.time') as mock_time:
                mock_time.return_value = 10.102
                TodoActionDispatcher()._update_action(mock_args.return_value)
                assert mock_todo.call_args == call(
                    context='update-text',
                    id=12,
                    update_at=10.102
                )
                assert mock_todo.return_value.update.call_count == 1


def test_complete_action():
    with patch('todo.cmd_manager.Todo') as mock_todo:
        with patch('argparse.ArgumentParser.parse_args',
                   return_value=argparse.Namespace(
                **{'complete-task-id': 10})) as mock_args:
            with patch('todo.cmd_manager.time.time') as mock_time:
                mock_time.return_value = 1010.1010
                TodoActionDispatcher()._complete_action(mock_args.return_value)
                assert mock_todo.call_args == call(
                    flag=True,
                    id=10,
                    update_at=1010.1010
                )
                assert mock_todo.return_value.update.call_count == 1


def test_show_action_when_choice_complete():
    with patch('todo.cmd_manager.Todo') as mock_todo:
        with patch('argparse.ArgumentParser.parse_args',
                   return_value=argparse.Namespace(
                **{'complete': True, 'all': False, 'incomplete': False})) as mock_args:
                TodoActionDispatcher()._show_action(mock_args.return_value)
                assert mock_todo.find_all.call_args == call(
                    {'flag': True}
                )


def test_show_action_when_choice_incomplete():
    with patch('todo.cmd_manager.Todo') as mock_todo:
        with patch('argparse.ArgumentParser.parse_args',
                   return_value=argparse.Namespace(
                **{'complete': False, 'all': False, 'incomplete': True})) as mock_args:
                TodoActionDispatcher()._show_action(mock_args.return_value)
                assert mock_todo.find_all.call_args == call(
                    {'flag': False}
                )


def test_show_action_when_choice_all():
    with patch('todo.cmd_manager.Todo') as mock_todo:
        with patch('argparse.ArgumentParser.parse_args',
                   return_value=argparse.Namespace(
                **{'complete': False, 'all': True, 'incomplete': False})) as mock_args:
                TodoActionDispatcher()._show_action(mock_args.return_value)
                assert mock_todo.find_all.call_args == call()


def test_generate_next_id():
    
    with patch('todo.cmd_manager.Todo') as mock_todo:
        mock_todo.find_all.return_value = [Todo(id=8)]
        result = TodoActionDispatcher().generate_next_id()
        assert mock_todo.find_all.call_args == call(order_by='id desc', size=1)
        assert result == 9
        mock_todo.find_all.return_value = None
        result = TodoActionDispatcher().generate_next_id()
        assert result == 1
