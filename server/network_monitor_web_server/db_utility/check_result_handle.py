# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     check_result_handle
   Description :
   Author :       'li'
   date：          2019/9/16
-------------------------------------------------
   Change Activity:
                   2019/9/16:
-------------------------------------------------
"""
import time

import pymysql

from common.utility.uuid_utility import get_uuid_str
from db_utility.db_pool import DB_POOL
from db_utility.sql_str import INSERT_PING_TO_MONITOR_DETAIL, \
    SELECT_MONITOR_VISUAL_BY_UNIQUE_IDENTIFY, \
    INSERT_INTO_MONITOR_VISUAL, UPDATE_MONITOR_VISUAL
from network_monitor.object_mapping.monitor_visualization import MONITOR_VISUALIZATION

__author__ = 'li'


def datestamp_to_datetime(date_stamp):
    """

    :param date_stamp:
    :return:
    """
    date_stamp = int(date_stamp)
    time_local = time.localtime(date_stamp)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return dt


def save_check_info_to_detail(results):
    """
    save check info to mysql
    :param results:
    :return:
    """
    sqls = []
    for result in results:
        if result.interval is None:
            result.interval = 0
        if result.end_time is None:
            result.end_time = time.time()
        if result.port is None:
            result.port = 0
        sql = INSERT_PING_TO_MONITOR_DETAIL. \
            format(pymysql.escape_string(get_uuid_str()),
                   pymysql.escape_string(result.ip), result.port,
                   pymysql.escape_string(result.check_type),
                   pymysql.escape_string(str(result.is_success)),
                   pymysql.escape_string(datestamp_to_datetime(result.start_time)),
                   pymysql.escape_string(datestamp_to_datetime(result.end_time)),
                   pymysql.escape_string(str(result.interval)))
        sqls.append(sql)
    DB_POOL.execute_sql_array(sqls)


def get_insert_or_update_visual(visual):
    """
    insert or update visual
    :param visual:
    :return:
    """
    sql = SELECT_MONITOR_VISUAL_BY_UNIQUE_IDENTIFY % visual.unique_identify
    count = DB_POOL.get_count(sql)
    if visual.port is None:
        visual.port = 0
    if count == 0:
        sql = INSERT_INTO_MONITOR_VISUAL % \
              (get_uuid_str(), visual.unique_identify, visual.ip, visual.port,
               visual.check_type, visual.interval,
               datestamp_to_datetime(visual.start_time),
               visual.check_result)
    else:
        sql = UPDATE_MONITOR_VISUAL % \
              (get_uuid_str(), visual.unique_identify, visual.ip, visual.port,
               visual.check_type, visual.interval,
               datestamp_to_datetime(visual.start_time),
               visual.check_result, visual.unique_identify)
    return sql


def update_monitor_visualization_db(result):
    """
    update monitor visualization
    :param result:
    :return:
    """
    sqls = []
    for item in result:
        visual = MONITOR_VISUALIZATION()
        visual.unique_identify = item.check_type + '_' + item.ip + '_' + str(item.port)
        visual.check_type = item.check_type
        visual.ip = item.ip
        visual.check_result = item.is_success
        visual.port = item.port
        visual.start_time = item.start_time
        if item.is_success:
            visual.interval = item.interval
        sql = get_insert_or_update_visual(visual)
        sqls.append(sql)
    if len(sqls) > 0:
        DB_POOL.execute_sql_array(sqls)
