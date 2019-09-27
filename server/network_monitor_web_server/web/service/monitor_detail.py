# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     monitor_detail
   Description :
   Author :       'li'
   date：          2019/9/24
-------------------------------------------------
   Change Activity:
                   2019/9/24:
-------------------------------------------------
"""
from db_utility.sql_str import QUERY_MONITOR_DETAIL_HALF_CONNECTION, QUERY_MONITOR_DETAIL_PING
from db_utility.db_pool import DB_POOL
__author__ = 'li'


def get_monitor_history_data(json_obj):
    """
    get monitor history data
    :param json_obj:
    :return:
    """
    ip = json_obj['ip']
    check_type = json_obj['check_type']
    port = 0
    if 'port' in json_obj['port']:
        port = str(json_obj['port'])
    start_time = json_obj['start_time']
    end_time = json_obj['end_time']
    if check_type == '半连接':
        check_type = 'half_connection'
        sql = QUERY_MONITOR_DETAIL_HALF_CONNECTION % start_time, end_time, ip, port, check_type
    else:
        sql = QUERY_MONITOR_DETAIL_PING % start_time, end_time, ip, check_type
    return DB_POOL.select(sql)
