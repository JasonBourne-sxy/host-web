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


def delete_all_data_from_redis():
    conn = redis.Redis(connection_pool=REDIS_POOL, decode_responses=True, encoding='utf8')
    keys = conn.keys()
    for key in keys:
        conn.delete(key)


if __name__ == '__main__':
    delete_all_data_from_redis()
