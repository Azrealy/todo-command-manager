# -*- coding: utf-8 -*-
import sqlite3
import time


class RecordIsNotFoundError(Exception):
    """
    Record is not found.
    """
    pass

class SQLConnection(object):
    """
    A connection of the sqlite3.
    """
    def __init__(self, path_to_data_file='file:/tmp/data.db'):
        """
        Initializes sqlite3 connection

        Parameters
        ----------
        data_file : str
            A path to data file.
        """
        self.conn = sqlite3.connect(path_to_data_file, uri=True)

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

def datetime_filter(stored_time):
    """
    Filter datetime

    Parameters
    ----------
    stored_time : time.time object
        Time stored in DB
    
    Returns
    -------
    message : str
        Message of elapsed time
    """
    delta = int(time.time() - stored_time)
    if delta < 60:
        return u'1 mins ago'
    if delta < 3600:
        return u'%s mins ago' % (delta // 60)
    if delta < 86400:
        return u'%s hours ago' % (delta // 3600)
    if delta < 604800:
        return u'%s days ago' % (delta // 86400)
    dt = datetime.fromtimestamp(stored_time)
    return u'%s year %s month %s day ago' % (dt.year, dt.month, dt.day)