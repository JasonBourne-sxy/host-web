# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     delete_all
   Description :
   Author :       'li'
   date：          2019/9/20
-------------------------------------------------
   Change Activity:
                   2019/9/20:
-------------------------------------------------
"""
__author__ = 'li'
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
    print(conn.delete(key))
