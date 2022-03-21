import aiohttp
import asyncio
import pymysql

def create_new_mysql(CONFIG,db='machinedb'):
    if CONFIG:
        mysql = pymysql.Connection(
                    host=CONFIG.get('host'),
                    port=CONFIG.get('port'),
                    user=CONFIG.get('user'),
                    password=CONFIG.get('password'),
                    db=db
                )

        cursor = mysql.cursor(cursor=pymysql.cursors.DictCursor)
        return mysql,cursor
    else:
        return None,None



