# coding:utf-8
# 处理时间格式装饰器
from datetime import datetime
import time
import traceback
from aiohttp import ClientTimeout
from asyncio import TimeoutError


# 处理特殊时间格式的装饰器
def ProcessTimeFormat(func):
    async def wrapper(*args, **kwargs):
        await func(args, **kwargs)

    return wrapper
