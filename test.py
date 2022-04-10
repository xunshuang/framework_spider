# coding:utf-8
import requests
from xml.etree import ElementTree
import jinja2

html = '<h1>{{ OK }}</h1>'

TEM = jinja2.Template(html)
TEM.render(OK='123')

print()