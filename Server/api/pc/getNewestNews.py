# coding:utf-8
# 获取最新的新闻

from Db.MySQLClient.client import MYSQL
from Config.GlobalSetting import MYSQL_CONFIG
from datetime import datetime
import random


def get_newest(mysqlOBJ):
    mysql, cursor = mysqlOBJ.get_mysql()
    SQL = 'SELECT ' \
          '`machineTitle`,' \
          '`machineImg`,' \
          '`machinePublishTime`,' \
          '`md5hash` ' \
          'FROM `machineNews` ' \
          'ORDER BY `machinePublishTime` DESC LIMIT 5'

    cursor.execute(SQL)
    mysql.commit()

    return cursor.fetchall()



if __name__ == '__main__':
    mysqlOBJ = MYSQL(CONFIG=MYSQL_CONFIG, db='machinedb')
    print(get_newest(mysqlOBJ))