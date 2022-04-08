# coding:utf-8
# 复读机模式

def repeat(Msg):
    if "收到不支持" in Msg:
        return "卧槽！你这表情包我没有！"
    return Msg