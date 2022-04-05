# coding:utf-8
# 获取最新的新闻

from Db.MySQLClient.client import MYSQL
from Config.GlobalSetting import MYSQL_CONFIG
from datetime import datetime
import random


def get_news_page(mysqlOBJ,md5hash):
    mysql, cursor = mysqlOBJ.get_mysql()
    SQL = 'SELECT * FROM `machineNews` WHERE `md5hash` = %s'

    cursor.execute(SQL,md5hash)
    mysql.commit()
    news_page = cursor.fetchone()
    news_page['machineContent'] = news_page['machineContent'].decode()

    news_page['machineContent'] = [
        _.strip() for _ in news_page['machineContent'].split('\n') if len(_.strip())
    ]
    return news_page



if __name__ == '__main__':
    mysqlOBJ = MYSQL(CONFIG=MYSQL_CONFIG, db='machinedb')
    x = get_news_page(mysqlOBJ,'4d1100ba4aca84052d1543830eded9ab')
    x['machineContent'] = x['machineContent'].decode()
    print(x)