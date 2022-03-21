# coding:utf-8

# MachineClassSpider 的 订制设置参数

# 存储 Mysql
MYSQL_CONFIG_CUSTOMER = {
    "host" : '120.53.104.160',
    "port" : 3306,
    "user" :'machineDb',
    "password" : 'wSFNnx8THjyirHdG',

}

# 存储目标表格
MYSQL_SAVE_TABLE_CUSTOMER = ''


# 插入SQL语句
MYSQL_SAVE_SQL_CUSTOMER = ""

# 更新SQL语句
MYSQL_UPDATE_SQL_CUSTOMER = ""

# 存储 Redis
REDIS_CONFIG_CUSTOMER = {
    "host": '120.53.104.160',
    "port": 6379,
    "password": 'XunShu4ng'
}


# 过滤 Redis
REDIS_FILTER_CONFIG_CUSTOMER = {
    "host": '120.53.104.160',
    "port": 6379,
    "password": 'XunShu4ng'
}

# 需要代理 IP
NEED_PROXY_CUSTOMER = False


# 并发数
WORKER_NUMBERS_CUSTOMER = 1


# 延时数
DELAY_CUSTOMER = 1


# 任务列表长度
MAX_TASK_CUSTOMER = 1


# 日志记录位置
LOG_FILE_PATH_CUSTOMER = 'F:/爬虫专用/framework_spider/Log'