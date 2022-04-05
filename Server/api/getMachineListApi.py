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

    return random.choices(resultList, k=10)


# 获取最大条数
def get_list_page(mysqlOBJ, levelClassOne=None, levelClassTwo=None, levelClassThree=None, machineSiteId=None):
    mysql, cursor = mysqlOBJ.get_mysql()
    levelClassOne = levelClassOne.replace("全部", '').replace("其他", '').replace("其它", '').strip() if levelClassOne else ""
    levelClassTwo = levelClassTwo.replace("全部", '').replace("其他", '').replace("其它", '').strip() if levelClassTwo else ""
    levelClassThree = levelClassThree.replace("全部", '').replace("其他", '').replace("其它",
                                                                                  '').strip() if levelClassThree else ""

    if machineSiteId:
        if levelClassOne and levelClassTwo and levelClassThree:
            sql_max_count = 'SELECT COUNT(`id`) ' \
                            'FROM `machineData` ' \
                            'WHERE `machineSiteId` = %s AND ' \
                            '`machineLevelOne` = %s AND ' \
                            '`machineLevelTwo` = %s AND ' \
                            '`machineLevelThree` = %s;'
        elif levelClassOne and levelClassTwo and not levelClassThree:
            sql_max_count = 'SELECT COUNT(`id`) ' \
                            'FROM `machineData` ' \
                            'WHERE `machineSiteId` = %s AND ' \
                            '`machineLevelOne` = %s AND ' \
                            '`machineLevelTwo` = %s;'

        elif levelClassOne and not levelClassTwo and not levelClassThree:
            sql_max_count = 'SELECT COUNT(`id`) ' \
                            'FROM `machineData` ' \
                            'WHERE `machineSiteId` = %s AND ' \
                            '`machineLevelOne` = %s;'

        else:
            sql_max_count = 'SELECT COUNT(`id`) FROM `machineData` WHERE `machineSiteId` =%s;'
    else:
        sql_max_count = 'SELECT COUNT(`id`) FROM `machineData`;'
    args = [ _ for _ in [machineSiteId,levelClassOne,levelClassTwo,levelClassThree] if _]
    cursor.execute(sql_max_count, args)
    mysql.commit()
    max_count = cursor.fetchone()['COUNT(`id`)']
    return max_count


# 翻页
def roll_page(mysqlOBJ, page, pagesize, levelClassOne, levelClassTwo, levelClassThree, machineSiteId=None):
    mysql, cursor = mysqlOBJ.get_mysql()
    levelClassOne = levelClassOne.replace("全部", '').replace("其他", '').replace("其它", '').strip() if levelClassOne else ""
    levelClassTwo = levelClassTwo.replace("全部", '').replace("其他", '').replace("其它", '').strip() if levelClassTwo else ""
    levelClassThree = levelClassThree.replace("全部", '').replace("其他", '').replace("其它",
                                                                                  '').strip() if levelClassThree else ""
    page = page - 1
    if machineSiteId:
        if levelClassOne and levelClassTwo and levelClassThree:
            sql_roll_page = 'SELECT `machineTitle`,`machineImg`,`machinePublishTime`,`md5hash` ' \
                            'FROM `machineData` ' \
                            'WHERE `machineSiteId` = %s AND ' \
                            '`machineLevelOne` = %s AND ' \
                            '`machineLevelTwo` = %s AND ' \
                            '`machineLevelThree` = %s ' \
                            'LIMIT %s,%s'

            cursor.execute(sql_roll_page,
                           (machineSiteId, levelClassOne, levelClassTwo, levelClassThree, page * pagesize, pagesize))
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
            sql_roll_page = 'SELECT `machineTitle`,`machineTitle`,`machineImg`,`machinePublishTime`,`md5hash` ' \
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
                        'FROM `machineData` LIMIT %s,%s' % (str(page * pagesize), str(pagesize))

        cursor.execute(sql_roll_page)
        mysql.commit()

        return cursor.fetchall()


# 获取翻页的列表 【0,1,2,3】
def get_page_list(max_page,now_page):
    l = [_ for _ in range((now_page - 2) if now_page > 2 else 1,max_page+1)][0:7]
    return l

if __name__ == '__main__':
    # mysqlOBJ, levelClassOne, levelClassTwo, levelClassThree, machineSiteId=None
    # mysqlOBJ = MYSQL(CONFIG=MYSQL_CONFIG, db='machinedb')  # 该视图的专用mysql对象
    # print(get_list_page(mysqlOBJ,levelClassOne='二手金属切削机床'))

    print(get_page_list(10,9))