# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     master
   Description :
   Author :       'li'
   date：          2019/9/12
-------------------------------------------------
   Change Activity:
                   2019/9/12:
-------------------------------------------------
"""
import copy
import json
import time

from common.log_util.log_utility import save_log_to_db
from network_monitor.warning_util.save_warning import save_warning_to_db
from redis_utility.get_all import delete_all_data_from_redis
from redis_utility.redis_operate import insert_to_redis, get_fuzzy_search_keys, get_from_redis

__author__ = 'li'
from db_utility.check_result_handle import save_check_info_to_detail, update_monitor_visualization_db
from db_utility.db_pool import DB_POOL, CHECK_INSTANCES_REDIS_FLAG
from db_utility.db_str.sql_str import SELECT_USED_MONITOR_INSTANCE, PING_DEFAULT_INTERVAL
from network_monitor.monitor.slaver_half_connection import HalfConnectionCheck, threading
from network_monitor.monitor.slaver_ping import PingCheck


class Monitor(object):
    """
    manager
    """

    def __init__(self):
        """
        init
        """
        delete_all_data_from_redis()
        self.timing_items = None
        self.ping_instances, self.half_connection_instances = \
            self.__get_monitor_instances()
        self.ping_instances, self.half_connection_instances = \
            self.__filter_instances()
        self.save_check_instances_to_redis()
        # self.timing_task_items = self.__load_timing_task_items()

    @staticmethod
    def __get_monitor_instances():
        """
        get monitor instances
        :return:
        """
        ping_instances = []
        half_connection_instances = []
        result = DB_POOL.select(SELECT_USED_MONITOR_INSTANCE)
        for instance in result:
            if '半连接' == instance['type']:
                half_connection_instances.append(instance)
            if 'ping' == instance['type'] or '半连接' == instance['type']:
                ping_instances.append(instance)
        return ping_instances, half_connection_instances

    @staticmethod
    def get_all_interval():
        """
        get all intervals
        :return:
        """
        re = 'CHECK_INSTANCE_*'
        keys = get_fuzzy_search_keys(re)
        intervals = []
        for key in keys:
            interval = int(str(key).split('_')[2])
            intervals.append(interval)
        return intervals

    def __filter_instances(self):
        """
        filter instances
        :return:
        """
        ping_items = set()
        for item in self.ping_instances:
            check_type = item['type']
            ip = item['ip']
            if check_type == 'ping':
                interval = item['interval']
                content = str(interval) + '_' + str(ip)
            else:
                content = str(PING_DEFAULT_INTERVAL) + '_' + str(ip)
            ping_items.add(content)
        half_connection_items = set()
        for item in self.half_connection_instances:
            ip = item['ip']
            port = item['port']
            interval = item['interval']
            content = str(interval) + '_' + str(ip) + '_' + str(port)
            half_connection_items.add(content)
        return ping_items, half_connection_items

    @staticmethod
    def check_ping(ping_items):
        """
        check ping
        :return:
        """
        print('check ping ')
        save_log_to_db(level='info', name='ping检查',
                       description='ping检查,总计检查IP数 :' +
                                   str(len(ping_items)))
        ping_check = PingCheck(ping_items)
        result = ping_check.get_ping_result()
        save_check_info_to_detail(result)
        update_monitor_visualization_db(result)
        save_warning_to_db(result)

    @staticmethod
    def check_half_connection(check_items):
        """
        check half connection
        :return:
        """
        save_log_to_db(level='info', name='半连接检查',
                       description='半连接检查,总计检查目标ip、端口个数 :' +
                                   str(len(check_items)))
        print('check_half connection')
        connection_check = HalfConnectionCheck(check_items)
        result = connection_check.get_half_connection_result()
        save_check_info_to_detail(result)
        update_monitor_visualization_db(result)
        save_warning_to_db(result)

    def __load_timing_task_items(self):
        """
        load timing task items
        :return:
        """
        total_instances = self.ping_instances | self.half_connection_instances
        timing_items = {}
        for instance in total_instances:
            items = instance.split('_')
            ip = items[0]
            if len(items) == 2:
                port = 0
                interval = items[1]
                check_type = 'ping'
            else:
                port = int(items[1])
                interval = (items[2])
                check_type = '半连接'
            item = {'ip': ip, 'port': port, 'check_type': check_type, 'interval': interval}
            interval = str(interval)
            if interval not in timing_items.keys():
                timing_items[interval] = {'ping': [], 'half_connection': []}
            if check_type == 'ping':
                timing_items[interval]['ping'].append(item)
                continue
            timing_items[interval]['half_connection'].append(item)
        self.timing_items = timing_items
        return timing_items

    def check(self, interval):
        """
        Perform ping and tcp  tasks at fixed intervals.
        :param interval:
        :return:
        """
        timing_item = self.timing_items[str(interval)]
        items = copy.deepcopy(timing_item)
        ping_instances, half_connection_instances = \
            items['ping'], items['half_connection']
        save_log_to_db(level='info', name='开启网络监控',
                       description='开启网络监控,检查间隔时间 :' +
                                   str(interval))
        if len(half_connection_instances) > 0:
            self.check_half_connection(half_connection_instances)
        if len(ping_instances) > 0:
            self.check_ping(ping_instances)
        interval = int(interval)
        timer = threading.Timer(interval, self.check,
                                args=(interval,))
        timer.start()

    def start(self):
        """
        :return:
        """
        current_second = 0
        while True:
            threading.Thread(target=self.start_check, args=(current_second,)).start()
            time.sleep(1)
            current_second = current_second + 1

    def save_check_instances_to_redis(self):
        """
        save to redis format  "KEY:CHECK_INSTANCE_INTERVAL_TYPE VALUE:[IP_PORT]"
        :return:h
        """
        all_mapping = {}
        for ping_instance in self.ping_instances:
            interval, ip = ping_instance.split('_')
            key = CHECK_INSTANCES_REDIS_FLAG + '_' + str(interval) + "_" + 'PING'
            if key not in all_mapping:
                all_mapping[key] = []
            all_mapping[key].append(ip)
        for instance in self.half_connection_instances:
            interval, ip, port = instance.split('_')
            key = CHECK_INSTANCES_REDIS_FLAG + '_' + \
                  str(interval) + "_" + 'HALF_CONNECTION'
            if key not in all_mapping:
                all_mapping[key] = []
            value = ip + '_' + str(port)
            all_mapping[key].append(value)
        self.__save_mapping_to_redis(all_mapping)

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

    def start_check(self, current_second):
        """
        check
        :param current_second:
        :return:
        """

        intervals = Monitor.get_all_interval()
        check_intervals = Monitor.get_check_interval(intervals, current_second)
        if len(check_intervals) > 0:
            print(current_second)
            Monitor.__check_instances(self, check_intervals)

    @staticmethod
    def get_check_interval(intervals, current_second):
        """
        get check interval
        :param intervals:
        :param current_second:
        :return:
        """
        check_intervals = set()
        for inter in intervals:
            if current_second % inter == 0:
                check_intervals.add(inter)
        return check_intervals

    def __check_instances(self, check_intervals):
        """
        CHECK_INSTANCE_INTERVAL_TYPE VALUE:[IP_PORT]
        get to check instances
        :param check_intervals:
        :return:
        """
        for check_interval in check_intervals:
            ping_key = """CHECK_INSTANCE_%s_PING""" % str(check_interval)
            half_key = """CHECK_INSTANCE_%s_HALF_CONNECTION""" % \
                       str(check_interval)
            ping_array = get_from_redis(ping_key)
            if ping_array is not None:
                ping_instances = []
                for ping in ping_array:
                    ping_instances.append({'ip': ping})
                self.check_ping(ping_instances)
            half_array = get_from_redis(half_key)
            if half_array is not None:
                half_instances = []
                for half in half_array:
                    ip, port = half.split('_')
                    half_instances.append({'ip': ip,
                                           'port': port,
                                           'interval': int(check_interval)})
                self.check_half_connection(half_instances)


def main():
    """

    :return:
    """
    master = Monitor()
    master.start()


if __name__ == '__main__':
    main()
