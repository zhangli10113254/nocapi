'''
Created on Apr 10, 2014

@author: zhangli
'''
import webob, json

class HttpResponse(webob.Response):
    pass

class JsonResponse(HttpResponse):
    
    def __init__(self, content = None):
        self.content = content
        super(JsonResponse, self).__init__(self.jsonbody, content_type = 'application/json')
        
    @property
    def jsonbody(self):
        def object2dict(o):
            datadict = dict()
            for key in o.__dict__:
                if key.startswith('__') and key.endswith('__'):
                    continue
                datadict[key] = o.__dict__[key]
            return datadict
        
        return json.dumps(self.content, default = object2dict)