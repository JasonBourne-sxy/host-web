# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     redis_connection_pool
   Description :
   Author :       'li'
   date：          2019/10/3
-------------------------------------------------
   Change Activity:
                   2019/10/3:
-------------------------------------------------
"""
__author__ = 'li'
from config import REDIS_PORT, REDIS_HOST

import redis

REDIS_POOL = redis.ConnectionPool(host=REDIS_HOST,
                                  port=REDIS_PORT,
                                  max_connections=10)
