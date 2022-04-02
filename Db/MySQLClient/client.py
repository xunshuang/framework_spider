import aiohttp
import asyncio
import pymysql


class MYSQL():
    def __init__(self,CONFIG,db):
        self.CONFIG = CONFIG
        self.db = db
        self.mysql,self.cursor = self.create_new_mysql(CONFIG,db)

    def create_new_mysql(self,CONFIG,db='machinedb'):
        if CONFIG:
            mysql = pymysql.Connection(
                        host=CONFIG.get('host'),
                        port=CONFIG.get('port'),
                        user=CONFIG.get('user'),
                        password=CONFIG.get('password'),
                        db=db
                    )

            cursor = mysql.cursor(cursor=pymysql.cursors.DictCursor)
            mysql.ping()
            return mysql,cursor
        else:
            return None,None



    def get_mysql(self):
        try:
            self.mysql.ping()
        except:
            self.mysql, self.cursor = self.create_new_mysql(self.CONFIG, self.db)
        return self.mysql,self.cursor