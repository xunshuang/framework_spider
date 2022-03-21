# coding:utf-8
import asyncio
import aiohttp
import redis
from hashlib import md5
from datetime import datetime,timedelta

def create_new_redis(CONFIG,db=0):
    if CONFIG:
        redis_pool = redis.ConnectionPool(
                    host=CONFIG.get('host'),
                    port=CONFIG.get('port'),
                    password=CONFIG.get('password'),
                    db=db,
                    decode_responses=True
                )
        redis_cli = redis.Redis(connection_pool=redis_pool)
        return redis_cli
    return None


# 不同的来源的过滤时间不同
def update_url_hash(url,db,day=0,hours=0,second=0):
    url_md5 = md5(url.encode()).hexdigest()
    redis_cli = create_new_redis(db)
    now = datetime.now()
    filter_time = timedelta(days=day,hours=hours,seconds=second)
    url_result = redis_cli.hgetall(url_md5)
    redis_cli.close()
    if url_result:
        if datetime.strptime(url_result['time'],"%Y-%m-%d %H:%M:%S") <= now - filter_time:
            return True
        else:
            return False
    else:
        return True


def save_url_hash(url,db):
    url_md5 = md5(url.encode()).hexdigest()
    redis_cli = create_new_redis(db)
    redis_cli.hset(url_md5,mapping={
        "time":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    print("存储成功")
    redis_cli.close()

if __name__ == '__main__':
    while True:
        if update_url_hash(url='https://www.baidu.com',db=0,day=0,second=50):
            save_url_hash(url='https://www.baidu.com',db=0)