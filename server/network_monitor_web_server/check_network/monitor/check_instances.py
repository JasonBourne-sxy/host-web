# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     check_instances
   Description :
   Author :       'li'
   date：          2019/10/3
-------------------------------------------------
   Change Activity:
                   2019/10/3:
-------------------------------------------------
"""
import json

from config import CHECK_INSTANCES_REDIS_FLAG
from db.mysql_relevant.service.monitor_instance_service import MonitorInstancesService
from db.redis_relevant.connection_pool.redis_operate import insert_to_redis, get_fuzzy_search_keys, get_from_redis


class CheckInstances:
    """
    check instances class
    """

    @staticmethod
    def get_check_instances():
        """
        get check instances
        :return:
        """
        ping_instances, half_connection_instances = [], []
        result = MonitorInstancesService.get_all_used_check_instances()
        for instance in result:
            if '半连接' == instance['type']:
                half_connection_instances.append(instance)
            if 'ping' == instance['type']:
                ping_instances.append(instance)
        ping_items = set()
        for item in ping_instances:
            ip = item['ip']
            interval = item['interval']
            content = str(interval) + '_' + str(ip)
            ping_items.add(content)
        half_connection_items = set()
        for item in half_connection_instances:
            ip = item['ip']
            port = item['port']
            interval = item['interval']
            content = str(interval) + '_' + str(ip) + '_' + str(port)
            half_connection_items.add(content)
        return ping_items, half_connection_items

    @staticmethod
    def save_check_instances_to_redis(ping_instances,
                                      half_connection_instances):
        """
        save check instances to redis
        :param ping_instances:
        :param half_connection_instances:
        :return:
        """
        all_mapping = {}
        for ping_instance in ping_instances:
            interval, ip = ping_instance.split('_')
            key = CHECK_INSTANCES_REDIS_FLAG + '_' + str(interval) + "_" + 'PING'
            if key not in all_mapping:
                all_mapping[key] = []
            all_mapping[key].append(ip)
        for instance in half_connection_instances:
            interval, ip, port = instance.split('_')
            key = CHECK_INSTANCES_REDIS_FLAG + '_' + \
                  str(interval) + "_" + 'HALF_CONNECTION'
            if key not in all_mapping:
                all_mapping[key] = []
            value = ip + '_' + str(port)
            all_mapping[key].append(value)
        CheckInstances.__save_mapping_to_redis(all_mapping)

    @staticmethod
    def __save_mapping_to_redis(all_mapping):
        """
        save mapping to redis
        :param all_mapping:
        :return:
        """
        for key in all_mapping:
            value = all_mapping[key]
            value_str = json.dumps(value)
            insert_to_redis(key, value_str)

    @staticmethod
    def get_all_interval():
        """
        get all intervals
        :return:
        """
        re = 'CHECK_INSTANCE_*'
        keys = get_fuzzy_search_keys(re)
        intervals = set()
        for key in keys:
            interval = int(str(key).split('_')[2])
            intervals.add(interval)
        return intervals

    @staticmethod
    def get_check_interval(intervals, current_second):
        """
        get all check interval
        :param intervals:
        :param current_second:
        :return:
        """
        check_intervals = set()
        for inter in intervals:
            if current_second % inter == 0:
                check_intervals.add(inter)
        return check_intervals

    @staticmethod
    def get_to_check_instances(check_intervals):
        """
        CHECK_INSTANCE_INTERVAL_TYPE VALUE:[IP_PORT]
        get to check instances
        :param check_intervals:
        :return:
        """
        ping_instances, half_instances = [], []
        for check_interval in check_intervals:
            ping_key = """CHECK_INSTANCE_%s_PING""" % str(check_interval)
            half_key = """CHECK_INSTANCE_%s_HALF_CONNECTION""" % \
                       str(check_interval)
            ping_array = get_from_redis(ping_key)
            if ping_array is not None:
                for ping in ping_array:
                    ping_instances.append({'ip': ping})
            half_array = get_from_redis(half_key)
            if half_array is not None:
                half_instances = []
                for half in half_array:
                    ip, port = half.split('_')
                    half_instances.append({'ip': ip,
                                           'port': port,
                                           'interval': int(check_interval)})
        return ping_instances, half_instances
