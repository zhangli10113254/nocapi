# -*-  coding:UTF-8   -*-

'''
Created on 2014年4月22日

@author: zhangli
'''
import os

# home directory
NOC_API_HOME = os.path.abspath(os.path.dirname(__file__))

# rest config file
REST_CONFIG_FILE = os.path.join(NOC_API_HOME, 'rest.xml')

# Mysql config
MYSQL_HOST = '192.168.0.215'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWD = 'root'
MYSQL_DB = 'nova'