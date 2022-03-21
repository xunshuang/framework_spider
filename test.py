# coding:utf-8


import inspect


def f():
    return [1, 2, 3]


a = 1
b = 2
c = 3


x = list(map(lambda x:x[0]+x[1],f()))

print(x)

