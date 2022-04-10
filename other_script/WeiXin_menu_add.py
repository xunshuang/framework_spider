# coding:utf-8
# 微信公众号菜单管理

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


def create_new_menu():
    menu_doc = {
        "button": [
            {
                "type": "click",
                "name": "今日新闻",
                "key": "V1001_TODAY_MUSIC"
            },
            {
                "name": "菜单",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "搜索",
                        "url": "http://www.soso.com/"
                    },

                    {
                        "type": "click",
                        "name": "赞一下我们",
                        "key": "V1001_GOOD"
                    }]
            }]
    }
    url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=' + get_accessToken()
    resp = requests.post(url=url,data=json.dumps(menu_doc,ensure_ascii=False).encode('utf-8')).json()
    print(resp)


create_new_menu()