# coding:utf-8
# 保存发布日志
import json
import requests
from Db.MySQLClient.client import MYSQL
from Config.GlobalSetting import MYSQL_CONFIG
from datetime import datetime
from threading import Thread
import asyncio
from asyncio import Queue
import aiohttp
import time


def save_pub_log(mysqlOBJ, article_id, title,article_url):
    mysql, cursor = mysqlOBJ.get_mysql()
    SQL = 'INSERT INTO `machineWXPubArticle`(`machineArticleId`,`machineTitle`,`machineUrl`,`machinePublishTime`) VALUES (%s,%s,%s,%s)'
    cursor.execute(SQL, (article_id, title,article_url ,datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
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

# 获取以及关注的且订阅本日新闻的列表
def get_fans_list(mysqlOBJ,offset=0):
    mysql, cursor = mysqlOBJ.get_mysql()
    SQL = 'SELECT `machineOpenId` FROM `machineWXUser` WHERE `machineSubMachine` = "1" LIMIT %s,100'
    cursor.execute(SQL,offset)
    mysql.commit()
    result = cursor.fetchall()
    for _ in result:
        yield _['machineOpenId']

    if len(result) == 100:
        __ = get_fans_list(mysqlOBJ,offset+100)
        for _ in __:
            yield _


def make_thread(mysqlOBJ,articleId):
    thread = Thread(target=loops,args=(mysqlOBJ,articleId))
    thread.start()
    thread.join()


def loops(mysqlOBJ,articleId):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_msg(mysqlOBJ,articleId,loop))
    loop.close()

async def send_msg(mysqlOBJ,articleId,loop):
    token = get_accessToken(mysqlOBJ)
    async with aiohttp.ClientSession(loop=loop) as client:
        workList = []
        for openId in get_fans_list(mysqlOBJ,offset=0):
            workList.append(
                asyncio.ensure_future(post(token,openId,articleId,client))
            )
            if len(workList) >= 100:
                await asyncio.gather(*workList)
                workList = []
        if len(workList):
            await asyncio.gather(*workList)

    await asyncio.sleep(0.5)

async def post(token,openId,articleId,client):
    url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={}".format(token)
    body = {
        "touser": f"{openId}",
        "msgtype": "mpnewsarticle",
        "mpnewsarticle": {
            "article_id": f"{articleId}"
        }
    }
    async with client.post(url=url,json=body) as resp:
        respJson = await resp.json()
        print(respJson)

def publish_event(*args, **kwargs):

    mysqlOBJ = kwargs.get('mysqlOBJ')
    xmlDict = kwargs.get('xmlDict')

    article_id = xmlDict['PublishEventInfo']['article_id']
    article_url = xmlDict['PublishEventInfo']['article_detail']['item']['article_url']
    doc = {
        "article_id": article_id
    }
    respContent = requests.post(
        url='https://api.weixin.qq.com/cgi-bin/freepublish/getarticle?access_token=' + get_accessToken(mysqlOBJ),
        json=doc).content
    respJson = json.loads(respContent.decode('utf-8'))
    title = respJson['news_item'][0]["title"]
    save_pub_log(mysqlOBJ, article_id, title,article_url)
    make_thread(mysqlOBJ,article_id)


if __name__ == '__main__':
    mysqlObj = MYSQL(MYSQL_CONFIG, db='machinedb')

    make_thread(mysqlObj, articleId="6beSyaQWnY50zaxEn-OkgSePIVO6w9O3wJuwWwhPfPp6mt0YvZbLIar_pQCzlM7R")
