'''
Created on 2014-4-29

@author: zhangli
'''

from context import TransactionContext
from compy.db.errors import TransactionError
import compy.db.transaction as transaction

class TransactionStatus(object):
    def __init__(self, transaction_object, propagation = transaction.PROPAGATION_REQUIRED, prev_transaction = None):
        self.transaction_object = transaction_object
        self.prev_transaction = prev_transaction
        self.propagation = propagation
    
    def get_transaction(self):
        return self.transaction_object

class TransactionObject(object):
    connection = None

class TransactionManager(object):
    def __init__(self, **kwargs):
        pass
    
    def start(self, propagation = transaction.PROPAGATION_REQUIRED):
        if not TransactionContext.get_transaction():
            transaction_object = TransactionObject()
            transaction_status = TransactionStatus(transaction_object)
            try:
                self.do_begin(transaction_object)
            except TransactionError as e:
                raise TransactionError(e.args)
            
            TransactionContext.set_transaction(transaction_status)
            return transaction_status
        else:
            prev_transaction = TransactionContext.get_transaction()
            transaction_object = TransactionObject()
            transaction_status = TransactionStatus(transaction_object, propagation, prev_transaction)
            if propagation == transaction.PROPAGATION_REQUIRED: 
                TransactionContext.set_transaction(transaction_status)
                return transaction_status
            else:
                try:
                    self.do_begin(transaction_object)
                except Exception as e:
                    raise TransactionError(e.args)
            
                TransactionContext.set_transaction(transaction_status)
                return transaction_status
    
    def commit(self, transaction_status):
        if not transaction_status.prev_transaction:
            self.do_commit(transaction_status.get_transaction())
            self.do_clear(transaction_status.get_transaction())
            TransactionContext.set_transaction(None)
        else:
            prev_transaction = transaction_status.prev_transaction
            if transaction_status.propagation == transaction.PROPAGATION_REQUIRED:
                self.do_clear(transaction_status.get_transaction())
            else:
                self.do_commit(transaction_status.get_transaction())
                self.do_clear(transaction_status.get_transaction())
            TransactionContext.set_transaction(prev_transaction)
            
                
    def rollback(self, transaction_status):
        if not transaction_status.prev_transaction:
            self.do_rollback(transaction_status.get_transaction())
            self.do_clear(transaction_status.get_transaction())
            TransactionContext.set_transaction(None)
        else:
            prev_transaction = transaction_status.prev_transaction
            if transaction_status.propagation == transaction.PROPAGATION_REQUIRED:
                self.do_clear(transaction_status.get_transaction())
            else:
                self.do_rollback(transaction_status.get_transaction())
                self.do_clear(transaction_status.get_transaction())
            TransactionContext.set_transaction(prev_transaction)
    
    def do_begin(self, transaction_object):
        pass
    
    def do_commit(self, transaction_object):
        pass
    
    def do_rollback(self, transaction_object):
        pass
    
    def do_clear(self, transaction_object):
        pass
    
class DataSourceTransactionManager(TransactionManager):
    def __init__(self, datasource, **kwargs):
        super(DataSourceTransactionManager, self).__init__(**kwargs)
        self.datasource = datasource
        
    def do_begin(self, transaction_object):
        transaction_object.connection = self.datasource.getConnection()
        
    def do_commit(self, transaction_object):
        transaction_object.connection.commit()
            
    def do_rollback(self, transaction_object):
        transaction_object.connection.rollback()
        
    def do_clear(self, transaction_object):
        if transaction_object.connection:
            transaction_object.connection.close()
        