# coding:utf-8
# 获取详情页信息


from Db.MySQLClient.client import create_new_mysql
from Config.GlobalSetting import MYSQL_CONFIG
from datetime import datetime
import random

# 获取单个详情页
def get_page(mysql,cursor,md5hash):
    sql_roll_page = 'SELECT * FROM `machineData` WHERE md5hash = %s'
    md5hash = md5hash.replace('.html','')
    cursor.execute(sql_roll_page,md5hash)
    mysql.commit()

    return cursor.fetchone()


# 获取 关联公司数据
def get_relation_page(mysql,cursor,contact):
    sql_relation_page = 'SELECT ' \
                        '`machineTitle`,`machineImg`,`machinePublishTime`,`md5hash` ' \
                        'FROM `machineData` ' \
                        'WHERE `machineContactInfo` = %s ' \
                        'ORDER BY `machinePublishTime` LIMIT 5;'
    cursor.execute(sql_relation_page, contact)
    mysql.commit()

    relation_results = cursor.fetchall()

    for res in relation_results:
        res['machineImg'] = res['machineImg'].split('$$$')[0]
        res["machinePublishTime"] = res["machinePublishTime"].strftime("%Y-%m-%d")
    return relation_results


if __name__ == '__main__':
    mysql, cursor = create_new_mysql(CONFIG=MYSQL_CONFIG)
    print(get_page(mysql,cursor,md5hash='\'1\' or 1=1 LIMIT 30'))