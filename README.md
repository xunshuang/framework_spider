# framework_spider
一个私人的机床爬虫框架

# Config
    ## GlobalSetting 一些全局设置，会被局部设置覆盖，包含一些 mysql,redis,日志存储位置的信息。
    ## ReplaceTxt 对一些数据源进行脱敏处理
    ## SpiderData 机床信息数据模板
    ## SpiderNews 机床新闻数据模板
    

# Core
    ## CityParser 对地名进行一些标准化处理
    ## DingTalkRobot 钉钉机器人
    ## enginer 负责大项任务调度（数据源之间切换 A网站爬完换B网站，根据每个网站预设的爬取频率分发任务）及任务完成情况统计
    ## ipool ip池（待完善）
    ## MachineMap 机床种类处理（二手机床-车床-等等）
    ## MachineMapCount 在每次爬虫结束后 统计Map 每个小支类的数据数量
    ## pipeline 类似阉割版 scrapy的pipeline,保存数据用
    ## request 对 请求做了封装
    ## response 对 响应做了封装
    ## spider 类似scrapy里的引擎。负责单个网站下的任务调度。
    
# Db
    ## 对 redis,mysql做了封装
    

# Decorator
    ## 一些重试装饰器


# Hook
    ## 暂未启用
    
 
# Log
    ## 日志按小时分块存储
    
    
# other_script
    ## 一些涉及到微信公众号 token校验，定时更新，用户订阅等等的一些定时操作 linux定时
    
 

    
# Server包
    ## 不是后端出身，写的比较幼稚…… 见笑了
    ## api Api包主要是一些算法实现
    ## bluePrint 主要是一些 接口
    ## templates 主要是一些 模板
    


# spider_files
    ## 爬虫文件合集
    
 
# CrawlerGo
    ## 一键启动
    
# kill_python
    ## 杀掉进程

