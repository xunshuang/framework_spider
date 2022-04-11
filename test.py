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
    doc = {
        "article_id":"6beSyaQWnY50zaxEn-Okgbplimax7ABJMIRC35LzRbj2LXHpkWbDk5Yw7dQQAXhl"
    }
    headers= {
        ""
    }
    respJson = requests.post(url='https://api.weixin.qq.com/cgi-bin/freepublish/getarticle?access_token='+ get_accessToken() + '&lang=zh_CN',json=doc)

    print(respJson)

#
get_media_list()

#
# xml = """<xml><ToUserName><![CDATA[gh_dcd30c3d7c29]]></ToUserName>\n<FromUserName><![CDATA[oKV3l6L6-0xMGcNtJ1zHt8WiaBLY]]></FromUserName>\n<CreateTime>1649669540</CreateTime>\n<MsgType><![CDATA[event]]></MsgType>\n<Event><![CDATA[PUBLISHJOBFINISH]]></Event>\n<PublishEventInfo>\n<publish_id>2247483707</publish_id>\n<publish_status>0</publish_status>\n<article_id><![CDATA[6beSyaQWnY50zaxEn-OkgTYQm2aZbsdNsSUoZW8c9EkavnUsUZN9ktmHC2GHmrL0]]></article_id>\n<article_detail>\n<count>1</count>\n<item>\n<idx>1</idx>\n<article_url><![CDATA[http://mp.weixin.qq.com/s?__biz=MzkwNzM0NTcwNQ==&mid=2247483707&idx=1&sn=3c67eb8efdaea707f0c1198fb633e280&chksm=c0dbeb7df7ac626b8cce9c0095fd2b355b4c0212ac4d66a77a546a32328e0189832d17131e43#rd]]></article_url>\n</item>\n</article_detail>\n</PublishEventInfo></xml>"""
#
#
# xmlDict = xmltodict.parse(xml)
#
# print(xmlDict['xml'])