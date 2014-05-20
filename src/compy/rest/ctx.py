'''
Created on 2014-5-16

@author: zhangli
'''

from compy.thread import ThreadLocal
import web

class Context(object):
    def __init__(self):
        self.__action_context = ThreadLocal()
        
    def _request_get(self):
        return self.__action_context.request
    
    def _request_set(self, request):
        self.__action_context.request = request
        
    def _request_del(self):
        del self.__action_context.request
    
    request = property(_request_get, _request_set, _request_del)
    
    def _session_get(self):
        _session = web.config.get('_session')
        return _session
    
    session = property(_session_get)

context = Context()