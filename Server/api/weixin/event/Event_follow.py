# coding:utf-8
from Db.MySQLClient.client import MYSQL
from Config.GlobalSetting import MYSQL_CONFIG
from datetime import datetime
import random

# 有人关注 加到粉丝列表内
def subscribe(*args,**kwargs):
    msgList = [
        '欢迎回到酒馆！',
        '你想来瓶酒吗？',
        '以前看小说总羡慕某某主角有个系统，从此人生像开了挂一样一帆风顺，现在这个系统摆在你眼前了！',
        '我不但能够查机床，我还能查新闻',
        '我不但能够查新闻，我还能查机床',
        '感谢关注！老板大气！老板身体健康！',
        '感谢关注！老板买菜不涨价！',
        '感谢关注！老板喝水不塞牙！',
        '感谢关注！老板吃肉不长胖！',
        '感谢关注！老板一胎三个娃！'
    ]
    mysqlOBJ = kwargs.get('mysqlOBJ')
    xmlDict = kwargs.get('xmlDict')

    FFromUserName=xmlDict.get('FromUserName') # openID

    mysql, cursor = mysqlOBJ.get_mysql()
    SQL_SUB_SEARCH = 'SELECT * FROM `machineWXUser` WHERE `machineOpenId` = %s'

    SQL_SUB_INSERT = 'INSERT INTO ' \
              '`machineWXUser`(`machineOpenId`,`machineSubscribe`,`machineInsertTime`) ' \
              'VALUES (%s,%s,%s)'

    SQL_SUB_UPDATE = 'UPDATE `machineWXUser` SET `machineSubscribe` = %s WHERE `machineOpenId` = %s'

    cursor.execute(SQL_SUB_SEARCH,FFromUserName)
    mysql.commit()
    if cursor.fetchone():
        cursor.execute(SQL_SUB_UPDATE,("1",FFromUserName))

        mysql.commit()
        return "嘿！老朋友！" + random.choice(msgList) + '\n输入【!help】查看帮助指令' + '\n更多精彩请移步【http://www.surefly.top】获取更多新闻'

    else:
        cursor.execute(SQL_SUB_INSERT,(FFromUserName,"1",datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        mysql.commit()
        return '嘿！新朋友！'+ random.choice(msgList) + '\n输入【!help】查看帮助指令' +'\n更多精彩请移步【http://www.surefly.top】获取更多新闻'

# 取消关注 从粉丝表内删掉  逻辑删除
def unsubscribe(*args,**kwargs):
    mysqlOBJ = kwargs.get('mysqlOBJ')
    xmlDict = kwargs.get('xmlDict')

    FFromUserName=xmlDict.get('FFromUserName') # openID
    mysql, cursor = mysqlOBJ.get_mysql()

    SQL_DELETE = 'UPDATE `machineWXUser` SET `machineSubscribe` = %s WHERE `machineOpenId` = %s'
    cursor.execute(SQL_DELETE,('2',FFromUserName))
    mysql.commit()
    return 'Good Bye!'