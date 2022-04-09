# coding:utf-8
# 定时拉取粉丝的 openId

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


def get_openId(openId=""):
    accessToken = get_accessToken()
    openidList = requests.get(
        f'https://api.weixin.qq.com/cgi-bin/user/get?access_token={accessToken}&next_openid={openId}').json()
    try:
        yield openidList.get('data').get('openid')

        if len(openidList.get('data').get('openid')) == 10000:
            x = get_openId(openidList.get('data').get('openid')[-1])
            yield [openId for openId in x]

    except:
        pass



def save_openId():
    SQL = 'INSERT INTO'
    openIdLists = get_openId()
    for openIdList in openIdLists:
        pass