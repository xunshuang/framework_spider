# coding:utf-8
import traceback

def message_switch(*args,**kwargs):
    mysqlOBJ = kwargs.get('mysqlOBJ')
    xmlDict = kwargs.get('xmlDict')
    Content = xmlDict.get('Content')
    MessageFuncMap = {
        "!helps":helps,
        "！helps": helps,
        "repeat":repeat
    }

    try:
        return MessageFuncMap[Content](mysqlOBJ=mysqlOBJ,xmlDict=xmlDict)
    except:
        try:
            return MessageFuncMap['repeat'](mysqlOBJ=mysqlOBJ,xmlDict=xmlDict) # 报错就复读机模式
        except:
            return "指令读取失败，输入!help(不限中英文标点符号) 查看帮助菜单!" # 复读失败就发送指令集


def helps(*args,**kwargs):
    help_list = """测试中！暂无帮助菜单！"""
    return help_list



def repeat(*args,**kwargs):
    xmlDict = kwargs.get('xmlDict')
    FContent = xmlDict.get('FContent')
    if "收到不支持" in FContent:
        return "卧槽！你这表情包我没有！"
    return FContent


def search_machine_by_publish_time(*args,**kwargs):
    mysqlOBJ = kwargs.get('mysqlOBJ')
    mysql,cursor = mysqlOBJ.get_mysql()

    FContent = kwargs.get('FContent') # 获取消息

