# coding:utf-8
import os
import sys

sys.path.append('/workspace/framework_spider/')

# 全局参数 会被 订制端覆盖

# 任务读取Mysql
MYSQL_CONFIG = {
    "host" : '127.0.0.1',
    "port" : 3306,
    "user" :'machineDb',
    "password" : 'wSFNnx8THjyirHdG',

}

# 存储目标表格
MYSQL_SAVE_TABLE = ''


# 插入SQL语句
MYSQL_SAVE_SQL = ""


# 更新SQL语句
MYSQL_UPDATE_SQL = ""


# 存储 Redis
REDIS_CONFIG = {
    "host": '120.53.104.160',
    "port": 6379,
    "password": 'XunShu4ng'
}


# 过滤 Redis
REDIS_FILTER_CONFIG = {
    "host": '120.53.104.160',
    "port": 6379,
    "password": 'XunShu4ng'
}


# 并发脚本数
MAX_RUN_SCRIPT = 2

# 时延数
DELAY = 0

# 允许等待数
ALLOW_DELAY_TIME = 5

# 日志记录位置
LOG_FILE_PATH = 'F:/爬虫专用/framework_spider/Log'