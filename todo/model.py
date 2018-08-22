# -*- coding: utf-8 -*-
from .field import Field
from .utility import SQLConnection

class ModelMetaclass(type):
    """
    Meta class of Model.
    """
    def __new__(cls, name, bases, attrs):
        """
        Customize the class instance creation

        Every child class which inherit from the `Model` class will automatically
        create the following attributes of that class.

        Definition Class Attributes:
        ----------------------------
            PRIMARY_KEY : Store the attribute name which is belong to
                        `Field` object with set argument (primary_key = True)
            COLUMN_TO_FILED : A dict which storing the relationship of the class
                       attribute name and it's bounded `Field` object. 
            TABLE_NAME : The name of table which be took from the class name.

        Parametes:
        ----------
        cls : object
            Object of the class.
        name : str
            Name of the class.
        bases : tuple
            A tuple of class that be inherited from.
        attrs : dict
            A dict of class attributes
        
        Returns
        -------
            A new instance of class
        """
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        table_name = name
        primary_key = None
        fields = []
        column_to_filed = dict()
        for k, v in attrs.items():
            if isinstance(v, Field):
                column_to_filed[k] = v
                if v.primary_key:
                    if primary_key:
                        raise NameError('Primary key should only be one.')
                    else:
                        primary_key = k
                else:
                    fields.append(k)
        if primary_key is None:
            raise NameError('Primary key not found.')
        # Delete the class attributes which is belong to `Field` object.
        # Because the class attributes may be overide by the same name of 
        # the class instance attributes.
        for key in column_to_filed:
            attrs.pop(key)

        attrs['PRIMARY_KEY'] = primary_key
        attrs['COLUMN_TO_FILED'] = column_to_filed
        attrs['TABLE_NAME'] = table_name
        return type.__new__(cls, name, bases, attrs)


