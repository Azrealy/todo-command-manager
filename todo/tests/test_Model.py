# -*- coding: utf-8 -*-
from unittest.mock import Mock, patch, call
import pytest
import sqlite3
from todo.model import Model

def test_model_execute_without_set_values_and_commit():
    """
    Test `Model.execute()` arguments without set values
    and commit.
    """
    mock_conn = Mock()
    mock_cursor = Mock()
    sqlite3.connect = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.return_value = None

    model = Model("data_file")
    model.conn = mock_conn
    model.execute('SELECT * FROM table_name;',
                  values=None, commit=False)
    
    assert mock_conn.call_count == 1
    assert mock_conn.call_args == call('data_file')
    assert mock_conn.cursor.call_count == 1
    assert mock_cursor.execute.call_count == 1
    assert mock_cursor.execute.call_args == call('SELECT * FROM table_name;')


def test_model_execute_with_set_values_and_commit():
    """
    Test `Model.execute()` arguments with set values
    and commit.
    """
    mock_conn = Mock()
    mock_cursor = Mock()
    sqlite3.connect = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.return_value = None

    model = Model("data_file")
    model.conn = mock_conn
    model.execute(
        'SELECT * FROM table_name; WHERE columns1 = ? and columns2 = ?',
        values=['value1', 'value2'], commit=True
    )
    
    assert mock_conn.call_count == 1
    assert mock_conn.call_args == call('data_file')
    assert mock_conn.cursor.call_count == 1
    assert mock_conn.commit.call_count == 1
    assert mock_cursor.execute.call_count == 1
    assert mock_cursor.execute.call_args == call(
        'SELECT * FROM table_name; WHERE columns1 = ? and columns2 = ?',
        list(['value1', 'value2'])
    )


def test_model_execute_with_set_values_without_commit():
    """
    Test `Model.execute()` arguments without set values
    and commit.
    """
    mock_conn = Mock()
    mock_cursor = Mock()
    sqlite3.connect = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.return_value = None

    model = Model("data_file")
    model.conn = mock_conn
    model.execute(
        'SELECT * FROM table_name; WHERE columns1 = ? and columns2 = ?',
        values=['value1', 'value2'], commit=False
    )
    
    assert mock_conn.call_count == 1
    assert mock_conn.call_args == call('data_file')
    assert mock_conn.cursor.call_count == 1
    assert mock_conn.commit.call_count == 0
    assert mock_cursor.execute.call_count == 1
    assert mock_cursor.execute.call_args == call(
        'SELECT * FROM table_name; WHERE columns1 = ? and columns2 = ?',
        list(['value1', 'value2'])
    )


def test_create_table_query():
    """
    Test `Model.create_table()` method
    """
    mock_execute = Mock()
    model = Model("data_file")
    model.execute = mock_execute
    model.create_table('todo_table', ['context TEXT NOT NULL', 
                                      'id  INTEGER NOT NULL'])
    assert mock_execute.call_count == 1
    assert mock_execute.call_args == call(
        'CREATE TABLE IF NOT EXISTS todo_table (context TEXT NOT NULL,id  INTEGER NOT NULL)',
        commit=True
    )
    assert mock_execute.return_value.close.call_count == 1


def test_select_query():
    """
    Test `Model.select()` method
    """
    mock_execute = Mock()
    model = Model("data_file")
    model.execute = mock_execute
    model.select('todo_table', id = 1, context = "text")
    assert mock_execute.call_count == 1
    assert mock_execute.call_args == call(
        'SELECT * FROM todo_table WHERE id=? and context=?',
        [1, 'text']
    )


def test_insert_query():
    """
    Test `Model.insert()` method
    """
    mock_execute = Mock()
    model = Model("data_file")
    model.execute = mock_execute
    model.insert('todo_table', id = 1, context = "text")
    assert mock_execute.call_count == 1
    assert mock_execute.call_args == call(
        'INSERT INTO todo_table (id,context) VALUES(?,?)',
        [1, 'text']
    )


def test_select_all_query_without_option():
    """
    Test `Model.select_all()` method without set option
    """
    mock_execute = Mock()
    model = Model("data_file")
    model.execute = mock_execute
    model.select_all('todo_table')
    assert mock_execute.call_count == 1
    assert mock_execute.call_args == call(
        'SELECT * FROM todo_table '
    )


def test_select_all_query_with_option():
    """
    Test `Model.select_all()` method with set option
    """
    mock_execute = Mock()
    model = Model("data_file")
    model.execute = mock_execute
    model.select_all('todo_table', 'order by id desc')
    assert mock_execute.call_count == 1
    assert mock_execute.call_args == call(
        'SELECT * FROM todo_table order by id desc'
    )


def test_update_item_query():
    """
    Test `Model.update_item()` method
    """
    mock_execute = Mock()
    model = Model("data_file")
    model.execute = mock_execute
    set_values = dict()
    set_values['context'] = 'new message'
    model.update_item('todo_table', set_values, id = 1)
    assert mock_execute.call_count == 1
    assert mock_execute.call_args == call(
        'UPDATE todo_table SET context=? WHERE id=?',
        ['new message', 1]
    )


def test_delete_item_query():
    """
    Test `Model.delete_item()` method
    """
    mock_execute = Mock()
    model = Model("data_file")
    model.execute = mock_execute
    model.delete_item('todo_table', id = 1)
    assert mock_execute.call_count == 1
    assert mock_execute.call_args == call(
        'DELETE FROM todo_table WHERE id=?',
        [1]
    )
    