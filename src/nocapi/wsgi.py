# -*-  coding:UTF-8   -*-

'''
Created on 2014年4月22日

@author: zhangli
'''

from compy.rest.controller import DispatchController

import noc_api_config, web


if __name__ == '__main__':
    
    urls = ('/(.*)', DispatchController(noc_api_config.REST_CONFIG_FILE))
    
    app = web.application(urls, globals())
    app.run()