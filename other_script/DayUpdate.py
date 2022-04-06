# coding:utf-8
import random
from Db.MySQLClient.client import MYSQL
from Config.GlobalSetting import MYSQL_CONFIG
from datetime import datetime
import os
import sys
# SQL_RANDOM = """SELECT
#  DISTINCT `machineTitle`,`machineImg`,`machinePublishTime`,`md5hash`
# FROM
# `machineData` AS MD
# JOIN (
# SELECT
# 		ROUND(
# 				RAND() * (
# 						(SELECT MAX(id) FROM `machineData`) - (SELECT MIN(id) FROM `machineData`)
# 				) + (SELECT MIN(id) FROM `machineData`)
# 		) AS id
# ) AS XX
# WHERE
# MD.id >= XX.id AND `machineImg` != "" AND DATE_SUB(CURDATE(), INTERVAL 30 DAY) < date(machinePublishTime)
#
# ORDER BY `machinePublishTime` DESC
#
# LIMIT 10;"""


# 每日更新一次
def data_updating(mysqlOBJ):
    mysql, cursor = mysqlOBJ.get_mysql()
    SQL_NEWEST = 'SELECT DISTINCT `machineTitle`,`machineImg`,`machinePublishTime`,`md5hash` ' \
                 'FROM `machineData` ORDER BY `machinePublishTime` DESC LIMIT 10 '
    cursor.execute(SQL_NEWEST)
    mysql.commit()
    resultList = cursor.fetchall()
    for res in resultList:
        res['machineImg'] = res['machineImg'].split('$$$')[0]
        res["machinePublishTime"] = res["machinePublishTime"].strftime("%Y-%m-%d")

    SQL_DELETE = 'TRUNCATE TABLE `machineDay`;'
    cursor.execute(SQL_DELETE)
    mysql.commit()

    args = [ (
        _["md5hash"],_['machineTitle'],_['machineImg'],_['machinePublishTime'],datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ) for _ in resultList]
    SQL_DAY = 'INSERT INTO `machineDay`(`md5hash`,`machineTitle`,`machineImg`,`machinePublishTime`,`machineInsertTime`) ' \
              'VALUES (%s,%s,%s,%s,%s)'
    cursor.executemany(SQL_DAY,args)
    mysql.commit()


if __name__ == '__main__':
    sys.path.append('/workspace/framework_spider/')
    mysqlOBJ = MYSQL(CONFIG=MYSQL_CONFIG, db='machinedb')
    data_updating(mysqlOBJ)