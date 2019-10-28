# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     redis_operate
   Description :
   Author :       'li'
   date：          2019/10/3
-------------------------------------------------
   Change Activity:
                   2019/10/3:
-------------------------------------------------
"""
import json
import redis

from db.redis_relevant.connection_pool.redis_connection_pool import REDIS_POOL


def insert_to_redis(key, value):
    """
    get from redis
    :param key:
    :param value:
    :return:
    """
    # conn = redis.Redis(connection_pool=REDIS_POOL,
    #                    decode_responses=True, encoding='utf8')
    # conn.set(key, value)
    # conn.close()
    pass


def get_from_redis(key):
    """
    get from redis
    :param key:
    :return:
    """
    # conn = redis.Redis(connection_pool=REDIS_POOL,
    #                    decode_responses=True, encoding='utf8')
    # value = conn.get(key)
    # conn.close()
    # if value is None:
    #     return None
    # json_obj = json.loads(str(value, encoding='utf8'))
    # return json_obj
    pass


def get_fuzzy_search_keys(re):
    """
    get from redis
    :param re:
    :return:
    """
    # conn = redis.Redis(connection_pool=REDIS_POOL,
    #                    decode_responses=True, encoding='utf8')
    # keys = conn.keys(pattern=re)
    # conn.close()
    # return keys
    pass


def delete_all_data_from_redis():
    # conn = redis.Redis(connection_pool=REDIS_POOL, decode_responses=True, encoding='utf8')
    # keys = conn.keys()
    # for key in keys:
    #     conn.delete(key)
    pass


def delete_all_instance_data_from_redis():
    """
    delete all instances data from redis
    :return:
    """
    # check_instances_key = 'CHECK_INSTANCE_*'
    # keys = get_fuzzy_search_keys(check_instances_key)
    # delete_keys(keys)
    pass


def delete_keys(keys):
    """
    delete keys
    :param keys:
    :return:
    """
    # conn = redis.Redis(connection_pool=REDIS_POOL, decode_responses=True, encoding='utf8')
    # for key in keys:
    #     conn.delete(key)
    pass


def get_all_key():
    # conn = redis.Redis(connection_pool=REDIS_POOL, decode_responses=True, encoding='utf8')
    # return conn.keys()
    pass


def main():
    keys = get_fuzzy_search_keys('*188.8.12.35_11033*')
    for key in keys:
        a = get_from_redis(key)
        print(key)
        # a['receive_time'] = TypeChange.date_stamp_to_datetime(a['receive_time'])
        print(a)
    pass


if __name__ == '__main__':
    main()
