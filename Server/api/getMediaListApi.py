# coding:utf-8
# 获取所有机床信源种类
from Db.MySQLClient.client import create_new_mysql
from Config.GlobalSetting import MYSQL_CONFIG
from datetime import datetime

# 获取信源种类、信源详情
def get_media(mysql,cursor):
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



if __name__ == '__main__':
    mysql,cursor = create_new_mysql(CONFIG=MYSQL_CONFIG)

    print(get_media(mysql,cursor))
