# coding:utf-8
# 获取机床信息列表页api 和 每日推荐 api

from Db.MySQLClient.client import MYSQL
from Config.GlobalSetting import MYSQL_CONFIG
from datetime import datetime
import random

# 随机推荐10个
def get_random_recommend(mysqlOBJ):
    mysql, cursor = mysqlOBJ.get_mysql()

    SQL_RANDOM = """SELECT
 DISTINCT `machineTitle`,`machineImg`,`machinePublishTime`,`md5hash`
FROM
`machineData` AS MD
JOIN (
SELECT
		ROUND(
				RAND() * (
						(SELECT MAX(id) FROM `machineData`) - (SELECT MIN(id) FROM `machineData`)
				) + (SELECT MIN(id) FROM `machineData`)
		) AS id
) AS XX
WHERE
MD.id >= XX.id AND `machineImg` != "" AND DATE_SUB(CURDATE(), INTERVAL 30 DAY) < date(machinePublishTime)

ORDER BY `machinePublishTime` DESC

LIMIT 10;"""

    cursor.execute(SQL_RANDOM)
    mysql.commit()
    resultList = cursor.fetchall()
    for res in resultList:
        res['machineImg'] = res['machineImg'].split('$$$')[0]
        res["machinePublishTime"] = res["machinePublishTime"].strftime("%Y-%m-%d")

    return random.choices(resultList,k=10)


# 获取最大条数
def get_list_page(mysqlOBJ,machineSiteId=None):
    mysql, cursor = mysqlOBJ.get_mysql()
    if machineSiteId:
        sql_max_count = 'SELECT COUNT(`id`) FROM `machineData` WHERE `machineSiteId` =%s;'
        cursor.execute(sql_max_count,machineSiteId)
    else:
        sql_max_count = 'SELECT COUNT(`id`) FROM `machineData`;'
        cursor.execute(sql_max_count)

    mysql.commit()
    max_count = cursor.fetchone()['COUNT(`id`)']
    return max_count


# 翻页
def roll_page(mysqlOBJ,page,pagesize,levelClassOne,levelClassTwo,levelClassThree,machineSiteId=None):
    mysql, cursor = mysqlOBJ.get_mysql()
    levelClassOne = levelClassOne.replace("全部",'').replace("其他",'').replace("其它",'').strip() if levelClassOne else ""
    levelClassTwo = levelClassTwo.replace("全部",'').replace("其他",'').replace("其它",'').strip() if levelClassTwo else ""
    levelClassThree = levelClassThree.replace("全部",'').replace("其他",'').replace("其它",'').strip() if levelClassThree else ""


    if machineSiteId:
        if levelClassOne and levelClassTwo and levelClassThree:
            sql_roll_page = 'SELECT `machineTitle`,`machineImg`,`machinePublishTime`,`md5hash` ' \
                            'FROM `machineData` ' \
                            'WHERE `machineSiteId` = %s AND ' \
                            '`machineLevelOne` = %s AND ' \
                            '`machineLevelTwo` = %s AND ' \
                            '`machineLevelThree` = %s ' \
                            'LIMIT %s,%s'

            cursor.execute(sql_roll_page,(machineSiteId,levelClassOne,levelClassTwo,levelClassThree,page * pagesize,pagesize))
            mysql.commit()

            return cursor.fetchall()
        elif levelClassOne and levelClassTwo and not levelClassThree:
            sql_roll_page = 'SELECT `machineTitle`,`machineImg`,`machinePublishTime`,`md5hash` ' \
                            'FROM `machineData` ' \
                            'WHERE `machineSiteId` = %s AND ' \
                            '`machineLevelOne` = %s AND ' \
                            '`machineLevelTwo` = %s ' \
                            'LIMIT %s,%s'

            cursor.execute(sql_roll_page,
                           (machineSiteId, levelClassOne, levelClassTwo, page * pagesize, pagesize))
            mysql.commit()

            return cursor.fetchall()
        elif levelClassOne and not levelClassTwo and not levelClassThree:
            sql_roll_page = 'SELECT `machineTitle`,`machineImg`,`machinePublishTime`,`md5hash` ' \
                            'FROM `machineData` ' \
                            'WHERE `machineSiteId` = %s AND ' \
                            '`machineLevelOne` = %s ' \
                            'LIMIT %s,%s'

            cursor.execute(sql_roll_page,
                           (machineSiteId, levelClassOne, page * pagesize, pagesize))
            mysql.commit()

            return cursor.fetchall()
        else:
            sql_roll_page = 'SELECT `machineTitle`,`machineImg`,`machinePublishTime`,`md5hash` ' \
                            'FROM `machineData` ' \
                            'WHERE `machineSiteId` = %s ' \
                            'LIMIT %s,%s'

            cursor.execute(sql_roll_page,
                           (machineSiteId, page * pagesize, pagesize))
            mysql.commit()

            return cursor.fetchall()
    else:
        sql_roll_page = 'SELECT `machineTitle`,`machineImg`,`machinePublishTime`,`md5hash` ' \
                        'FROM `machineData` LIMIT %s,%s' %(str(page * pagesize), str(pagesize))

        cursor.execute(sql_roll_page)
        mysql.commit()

        return cursor.fetchall()

