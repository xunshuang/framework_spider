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
    mysql, cursor = mysqlObj.get_mysql()
    SQL = 'SELECT `machineArticleId` FROM `machineWXPubArticle` ORDER BY `id` DESC LIMIT 1'
    cursor.execute(SQL)
    mysql.commit()

    _ = cursor.fetchone()
    menu_doc = {
        "button": [
            {
                "type": "article_id",
                "name": "📰最新一期",
                "article_id": f"{_['machineArticleId']}"
            },
            {
                "name": "🚪财富之门",
                "sub_button": [

                    {
                        "type": "view",
                        "name": "🔍打开主页",
                        "url": "http://www.surefly.top/"
                    }]
            },
            {
                "type": "article_id",
                "name": "📞联系我们",
                "article_id": "6beSyaQWnY50zaxEn-OkgVNIW-6jvNqmwWIQC9jvopsGHJx06g6Z0CpNfX2mC_tN"
            }]
    }
    url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=' + get_accessToken()
    resp = requests.post(url=url, data=json.dumps(menu_doc, ensure_ascii=False).encode('utf-8')).json()
    print(resp)


create_new_menu()
