# coding:utf-8
import os
import sys

sys.path.append('/workspace/framework_spider/')
import requests
from Db.MySQLClient.client import MYSQL
from Config.GlobalSetting import MYSQL_CONFIG
from datetime import datetime

url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxb28f616376c291c5&secret=af45f60a585ebb78ac5b7876318c9216'

respJson = requests.get(url).json()


if respJson['access_token']:
    mysqlObj = MYSQL(MYSQL_CONFIG,db='machinedb')
    mysql,cursor = mysqlObj.get_mysql()

    SQL = 'TRUNCATE TABLE `machineToken`;'

    cursor.execute(SQL)
    mysql.commit()

    SQL_INSERT = 'INSERT INTO `machineToken`(`machineAccessToken`,`machineInsertTime`) VALUES (%s,%s)'

    cursor.execute(SQL_INSERT,(respJson['access_token'],datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    mysql.commit()
    print("存储成昆！")