# coding:utf-8
from datetime import datetime,timedelta
from Db.RedisClient.client import create_new_redis
from Config import GlobalSetting
import aiohttp
import asyncio


class IPool(object):
    def __init__(self):
        pass


