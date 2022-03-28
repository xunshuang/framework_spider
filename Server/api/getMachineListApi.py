# coding:utf-8
# 获取机床信息列表页api 和 每日推荐 api

from Db.MySQLClient.client import create_new_mysql
from Config.GlobalSetting import MYSQL_CONFIG
from datetime import datetime
import random

def get_day_recommend(mysql,cursor):
    sql_max_count = 'SELECT MAX(`id`) FROM `machineData`;'
    cursor.execute(sql_max_count)
    mysql.commit()
    max_count = cursor.fetchone()['MAX(`id`)']

    resultList = []
    while True:
        random_args = random.randint(1, max_count)
        sql_random_choice = 'SELECT * FROM `machineData` LIMIT %s,10'

        cursor.execute(sql_random_choice,random_args)
        mysql.commit()
        random_result = cursor.fetchall()
        if random_result:
            resultList += list(random_result)

            if len(resultList) >= 10:
                break
        else:
            print(random_args)

    return random.choices(resultList,k=10)


if __name__ == '__main__':
    mysql, cursor = create_new_mysql(CONFIG=MYSQL_CONFIG)
    print(get_day_recommend(mysql,cursor))