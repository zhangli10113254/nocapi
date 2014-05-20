from compy.db.transaction.context import TransactionContext
from compy.db.errors import DataAccessError

PROPAGATION_REQUIRED = 0
PROPAGATION_REQUIRE_NEW = 1

def transaction(propagation = PROPAGATION_REQUIRED):
    def _transaction(func):
        if not TransactionContext.get_transaction_manager():
            return func
        
        def _transaction_proxy(*args, **kwargs):
            transaction_manager = TransactionContext.get_transaction_manager()
            transaction_status = transaction_manager.start()
            try:
                func(*args, **kwargs)
                transaction_manager.commit(transaction_status)
            except Exception as e:
                transaction_manager.rollback(transaction_status)
                raise e
            
        return _transaction_proxy
        
    return _transaction