# coding:utf-8
# 复读机模式

def repeat(*args,**kwargs):
    FContent = kwargs.get('FContent')
    if "收到不支持" in FContent:
        return "卧槽！你这表情包我没有！"
    return FContent