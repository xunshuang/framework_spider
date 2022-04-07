# coding:utf-8
from Db.MySQLClient.client import MYSQL
from Config.GlobalSetting import MYSQL_CONFIG

mysqlOBJ = MYSQL(CONFIG=MYSQL_CONFIG, db='machinedb')  # 该视图的专用mysql对象

mysql,cursor = mysqlOBJ.get_mysql()
count = 0

while True:
    sql = 'SELECT `machineTitle`,`machineLevelOne`,`machineLevelTwo`,`machineLevelThree` FROM `machineData` LIMIT %s,10000'

    cursor.execute(sql,count)
    mysql.commit()

    result = cursor.fetchall()
    print(result[0]['machineLevelOne'],result[0]['machineTitle'])
    if result:
        count += 10000
    else:
        break
