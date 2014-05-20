'''
Created on 2014-4-29

@author: zhangli
'''

from compy.thread import ThreadLocal

class TransactionContext(object):
    transaction_holder = ThreadLocal()
    transaction_manager = None
    
    @classmethod
    def get_transaction(cls):
        if hasattr(cls.transaction_holder, 'transaction'):
            return cls.transaction_holder.transaction
        return None
    
    @classmethod
    def set_transaction(cls, transaction_status):
        cls.transaction_holder.transaction = transaction_status
        
    @classmethod
    def get_transaction_manager(cls):
        return cls.transaction_manager
    
    @classmethod
    def set_transaction_manager(cls, transaction_manager):
        cls.transaction_manager = transaction_manager