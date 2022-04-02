# coding:utf-8
# 获取详情页信息

from Config.GlobalSetting import MYSQL_CONFIG
from datetime import datetime
import random

# 获取单个详情页
def get_page(mysqlOBJ,md5hash):
    mysql, cursor = mysqlOBJ.get_mysql()
    sql_roll_page = 'SELECT * FROM `machineData` WHERE md5hash = %s'
    md5hash = md5hash.replace('.html','')
    cursor.execute(sql_roll_page,md5hash)
    mysql.commit()

    return cursor.fetchone()


# 获取 关联公司数据
def get_relation_page(mysqlOBJ,contact):
    mysql, cursor = mysqlOBJ.get_mysql()
    sql_relation_page = 'SELECT ' \
                        '`machineTitle`,`machineImg`,`machinePublishTime`,`md5hash` ' \
                        'FROM `machineData` ' \
                        'WHERE `machineContactInfo` = %s ' \
                        'ORDER BY `machinePublishTime` LIMIT 5;'
    cursor.execute(sql_relation_page, contact)
    mysql.commit()

    relation_results = cursor.fetchall()

    for res in relation_results:
        res['machineImg'] = res['machineImg'].split('$$$')[0] if res['machineImg'] else ""
        res["machinePublishTime"] = res["machinePublishTime"].strftime("%Y-%m-%d")
        if not res['machineImg']:
            res['machineImg'] = '/images/imageLost.png'
    return relation_results


