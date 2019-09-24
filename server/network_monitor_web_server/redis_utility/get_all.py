# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     get_all
   Description :
   Author :       'li'
   date：          2019/9/16
-------------------------------------------------
   Change Activity:
                   2019/9/16:
-------------------------------------------------
"""
import json

from db_utility.check_result_handle import datestamp_to_datetime
from redis_utility.redis_connection_pool import REDIS_POOL

__author__ = 'li'
import redis

conn = redis.Redis(connection_pool=REDIS_POOL, decode_responses=True, encoding='utf8')
keys = conn.keys()
print(keys)
print(len(keys))
for key in keys:
    print(key)
    print(conn.get(key))
    content = json.loads(str(conn.get(key), encoding='utf8'))
    time = datestamp_to_datetime(content['receive_time'])
    print(time)
