# coding:utf-8
# 将用户的订阅能力清除

import os
import sys
import time
import json
import hashlib
import jinja2

sys.path.append('/workspace/framework_spider/')
import requests
from Db.MySQLClient.client import MYSQL
from Config.GlobalSetting import MYSQL_CONFIG
from datetime import datetime

mysqlObj = MYSQL(MYSQL_CONFIG, db='machinedb')


def refresh():
    mysql,cursor = mysqlObj.get_mysql()
    SQL = 'UPDATE `machineWXUser` SET `machineSubMachine` = "2" WHERE `machineSubMachine` = "1";'
    cursor.execute(SQL)
    mysql.commit()
    print('用户态刷新成功！')



if __name__ == '__main__':
    refresh()
