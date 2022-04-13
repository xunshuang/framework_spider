# coding:utf-8
# 微信公众号点击菜单事件
from datetime import datetime
from datetime import timedelta
from Db.MySQLClient.client import MYSQL
from Config.GlobalSetting import MYSQL_CONFIG
import re
def event_key_switch(*args, **kwargs):
    mysqlOBJ = kwargs.get('mysqlOBJ')
    xmlDict = kwargs.get('xmlDict')
    EventKey = xmlDict.get('EventKey')
    EventFuncMap = {
        "MENU_SEARCH":MENU_SEARCH,
        "MENU_TODAY":MENU_TODAY,
        "MENU_SEARCH_MACHINE":MENU_SEARCH_MACHINE,
        "MENU_NEWS":MENU_NEWS
    }
    return EventFuncMap[EventKey](mysqlOBJ=mysqlOBJ,xmlDict=xmlDict)


# 地库查询！
def MENU_SEARCH(*args, **kwargs):
    """查看往期消息"""
    mysqlOBJ = kwargs.get('mysqlOBJ')
    mysql,cursor = mysqlOBJ.get_mysql()
    SQL = 'SELECT `machineArticleId`,`machineTitle`,`machineUrl` ' \
          'FROM `machineWXPubArticle` WHERE ' \
          '`machinePublishTime` LIKE %s'

    cursor.execute(SQL,(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d") + "%")
    mysql.commit()

    txt = ""
    result = cursor.fetchall()
    for res in result[0:10]:
        title = re.sub('20\d{2}-\d{2}-\d{2}\s*第\d+份','',res["machineTitle"])
        txt += f'<a href="{res["machineUrl"]}">{title}</a>' + '\n\n'
    return """
👀昨日机床推送合集👀
因字符限制只显示10条
    """ + '\n' + txt

# 今日更新
def MENU_TODAY(*args,**kwargs):
    """查看今日新增"""
    mysqlOBJ = kwargs.get('mysqlOBJ')
    mysql, cursor = mysqlOBJ.get_mysql()
    SQL = 'SELECT `machineArticleId`,`machineTitle`,`machineUrl` ' \
          'FROM `machineWXPubArticle` WHERE ' \
          '`machinePublishTime` LIKE %s'

    cursor.execute(SQL, (datetime.now() - timedelta(days=0)).strftime("%Y-%m-%d") + "%")
    mysql.commit()
    print('new!')
    txt = ""
    result = cursor.fetchall()
    for res in result[0:10]:
        title = re.sub('20\d{2}-\d{2}-\d{2}\s*第\d+份','',res["machineTitle"])
        txt += f'<a href="{res["machineUrl"]}">{title}</a>' + '\n\n'
    print(txt)
    return """
👀今日机床推送合集👀
因字符限制只显示10条
    """ + '\n' + txt

def MENU_SEARCH_MACHINE(*args, **kwargs):
    """查看搜索符合条件的机床信息"""
    return "搜索测试"


def MENU_NEWS(*args, **kwargs):
    """查看新闻列表"""
    return "新闻测试"


if __name__ == '__main__':
    mysqlOBJ = MYSQL(MYSQL_CONFIG, db='machinedb')

    print(MENU_YESTERDAY(mysqlOBJ=mysqlOBJ))