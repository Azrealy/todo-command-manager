# -*- coding: utf-8 -*-

class Field(object):
    """
    Base class of SQL column type class.
    """

    def __init__(self, column_type, primary_key, default):
        """
        Parameters:
        ---–––––––-
        column_type : str
            Type of column type
        primary_key : bool
            Whether column type is primary key
        default : str | bool | int
            The default value of column
        """
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __repr__(self):
        """
        Represent the class name and the column type.
        """
        return '<{}, {}>'.format(self.__class__.__name__, self.column_type)


class TextField(Field):
    """
    Class of TEXT column type.
    """
    def __init__(self, column_type='TEXT', default=None, primary_key=False):
        """
        Parameters
        ---–––––––
        column_type : str
            Type of column type.
        primary_key : bool
            Whether column type is primary key
        default : str or None
            The default value of column
        """
        super(TextField, self).__init__(column_type, primary_key, default)


class IntegerField(Field):
    """
    Class of INTEGER column type.
    """
    def __init__(self, column_type='INTEGER', default=None, primary_key=False):
        """
        Parameters
        ---–––––––
        column_type : str
            Type of column type.
        primary_key : bool
            Whether column type is primary key
        default : int or None
            The default value of column
        """
        super(IntegerField, self).__init__(column_type, primary_key, default)


class BooleanField(Field):
    """
    Class of BOOLEAN column type.
    """
    def __init__(self, column_type='BOOLEAN', default=False, primary_key=False):
        """
        Parameters
        ---–––––––
        column_type : str
            Type of column type.
        primary_key : bool
            Whether column type is primary key
        default : bool or None
            The default value of column
        """
        super(BooleanField, self).__init__(column_type, primary_key, default)


class FloatField(Field):
    """
    Class of FLOAT column type.
    """

    def __init__(self, column_type='REAL', default=0.0, primary_key=False):
        """
        Parameters
        ---–––––––
        column_type : str
            Type of column type.
        primary_key : bool
            Whether column type is primary key
        default : float or None
            The default value of column
        """
        super(FloatField, self).__init__(column_type, primary_key, default)