class Model(dict, metaclass=ModelMetaclass):
    """
    The base class of DB model that provides simple ORM.

    This class is inherit dict object so the arguments setting
    of this child class will be like `Todo(id = 1, text = 'hello')`

    The inherit class should define class attributes like following:
    
    ```
    Class Todo(Model):
        id = IntegerField()
        text = TextField()
    ```

    For that the `COLUMN_TO_FILED` attribute what create a `ModelMetaclass`
    will storing the relationship of attribute with it's `Field` object

    Class Methods for DB Manipulation
    ---------------------------------

    - ``Model.create_table()``: issues 'CREATE TABLE' statement
    - ``Model.find_all()``: issues 'SELECT' statement and optional with
                            'WHERE' statement
    - ``Model.drop_table()``:  issues 'DROP TABLE' statement
    - ``Model.find()``: issues 'SELECT' and 'WHERE' statement with primary key.

    Instance Methods for DB Manipulation
    ------------------------------------

    - ``instance.update()``: issues 'UPDATE' statement
    - ``instance.save()``: issues 'INSERT' statement
    - ``instance.remove()``: issues 'DELETE' statement
    """
    def __init__(self, **kwargs):
        """
        Inherit dict object.
        """
        super(Model, self).__init__(**kwargs)

    def __getattr__(self, key):
        """
        Get instance attributes method
        
        Example : 
        >>> model = Model(id=1)
        >>> model.id 
        1
        """
        try:
            return self[key]
        except KeyError:
            raise AttributeError("'Model' object not has attribute {}".format(key))

    def __setattr__(self, key, value):
        """
        Set instance attributes method

        Example
        ------- 
        >>> model = Model()
        >>> model.id = 1
        {'id' : 1}
        """
        self[key] = value

    def _get_value_or_default(self, key):
        """
        Get the instance attribute value
        
        Parameters
        ----------
        key : str
            The name of attribute
        
        Returns
        -------
        value : str or int or bool
            The value of the instance attribute.
            Or the default value which set in the 
            `Field` Object.
        """
        value = getattr(self, key, None)
        if value is None:
            field = self.COLUMN_TO_FILED[key]
            if field.default is not None:
                value = field.default
                setattr(self, key, value)
        return value

    @classmethod
    def _select(cls):
        """
        SELECT SQL statement
        """
        return 'SELECT {} FROM {}'.format(
            ', '.join([key for key in cls.COLUMN_TO_FILED]),
            cls.TABLE_NAME
        )

    @classmethod
    def _delete(cls):
        """
        DELETE SQL statement
        """
        return 'DELETE FROM {} WHERE {}=?'.format(
            cls.TABLE_NAME,
            cls.PRIMARY_KEY
        )

    @classmethod
    def create_table(cls):
        """
        Execute create table SQL statement.
        """
        values = []
        for key, field in cls.COLUMN_TO_FILED.items():
            sql = ' '.join(
                [key, field.column_type, 'PRIMARY KEY' if field.primary_key else ''])
            values.append(sql)
        sql = 'CREATE TABLE IF NOT EXISTS {} ({})'.format(cls.TABLE_NAME, ','.join(values))
        cursor = SQLConnection().execute(sql)
        cursor.close()

    @classmethod
    def drop_table(cls):
        """
        Execute drop table SQL statement.
        """
        sql = 'DROP TABLE {}'.format(cls.TABLE_NAME)
        cursor = SQLConnection().execute(sql)
        cursor.close()

    @classmethod
    def find_all(cls, condition=None, size=None, **kwargs):
        """
        DB Manipulation of 'SELECT' statement with optional 'WHERE'
        
        ``conditions`` is a dict of condition and corresponding value.
        e.g.:

        >>> conditions={'id': 1, 'is_completed': True}

        Parameters
        ----------
        condition : dict or None
            Column names with condition value.
        size : int or None
            The size of result

        Returns
        -------
        object : list(object) or None
            A list of object dict.

        Examples
        --------
        >>> Todo.find_all()
        [{'id': 1, 'text': 'Hello world', 'is_completed': True },
         {'id': 2, 'text': 'Hello japan', 'is_completed': False }]

        >>> Todo.find_all({'is_completed' : True})
        [{'id': 1, 'text': 'Hello world', 'is_completed': True }]

        >>> Todo.find_all(order_by = 'id desc')
        [{'id': 2, 'text': 'Hello japan', 'is_completed': False },
         {'id': 1, 'text': 'Hello world', 'is_completed': True }]
        """
        sql = [cls._select()]
        args = []
        if condition:
            for key, value in condition.items():
                sql.append('WHERE {}=?'.format(key))
                args.append(value)
        order_by = kwargs.get('order_by')
        if order_by:
            sql.append('ORDER BY')
            sql.append(order_by)
        cursor = SQLConnection().execute(' '.join(sql), args)
        if size:
            result = cursor.fetchmany(size)
        else:
            result = cursor.fetchall()
        cursor.close()
        return cls.convert_result_to_object(result)

    @classmethod
    def find(cls, primary_key):
        """
        DB Manipulation of 'SELECT' and 'WHERE' statement with primary key.

        Parameters
        ----------
        primary_key : Filed object default type
            The value of primary key

        Returns
        -------
        object : list(object) or None
            A list of object dict.
        
        Example
        -------
        >>> Todo.find(1)
        [{'id': 1, 'text': 'Hello world', 'is_completed': True }]
        """
        sql = '{} WHERE {} = ?'.format(cls._select(), cls.PRIMARY_KEY)
        cursor = SQLConnection().execute(sql, [primary_key])
        result = cursor.fetchmany(1)
        cursor.close()
        return cls.convert_result_to_object(result)

    def remove(self):
        """
        DB Manipulation of 'DELETE' statement

        Returns:
        --------
        is_completed: bool
            If DB manipulation successful return True
        
        Example:
        -------
        >>> Todo(id=1).remove()
        True
        """
        cursor = SQLConnection().execute(
            self._delete(), [self._get_value_or_default(self.PRIMARY_KEY)])
        count = cursor.rowcount
        result = True if count == 1 else False
        cursor.close()
        return result

    def update(self):
        """
        DB Manipulation of 'UPDATE' statement

        Returns:
        --------
        is_completed: bool
            If DB manipulation successful return True

        Example:
        -------
        >>> Todo(id=1, is_completed= True).update()
        True
        """
        sql = 'UPDATE {} SET  {} where {}=?'.format(
           self.TABLE_NAME,
           ', '.join(map(lambda f: '{}=?'.format(f), self)),
           self.PRIMARY_KEY
        )
        args = list(map(self._get_value_or_default, self))
        args.append(self._get_value_or_default(self.PRIMARY_KEY))
        cursor = SQLConnection().execute(sql, args)
        count = cursor.rowcount
        result = True if count == 1 else False
        cursor.close()
        return result

    def save(self):
        """
        DB Manipulation of 'INSERT' statement

        Returns:
        --------
        is_completed: bool
            If DB manipulation successful return True

        Example:
        -------
        >>> Todo(id=1, text='Hello', is_completed=True).save()
        True
        """
        args = list(map(self._get_value_or_default, self.COLUMN_TO_FILED))
        columns = list(map(lambda k: k, self.COLUMN_TO_FILED))
        sql =  'INSERT INTO {} ({}) VALUES({})'.format(
            self.TABLE_NAME,
            ', '.join(columns),
            ','.join('?'*len(columns))
        )
        cursor = SQLConnection().execute(sql, args)
        count = cursor.rowcount
        result = True if count == 1 else False
        cursor.close()
        return result

    @classmethod
    def convert_result_to_object(cls, result):
        """
        Convert the result from DB to the object dict.
        
        Parameters:
        -----------
        result : list(tuple)
            The result fetch from the DB

        Returns
        -------
        object : list(dict) or None
            A list of object dict.
        """
        keys = cls.COLUMN_TO_FILED
        if len(result) == 0:
            return None
        else:
            return [cls(**dict(zip(keys, r))) for r in result]
