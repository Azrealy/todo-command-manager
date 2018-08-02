# -*- coding: utf-8 -*-
import sqlite3

queries = {
    'CREATE_TABLE': 'CREATE TABLE IF NOT EXISTS {} ({})',
    'SELECT': 'SELECT {} FROM {} WHERE {}',
    'INSERT': 'INSERT INTO {} ({}) VALUES({})',
    'SELECT_ALL': 'SELECT {} FROM {} {}',
    'UPDATE': 'UPDATE {} SET {} WHERE {}',
    'DELETE': 'DELETE FROM {} WHERE {}',
    'DROP_TABLE': 'DROP TABLE {}'
}

class Model(object):
    
    def __init__(self, data_file):
        """
        DB model class, which use to create/execute
        SQL statement and create connection with DB.

        Parameters
        ----------
        data_file : str
            Name of data file.
        """
        self.conn = sqlite3.connect(data_file, uri=True)

    
    def execute(self, query, values=None, commit=False):
        """
        Execute SQL query.

        Parameters
        ----------
        query : str
            An SQL query
        values : list
            A list, with query parameters
        commit : bool
            Determine if need commit DB

        Returns
        -------
        cursor : sqlite3.Cursor
            An instance of Cursor object
        """
        cursor = self.conn.cursor()
        if values:
            cursor.execute(query, list(values))
        else:
            cursor.execute(query)
        if commit:
            self.conn.commit()
        return cursor
    
    def create_table(self, table_name, values):
        """
        Execute create table SQL query.

        Example of SQL query:
            CREATE TABLE IF NOT EXISTS table_name (
                column1 datetype,
                column2 datetype,
                ...
            )

        Parameters
        ----------
        table_name : str
            Table name
        values : list
            List of every column value.
        """
        query = queries['CREATE_TABLE'].format(table_name, ','.join(values))
        cursor = self.execute(query, commit=True)
        cursor.close()

    def select(self, table_name, **kwargs):
        """
        Execute select SQL query.

        Example of SQL query:
            SELECT * FROM table_name;
            WHERE columns1 = ? and columns2 = ? and ..;

        Parameters
        ----------
        table_name : str
            Table name
        """
        conds = ' and '.join(['{}=?'.format(k) for k in kwargs])
        values = [kwargs[k] for k in kwargs]
        query = queries['SELECT'].format('*', table_name, conds)
        return self.execute(query, values)

    def insert(self, table_name, **kwargs):
        """
        Execute insert SQL query.

        Example of SQL query:
            INSERT INTO table_name (columns1, column2, ...);
            VALUES (?, ?, ...);

        Parameters
        ----------
        table_name : str
            Table name
        """
        args = ','.join('?' for _ in kwargs)
        parameter = ','.join([k for k in kwargs])
        query = queries['INSERT'].format(table_name, parameter, args)
        values = [kwargs[k] for k in kwargs]
        return self.execute(query, values)
    
    def select_all(self, table_name, option=""):
        """
        Execute select all SQL query.

        Example of SQL query:
            SELECT * FROM table_name (order by id);

        Parameters
        ----------
        table_name : str
            Table name
        option : str
            Option query of select all
        """
        query = queries['SELECT_ALL'].format('*', table_name, option)
        return self.execute(query)
    
    def update_item(self, table_name, set_values, **kwargs):
        """
        Execute update SQL query.

        Example of SQL query:
            UPDATE table_name
            SET column1 = ?, column2 = ?, ...
            WHERE columns1 = ? and columns2 = ? and ..;

        Parameters
        ----------
        table_name : str
            Table name
        set_values : dict
            Values need to update.
        """
        updates = ['{}=?'.format(k) for k in set_values]
        update_values = [set_values[k] for k in set_values]
        condition = ['{}=?'.format(k) for k in kwargs]
        condition_values = [kwargs[k] for k in kwargs]

        query = queries['UPDATE'].format(table_name, ', '.join(updates), ' and '.join(condition))
        return self.execute(query, update_values + condition_values)

    def delete_item(self, table_name, **kwargs):
        """
        Execute delete SQL query.

        Example of SQL query:
            DELETE FROM table_name;
            WHERE columns1 = ? and columns2 = ? and ..;

        Parameters
        ----------
        table_name : str
            Table name
        """
        condition = ['{}=?'.format(k) for k in kwargs]
        condition_values = [kwargs[k] for k in kwargs]
        query = queries['DELETE'].format(table_name, 'and '.join(condition))
        return self.execute(query, condition_values)

    def drop_table(self, table_name):
        """
        Execute drop table SQL query.

        Example of SQL query:
            DROP TABLE table_name;

        Parameters
        ----------
        table_name : str
            Table name
        """
        query = queries['DROP_TABLE'].format(table_name)
        return self.execute(query)

    def close(self, cursor):
        """
        Close cursor of DB

        Parameters
        ----------
        cursor : sqlite3.Cursor
            An instance of Cursor object
        """
        cursor.close()