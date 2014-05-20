# -*-  coding:UTF-8   -*-

'''
Created on 2014年4月11日

@author: zhangli
'''
from errors import DataAccessError

DATA_SOURCE_DRIVERS = {}

class DataSource(object):
    def __init__(self, driver = 'mysql', **params):
        if driver in DATA_SOURCE_DRIVERS:
            self.driver = DATA_SOURCE_DRIVERS[driver](**params)
        else:
            raise DataAccessError('Driver is not supported')
    
    def getConnection(self):
        pass
    
class DefaultDataSource(DataSource):
    def getConnection(self):
        return self.driver.getConnection()

class DataSourceDriver(object):
    def getConnection(self):
        pass
    
class MysqlDriver(DataSourceDriver):
    def __init__(self, **params):
        self.host = params.get('host', None)
        self.port = params.get('port', 3306)
        self.user = params.get('user', None)
        self.passwd = params.get('passwd', None)
        self.db = params.get('db', None)
        
    def getConnection(self):
        import MySQLdb
        return MySQLdb.connect(host = self.host, port = self.port, user = self.user, passwd = self.passwd, db = self.db)
    
DATA_SOURCE_DRIVERS['mysql'] = MysqlDriver