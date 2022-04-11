# coding:utf-8
# 微信公众号点击菜单事件

def event_key_switch(*args, **kwargs):
    mysqlOBJ = kwargs.get('mysqlOBJ')
    xmlDict = kwargs.get('xmlDict')
    EventKey = xmlDict.get('EventKey')
    EventFuncMap = {
        "MENU_HISTORY":MENU_HISTORY,
        "MENU_SEARCH_MACHINE":MENU_SEARCH_MACHINE,
        "MENU_NEWS":MENU_NEWS
    }
    return EventFuncMap[EventKey](mysqlOBJ=mysqlOBJ,xmlDict=xmlDict)

def MENU_HISTORY(*args, **kwargs):
    """查看往期消息"""
    return "往期消息测试"


def MENU_SEARCH_MACHINE(*args, **kwargs):
    """查看搜索符合条件的机床信息"""
    return "搜索测试"


def MENU_NEWS(*args, **kwargs):
    """查看新闻列表"""
    return "新闻测试"

