# coding:utf-8
# 保存发布日志
import json
import requests
from Db.MySQLClient.client import MYSQL
from Config.GlobalSetting import MYSQL_CONFIG
from datetime import datetime
import time


def save_pub_log(mysqlObj, article_id, title):
    mysql, cursor = mysqlObj.get_mysql()
    SQL = 'INSERT INTO `machineWXPubArticle`(`machineArticleId`,`machineTitle`,`machinePublishTime`) VALUES (%s,%s,%s)'
    cursor.execute(SQL, (article_id, title, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    mysql.commit()
    print('保存日志成功！')


def get_accessToken(mysqlObj):
    mysql, cursor = mysqlObj.get_mysql()
    sql = 'SELECT `machineAccessToken` FROM `machineToken`;'
    cursor.execute(sql)
    mysql.commit()
    _ = cursor.fetchone()
    if _['machineAccessToken']:
        return _['machineAccessToken']
    else:
        time.sleep(1)
        return get_accessToken(mysqlObj)


def publish_event(*args, **kwargs):
    mysqlObj = kwargs.get('mysqlObj')
    xmlDict = kwargs.get('xmlDict')
    print(xmlDict)
    article_id = xmlDict['article_id']
    doc = {
        "article_id": article_id
    }
    respContent = requests.post(
        url='https://api.weixin.qq.com/cgi-bin/freepublish/getarticle?access_token=' + get_accessToken(mysqlObj),
        json=doc).content
    respJson = json.loads(respContent.decode('utf-8'))
    title = respJson['news_item'][0]["title"]
    save_pub_log(mysqlObj, article_id, title)
