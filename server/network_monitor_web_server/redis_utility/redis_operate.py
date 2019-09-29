# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     redis_operate
   Description :
   Author :       'li'
   date：          2019/9/16
-------------------------------------------------
   Change Activity:
                   2019/9/16:
-------------------------------------------------
"""
import json
from redis_utility.redis_connection_pool import REDIS_POOL

__author__ = 'li'
import redis


def insert_to_redis(key, value):
    """
    get from redis
    :param key:
    :param value:
    :return:
    """
    conn = redis.Redis(connection_pool=REDIS_POOL,
                       decode_responses=True, encoding='utf8')
    conn.set(key, value)
    conn.close()


def get_from_redis(key):
    """
    get from redis
    :param key:
    :return:
    """
    conn = redis.Redis(connection_pool=REDIS_POOL,
                       decode_responses=True, encoding='utf8')
    value = conn.get(key)
    conn.close()
    if value is None:
        return None
    json_obj = json.loads(str(value, encoding='utf8'))
    return json_obj


def get_fuzzy_search_keys(re):
    """
    get from redis
    :param re:
    :return:
    """
    conn = redis.Redis(connection_pool=REDIS_POOL,
                       decode_responses=True, encoding='utf8')
    keys = conn.keys(pattern=re)
    conn.close()
    return keys


def main():
    conn = redis.Redis(connection_pool=REDIS_POOL,
                       decode_responses=True, encoding='utf8')
    keys = conn.keys()
    for key in keys:
        value = get_from_redis(key)
        print(value)


if __name__ == '__main__':
    main()
