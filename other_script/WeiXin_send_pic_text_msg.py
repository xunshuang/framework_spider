# coding:utf-8
# 定时发送图文消息

import os
import sys
import time
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


def get_machine_msg():
    pass


def get_openid(openId=None):
    accessToken = get_accessToken()
    openidList = requests.get(
        f'https://api.weixin.qq.com/cgi-bin/user/get?access_token={accessToken}&next_openid={openId}').json()
    for openid in openidList.get('data').get('openid'):
        yield openid

def get_media_id():
    pass

# 发送消息
def send_msg():
    doc = {

    }


if __name__ == '__main__':
    print(get_openid())