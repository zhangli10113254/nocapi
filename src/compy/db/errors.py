# -*-  coding:UTF-8   -*-

'''
Created on 2014年4月11日

@author: zhangli
'''

class DBError(Exception):
    pass

class DataAccessError(DBError):
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super(DBError, self).__init__(*(code, message))

class TransactionError(DBError):
    def __init__(self, *args):
        super(TransactionError, self).__init__(*args)