# coding:utf-8
import traceback
from datetime import datetime

def message_switch(*args,**kwargs):
    mysqlOBJ = kwargs.get('mysqlOBJ')
    xmlDict = kwargs.get('xmlDict')
    Content = xmlDict.get('Content')
    MessageFuncMap = {
        "!help":helps,
        "！help": helps,
        "repeat":repeat,
        "订阅":sub_machine
    }

    try:
        return MessageFuncMap[Content](mysqlOBJ=mysqlOBJ,xmlDict=xmlDict)
    except:
        try:
            return MessageFuncMap['repeat'](mysqlOBJ=mysqlOBJ,xmlDict=xmlDict) # 报错就复读机模式
        except:

            return "指令读取失败，输入!help(不限中英文标点符号) 查看帮助菜单!" # 复读失败就发送指令集


def sub_machine(*args,**kwargs):
    xmlDict = kwargs.get('xmlDict')
    mysqlOBJ = kwargs.get('mysqlOBJ')
    mysql,cursor = mysqlOBJ.get_mysql()

    FContent = xmlDict.get('Content')
    SQL_SUB_MACHINE = 'UPDATE `machineWXUser` SET `machineSubMachine` = %s'
    try:
        cursor.execute(SQL_SUB_MACHINE,"1")
        mysql.commit()
    except:
        print(traceback.format_exc())
        mysql.rollback()

        SQL_INSERT = 'INSERT INTO ' \
                     '`machineWXUser`(`machineOpenId`,`machineSubscribe`,`machineSubMachine`,`machineSubNews`,`machineSubSpecial`,' \
                     '`machineSubSpecialMSearchKey`,`machineSubSpecialNSearchKey`,`machineInsertTime`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            cursor.execute(SQL_INSERT,(xmlDict["FromUserName"],"1","1","2","2","","",datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

            mysql.commit()
        except:
            print(traceback.format_exc())

            mysql.rollback()

def helps(*args,**kwargs):
    help_list = """1.发送【订阅】即可接收 今日订阅推送 """
    return help_list



def repeat(*args,**kwargs):
    xmlDict = kwargs.get('xmlDict')
    FContent = xmlDict.get('Content')
    if "收到不支持" in FContent:
        return "卧槽！你这表情包我没有！"
    return FContent


def search_machine_by_publish_time(*args,**kwargs):
    mysqlOBJ = kwargs.get('mysqlOBJ')
    mysql,cursor = mysqlOBJ.get_mysql()

    FContent = kwargs.get('FContent') # 获取消息

