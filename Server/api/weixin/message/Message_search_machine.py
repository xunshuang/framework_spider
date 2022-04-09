# coding:utf-8
# 查询十个最新机床数据
from Config.GlobalSetting import MYSQL_CONFIG
from datetime import datetime
import random


def search_machine_by_publish_time(*args,**kwargs):
    mysqlOBJ = kwargs.get('mysqlOBJ')
    mysql,cursor = mysqlOBJ.get_mysql()

    FContent = kwargs.get('FContent') # 获取消息

