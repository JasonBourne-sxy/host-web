# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     slaver_half_connection
   Description :
   Author :       'li'
   date：          2019/9/17
-------------------------------------------------
   Change Activity:
                   2019/9/17:
-------------------------------------------------
"""
from concurrent.futures import ThreadPoolExecutor

from check_network.monitor.check_condition import CheckCondition
from common.log_util.log_utility import save_log_to_db
from config import SAVE_SNIFF_RESULT
from db.redis_relevant.connection_pool.redis_operate import get_from_redis

from scapy.layers.inet import IP, TCP
from scapy.all import *


class HalfConnectionCheck(object):
    """
    ping check
    """

    def __init__(self, half_connection):
        """
        init
        """
        self.half_connection = half_connection
        self.send_packet = []
        self.sleep_time = 3

    def get_half_connection_result(self):
        """
        get ping result
        :return:
        """
        print('start check half connection')
        self.__send_half_connection()
        if len(self.half_connection) > 0:
            time.sleep(self.sleep_time)
        return self.__get_half_connection_result()

    def __send_half_connection(self):
        """
        get ping result
        :return:
        """
        start_time = time.time()
        results = []
        for instance in self.half_connection:
            # print(instance)
            ip, port = instance['ip'], instance['port']
            send_syn(ip, port, results)
        during = time.time() - start_time
        send_size = len(self.half_connection)
        info = '发送半连接完成，发送数：' + str(send_size) + ', 耗时：' + str(during) + 's'
        print(info)
        save_log_to_db(level='info', name='check',
                       description=info)
        self.send_packet = results

    def __get_half_connection_result(self):
        """
        get ping result
        :return:
        """
        for package in self.send_packet:
            key = SAVE_SNIFF_RESULT + '_' + package.check_type + \
                  '_' + package.ip + '_' + str(package.port)
            value = get_from_redis(key)
            if value is None:
                package.is_success = False
                continue
            end_time = value['receive_time']
            cost_time = abs(end_time - package.start_time)
            if cost_time > 10:
                package.is_success = False
                continue
            package.is_success = True
            package.end_time = end_time
            package.interval = int(abs(package.end_time -
                                       package.start_time) * 1000)
        return self.send_packet


def send_syn(ip, port, results):
    """
    ping method
    :return:
    """
    package = IP(dst=ip) / TCP(dport=int(port), flags="S")
    send(package, verbose=False)
    start_time = package.sent_time
    check_result = CheckCondition('half_connection',
                                  ip=ip, port=port, start_time=start_time)
    results.append(check_result)
