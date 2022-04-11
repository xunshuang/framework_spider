# coding:utf-8
import requests
from xml.etree import ElementTree

import os
import sys
import time
import json
import hashlib
import jinja2

sys.path.append('/workspace/framework_spider/')
import requests
from Db.MySQLClient.client import MYSQL
from Config.GlobalSetting import MYSQL_CONFIG
from datetime import datetime

mysqlObj = MYSQL(MYSQL_CONFIG, db='machinedb')

# 获取 accessToken
def get_accessToken():
    mysql, cursor = mysqlObj.get_mysql()
    sql = 'SELECT `machineAccessToken` FROM `machineToken`;'
    cursor.execute(sql)
    mysql.commit()
    _ = cursor.fetchone()
    if _['machineAccessToken']:
        return _['machineAccessToken']
    else:
        time.sleep(1)
        return get_accessToken()

respJson = requests.get(url='https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token='+ get_accessToken()).json()

print(respJson)