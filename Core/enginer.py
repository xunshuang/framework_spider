# coding:utf-8
import asyncio
import aiohttp
import redis
import time
from datetime import datetime,timedelta

from Db.RedisClient.client import create_new_redis
from Db.MySQLClient.client import MYSQL
from Core.DingTalkRobot import DingTalk
from Config import GlobalSetting
from Core.MachineMap import MachineMap
from Core.MachineMapCount import MachineMapCount

from concurrent.futures import ThreadPoolExecutor


class Enginer(object):
    def __init__(self):
        self.redis_cli = create_new_redis(CONFIG=GlobalSetting.REDIS_CONFIG,db=0) # 0_DB
        self.mysqlObject = MYSQL(CONFIG=GlobalSetting.MYSQL_CONFIG,db='machinedb')
        self.mysql,self.cursor = self.mysqlObject.get_mysql() # mysql db
        self.DingTalk = DingTalk()
        self.task_list = None
        self.status = False # 是否启动钉钉机器人发送爬取结束任务


    # 获取起始任务
    def read_task(self):
        self.mysql,self.cursor = self.mysqlObject.get_mysql()
        self.cursor.execute(
            'SELECT * FROM `machineSite`'
        )
        task_list_raw = self.cursor.fetchall()
        task_list = self.order_task(task_list_raw)
        self.task_list = task_list
        if task_list:
            crawlerText = ""
            crawlerText += f"**爬虫框架总任务数为:{len(task_list_raw)}个**\n"
            crawlerText += f"**待执行总任务数为:{len(task_list)}个**\n"
            crawlerText += "\n\n".join([ f"--> 爬虫名称:【{_['machineSpiderName']}】\n--> 目标网站名称:【{_['machineSiteName']}】" for _ in task_list])
            self.DingTalk.send("15566528051", f"\n{crawlerText}")
            self.status = True

            for _ in task_list:
                yield _
        else:
            time.sleep(60) # 默认60秒扫描一次任务表
            yield

    # 给任务执行时间排序
    def order_task(self,taskList):
        taskList = sorted(taskList,key=lambda x:x['machineLastTime']) # 按照后执行时间排序，优先执行离现在时间长的
        for task in taskList[:]:
            try:
                if task["machineLastTime"] > datetime.now() - timedelta(days=task['machineT']):
                    taskList.remove(task)
            except:
                pass
        return taskList

    # 单轮任务结束后，发送钉钉预警单
    def send_ding_msg(self):
        msg = "👻本轮任务爬取结果统计👻\n"

        sql = 'SELECT * FROM `machineSite` WHERE `machineSiteId` = "%s";'
        args = [ (_["machineSiteId"],) for _ in self.task_list]
        results = []
        for arg in args:
            s = sql %(arg[0])
            self.cursor.execute(s)

            self.mysql.commit()
            results.append(self.cursor.fetchall()[0])

        for res in results:
            msg += f"总量:{res['machineAllDataSum'] or 0}\n" \
                   f"新增:{res['machineInsertDataSum'] or 0}\n" \
                   f"更新:{res['machineUpdateDataSum'] or 0}\n" \
                   f"爬虫名称:【{res['machineSpiderName']}】\n" \
                   f"目标网站:【{res['machineSiteName']}】\n" \
                   f"耗时:【{res['machineCostTime'] or 0}】\n\n"

        self.DingTalk.send("15566528051", f"\n{msg}")

    # 读取所有待命爬虫
    def get_all_spider(self,taskMsg):
        spider_files = __import__(f'spider_files.{taskMsg["machineSpiderName"]}.{taskMsg["machineSpiderName"]}',fromlist=["start"])
        try:
            spider_files.start()
        except:
            pass
        finally:
            if str(taskMsg['machineSiteType']) == '1':
                x = MachineMap()
                x.init_spider_name(spiderSiteId=taskMsg["machineSiteId"]) # 更新 类别字典
                x.make_machine_map()

                o = MachineMapCount()
                o.init_spider_name(spiderSiteId=taskMsg["machineSiteId"]) # 更新 类别统计数
                o.read_machine_map()

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
        if f.status:
            f.send_ding_msg()

if __name__ == '__main__':
    Enginer.start()