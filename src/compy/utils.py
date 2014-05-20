'''
Created on 2014-5-16

@author: zhangli
'''

class ObjectUtils(object):
    
    @staticmethod
    def initialize(module, clazz):
        mod = __import__(module, None, None, [''])
        cls = getattr(mod, clazz)
        return cls()
        
        