# -*- coding: utf-8 -*-
from unittest.mock import Mock, patch, call
import pytest
import sqlite3
from todo.utility import SQLConnection

def test_model_execute_with_sql_arguments():
    """
    Test `SQLConnection.execute()` with arguments sql.
    """
    mock_conn = Mock()
    mock_cursor = Mock()
    sqlite3.connect = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.return_value = None

    model = SQLConnection()
    model.conn = mock_conn
    model.execute('SELECT * FROM table_name;')
    
    assert mock_conn.call_count == 1
    assert mock_conn.call_args == call('file:/tmp/data.db', uri=True)
    assert mock_conn.commit.call_count == 1
    assert mock_conn.cursor.call_count == 1
    assert mock_cursor.execute.call_count == 1
    assert mock_cursor.execute.call_args == call('SELECT * FROM table_name;', ())


def test_model_execute_with_sql_and_args_arguments():
    """
    Test `SQLConnection.execute()` with sql and args arguments.
    """
    mock_conn = Mock()
    mock_cursor = Mock()
    sqlite3.connect = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.return_value = None

    model = SQLConnection()
    model.conn = mock_conn
    model.execute('SELECT * FROM table_name WHERE column = ?', ['values'])
    
    assert mock_conn.call_count == 1
    assert mock_conn.call_args == call('file:/tmp/data.db', uri=True)
    assert mock_conn.commit.call_count == 1
    assert mock_conn.cursor.call_count == 1
    assert mock_cursor.execute.call_count == 1
    assert mock_cursor.execute.call_args == call(
        'SELECT * FROM table_name WHERE column = ?', ['values']
    )


def test_model_execute_set_autocommit_is_false():
    """
    Test `SQLConnection.execute()` set autocommit is false.
    """
    mock_conn = Mock()
    mock_cursor = Mock()
    sqlite3.connect = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.return_value = None

    model = SQLConnection()
    model.conn = mock_conn
    model.execute(
        'SELECT * FROM table_name WHERE column = ?',
        ['values'],
        False
    )
    
    assert mock_conn.call_count == 1
    assert mock_conn.call_args == call('file:/tmp/data.db', uri=True)
    assert mock_conn.commit.call_count == 0
    assert mock_conn.cursor.call_count == 1
    assert mock_cursor.execute.call_count == 1
    assert mock_cursor.execute.call_args == call(
        'SELECT * FROM table_name WHERE column = ?', ['values']
    )