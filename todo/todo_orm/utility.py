# -*- coding: utf-8 -*-
import sqlite3


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
