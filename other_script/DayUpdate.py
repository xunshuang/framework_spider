# coding:utf-8
import random
import os
import sys
sys.path.append('/workspace/framework_spider/')
from Db.MySQLClient.client import MYSQL
from Config.GlobalSetting import MYSQL_CONFIG
from datetime import datetime

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


    ARGS = []
    # 推荐当然要推荐精品啦！
    for siteId in ['A001','A002','A003']:
        SQL_NEWEST = f'SELECT DISTINCT `machineTitle`,`machineImg`,`machinePublishTime`,`md5hash` FROM `machineData` WHERE `machineSiteId` = "{siteId}" AND `machineTitle` NOT LIKE "%回收%" AND `machineImg` != "" ORDER BY `machinePublishTime` DESC LIMIT 30 '
        cursor.execute(SQL_NEWEST)
        mysql.commit()
        resultList = cursor.fetchall()
        for res in resultList:
            res['machineImg'] = res['machineImg'].split('$$$')[0]
            res["machinePublishTime"] = res["machinePublishTime"].strftime("%Y-%m-%d")



        args = [ (
            _["md5hash"],_['machineTitle'],_['machineImg'],_['machinePublishTime'],datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ) for _ in resultList]
        ARGS += args
        print(siteId)

    SQL_DAY = 'INSERT INTO `machineDay`(`md5hash`,`machineTitle`,`machineImg`,`machinePublishTime`,`machineInsertTime`) ' \
              'VALUES (%s,%s,%s,%s,%s)'

    ARGS.sort(key=lambda x:x[-2],reverse=True)

    SQL_DELETE = 'TRUNCATE TABLE `machineDay`;'
    cursor.execute(SQL_DELETE)
    mysql.commit()

    cursor.executemany(SQL_DAY,ARGS)
    mysql.commit()


if __name__ == '__main__':

    mysqlOBJ = MYSQL(CONFIG=MYSQL_CONFIG, db='machinedb')
    data_updating(mysqlOBJ)