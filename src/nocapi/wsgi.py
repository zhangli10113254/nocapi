# -*-  coding:UTF-8   -*-

'''
Created on 2014年4月22日

@author: zhangli
'''
import noc_api_config
import web

# initialize logging
import logging.config
logging.config.fileConfig(noc_api_config.LOGGING_CONFIG_FILE)

from compy.rest.controller import DispatchController

if __name__ == '__main__':
    
    urls = ('/(.*)', DispatchController(noc_api_config.REST_CONFIG_FILE))
    
    app = web.application(urls, globals())
    app.run()
