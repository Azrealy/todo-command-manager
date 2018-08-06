# -*- coding: utf-8 -*-
import pytest
from todo.model import Model
from todo.field import IntegerField, TextField, BooleanField, FloatField
from sqlite3 import OperationalError
import time


class User(Model):
    """
    The simplest model class which has a single primary key.
    """
    user_id = IntegerField(primary_key=True)
    user_name = TextField(default='Administrator')
    user_auth = BooleanField()
    user_created_at = FloatField()


@pytest.fixture(scope='function', autouse=True)
def scope_function():
    # create table
    User.create_table()
    yield
    # drop table
    User.drop_table()

def test_crud():
    # create a user record at DB
    times1 = time.time()
    alice = User(user_id=1234, user_name='Alice wonderland',
                 user_auth=True, user_created_at=times1)
    alice.save()
    jack = User(user_id=4321, user_name='Black jack')
    jack.save()
    
    assert [alice, jack] == User.find_all()
    assert [jack] == User.find_all(size=1, order_by='user_id desc')
    assert [alice] == User.find_all({'user_auth': True})
    alice_find = User.find(1234)
    assert [alice] == alice_find
    assert None == User.find(1111)
    
    User(user_id=4321).remove()
    assert [alice] == User.find_all()

    assert False == User(user_id=1111, user_name='Alice').update()
    User(user_id=1234, user_name='New Alice wonderland').update()

    assert User.find(1234) == [User(
        user_id=1234,
        user_name='New Alice wonderland',
        user_auth=True,
        user_created_at=times1
    )]
