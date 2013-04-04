from PyQt4 import QtCore, QtGui, QtSql


class TypeData(object):
    pass


class TypeFactory(object):
    
    def __init__(self):
        self.types = {}
        
    def addType(self, name):
        nameType = 'Type{0:s}'.format(name[0].upper() + name[1:].lower())
        self.types[nameType] = type(nameType, (), {'name': name})
        
        
dataTypes = TypeFactory()
types = ['NULL', 'INTEGER', 'REAL', 'TEXT', 'BLOB']
for t in types:
    dataTypes.addType(t)
    
    
    
class Record(object):
    
    def __init__(self):
        self.fields = {}
        
    def addField(self, nameCol, field):
        self.fields[nameCol] = field
        
    
class Table(object):
    
    def __init__(self, name):
        self.name = name
        self.columns = {}
        
    def addColumn(self, name, dataType, primary=False):
        self.columns[name] = dataType
        if primary:
            self.primary = name
        

class Database(object):
    
    def __init__(self, name, testMode=False):
        self.name = name
        self.useType = True
        self.testMode = testMode
        self.connection = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.connection.setDatabaseName(self.name)
        if not self.connection.open():
            print('cannot establish a database connection')
        self.tables = {}
        self.loadDatabase()
        
    def loadDatabase(self):
        for tableName in [str(t) for t in self.connection.tables()]:
            table = Table(tableName)
            record = self.connection.record(table.name)
            self.tables[table.name] = table
            for i in range(record.count()):
                print(QtCore.QVariant(record.field(i).type()).typeName())
        
            
    def addTable(self, table):
        if table.name not in self.connection.tables():
            self.tables[table.name] = table
            cols = ['{0:s} {1:s}'.format(name, dataType.name) 
                for name, dataType in  table.columns.iteritems()]
            statement = 'CREATE TABLE {0:s}({1:s})'.format(table.name, 
                ', '.join(cols))
            if self.testMode:
                print(statement)
            else: 
                self.connection.exec_(statement)
        else:
            print('table already exists')
        
    def addRecord(self, nameTable, record):
        if nameTable in self.connection.tables():
            cols = self.tables[nameTable].columns
            if False not in [f in cols.keys() for f in record.fields]:
                values = ', '.join(['"{0:s}"'.format(str(f)) 
                    for f in record.fields.values()])
                if self.useType:
                    nameTypes = '({0:s})'.format(', '.join(cols.keys()))
                else:
                    nameTypes = ''
                statement = 'INSERT INTO {0:s}{1:s} VALUES({2:s})'.format(
                    nameTable, nameTypes, values)
                if self.testMode:
                    print(statement)
                else:
                    self.connection.exec_(statement)
        

if __name__ == '__main__':
    db = Database('test.db', testMode=True)
    #for key, value in dataTypes.types.iteritems():
    #    print(key, value)
    t1 = Table('cars')
    t1.addColumn('id', dataTypes.types['TypeInteger'](), primary=True)
    t1.addColumn('name', dataTypes.types['TypeText']())
    t1.addColumn('year', dataTypes.types['TypeInteger']())
    t1.addColumn('weight', dataTypes.types['TypeReal']())
    db.addTable(t1)
    r = Record()
    r.addField('id', 1)
    r.addField('name', 'Audi A3')
    r.addField('year', 1982)
    r.addField('weight', '1560.80')
    db.addRecord(t1.name, r)    