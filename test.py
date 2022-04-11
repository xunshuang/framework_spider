# coding:utf-8
import requests
from xml.etree import ElementTree

import os
import sys
import time
import json
import hashlib
import jinja2
import xmltodict
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


def get_media_list():
    for i in range(20):
        url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={}".format(get_accessToken())
        print(url)

        body = {
            "touser": "oKV3l6GA5S1Bnnakk_ThJvqdbbIA",
            "msgtype": "mpnewsarticle",
            "mpnewsarticle":{
                "article_id": "6beSyaQWnY50zaxEn-OkgSePIVO6w9O3wJuwWwhPfPp6mt0YvZbLIar_pQCzlM7R"

            }
        }
        data = bytes(json.dumps(body, ensure_ascii=False).encode('utf-8'))
        print(data)
        response = requests.post(url, data=data)
        # 这里可根据回执code进行判定是否发送成功(也可以根据code根据错误信息)
        result = response.json()
        print(result)




# get_media_list()

