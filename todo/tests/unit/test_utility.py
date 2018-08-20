# -*- coding: utf-8 -*-
from unittest.mock import Mock, patch, call
import pytest
import sqlite3
from todo.utility import SQLConnection

def test_initialize_sql_connection():
    """
    Test `SQLConnection initialize`
    """
    with patch('todo.utility.sqlite3.connect') as mock_conn:
        SQLConnection.initialize('file:/tmp/data-test.db')
        SQLConnection()
        assert SQLConnection.PATH == 'file:/tmp/data-test.db'
        assert mock_conn.call_args == call('file:/tmp/data-test.db', uri=True)


def test_singleton_model_of_sql_connection():
    """
    Test `SQLConnection` satisfied tje singleton design
    """
    instance1 = SQLConnection()
    instance2 = SQLConnection()
    assert instance1 == instance2


def test_model_execute_with_sql_arguments():
    """
    Test `SQLConnection.execute()` with arguments sql.
    """
    with patch('todo.utility.sqlite3.connect') as mock_conn:
        SQLConnection.initialize('file:/tmp/data-test.db')
        SQLConnection().execute('SELECT * FROM table_name;')
        assert mock_conn.call_args == call('file:/tmp/data-test.db', uri=True)
        assert mock_conn.return_value.commit.call_count == 1
        assert mock_conn.return_value.cursor.call_count == 1
        assert mock_conn.return_value.cursor.return_value.execute.call_count == 1
        assert mock_conn.return_value.cursor.return_value.execute.call_args == call(
            'SELECT * FROM table_name;', ())


def test_model_execute_with_sql_and_args_arguments():
    """
    Test `SQLConnection.execute()` with sql and args arguments.
    """     
    with patch('todo.utility.sqlite3.connect') as mock_conn:
        SQLConnection.initialize('file:/tmp/data-test.db')
        SQLConnection().execute(
            'SELECT * FROM table_name WHERE column = ?', ['values'])
        assert mock_conn.call_args == call('file:/tmp/data-test.db', uri=True)
        assert mock_conn.return_value.commit.call_count == 1
        assert mock_conn.return_value.cursor.call_count == 1
        assert mock_conn.return_value.cursor.return_value.execute.call_count == 1
        assert mock_conn.return_value.cursor.return_value.execute.call_args == call(
            'SELECT * FROM table_name WHERE column = ?', ['values'])



def test_model_execute_set_autocommit_is_false():
    """
    Test `SQLConnection.execute()` set autocommit is false.
    """
    with patch('todo.utility.sqlite3.connect') as mock_conn:
        SQLConnection.initialize('file:/tmp/data-test.db')
        SQLConnection().execute(
            'SELECT * FROM table_name WHERE column = ?',
            ['values'],
            False
        )
        assert mock_conn.call_args == call('file:/tmp/data-test.db', uri=True)
        assert mock_conn.return_value.commit.call_count == 0
        assert mock_conn.return_value.cursor.call_count == 1
        assert mock_conn.return_value.cursor.return_value.execute.call_count == 1
        assert mock_conn.return_value.cursor.return_value.execute.call_args == call(
            'SELECT * FROM table_name WHERE column = ?', ['values'])
