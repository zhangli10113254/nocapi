'''
Created on 2014-5-16

@author: zhangli
'''
from config import XMLConfigReader
from request import HttpRequest
from response import JsonResponse, HttpResponse
from ctx import context
from compy.utils import ObjectUtils

import web

class DispatchController(object):
    def __init__(self, config_file):
        reader = XMLConfigReader(config_file)
        self.actions = reader.read()
        
    def _match_action(self, path):
        for action in self.actions:
            if self._url_match(path, action):
                return action
        return None
    
    def _url_match(self, url, action):
        url_split = url.split('/')
        
        # match version
        if url_split[1] != action.get('version'):
            return False
        
        url_stack = url_split[2:]
        config_url_stack = action.get('url').split('/')[1:]
        
        if(len(url_stack) != len(config_url_stack)):
            return False
        
        for i in range(len(url_stack)):
            if config_url_stack[i].startswith('$'):
                continue
            if config_url_stack[i] != url_stack[i]:
                return False
        return True
    
    def _do_exec_result(self, action, result):
        if isinstance(result, HttpResponse):
            return result
        
        return JsonResponse(result)
        
    def __call__(self):
        request = HttpRequest(web.ctx.env)
        context.request = request
        
        action = self._match_action(request.path_info)
        
        if not action:
            print 'Api not found in path: ' + request.path_info
            return 'Api not found in path: ' + request.path_info
        
        action_invoker = ActionInvoker(action)
        result = action_invoker.invoke()
        
        response = self._do_exec_result(action, result)
        
        web.ctx.status, web.ctx.headers = response.status, response.headerlist

        return response.body
    
class ActionInvoker(object):
    def __init__(self, action):
        self.action = action
        self.interceptor_iter = iter(action.get('interceptors'))
        self.action_proxy = ActionProxy(action)
        
    def invoke(self):
        result = None
        
        if not self.interceptor_iter:
            result = self.action_proxy()
        else:
            try:
                interceptor = self.interceptor_iter.next()
                result = interceptor.intercept(self)
            except StopIteration:
                result = self.action_proxy()
                
        return result
        
class ActionProxy(object):
    def __init__(self, action):
        self.action = action
        self.action_instance = ObjectUtils.initialize(action.get('module'), action.get('clazz'))
        self.action_method = getattr(self.action_instance, action.get('method'))
    
    def __call__(self):
        return self.action_method()