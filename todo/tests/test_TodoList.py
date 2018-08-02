# -*- coding: utf-8 -*-
from unittest.mock import Mock, patch, call
import pytest
import sqlite3
from todo.model import Model
from todo.todo import check_task_exist, RecordIsNotFoundError, TodoList


class DummyTodoListClass(Model):

    def __init__(self, data_file = 'tests/data/dummy'):
        
        super(DummyTodoListClass, self).__init__(data_file)
        self.table_name = 'test_table'

    @check_task_exist
    def test(self, index):
        """
        Dummy method with task existence check.
        """
        return index


def test_check_task_exits_when_task_is_exist():
    """
    Tests `@check_task_exits` does not raise any errors
    if task can find from the db.
    """
    mock_select = Mock()
    mock_select.return_value.fetchall.return_value = 'result'
    d = DummyTodoListClass()
    d.select = mock_select
    result = d.test(index=1)
    assert mock_select.call_count == 1
    assert mock_select.call_args == call(
       id=1, table_name='test_table' 
    )
    assert mock_select.return_value.fetchall.call_count == 1
    assert result == 1


def test_check_task_exits_when_task_not_exist():
    """
    Tests `@check_task_exits` does not raise any errors
    if task can not find from the db.
    """
    mock_select = Mock()
    mock_select.return_value.fetchall.return_value = None
    d = DummyTodoListClass()
    d.select = mock_select
    with pytest.raises(RecordIsNotFoundError) as excinfo:
        d.test(index=1)
    assert mock_select.call_count == 1
    assert mock_select.call_args == call(
       id=1, table_name='test_table' 
    )
    assert mock_select.return_value.fetchall.call_count == 1
    assert str(excinfo.value) == 'This id of task not exist.'

def test_create_table():
    """
    Test create table at the __init__ method.
    """
    mock_create_table = Mock()
    todo = TodoList('test_file')
    todo.create_table = mock_create_table
    todo.__init__('data_file')
    assert mock_create_table.call_count == 1

def test_get_greatest_id_when_todo_list_is_empty():
    """
    Test `get_greatest_id` method when todo list in
    db is empty.
    """
    mock_select_all = Mock()
    mock_select_all.return_value.fetchone.return_value = None
    todo = TodoList('test_file')
    todo.select_all = mock_select_all
    todo._get_greatest_id()
    assert mock_select_all.call_count == 1
    assert mock_select_all.return_value.fetchone.call_count == 1
    assert mock_select_all.return_value.close.call_count == 1
    assert mock_select_all.call_args == call(
        'todo_list',
        option = 'order by id desc'
    )
    assert todo._get_greatest_id() == 0


def test_get_greatest_id_when_todo_list_not_empty():
    """
    Test `get_greatest_id` method when todo list is
    not empty.
    """
    mock_select_all = Mock()
    mock_select_all.return_value.fetchone.return_value = [1]
    todo = TodoList('test_file')
    todo.select_all = mock_select_all
    todo._get_greatest_id()
    assert mock_select_all.call_count == 1
    assert mock_select_all.return_value.fetchone.call_count == 1
    assert mock_select_all.return_value.close.call_count == 1
    assert mock_select_all.call_args == call(
        'todo_list',
        option = 'order by id desc'
    )
    assert todo._get_greatest_id() == 1


def test_show_todo_list_by_status():
    """
    Test `show_todo_list_by_status` method.
    """
    mock_select = Mock()
    todo = TodoList('test_file')
    todo.select = mock_select
    todo.show_todo_list_by_status(True)
    assert mock_select.call_count == 1
    assert mock_select.return_value.fetchall.call_count == 1
    assert mock_select.return_value.close.call_count == 1
    assert mock_select.call_args == call(
        completed=True, table_name='todo_list'
    )


def test_show_todo_list():
    """
    Test `show_todo_list` method.
    """
    mock_select_all = Mock()
    todo = TodoList('test_file')
    todo.select_all = mock_select_all
    todo.show_todo_list()
    assert mock_select_all.call_count == 1
    assert mock_select_all.return_value.fetchall.call_count == 1
    assert mock_select_all.return_value.close.call_count == 1
    assert mock_select_all.call_args == call(
        table_name='todo_list'
    )


def test_add_task():
    """
    Test `add_task` method.
    """
    mock_insert = Mock()
    mock_get_id = Mock()
    mock_get_id.return_value = 1
    todo = TodoList('test_file')
    todo.insert = mock_insert
    todo._get_greatest_id = mock_get_id
    todo.add_task('new message')
    assert mock_insert.call_count == 1
    assert mock_insert.return_value.close.call_count == 1
    assert mock_insert.call_args == call(
        'todo_list',
        completed = False,
        context='new message',
        id = 2
    )


def test_complete_task_by_id():
    """
    Test `complete_task_by_id` method.
    """
    mock_update_item = Mock()
    mock_select = Mock()
    mock_select.return_value.fetchall.return_value = 'result'
    todo = TodoList('test_file')
    todo.select = mock_select
    todo.update_item = mock_update_item
    todo.complete_task_by_id(index = 1)
    assert mock_update_item.call_count == 1
    assert mock_update_item.return_value.close.call_count == 1
    assert mock_update_item.call_args == call(
        id=1,
        set_values={'completed': True},
        table_name='todo_list'
    )


def test_update_task_by_id():
    """
    Test `update_task_by_id` method.
    """
    mock_update_item = Mock()
    mock_select = Mock()
    mock_select.return_value.fetchall.return_value = 'result'
    todo = TodoList('test_file')
    todo.select = mock_select
    todo.update_item = mock_update_item
    todo.update_task_by_id(1, 'new message')
    assert mock_update_item.call_count == 1
    assert mock_update_item.return_value.close.call_count == 1
    assert mock_update_item.call_args == call(
        id=1,
        set_values={'context': 'new message'},
        table_name='todo_list'
    )


def test_delete_task_by_id():
    """
    Test `delete_task_by_id` method.
    """
    mock_delete_item = Mock()
    mock_select = Mock()
    mock_select.return_value.fetchall.return_value = 'result'
    todo = TodoList('test_file')
    todo.select = mock_select
    todo.delete_item = mock_delete_item
    todo.delete_task_by_id(1)
    assert mock_delete_item.call_count == 1
    assert mock_delete_item.return_value.close.call_count == 1
    assert mock_delete_item.call_args == call(
        id=1,
        table_name='todo_list'
    )


