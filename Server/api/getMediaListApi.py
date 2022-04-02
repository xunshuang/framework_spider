# coding:utf-8
# 获取所有机床信源种类
from Db.MySQLClient.client import MYSQL
from Config.GlobalSetting import MYSQL_CONFIG
from datetime import datetime

# 获取信源种类、信源详情
def get_media(mysqlOBJ):
    mysql, cursor = mysqlOBJ.get_mysql()

    sql = 'SELECT * FROM `machineSite`;'

    cursor.execute(sql)
    mysql.commit()

    result = cursor.fetchall()
    return [
        {
            "machineSiteId":_["machineSiteId"],
            "machineSiteName":_["machineSiteName"],
            "machineT":_["machineT"],
            "machineSiteType":_["machineSiteType"],
            "machineLastTime":_["machineLastTime"].strftime("%Y-%m-%d %H:%M:%S")
        } for _ in result
    ]

# 获取媒体字典
def get_media_dict(mysqlOBJ,machineSiteId):
    mysql, cursor = mysqlOBJ.get_mysql()

    sql = 'SELECT `machineJson` FROM `machineMap` WHERE `machineSiteId` = %s;'

    cursor.execute(sql,machineSiteId)
    mysql.commit()

    result = cursor.fetchone()
    return result['machineJson']



