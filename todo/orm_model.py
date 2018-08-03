class Field(object):
    
    def __init__(self, column_type, primary_key, default):
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __repr__(self):
        return '<{}, {}>'.format(self.__class__.__name__, self.column_type)

class TextField(Field):
    
    def __init__(self, column_type='TEXT', default=None, primary_key=False):
        super(TextField, self).__init__(column_type, primary_key, default)
        
class IntegerField(Field):
    
    def __init__(self, column_type='INTEGER', default=1, primary_key=False):
        super(IntegerField, self).__init__(column_type, primary_key, default)
        
class BooleanField(Field):
    
    def __init__(self, column_type='BOOLEAN', default=False, primary_key=False):
        super(BooleanField, self).__init__(column_type, primary_key, default)


class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        table_name = name
        fields = []
        mappings = dict()
        for k, v in attrs.items():
            if isinstance(v, Field):
                mappings[k] = v
                if v.primary_key:
                    primary_key = k
                else:
                    fields.append(k)
                    
        for k in mappings.keys():
            attrs.pop(k)
        escaped_fields = list(map(lambda f: '{}'.format(f), fields))
        attrs['PRIMARY_KEY'] = primary_key
        attrs['MAPPINGS'] = mappings
        attrs['TABLE_NAME'] = table_name
        attrs['FIELD'] = fields
        return type.__new__(cls, name, bases, attrs)        
# Define the basic class of ORM Model
class Model(dict, metaclass = ModelMetaclass):
    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)
        
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError("'Model' object not has attribute {}".format(key))
    
    def __setattr__(self, key, value):
        self[key] = value
    
    def _get_value(self, key):
        value = getattr(self, key, None)
        if value is None:
            # If instance have not set the value of the key
            # try to get the default value from Field object.
            field = self.MAPPINGS[key]
            if field.default is not None:
                value = field.default
                setattr(self, key, value)
        return value
    
    def create_table(self):
        values = []
        for key, field in self.MAPPINGS.items():
            sql = ' '.join([key, field.column_type, 'PRIMARY KEY' if field.primary_key else ''])
            values.append(sql)
        #cur.execute(sql, args)
        print("execute")
        return 'CREATE TABLE IF NOT EXISTS {} ({})'.format(self.TABLE_NAME, ','.join(values))
    
    def save(self):
        args = list(map(self._get_value, self.MAPPINGS))
        columns = list(map(lambda k: k, self.MAPPINGS))
        #cur.execute(sql, args)
        print(args)
        return 'INSERT INTO {} ({}) VALUES({})'.format(self.TABLE_NAME, ', '.join(columns), ','.join('?'*len(columns)))
    
    @classmethod
    def find(self, primary_key):
        pass
        
      
class Todo(Model):
    id = IntegerField(primary_key=True)
    context = TextField()
    flag = BooleanField()
    def __init__(self):
        self.create_table()