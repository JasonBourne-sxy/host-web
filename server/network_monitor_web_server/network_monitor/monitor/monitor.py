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

from common.log_util.log_utility import save_log_to_db

__author__ = 'li'
from db_utility.check_result_handle import save_check_info_to_detail, update_monitor_visualization_db
from db_utility.db_pool import DB_POOL
from db_utility.sql_str import SELECT_USED_MONITOR_INSTANCE, PING_DEFAULT_INTERVAL
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
        self.timing_items = None
        self.ping_instances, self.half_connection_instances = \
            self.__get_monitor_instances()
        self.ping_instances, self.half_connection_instances = \
            self.__filter_instances()
        self.timing_task_items = self.__load_timing_task_items()

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
                content = str(ip) + '_' + str(interval)
            else:
                content = str(ip) + '_' + str(PING_DEFAULT_INTERVAL)
            ping_items.add(content)
        half_connection_items = set()
        for item in self.half_connection_instances:
            ip = item['ip']
            port = item['port']
            interval = item['interval']
            content = str(ip) + '_' + str(port) + '_' + str(interval)
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
        intervals = self.timing_task_items.keys()
        for interval in intervals:
            timer = threading.Timer(0, self.check,
                                    args=(interval,))
            timer.start()


def main():
    """

    :return:
    """
    master = Monitor()
    master.start()


if __name__ == '__main__':
    main()
