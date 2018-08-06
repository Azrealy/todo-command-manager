# -*- coding: utf-8 -*-
from unittest.mock import Mock, patch, call
import pytest
import sqlite3
from todo.todo import Todo
import argparse
from todo.cmd_parser import CmdLineParser, generate_next_id, datetime_filter


def test_add_subcommand_with_set_context():
    
    parser = CmdLineParser(['add', 'hello']).dict_args
    assert parser == {'add-text': 'hello', 'init': False}


def test_add_subcommand_without_set_context():
    
    with pytest.raises(SystemExit):
        CmdLineParser(['add'])


def test_delete_subcommand_with_set_args():
    
    parser = CmdLineParser(['delete', '1']).dict_args
    assert parser == {'del-task-id': 1, 'init': False}


def test_delete_subcommand_without_set_args():
    
    with pytest.raises(SystemExit):
        CmdLineParser(['delete'])


def test_update_subcommand_with_set_args():
    
    parser = CmdLineParser(['update', '-i', '1', '-t', 'Hello']).dict_args
    assert parser == {'init': False, 'update_task_id': 1, 'update_task_text': 'Hello'}


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
    
    parser = CmdLineParser(['show', '-c']).dict_args
    assert parser == {'all': False, 'complete': True, 'incomplete': False, 'init': False}

    parser = CmdLineParser(['show', '-i']).dict_args
    assert parser == {'all': False, 'complete': False, 'incomplete': True, 'init': False}

    parser = CmdLineParser(['show', '-a']).dict_args
    assert parser == {'all': True, 'complete': False, 'incomplete': False, 'init': False}


def test_complete_subcommand_set_args():
    
    parser = CmdLineParser(['complete', '1']).dict_args
    assert parser == {'complete-task-id': 1, 'init': False}


def test_complete_subcommand_withou_set_args():
    with pytest.raises(SystemExit):
        CmdLineParser(['complete'])


def test_execute_sql_by_command():
    with patch('todo.cmd_parser.Todo') as mock_todo:
        with patch('todo.cmd_parser.generate_next_id') as mock_id:
            with patch('todo.cmd_parser.time.time') as mock_time:
                mock_id.return_value = 1
                CmdLineParser(['add', 'hello']).execute_sql_by_command()
                assert mock_todo.call_args == call(context='hello', id=1)
                assert mock_todo.return_value.save.call_count == 1
                assert mock_todo.find_all.call_args == call({'flag': False})

                CmdLineParser(['delete', '1']).execute_sql_by_command()
                assert mock_todo.call_args == call(id=1)
                assert mock_todo.return_value.remove.call_count == 1
                
                mock_time.return_value = 12.00
                CmdLineParser(['update', '-i', '1', '-t', 'hello']).execute_sql_by_command()
                assert mock_todo.call_args == call(context='hello', id=1, update_at=12.0)
                assert mock_todo.return_value.update.call_count == 1

                CmdLineParser(['complete', '1']).execute_sql_by_command()
                assert mock_todo.call_args == call(flag=True, id=1, update_at=12.0)

                CmdLineParser(['show', '-c']).execute_sql_by_command()
                assert mock_todo.find_all.call_args == call({"flag" : True})

                CmdLineParser(['show', '-i']).execute_sql_by_command()
                assert mock_todo.find_all.call_args == call({"flag" : False})

                CmdLineParser(['show', '-a']).execute_sql_by_command()
                assert mock_todo.find_all.call_args == call()
        

def test_generate_next_id():
    
    with patch('todo.cmd_parser.Todo') as mock_todo:
        mock_todo.find_all.return_value = [Todo(id=4)]
        result = generate_next_id()
        assert mock_todo.find_all.call_args == call(order_by='id desc', size=1)
        assert result == 5
        mock_todo.find_all.return_value = []
        result = generate_next_id()
        assert result == 1