'''
Created on Apr 9, 2014

@author: zhangli
'''

import webob
import base64

class HttpRequest(webob.Request):
    '''
    Inherit Request of webob 
    '''
    @property
    def basic_authorization(self):
        if self.authorization and self.authorization.startswith('Basic'):
            auth_info = base64.b64decode(self.authorization[6:])
            if len(auth_info.split(':')) == 2:
                return tuple(auth_info.split(':'))
        
        return None
            