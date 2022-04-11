# coding:utf-8
# 对一些事件及自定义消息的回应
from Server.api.weixin.event.Event_follow import *
from Server.api.weixin.message.Message_switch import *
from Server.api.weixin.event.Event_pub_finish import *
from Server.api.weixin.event.Event_click import *

# 每一个函数必传参数
# 1.mysqlObj
# 2.xmlDict

Map = {
    "event": {
        "subscribe": subscribe, # 订阅
        "unsubscribe": unsubscribe, # 取消订阅

        "PUBLISHJOBFINISH": publish_event,  # 推送成功接收！

        "CLICK": event_key_switch,  # 菜单点击事件

        "VIEW": {

        }  # 菜单视图事件
    },
    "message": message_switch
}
