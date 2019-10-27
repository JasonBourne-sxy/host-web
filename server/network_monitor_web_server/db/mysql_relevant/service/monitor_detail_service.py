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
import time

import pymysql

from common.utility.sql_parameter_type_change import TypeChange
from common.utility.uuid_utility import get_uuid_str
from db.mysql_relevant.connection_pool.db_pool import DB_POOL
from db.mysql_relevant.sql_str.sql_str import QUERY_MONITOR_DETAIL_HALF_CONNECTION, QUERY_MONITOR_DETAIL_PING, \
    INSERT_PING_TO_MONITOR_DETAIL

__author__ = 'li'


class MonitorDetailService:
    @staticmethod
    def get_monitor_history_data(json_obj):
        """
        get monitor history data
        :param json_obj:
        :return:
        """
        ip = json_obj['ip']
        check_type = json_obj['check_type']
        port = 0
        if 'port' in json_obj:
            port = str(json_obj['port'])
        start_time = json_obj['start_time'].replace('T', ' ').split('.')[0]
        end_time = json_obj['end_time'].replace('T', ' ').split('.')[0]
        if check_type == '半连接':
            check_type = 'half_connection'
            sql = QUERY_MONITOR_DETAIL_HALF_CONNECTION % (start_time, end_time, ip, port, check_type)
        else:
            sql = QUERY_MONITOR_DETAIL_PING % (start_time, end_time, ip, check_type)
        sql = sql + ' order by start_time asc'
        print(sql)
        res = DB_POOL.select(sql)
        filter_monitor_result = MonitorDetailService.__filter_monitor_detail(res)
        return filter_monitor_result

    @staticmethod
    def save_check_result_to_detail(results):
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
                       pymysql.escape_string(TypeChange.date_stamp_to_datetime(result.start_time)),
                       pymysql.escape_string(TypeChange.date_stamp_to_datetime(result.end_time)),
                       pymysql.escape_string(str(result.interval)))
            sqls.append(sql)
        DB_POOL.execute_sql_array(sqls)

    @staticmethod
    def __filter_monitor_detail(res):
        """
        fiter monitor detail
        :param res:
        :return:
        """
        time_array = []
        check_result_array = []
        last_state = None
        total_length = len(res)
        for index, result in enumerate(res):
            check_time = str(result['start_time'])
            check_result = result['result'] == 'True'
            if check_result:
                check_result = 1
            else:
                check_result = 0
            if index == total_length - 1:
                time_array.append(check_time)
                check_result_array.append(check_result)
                return time_array, check_result_array
            if last_state is None:
                time_array.append(check_time)
                check_result_array.append(check_result)
                last_state = check_result
            else:
                if last_state != check_result:
                    time_array.append(check_time)
                    check_result_array.append(check_result)
                    last_state = check_result
        return time_array, check_result_array
