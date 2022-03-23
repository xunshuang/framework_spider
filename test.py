# coding:utf-8


import inspect

import pymysql

mysql = pymysql.Connection(
                    host="120.53.104.160",
                    port=3306,
                    user="machineDb",
                    password="wSFNnx8THjyirHdG",
                    db="machinedb"
                )

cursor = mysql.cursor(cursor=pymysql.cursors.DictCursor)


cursor.execute('select `machineInfo` from `machineData`')

mysql.commit()

x = cursor.fetchall()

print(x[0]['machineInfo'].decode())