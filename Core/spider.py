# coding:utf-8
import aiohttp
import asyncio
import typing
from aiohttp.client import ClientSession
from types import AsyncGeneratorType,CoroutineType

from Core.request import *
from Core.pipeline import PipeLine
from Core.CityParser import CityParser
from Db.MySQLClient.client import create_new_mysql
from Db.RedisClient.client import create_new_redis
from Config import GlobalSetting
from datetime import datetime
import logging
import traceback
import os

class Spider(object):
    spider_name = None # 爬虫名称
    start_urls: list = None # 起始url
    headers = {} # headers

    setting = None # 客服端设置
    setting_global = GlobalSetting # 全局参数
    meta = None # meta
    sql_insert = None # 待执行存储sql语句
    sql_update = None # 待执行更新sql语句
    sql_table = None # sql表
    log_path = None # log存储位置
    data_type = 0 # 数据类别 0:机床数据 1:机床公司数据 2:机床公司舆情 3:行业热点新闻

    def __init__(self,loop):
        self.headers = self.headers or {} # headers
        self.request_session = ClientSession() # 初始化session
        self.aio_queue = asyncio.queues.LifoQueue(0) # 初始化消息队列
        self.meta = self.meta or {} # meta
        self.mysql_config = None # mysql_config
        self.redis_config = None # redis_config
        self.redis_filter_config = None # redis_过滤
        self.spider_name = self.spider_name or None
        self.read_setting()
        self.pipeline = PipeLine
        self.mysql,self.cursor = self._create_mysql_()
        self.redis_cli = self._create_mysql_()
        self.oaLog = self.init_logger
        self.loop = loop
        self.worker_tasks = []
        self._check_sql_available()

        self.start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 程序开始时间
        self.end_time = None # 程序结束时间
        self.all = 0 # 该爬虫信源总量
        self.insert = 0 # 该爬虫单次插入量
        self.update = 0 # 该爬虫单次更新量
        self._id = None # site id
        self._get_task_status()

        self.CityParser = CityParser()

    def _get_task_status(self):
        if self.spider_name and self.sql_insert:
            SQL = 'SELECT ' \
                  '`id`,' \
                  '`machineAllDataSum`' \
                  f'FROM `machineSite` WHERE `machineSpiderName` = "{self.spider_name}"'

            self.oaLog.info("<_get_task_status> 读取任务状态")

            self.cursor.execute(SQL)
            self.mysql.commit()
            task_info = self.cursor.fetchall()
            if task_info:
                self.all = self.all or (task_info[0].get('machineAllDataSum') or 0)

                self._id = task_info[0].get('id')
            else:
                self.oaLog.warning("<_get_task_status> 未获取到任务信息,请将其添加到任务表格中")

    def _change_task_status(self):
        if self.sql_insert:
            costTime = (datetime.strptime(self.end_time,"%Y-%m-%d %H:%M:%S") -
                        datetime.strptime(self.start_time,"%Y-%m-%d %H:%M:%S")).total_seconds()
            self.oaLog.info("<_get_task_status> 读取任务状态成功")
            SQL_U = 'UPDATE `machineSite` SET `machineAllDataSum`= "%s",' \
                    '`machineInsertDataSum`= "%s",' \
                    '`machineUpdateDataSum`= "%s",' \
                    '`machineLastTime`= "%s",' \
                    '`machineCancelTime`= "%s",' \
                    '`machineCostTime`= "%s" ' \
                    'WHERE `id` = "%s"' %(
                self.all,self.insert,self.update,self.start_time,self.end_time,int(costTime),self._id
            )

            try:
                self.cursor.execute(SQL_U)
                self.mysql.commit()
                self.oaLog.info("<_get_task_status> 更改任务状态成功")

            except:
                self.mysql.rollback()
                self.oaLog.info("<_get_task_status> 更改任务状态失败")




    def _check_sql_available(self):
        self.oaLog.info('<_check_sql_available> 检查 SQL设置 可用性')
        self.sql_insert = self.sql_insert or self.setting.MYSQL_SAVE_SQL_CUSTOMER
        if not self.sql_insert:
            self.oaLog.warning('<_check_sql_available> <存储> SQL 语句 Setting读取异常 切换到全局 Setting!')

            self.sql_insert = self.setting_global.MYSQL_SAVE_SQL
            if not self.sql_insert:

                self.oaLog.error('<_check_sql_available> <存储> SQL 语句 全局 Setting读取异常!')
                self.oaLog.error('<_check_sql_available> <存储> 未读取到可用存储语句 默认存储JSON')

        self.sql_update = self.sql_update or self.setting.MYSQL_UPDATE_SQL_CUSTOMER
        if not self.sql_update:
            self.oaLog.warning('<_check_sql_available> <更新> SQL 语句 Setting读取异常 切换到全局 Setting!')

            self.sql_update = self.setting_global.MYSQL_UPDATE_SQL
            if not self.sql_update:

                self.oaLog.error('<_check_sql_available> <更新> SQL 语句 全局 Setting读取异常! 未设置更新 SQL')


        self.sql_table = self.sql_table or self.setting.MYSQL_SAVE_TABLE_CUSTOMER
        if not self.sql_table:
            self.oaLog.warning('<_check_sql_available> SQL 表名 Setting读取异常 切换到全局 Setting!')

            self.sql_table = self.setting_global.MYSQL_SAVE_TABLE
            if not self.sql_table:
                self.oaLog.error('<_check_sql_available> SQL 表名 全局 Setting读取异常!')

    def _create_mysql_(self):
        if self.setting and self.mysql_config:
            return create_new_mysql(CONFIG=self.mysql_config)

    def _create_redis_(self):
        if self.setting and self.redis_config:
            return create_new_redis(CONFIG=self.redis_config)


    def read_setting(self):
        if self.setting:
            try:
                self.mysql_config = self.setting.MYSQL_CONFIG_CUSTOMER or self.setting_global.MYSQL_CONFIG # 初始化 mysql config
                self.redis_config = self.setting.REDIS_CONFIG_CUSTOMER or self.setting_global.REDIS_CONFIG # 初始化 redis config
                self.redis_filter_config = self.setting.REDIS_FILTER_CONFIG_CUSTOMER or self.setting_global.REDIS_FILTER_CONFIG # 初始化过滤redis config
                self.worker_numbers = self.setting.WORKER_NUMBERS_CUSTOMER or self.setting_global.WORKER_NUMBERS
                self.max_task = self.setting.MAX_TASK_CUSTOMER or self.setting_global.MAX_TASK
                self.log_path = self.log_path or (self.setting.LOG_FILE_PATH_CUSTOMER or self.setting_global.LOG_FILE_PATH)

            except:
                self.oaLog.error(
                    "<read_setting> 未设置客户端 或者 全局 setting"
                )

    def get_logger(self,name, fileName=None, level=logging.INFO):
        logging_format = f"[%(asctime)s] %(levelname)-5s %(name)-{len(name)}s "
        logging_format += "%(message)s"
        fileName = self.classification_by_time(fileName,name)

        logging.basicConfig(
            filename=fileName, filemode='a',
            format=logging_format, level=level, datefmt="%Y:%m:%d %H:%M:%S"
        )
        return logging.getLogger(name)

    def classification_by_time(self,fileName,name):
        now = datetime.now().strftime('%Y-%m-%d %H')
        if not os.path.exists(self.log_path + f'/{now}'):
            os.mkdir(self.log_path + f'/{now}')
        return f'{fileName}'+ f'/{now}/' + name + '.log'


    @property
    def init_logger(self): # 初始化一个logger
        if  self.log_path: # 有可存储位置 则做log存储
            return self.get_logger(name=self.spider_name or "FrameSpider",fileName=self.log_path)
        else: # 未指定存储位置的 控制台输出
            return self.get_logger(name=self.spider_name or "FrameSpider")

    def request(
        self,
        url: str,
        method: str = "GET",
        *,
        callback=None,
        encoding: typing.Optional[str] = None,
        headers: dict = None,
        meta: dict = None,
        custom_settings: dict = None,
        request_session=None,
        **aiohttp_kwargs,
    ):
        """初始化一个Request类"""
        headers = headers or (self.headers or {})
        meta = meta or {}
        custom_settings = custom_settings or {}
        request_session = request_session or self.request_session

        headers.update(self.headers.copy())

        return Request(
            url=url,
            method=method,
            setting = self.setting,
            callback=callback,
            oaLog=self.oaLog,
            delayTime=self.setting.DELAY_CUSTOMER or self.setting_global.DELAY,
            allow_wait=self.setting.ALLOW_DELAY_TIME_CUSTOMER or self.setting_global.ALLOW_DELAY_TIME,
            encoding=encoding,
            headers=headers,
            meta=meta,
            custom_settings=custom_settings,
            request_session=request_session,
            **aiohttp_kwargs,
        )

    async def parse(self,response):
        pass

    async def start_requests(self):
        """
        :return: 一个异步的生成器
        """
        for url in self.start_urls:
            yield self.request(url=url, callback=self.parse, meta=self.meta)




    async def handle_request(self,request:Request):
        callback_result,response = None,None
        try:
            callback_result,response = await request.fetch_callback()

        except:
            pass

        return callback_result, response

    async def handle_callback(self,callback_,response):
        callback_result = None
        try:
            callback_result = await callback_
        except Exception as e:
            self.oaLog.error(
                f"handle_callback {str(e).lower()}"
            )
            self.oaLog.error(
                f"{traceback.format_exc()}"
            )

        return callback_result,response

    async def dispatch_slaver(self):
        worker_task = []
        while True:
            request_item = await self.aio_queue.get()
            # self.worker_tasks.append(request_item)
            worker_task.append(request_item)
            if self.aio_queue.empty() or len(worker_task) >= self.max_task:
                results = await asyncio.gather(
                    *worker_task, return_exceptions=True
                )
                for task_result in results:
                    if not isinstance(task_result, RuntimeError) and task_result:
                        callback_results, response = task_result
                        if isinstance(callback_results, AsyncGeneratorType):
                            await self.process_results(
                                callback_results, response
                            )

                worker_task = []
            print(self.aio_queue.qsize())
            self.aio_queue.task_done()


    async def save_data(self):
        return ""



    async def process_results(self,callback_results:AsyncGeneratorType,response:Response=None):

        async for callback_result in callback_results:
            if isinstance(callback_result,dict):
                pipeline = self.pipeline(
                    mysqlConfig={
                        "mysql":self.mysql,
                        "cursor":self.cursor
                    },redisConfig={

                    },csvConfig={
                        "redis_cli":self.redis_config
                    },callback_result=callback_result,
                    response=response,
                    oaLog = self.oaLog,
                    spiderName = self.spider_name
                )
                pipeline.save_to_mysql(data=callback_result,sql_insert=self.sql_insert,sql_update = self.sql_update,tableName=self.sql_table)
                self.all, self.insert, self.update = pipeline.read_task_status(self.all)

            elif isinstance(callback_result,list):
                pipeline = self.pipeline(
                    mysqlConfig={
                        "mysql": self.mysql,
                        "cursor": self.cursor
                    }, redisConfig={

                    }, csvConfig={
                        "redis_cli": self.redis_config
                    }, callback_result=callback_result,
                    response=response,
                    oaLog=self.oaLog,
                    spiderName=self.spider_name

                )
                pipeline.save_to_mysql(data=callback_result,sql_insert=self.sql_insert,sql_update = self.sql_update,tableName=self.sql_table)
                self.all, self.insert, self.update = pipeline.read_task_status(self.all)
            elif isinstance(callback_result,AsyncGeneratorType):
                await self.process_results(callback_result,response)

            elif isinstance(callback_result,Request):
                self.aio_queue.put_nowait(self.handle_request(request=callback_result))

            elif isinstance(callback_result,typing.Coroutine):
                self.aio_queue.put_nowait(self.handle_callback(callback_=callback_result,response=response))

    async def start_master(self):
        """
        开始爬取
        :return:
        """
        async for _request in self.start_requests():
            self.aio_queue.put_nowait(self.handle_request(_request))

        workers = [
            asyncio.ensure_future(self.dispatch_slaver())
            for i in range(self.worker_numbers)
        ]
        self.oaLog.info(f'<start_master> 开始爬取！')

        for work in workers:
            self.oaLog.info(f'ensure_future 开始工作,内存Id 为:{id(work)}')
        await self.aio_queue.join()
        self.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self._change_task_status()


    @classmethod
    def start(cls,loop=None):
        loop = loop or asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        spider = cls(loop=loop)
        spider.loop.run_until_complete(
            spider.start_master()
        )
        spider.oaLog.info(f'<{spider.spider_name or "无敌智能采集平台"}> 爬取结束')