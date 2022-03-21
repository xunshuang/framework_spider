# coding:utf-8
import aiohttp
import asyncio
from types import AsyncGeneratorType,CoroutineType
import typing


async def t1():
    yield 1


async def t2():
    return 2


def t3():
    return 3


print(
    isinstance(t2(),typing.Coroutine)
)
