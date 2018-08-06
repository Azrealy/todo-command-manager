# -*- coding: utf-8 -*-
from unittest.mock import Mock, patch, call
import pytest
import sqlite3
from todo.model import Model
from textwrap import dedent
from todo.field import IntegerField, TextField, BooleanField, FloatField


class User(Model):
    """
    The simplest model class which has a single primary key.
    """
    user_id = IntegerField(primary_key=True)
    user_name = TextField(default='Administrator')
    user_auth = BooleanField()
    user_created_at = FloatField()

# --- Initialization attribute of  `PRIMARY_KEY`, `MAPPINGS`, `TABLE_NAME`, `FIELDS` ---

def test_init():
    assert User.PRIMARY_KEY == 'user_id'
    assert User.MAPPINGS == {
        'user_id': IntegerField(primary_key=True),
        'user_name': TextField(default='Administrator'),
        'user_auth': BooleanField(),
        'user_created_at': FloatField()
    }
    assert User.TABLE_NAME == 'User'
    assert set(User.FIELDS) == set(['user_name', 'user_auth', 'user_created_at'])
    user = User(user_id=1, user_name='Alice')
    assert user.user_id == 1 and user.user_name == 'Alice'
    assert user.user_name == 'Alice'
    user.user_auth = True
    assert user.user_auth == True
    assert User._select() == dedent('''
            SELECT user_id, user_name, user_auth, user_created_at FROM User
        ''').strip()
    assert User._delete() == dedent(
        '''
        DELETE FROM User WHERE user_id=?
        '''
    ).strip()


def test_get_value_or_default():
    assert User()._get_value_or_default('user_name') == 'Administrator'
    assert User(user_name='Alice')._get_value_or_default('user_name') == 'Alice'

# --- SQL parts ---

def test_create_table():
    with patch('todo.model.SQLConnection.execute') as execute_sql:
        User.create_table()
        sql = [
            'CREATE TABLE IF NOT EXISTS User ',
            '(user_id INTEGER PRIMARY KEY,user_name TEXT ,',
            'user_auth BOOLEAN ,user_created_at REAL )'
        ]
        assert execute_sql.call_args == call(''.join(sql))
        assert execute_sql.return_value.close.call_count == 1


def test_drop_table():
    with patch('todo.model.SQLConnection.execute') as execute_sql:
        User.drop_table()
        assert execute_sql.call_args == call('DROP TABLE User')
        assert execute_sql.return_value.close.call_count == 1


def test_convert_result_to_object():
    convert_result = User.convert_result_to_object([(1, 'A', True, 123456789.123450)])
    assert convert_result == [{
        'user_auth': True,
        'user_created_at': 123456789.123450,
        'user_id': 1,
        'user_name': 'A'
    }]
    convert_result = User.convert_result_to_object([
        (1, 'A', True, 123456789.123450),
        (2, 'B', False, 987654321.123456)
    ])
    assert convert_result == [
        {
            'user_auth': True,
            'user_created_at': 123456789.123450,
            'user_id': 1,
            'user_name': 'A'
        },
        {
            'user_auth': False,
            'user_created_at': 987654321.123456,
            'user_id': 2,
            'user_name': 'B'
        }
    ]


def test_find_all():
    
    with patch('todo.model.SQLConnection.execute') as execute_sql:

        User.find_all()
        assert execute_sql.call_args == call(
            'SELECT user_id, user_name, user_auth, user_created_at FROM User',
            []
        )
        assert execute_sql.return_value.fetchall.call_count == 1
        assert execute_sql.return_value.close.call_count == 1

        User.find_all({'user_id': 1})
        assert execute_sql.call_args == call(
            'SELECT user_id, user_name, user_auth, user_created_at FROM User WHERE user_id=?',
            [1]
        )
        assert execute_sql.return_value.fetchall.call_count == 2
        assert execute_sql.return_value.close.call_count == 2

        User.find_all({'user_auth': True}, size=1, order_by='id desc')
        sql = [
            'SELECT user_id, user_name, user_auth, user_created_at FROM User',
            ' WHERE user_auth=? ORDER BY id desc'
        ]
        assert execute_sql.call_args == call(
            ''.join(sql),
            [True]
        )
        assert execute_sql.return_value.fetchall.call_count == 2
        assert execute_sql.return_value.fetchmany.call_count == 1
        assert execute_sql.return_value.fetchmany.call_args == call(1)
        assert execute_sql.return_value.close.call_count == 3


def test_find():
    
    with patch('todo.model.SQLConnection.execute') as execute_sql:
        User.find(1)
        assert execute_sql.call_args == call(
            'SELECT user_id, user_name, user_auth, user_created_at FROM User WHERE user_id = ?',
            [1]
        )
        assert execute_sql.return_value.fetchmany.call_count == 1
        assert execute_sql.return_value.fetchmany.call_args == call(1)
        assert execute_sql.return_value.close.call_count == 1


def test_remove():
    with patch('todo.model.SQLConnection.execute') as execute_sql:
        User(user_id=1).remove()
        assert execute_sql.call_args == call('DELETE FROM User WHERE user_id=?', [1])


def test_update():
    with patch('todo.model.SQLConnection.execute') as execute_sql:
        User(user_id=1, user_name='user').update()
        assert execute_sql.call_args == call(
            'UPDATE User SET  user_id=?, user_name=? where user_id=?',
            [1, 'user', 1]
        )
    

def test_save():
    with patch('todo.model.SQLConnection.execute') as execute_sql:
        User(user_id=1, user_name='user').save()
        assert execute_sql.call_args == call(
            'INSERT INTO User (user_id, user_name, user_auth, user_created_at) VALUES(?,?,?,?)',
            [1, 'user', False, 0.0]
        )
        User().save()
        assert execute_sql.call_args == call(
            'INSERT INTO User (user_id, user_name, user_auth, user_created_at) VALUES(?,?,?,?)',
            [None, 'Administrator', False, 0.0]
        )
    