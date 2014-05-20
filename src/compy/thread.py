# -*-  coding:UTF-8   -*-

'''
Created on 2014年4月22日

@author: zhangli
'''
import threading

class ThreadLocal(object):
    
    def __setattr__(self, name, value):
        self._get_thread_dict()[name] = value
        
    def __getattr__(self, name):
        _dict = self._get_thread_dict()
        
        return self._get_thread_dict().get(name, None)
    
    def __delattr__(self, name):
        del self._get_thread_dict()[name]
    
    def _get_thread_dict(self):
        if not hasattr(threading.current_thread(), '_dict'):
            threading.current_thread()._dict = dict()
            
        _dict = threading.current_thread()._dict
        if self not in _dict:
            _dict[self] = dict()
            
        return _dict[self]