# coding:utf-8
# 获取新闻列表页

from Db.MySQLClient.client import MYSQL
from Config.GlobalSetting import MYSQL_CONFIG
from datetime import datetime
import random


def get_news_list(mysqlOBJ, page):
    mysql, cursor = mysqlOBJ.get_mysql()

    if page:
        page = page - 1

    SQL = 'SELECT `machineTitle`,`machineImg`,`machinePublishTime`,`md5hash`,`machineDescription`,`machineKeywords` ' \
          'FROM `machineNews` ' \
          'ORDER BY `machinePublishTime` desc ' \
          'LIMIT %s,10;'

    cursor.execute(
        SQL, page * 10
    )
    mysql.commit()
    news_result = cursor.fetchall()

    for _ in news_result:
        _['machinePublishTime'] = _['machinePublishTime'].strftime("%Y-%m-%d")

    return news_result

# 获取翻页的列表 【0,1,2,3】
def get_page_list(max_page,now_page):
    l = [_ for _ in range((now_page - 2) if now_page > 2 else 1,max_page+1)][0:7]
    return l

def get_news_max(mysqlOBJ):
    sql_max_count = "SELECT COUNT(`id`) FROM `machineNews`"
    mysql, cursor = mysqlOBJ.get_mysql()
    cursor.execute(sql_max_count)
    mysql.commit()
    max_count = cursor.fetchone()['COUNT(`id`)']
    return max_count


if __name__ == '__main__':
    mysqlOBJ = MYSQL(CONFIG=MYSQL_CONFIG, db='machinedb')  # 该视图的专用mysql对象
    print(get_news_list(mysqlOBJ, 1))
