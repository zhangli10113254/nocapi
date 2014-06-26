'''
Created on 2014-5-15

@author: zhangli
'''
from compy.utils import ObjectUtils
import xml.dom.minidom as minidom
import os

_SCAN_ACTIONS = []

class request():
    def __init__(self, clz):
        if clz.REQUEST_INFO:
            module = clz.__module__
            clazz = clz.__name__
            version = clz.REQUEST_INFO['version']
            method = clz.REQUEST_INFO['method']
            url = clz.REQUEST_INFO['url']
            interceptor_names = list(clz.REQUEST_INFO['imterceptors']) if 'imterceptors' in clz.REQUEST_INFO else []
            name = clz.REQUEST_INFO['name'] if 'name' in clz.REQUEST_INFO else module + '.' + clazz
            _SCAN_ACTIONS.append(dict(name = name, url = url, version = version, module = module, clazz = clazz, method = method, interceptor_names = interceptor_names))
            
        self.clz = clz
        
    def __call__(self, *argv, **kwargv):
        return self.clz(*argv, **kwargv)

class XMLConfigReader(object):
    def __init__(self, config_file):
        self.config_file = config_file
        
    def read(self):
        doc = minidom.parse(self.config_file)
        root = doc.documentElement
        
        for node in root.childNodes:
            if node.nodeName == 'interceptors':
                interceptors = self.read_interceptors(node)
            if node.nodeName == 'interceptor-stacks':
                interceptor_stacks = self.read_interceptor_stacks(node)
            if node.nodeName == 'default-interceptor':
                default_interceptor = self.read_default_interceptor(node)
            if node.nodeName == 'actions':
                actions = self.read_actions(node)
                
        for name, interceptor_names in interceptor_stacks.iteritems():
            interceptor_stacks[name] = [interceptors[interceptor_name] for interceptor_name in interceptor_names]
            
        default_interceptor = interceptors[default_interceptor] if default_interceptor in interceptors else interceptor_stacks[default_interceptor]
        
        for action in actions:
            if not action['interceptor_names']:
                action['interceptors'] = list(default_interceptor)
            else:
                action['interceptors'] = [interceptors[interceptor_name] for interceptor_name in action['interceptor_names']]
                
        return actions
    
    def read_interceptors(self, interceptors_node):
        interceptors = dict()
        for node in interceptors_node.getElementsByTagName('interceptor'):
            name = node.getAttribute('name')
            module = node.getAttribute('module')
            clazz = node.getAttribute('cls')
            interceptors[name] = ObjectUtils.initialize(module, clazz)
        return interceptors
    
    def read_interceptor_stacks(self, interceptor_stacks_node):
        interceptor_stacks = dict()
        for node in interceptor_stacks_node.getElementsByTagName('interceptor-stack'):
            name = node.getAttribute('name')
            interceptor_names = [ref_node.getAttribute('ref') for ref_node in node.getElementsByTagName('interceptor')]
            interceptor_stacks[name] = interceptor_names
        return interceptor_stacks
            
    
    def read_default_interceptor(self, default_interceptor_node):
        return default_interceptor_node.getAttribute('ref')
    
    def read_actions(self, actions_node):
        actions = list()
        
        if actions_node.hasAttribute('scan_package'):
            def _scan_and_import(scan_package):
                package_path = os.path.dirname(__import__(scan_package, fromlist = ['']).__file__)
                for file in os.listdir(package_path):
                    if file.startswith('__init__'):
                        continue
                    
                    if os.path.isdir(package_path + '/' + file):
                        _scan_and_import(scan_package + '.' + file)
                    else:
                        mod_name = scan_package + '.' + file.split('.')[0]
                        __import__(mod_name)
                        
            scan_package = actions_node.getAttribute('scan_package')
            _scan_and_import(scan_package)
            
            actions =   list(_SCAN_ACTIONS)
            
        else:
            for node in actions_node.getElementsByTagName('action'):
                name = node.getAttribute('name')
                url = node.getAttribute('url')
                version = node.getAttribute('version')
                module = node.getAttribute('module')
                clazz = node.getAttribute('cls')
                method = node.getAttribute('method')
                interceptor_names = [ref_node.getAttribute('ref') for ref_node in node.getElementsByTagName('interceptor')]
                actions.append(dict(name = name, url = url, version = version, module = module, clazz = clazz, method = method, interceptor_names = interceptor_names))
                
        return actions  