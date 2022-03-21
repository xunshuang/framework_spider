# coding:utf-8
# 重试器
from datetime import datetime
import time
import traceback
from aiohttp import ClientTimeout
from asyncio import TimeoutError



# http请求重试
def Retry(func):
    async def wrapper(*args, **kwargs):
        for i in range(3):
            try:
                result = await func(args[0], **kwargs)
                return result

            except:
                import traceback
                print(traceback.format_exc())
        raise Exception("请求失败")

    return wrapper
