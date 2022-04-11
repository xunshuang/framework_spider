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




#
get_media_list()

#
# xml = """<xml><ToUserName><![CDATA[gh_dcd30c3d7c29]]></ToUserName>\n<FromUserName><![CDATA[oKV3l6L6-0xMGcNtJ1zHt8WiaBLY]]></FromUserName>\n<CreateTime>1649681285</CreateTime>\n<MsgType><![CDATA[event]]></MsgType>\n<Event><![CDATA[PUBLISHJOBFINISH]]></Event>\n<PublishEventInfo>\n<publish_id>2247483715</publish_id>\n<publish_status>0</publish_status>\n<article_id><![CDATA[6beSyaQWnY50zaxEn-OkgdWtQd4c4cOFmNktR_jcT8KxQvDbkN9qsYGuSDNYaobi]]></article_id>\n<article_detail>\n<count>1</count>\n<item>\n<idx>1</idx>\n<article_url><![CDATA[http://mp.weixin.qq.com/s?__biz=MzkwNzM0NTcwNQ==&mid=2247483715&idx=1&sn=c6c77951b7fa1a8cb91c8cee2d2224fc&chksm=c0dbeb05f7ac6213b2cb8e335d8614d37a1695f06d547ccffe6277f631c27efc9a98186a57fb#rd]]></article_url>\n</item>\n</article_detail>\n</PublishEventInfo></xml>"""
#
# xmlDict = xmltodict.parse(xml)['xml']
#
# print(xmlDict)