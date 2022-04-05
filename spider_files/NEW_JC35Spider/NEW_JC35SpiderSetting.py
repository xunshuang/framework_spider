# coding:utf-8

# AJSpider 的 订制设置参数

# 存储 Mysql
MYSQL_CONFIG_CUSTOMER = {}

# 存储目标表格
MYSQL_SAVE_TABLE_CUSTOMER = 'machineNews'

# 插入SQL语句
MYSQL_SAVE_SQL_CUSTOMER = """INSERT INTO `machineNews`(
`machineSiteId`,
`md5hash`,
`machineSource`,
`machineRealSource`,
`machineTitleHash`,
`machineTitle`,
`machineAuthor`,
`machineImg`,
`machineKeywords`,
`machineDescription`,
`machineContent`,
`machinePublishTime`,
`machineInsertTime`
) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""



# 更新SQL语句
MYSQL_UPDATE_SQL_CUSTOMER = """UPDATE `machineNews`
SET `machineSource` = %s,
`machineRealSource` = %s,
`machineTitleHash` = %s,
`machineTitle` = %s,
`machineAuthor` = %s,
`machineImg` = %s,
`machineKeywords` = %s,
`machineDescription` = %s,
`machineContent` = %s,
`machinePublishTime` = %s,
`machineInsertTime` = %s WHERE `md5hash` = %s"""

# 存储 Redis
REDIS_CONFIG_CUSTOMER = {

}

# 过滤 Redis
REDIS_FILTER_CONFIG_CUSTOMER = {

}

# 并发数
WORKER_NUMBERS_CUSTOMER =2

# 延时数
DELAY_CUSTOMER = 0

# 请求允许等待时间
ALLOW_DELAY_TIME_CUSTOMER = 10

# 任务列表长度
MAX_TASK_CUSTOMER = 10

# 日志记录位置
# LOG_FILE_PATH_CUSTOMER = 'F:/爬虫专用/framework_spider/Log'
LOG_FILE_PATH_CUSTOMER = ''