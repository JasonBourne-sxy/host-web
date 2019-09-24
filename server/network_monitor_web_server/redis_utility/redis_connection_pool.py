# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     redis_connection_pool
   Description :
   Author :       'li'
   date：          2019/9/16
-------------------------------------------------
   Change Activity:
                   2019/9/16:
-------------------------------------------------
"""
from config import REDIS_PORT, REDIS_HOST

__author__ = 'li'
import redis

# 拿到一个redis的连接池
REDIS_POOL = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, max_connections=10)

# # 从池子中拿一个链接
# conn = redis.Redis(connection_pool=pool, decode_responses=True, encoding='utf8')
