# coding:utf-8
import asyncio
import aiohttp
import redis

from datetime import datetime,timedelta

from Db.RedisClient.client import create_new_redis
from Db.MySQLClient.client import create_new_mysql
from Config import GlobalSetting

from concurrent.futures import ThreadPoolExecutor

class Enginer(object):
    def __init__(self):
        self.redis_cli = create_new_redis(CONFIG=GlobalSetting.REDIS_CONFIG,db=0) # 0_DB
        self.mysql,self.cursor = create_new_mysql(CONFIG=GlobalSetting.MYSQL_CONFIG,db='machinedb') # mysql db

    # 获取起始任务
    def read_task(self):
        self.mysql.ping() # 先ping 一下证明存活
        self.cursor.execute(
            'SELECT * FROM `machineSite`'
        )
        task_list = self.order_task(self.cursor.fetchall())
        for _ in task_list:
            yield _


    # 给任务执行时间排序
    def order_task(self,taskList):
        taskList = sorted(taskList,key=lambda x:x['machineLastTime']) # 按照后执行时间排序，优先执行离现在时间长的
        for task in taskList[:]:
            if task["machineLastTime"] > datetime.now() - timedelta(days=task['machineT']):
                taskList.remove(task)
        return taskList

    # 读取所有待命爬虫
    def get_all_spider(self,taskMsg):
        spider_files = __import__(f'spider_files.{taskMsg["machineSpiderName"]}.{taskMsg["machineSpiderName"]}',fromlist=["start"])
        spider_files.start()

    # 派发任务
    def send_work(self,taskMsg):
        self.get_all_spider(taskMsg)

    def loop(self):
        with ThreadPoolExecutor(max_workers=GlobalSetting.MAX_RUN_SCRIPT) as exe:
            exe.map(
                self.send_work,[ _ for _ in self.read_task()]
            )

    @classmethod
    def start(cls):
        f = cls()
        f.loop()

Enginer.start()