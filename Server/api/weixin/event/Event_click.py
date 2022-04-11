# coding:utf-8
# 微信公众号点击菜单事件
from datetime import datetime
from datetime import timedelta
from Db.MySQLClient.client import MYSQL
from Config.GlobalSetting import MYSQL_CONFIG

def event_key_switch(*args, **kwargs):
    mysqlOBJ = kwargs.get('mysqlOBJ')
    xmlDict = kwargs.get('xmlDict')
    EventKey = xmlDict.get('EventKey')
    EventFuncMap = {
        "MENU_YESTERDAY":MENU_YESTERDAY,
        "MENU_SEARCH_MACHINE":MENU_SEARCH_MACHINE,
        "MENU_NEWS":MENU_NEWS
    }
    return EventFuncMap[EventKey](mysqlOBJ=mysqlOBJ,xmlDict=xmlDict)

# 昨日发的
def MENU_YESTERDAY(*args, **kwargs):
    """查看往期消息"""
    mysqlOBJ = kwargs.get('mysqlOBJ')
    mysql,cursor = mysqlOBJ.get_mysql()
    SQL = 'SELECT `machineArticleId`,`machineTitle`,`machineUrl` ' \
          'FROM `machineWXPubArticle` WHERE ' \
          '`machinePublishTime` LIKE %s'

    cursor.execute(SQL,(datetime.now() - timedelta(days=0)).strftime("%Y-%m-%d") + "%")
    mysql.commit()
    result = cursor.fetchall()
    return result

# 今日更新
def MENU_TODAY(*args,**kwargs):
    """查看今日新增"""
    return ""

def MENU_SEARCH_MACHINE(*args, **kwargs):
    """查看搜索符合条件的机床信息"""
    return "搜索测试"


def MENU_NEWS(*args, **kwargs):
    """查看新闻列表"""
    return "新闻测试"


if __name__ == '__main__':
    mysqlOBJ = MYSQL(MYSQL_CONFIG, db='machinedb')

    print(MENU_YESTERDAY(mysqlOBJ=mysqlOBJ))