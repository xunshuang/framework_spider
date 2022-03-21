# coding:utf-8
import parsel
import re

class Response():
    def __init__(self,method,resp,respText,meta):
        self._method = method
        self._resp = resp
        self._respText = respText
        self._status = resp.status == 0 or 200<=resp.status<=299
        self._meta = meta


    @property
    def request_ok(self):
        if self._status:
            return True
        else:
            return False

    @property
    def meta(self):
        return self._meta


    @property
    def xpath(self):
        return parsel.Selector(self._respText).xpath


    @property
    def re(self):
        return parsel.Selector(self._respText).re


    @property
    def respText(self):
        return self._respText


    @property
    def resp(self):
        return self._resp


    async def json(self):
        return await self._resp.json()


    async def read(self):
        return await self._resp.content()


    def __repr__(self):
        return f'<Response url[{self._method}]: {self._resp.url} status: {self._status}>'