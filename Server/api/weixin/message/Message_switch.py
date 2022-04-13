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
        "订阅":sub_machine,
        "订阅状态":sub_check
    }

    try:
        return MessageFuncMap[Content](mysqlOBJ=mysqlOBJ,xmlDict=xmlDict)
    except:
        try:
            return MessageFuncMap['repeat'](mysqlOBJ=mysqlOBJ,xmlDict=xmlDict) # 报错就复读机模式
        except:

            return "指令读取失败，输入!help(不限中英文标点符号) 查看帮助菜单!" # 复读失败就发送指令集

# 查看订阅
def sub_check(*args,**kwargs):
    xmlDict = kwargs.get('xmlDict')
    mysqlOBJ = kwargs.get('mysqlOBJ')
    mysql,cursor = mysqlOBJ.get_mysql()
    SQL = 'SELECT `machineSubMachine` FROM `machineWXUser` WHERE `machineOpenId` = %s'
    try:
        cursor.execute(SQL,(xmlDict["FromUserName"]))
        mysql.commit()
    except:
        print(traceback.format_exc())
        mysql.rollback()

    check_result = cursor.fetchone()
    if str(check_result['machineSubMachine']) == '1':
        return "订阅生效中，有效期至次日凌晨0:30。"

    elif str(check_result['machineSubMachine']) == '2':
        return "订阅已失效，请重新发送【订阅】进行今日份订阅"

# 订阅
def sub_machine(*args,**kwargs):
    xmlDict = kwargs.get('xmlDict')
    mysqlOBJ = kwargs.get('mysqlOBJ')
    mysql,cursor = mysqlOBJ.get_mysql()

    FContent = xmlDict.get('Content')
    SQL_SUB_MACHINE = 'UPDATE `machineWXUser` SET `machineSubMachine` = %s WHERE `machineOpenId` = %s'
    try:
        cursor.execute(SQL_SUB_MACHINE,("1",xmlDict["FromUserName"]))
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

    return "订阅成功！有效期到次日0:30，记得续订哦！错过的消息仍然可在菜单中的今日推送中查看"


def helps(*args,**kwargs):
    help_list = """1.发送【订阅】即可接收 今日订阅推送 
2.发送【订阅状态】 查看订阅生效状态"""
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

