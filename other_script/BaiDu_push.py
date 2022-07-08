# coding:utf-8
# 百度收录推送
import aiohttp
import asyncio
import random
import os
import sys
sys.path.append('/workspace/framework_spider/')
from Db.MySQLClient.client import MYSQL
from Config.GlobalSetting import MYSQL_CONFIG
from datetime import datetime

mysqlOBJ = MYSQL(CONFIG=MYSQL_CONFIG, db='machinedb')


def read_article():
    start = 0
    while True:
        mysql,cursor = mysqlOBJ.get_mysql()
        SQL = 'SELECT `md5hash` FROM `machineData` ORDER BY `machinePublishTime` DESC LIMIT %s,100'
        cursor.execute(SQL,start)
        mysql.commit()
        result = cursor.fetchall()
        if len(result) == 100:
            start += 100 
            yield ['http://www.surefly.top/single/' + _['md5hash'] + '.html' for _ in result]
        else:
            yield ['http://www.surefly.top/single/' + _['md5hash'] + '.html' for _ in result]
            break


async def push():
    for lis in read_article():
        url = 'http://data.zz.baidu.com/urls?site=www.surefly.top&token=11'
        async with aiohttp.request('post',url=url,data='\n'.join(lis)) as resp:
            respJson = await resp.json()
            print(respJson)



asyncio.run(push())