# coding:utf-8
import pymysql
import redis
import json
import csv
import re

from Db.RedisClient.client import create_new_redis,save_url_hash,update_url_hash

class PipeLine(object):
    def __init__(self,mysqlConfig,redisConfig,csvConfig,callback_result,response,oaLog,spiderName):
        # 默认支持三种存储方式
        if mysqlConfig:
            self.mysql = mysqlConfig.get('mysql')
            self.cursor = mysqlConfig.get('cursor')
            self.mysqlConfig = mysqlConfig

        if redisConfig:
            self.redis_cli = mysqlConfig.get('redis_cli')
            self.redisConfig = redisConfig

        if csvConfig:
            self.csv = True
            self.csvConfig = csvConfig


        self.url = response.resp.url
        self.oaLog = oaLog
        self.spiderName = spiderName
        self.insert = 0 # 该爬虫单次插入量
        self.update = 0 # 该爬虫单次更新量


    def read_task_status(self,_all):
        return _all+self.insert,self.insert,self.update



    def save_to_mysql(self,data,sql_insert,sql_update,tableName):
        if sql_insert:
            self.oaLog.info(f'<save_to_mysql> 存储表名称为:[{tableName}] 存储语句为:[{sql_insert}]')
            _fail = 0

            # 默认十条一存储，降低网络 I/O 频率
            if not isinstance(data,list):
                data = [data]

            self.mysql.ping()
            for dat in data:
                args = list(dat.values())

                try:
                    self.cursor.execute(
                        query=sql_insert,args=args
                    )
                    self.mysql.commit()
                    self.insert += 1
                except pymysql.err.IntegrityError as e:
                    _id = int(re.findall("Duplicate entry '(\d+)' for key 'md5'",str(e))[0])

                    self.mysql.rollback()
                    try:
                        self.cursor.execute(
                            sql_update+ f" WHERE `md5hash` = '{_id}'", args[1:]
                        )
                        self.mysql.commit()
                        self.update += 1
                    except:
                        _fail += 1
                        self.mysql.rollback()
                except:
                    raise Exception("存储错误")

            self.oaLog.info(f'<save_to_mysql> 入库数据长度:{len(data)} '
                            f'\n\t成功入库条数:{self.insert}'
                            f'\n\t成功更新条数:{self.update}'
                            f'\n\t失败条数:{_fail}')
        else:
            self.save_to_json(data,tableName)


    def save_to_json(self,data,tableName):

        self.oaLog.info("<save_to_json> 未发现可用 存储sql 默认更改为存储json")

        _ = tableName or (self.spiderName or "data")
        if not isinstance(data,list):
            data = [data]
        with open(f'{_}.json','a+') as f:
            for dat in data:
                f.write(json.dumps(dat,ensure_ascii=False) + '\n')


        self.oaLog.info(f"<save_to_json> Json转存成功 文件名为:{_}.json")
