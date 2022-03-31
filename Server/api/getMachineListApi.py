# coding:utf-8
# 获取机床信息列表页api 和 每日推荐 api

from Db.MySQLClient.client import create_new_mysql
from Config.GlobalSetting import MYSQL_CONFIG
from datetime import datetime
import random

# 随机推荐10个
def get_random_recommend(mysql,cursor):
    sql_max_count = 'SELECT MAX(`id`) FROM `machineData`;'
    cursor.execute(sql_max_count)
    mysql.commit()
    max_count = cursor.fetchone()['MAX(`id`)']

    resultList = []
    while True:
        random_args = random.randint(1, max_count)
        sql_random_choice = 'SELECT `machineTitle`,`machineImg`,`machinePublishTime` FROM `machineData` WHERE `machineImg` != "" LIMIT %s,10'

        cursor.execute(sql_random_choice,random_args)
        mysql.commit()
        random_result = cursor.fetchall()
        if random_result:
            resultList += list(random_result)

            if len(resultList) >= 10:
                break
        else:
            print(random_args)
    for res in resultList:
        res['machineImg'] = res['machineImg'].split('$$$')[0]
        res["machinePublishTime"] = res["machinePublishTime"].strftime("%Y-%m-%d")

    return random.choices(resultList,k=10)


# 获取最大条数
def get_list_page(mysql,cursor,machineSiteId=None):
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
def roll_page(mysql,cursor,page,pagesize,machineSiteId=None):
    if machineSiteId:
        sql_roll_page = 'SELECT `machineTitle`,`machineImg`,`machinePublishTime` ' \
                        'FROM `machineData` WHERE `machineSiteId` = "%s" LIMIT %s,%s' %(machineSiteId,str(page*pagesize),str(pagesize))

        cursor.execute(sql_roll_page)
        mysql.commit()

        return cursor.fetchall()
    else:
        sql_roll_page = 'SELECT `machineTitle`,`machineImg`,`machinePublishTime` ' \
                        'FROM `machineData` LIMIT %s,%s' %(str(page * pagesize), str(pagesize))

        cursor.execute(sql_roll_page)
        mysql.commit()

        return cursor.fetchall()

if __name__ == '__main__':
    mysql, cursor = create_new_mysql(CONFIG=MYSQL_CONFIG)
    print(roll_page(mysql,cursor,1,20,machineSiteId='A002'))