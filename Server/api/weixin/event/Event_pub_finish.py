# coding:utf-8
# 保存发布日志
import json
import requests
from Db.MySQLClient.client import MYSQL
from Config.GlobalSetting import MYSQL_CONFIG
from datetime import datetime
import time


def save_pub_log(mysqlOBJ, article_id, title):
    mysql, cursor = mysqlOBJ.get_mysql()
    SQL = 'INSERT INTO `machineWXPubArticle`(`machineArticleId`,`machineTitle`,`machinePublishTime`) VALUES (%s,%s,%s)'
    cursor.execute(SQL, (article_id, title, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    mysql.commit()
    print('保存日志成功！')


def get_accessToken(mysqlOBJ):
    mysql, cursor = mysqlOBJ.get_mysql()
    sql = 'SELECT `machineAccessToken` FROM `machineToken`;'
    cursor.execute(sql)
    mysql.commit()
    _ = cursor.fetchone()
    if _['machineAccessToken']:
        return _['machineAccessToken']
    else:
        time.sleep(1)
        return get_accessToken(mysqlOBJ)


def publish_event(*args, **kwargs):

    mysqlOBJ = kwargs.get('mysqlOBJ')
    xmlDict = kwargs.get('xmlDict')

    article_id = xmlDict['PublishEventInfo']['article_id']
    doc = {
        "article_id": article_id
    }
    respContent = requests.post(
        url='https://api.weixin.qq.com/cgi-bin/freepublish/getarticle?access_token=' + get_accessToken(mysqlOBJ),
        json=doc).content
    respJson = json.loads(respContent.decode('utf-8'))
    title = respJson['news_item'][0]["title"]
    save_pub_log(mysqlOBJ, article_id, title)
