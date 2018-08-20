# -*- coding: utf-8 -*-
import sqlite3
import time
from datetime import datetime


class RecordIsNotFoundError(Exception):
    """
    Record is not found.
    """
    pass

class Singleton(type):
    """
    Singleton metaclass

    Example:
        class model(object, Singleton):
            pass
    >>> m1 = model()
    >>> m2 = model()
    >>> m1 == m2
    True
    """
    _instance = dict()
    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance[cls.__name__] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance[cls.__name__]

class SQLConnection(object, metaclass=Singleton):
    """
    A connection of the sqlite3.
    """
    PATH = None 

    def __init__(self):
        """
        Initialize SQLConnection instance.
        """
        self.conn = sqlite3.connect(self.PATH if self.PATH else 'file:/tmp/data.db', uri=True)

    @classmethod
    def initialize(cls, path_to_file=None):
        """
        Initialize SQLConnection class instance.

        Parameters
        ----------
        data_file: str
            A path to data file.
        """
        if cls._instance:
            cls._instance = dict()
        cls.PATH = path_to_file


    def execute(self, sql, args=(), autocommit=True):
        """
        Prepare and execute a database query.

        Parameters
        ----------
        sql : str
            A SQL query
        args : tuple or list or dict
            A list, tuple or dict with query parameters.
        autocommit : bool
            Determine whether need commit DB

        Returns
        -------
        cursor : sqlite3.Cursor
            An `cursor` object of sqlite3 connection.
        """
        cursor = self.conn.cursor()
        cursor = cursor.execute(sql, args)
        if autocommit:
            self.conn.commit()
        return cursor

def convert_time_to_message(epoch_time):
    """
    Convert time to message

    Parameters
    ----------
    epoch_time : float
        Float point number of epoch time
    
    Returns
    -------
    message : str
        Message of elapsed time
    """
    delta = int(time.time() - epoch_time)
    if delta < 60:
        return '1 mins ago'
    if delta < 3600:
        return '%s mins ago' % (delta // 60)
    if delta < 86400:
        return '%s hours ago' % (delta // 3600)
    if delta < 604800:
        return '%s days ago' % (delta // 86400)
    dt = datetime.fromtimestamp(epoch_time)
    return '%s year %s month %s day ago' % (dt.year, dt.month, dt.day)
