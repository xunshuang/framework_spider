# coding:utf-8
# 对一些事件及自定义消息的回应
from Server.api.weixin.event.Event_follow import *
from Server.api.weixin.message.Message_repeat import *
from Server.api.weixin.message.Message_help import *
from Server.api.weixin.event.Event_click import *

Map = {
    "event": {
        "SUB": {
            "subscribe": subscribe,
            "unsubscribe": unsubscribe,
        },

        "CLICK": {
            "MENU_HISTORY": MENU_HISTORY,
            "MENU_SEARCH_MACHINE": MENU_SEARCH_MACHINE,
            "MENU_NEWS": MENU_NEWS

        },  # 菜单点击事件
        "VIEW": {

        }  # 菜单视图事件
    },
    "message": {
        "repeat": repeat,
        "!help": helps,
        "！help": helps,

    }
}
