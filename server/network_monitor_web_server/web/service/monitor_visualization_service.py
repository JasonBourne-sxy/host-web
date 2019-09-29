# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     monitor_visualization_service
   Description :
   Author :       'li'
   date：          2019/9/24
-------------------------------------------------
   Change Activity:
                   2019/9/24:
-------------------------------------------------
"""

from db_utility.db_pool import DB_POOL
from db_utility.db_str.monitor_visualization import *
from db_utility.db_str.sql_str import SELECT_INSTANCE_FROM_SYS_ID, SELECT_VISUAL_FROM_CHECK_TYPE

__author__ = 'li'


class MonitorVisualizationService:
    @staticmethod
    def change_result(boole):
        """
        change result
        :param boole:
        :return:
        """
        if boole == 'True':
            return '正常'
        return '不正常'

    @staticmethod
    def format_space_time(space_time):
        """
        format space time
        :param space_time:
        :return:
        """
        if str(space_time) == 'None':
            return '超时'
        return space_time

    @staticmethod
    def get_monitor_visualization(sys_id, check_type):
        """
        get monitor visualization
        :param sys_id:
        :param check_type:
        :return:
        """
        sql = SELECT_INSTANCE_FROM_SYS_ID % sys_id
        instances = DB_POOL.select(sql)
        sql = SELECT_VISUAL_FROM_CHECK_TYPE % check_type
        visuals = DB_POOL.select(sql)
        new_result = []
        for instance in instances:
            if instance['type'] != check_type:
                continue
            for vis in visuals:
                if check_type == 'ping':
                    if instance['ip'] == vis['ip']:
                        instance['start_time'] = str(vis['start_time'])
                        instance['check_result'] = \
                            MonitorVisualizationService.change_result((vis['check_result']))
                        instance['space_time'] = \
                            MonitorVisualizationService.format_space_time(vis['interval'])
                        new_result.append(instance)
                else:
                    if instance['ip'] == vis['ip'] and instance['port'] == vis['port']:
                        instance['start_time'] = str(vis['start_time'])
                        instance['check_result'] = \
                            MonitorVisualizationService.change_result((vis['check_result']))
                        instance['space_time'] = \
                            MonitorVisualizationService.format_space_time(vis['interval'])
                        new_result.append(instance)
        return new_result

    @staticmethod
    def query_realtime_monitor_result(json_obj):
        """
        query real time monitor result
        :param json_obj:
        :return:
        """
        check_result, ip, check_type, sys_name = json_obj.get('check_result'), \
                                                 json_obj.get('ip'), \
                                                 json_obj.get('check_type'), \
                                                 json_obj.get('sys_name')
        base_sql = QUERY_REAL_TIME_MONITOR_RESULT_BASE_SQL
        if sys_name is not None and len(sys_name) > 0:
            base_sql = base_sql + "and sys_name like '%" + sys_name + "%'"
        if ip is not None and len(ip) > 0:
            base_sql = base_sql + "and ip like '%" + ip + "%'"
        if check_result is not None and len(check_result) > 0:
            base_sql = base_sql + "and check_result like '%" + check_result + "%'"
        if check_type is not None and len(check_type) > 0:
            base_sql = base_sql + "and type like '%" + check_type + "%'"
        base_sql = base_sql + 'order by sys_name ;'
        results = DB_POOL.select(base_sql)
        return MonitorVisualizationService.format_monitor_result(results)

    @staticmethod
    def format_monitor_result(results):
        """
        format monitor result
        :param results:
        :return:
        """
        for result in results:
            if 'None' == result['response_time']:
                result['response_time'] = '超时'
            if 'True' == result['check_result']:
                result['check_result'] = '正常'
            else:
                result['check_result'] = '异常'
            if result['type'] == 'ping':
                result['port'] = ' '
            result['start_time'] = str(result['start_time'])
        return results
