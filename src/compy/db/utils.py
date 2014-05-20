# -*-  coding:UTF-8   -*-

'''
Created on 2014年4月22日

@author: zhangli
'''
from compy.db.transaction.context import TransactionContext

class DatasourceUtil(object):
    @classmethod
    def get_connection(cls, datasource):
        transaction_status = TransactionContext.get_transaction()
        if transaction_status:
            transaction_object = transaction_status.get_transaction()
            while not transaction_object.connection and transaction_status.prev_transaction:
                transaction_status = transaction_status.prev_transaction
                transaction_object = transaction_status.get_transaction()
            return transaction_object.connection
        else:
            return datasource.getConnection()
    
    @classmethod
    def connection_commit(cls, conn):
        if not TransactionContext.get_transaction():
            conn.commit()
    
    @classmethod
    def release_connection(cls, conn):
        if not TransactionContext.get_transaction():
            conn.close()