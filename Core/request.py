# coding:utf-8

import aiohttp
import asyncio
import typing
import async_timeout
from Decorator.retry import Retry
from Core.response import Response
import inspect
import time

class Request(object):
    name = 'Request'

    def __init__(self,
                 url,
                 method= "GET",
                 setting=None,
                 callback=None, encoding=None,
                 headers: dict = None,
                 meta: dict = None,
                 verify=True,
                 oaLog = None,
                 delayTime = 0,
                 allow_wait = 10,
                 request_session=None,**kwargs):
        self.url = url
        self.method = method.upper()

        self.callback = callback

        self.headers = headers or {}
        self.meta = meta
        self.client = request_session
        self.verify = verify
        self.oaLog = oaLog
        self.delayTime =  delayTime
        self.allow_wait = allow_wait

        self.aio_kwargs = kwargs

    @property
    def __create_new_session__(self):
        if not self.client:
            if not self.verify:
                conn = aiohttp.TCPConnector(verify_ssl=False)
                self.client = aiohttp.client.ClientSession(headers=self.headers,connector=conn)
            else:
                self.client = aiohttp.client.ClientSession(headers=self.headers)
        return self.client


    async def _start_requests(self):
        data = self.aio_kwargs.get('data')
        json = self.aio_kwargs.get('json')
        params = self.aio_kwargs.get('params')
        bt = time.time()
        resp = await self.client.request(self.method,self.url,data=data,json=json,params=params)
        end = time.time()
        self.oaLog.info(
            f'<_start_request> method:{self.method} url:{self.url} status:{resp.status} timeCost:{end - bt}'
        )
        return resp

    async def fetch_callback(self):
        try:
            response = await self.fetch()
            if self.callback is not None:
                if inspect.isasyncgenfunction(self.callback):
                    # 如果协程生成器
                    # callback_result = self.callback(response)
                    callback_result =  self.callback(response)

                elif inspect.iscoroutinefunction(self.callback):
                    # 如果协程函数
                    callback_result = await self.callback(response)

                else:
                    # 其他，同步函数
                    callback_result = self.callback(response)

                return callback_result,response
            else:
                return None,response
        except:
            return None,None
    @Retry
    async def fetch(self):
        self.oaLog.info('<fetch> 开始！')
        if self.delayTime:
            await asyncio.sleep(int(self.delayTime))

        async with async_timeout.timeout(delay=self.allow_wait):

            resp = await self._start_requests()

        try:
            respText = await resp.text()
        except:
            respText = str(await resp.read(),errors='replace')

        response = Response(
            method=self.method,
            resp = resp,
            respText= respText,
            meta=self.meta,
        )

        if response.request_ok:
            return response

        else:
            raise Exception('[*] 请求失败！')