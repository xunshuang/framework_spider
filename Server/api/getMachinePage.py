# coding:utf-8
# 获取详情页信息


from Db.MySQLClient.client import create_new_mysql
from Config.GlobalSetting import MYSQL_CONFIG
from datetime import datetime
import random

# 获取单个详情页
def get_page(mysql,cursor,md5hash):
    sql_roll_page = 'SELECT * FROM `machineData` WHERE md5hash = %s'

    cursor.execute(sql_roll_page,md5hash)
    mysql.commit()

    return cursor.fetchall()




if __name__ == '__main__':
    mysql, cursor = create_new_mysql(CONFIG=MYSQL_CONFIG)
    print(get_page(mysql,cursor,md5hash='\'1\' or 1=1 LIMIT 30'))