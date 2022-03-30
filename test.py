# coding:utf-8
import pymysql
import traceback
mysql = pymysql.Connection(
                    host="127.0.0.1",
                    port=3306,
                    user="machineDb",
                    password="wSFNnx8THjyirHdG",
                    db="machinedb"
                )

cursor = mysql.cursor(cursor=pymysql.cursors.DictCursor)


sql = 'INSERT INTO `machineTest`(`letter`,`data`) VALUES (%s,%s)'



for _ in ['a','b','c','d','e','f','g','h']:
        args = [(_,i) for i in range(10000)]
        try:
            cursor.executemany(sql,args=(_,i))
            mysql.commit()
            print("存储成功")
        except:
            print(traceback.format_exc())
            mysql.rollback()


