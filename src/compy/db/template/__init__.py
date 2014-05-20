# -*-  coding:UTF-8   -*-

'''
Created on 2014年4月11日

@author: zhangli
'''
from compy.db.utils import DatasourceUtil

class DataAccessTemplate(object):
    def __init__(self, datasource):
        self.datasource = datasource
    
    def get_connection(self):
        return DatasourceUtil.get_connection(self.datasource)
    
    def connection_commit(self, conn):
        DatasourceUtil.connection_commit(conn)
    
    def release_connection(self, conn):
        DatasourceUtil.release_connection(conn)