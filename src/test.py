'''
Created on 2014-4-29

@author: zhangli
'''
from compy.db.datasource import DefaultDataSource
from compy.db.template.mysql import MySQLTemplate
from compy.db.transaction import transaction
from compy.db.transaction.context import TransactionContext
from compy.db.transaction.manager import DataSourceTransactionManager

datasource = DefaultDataSource(host = '192.168.0.215', port = 3306, user = 'root', passwd = 'nova', db = 'nova_new')
tpl = MySQLTemplate(datasource)

transaction_manager = DataSourceTransactionManager(datasource)
TransactionContext.set_transaction_manager(transaction_manager)

class Storage(object):
    sr_id = 9
    shared = 0
    block = 1
    host_info = 'host'
    display_type = 'ISCSI'
    display_name = 'test storage'
    display_desc = 'test storage'
    capacity_total = 10000
    capacity_free = 5000

    def __str__(self):
        return str(self.__dict__)

@transaction()
def insert():
    tpl.insert("insert into StorageResourceInfo values(%s, %s, %s, %s, %s, %s, %s, %s, %s)", (Storage.sr_id, Storage.shared, Storage.block,Storage.host_info, Storage.display_type, Storage.display_name, Storage.display_desc, Storage.capacity_total, Storage.capacity_free))

@transaction()
def update():
    tpl.update('update StorageResourceInfo set shared = %s', [3])
    
def query():
    def row_mapper(_d):
        storage = Storage()
        storage.sr_id = _d['sr_id']
        return storage
        
    return tpl.query_for_obj('select * from StorageResourceInfo where sr_id = %s', [4], obj_class = Storage)
    
@transaction()
def batch():
    insert()
    update()

if __name__ == '__main__':

    update()
