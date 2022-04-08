# coding:utf-8
# 对一些事件及自定义消息的回应
from Server.api.weixin.event.Event_follow import *
from Server.api.weixin.message.Message_repeat import *

Map = {
    "event": {
        "subscribe": subscribe,
        "unsubscribe": unsubscribe
    },
    "message":{
        "repeat":repeat
    }
}
