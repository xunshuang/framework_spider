# coding:utf-8
import pymysql
import traceback
mysql = pymysql.Connection(
                    host="120.53.104.160",
                    port=3306,
                    user="machineDb",
                    password="wSFNnx8THjyirHdG",
                    db="machinedb"
                )

cursor = mysql.cursor(cursor=pymysql.cursors.DictCursor)


sql = 'INSERT INTO `machineTest`(`hash1`,`data`) VALUES (%s,%s)'


for i in range(10):
    try:
        cursor.execute(sql,args=('c','asd'))
        mysql.commit()
    except:
        print(traceback.format_exc())
        mysql.rollback()
        sql2 = 'alter table machineTest auto_increment=2;'
        cursor.execute(sql2)
        mysql.commit()

