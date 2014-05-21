'''
Created on 2014-5-15

@author: zhangli
'''

from compy.rest.ctx import context
import os

class Interceptor(object):
    def intercept(self, action_invoker):
        pass
        
class PropertySetInterceptor(Interceptor):
    def intercept(self, action_invoker):
        request = context.request
        url = os.path.normpath(request.path_info)
        
        url_stack = url.split('/')[2:]
        config_url_stack = action_invoker.action.get('url').split('/')[1:]
        
        action_instance = action_invoker.action_proxy.action_instance
        for index in range(len(url_stack)):
            if config_url_stack[index].startswith('$'):
                url_property = config_url_stack[index][2:len(config_url_stack[index]) - 1]
                if hasattr(action_instance, url_property):
                    setattr(action_instance, url_property, url_stack[index])
               
        return action_invoker.invoke()
    
class ExceptionInterceptor(Interceptor):
    def intercept(self, action_invoker):
        try:
            return action_invoker.invoke()
        except Exception as e:
            return 'System Error!' + str(e)