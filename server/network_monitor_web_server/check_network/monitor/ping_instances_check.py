# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     slaver_ping
   Description :
   Author :       'li'
   date：          2019/9/12
-------------------------------------------------
   Change Activity:
                   2019/9/12:
-------------------------------------------------
"""
from scapy.layers.inet import IP, ICMP
from scapy.all import *
from random import randint

from check_network.monitor.check_condition import CheckCondition
from common.log_util.log_utility import save_log_to_db
from config import SAVE_SNIFF_RESULT
from db.redis_relevant.connection_pool.redis_operate import get_from_redis

__author__ = 'li'


class PingCheck(object):
    """
    ping check
    """

    def __init__(self, ping_instances):
        """
        init
        :param ping_instances:
        """
        self.ping_instances = ping_instances
        self.send_packet = []
        self.sleep_time = 3

    def get_ping_result(self):
        """
        get ping result
        :return:
        """
        self.__send_ping()
        if len(self.ping_instances) > 0:
            time.sleep(self.sleep_time)
        return self.__get_ping_result()

    def __send_ping(self):
        """
        get ping result
        :return:
        """
        start_time = time.time()
        check_condition = []
        for instance in self.ping_instances:
            ip = instance['ip']
            ping_once(ip, check_condition)
        during = time.time() - start_time
        send_size = len(self.ping_instances)
        save_log_to_db(level='info', name='check',
                       description='发送ping 完成，发送数：'
                                   + str(send_size) + ', 耗时：' + str(during) + 's')
        self.send_packet = check_condition

    def __get_ping_result(self):
        """
        get ping result
        :return:
        """
        for package in self.send_packet:
            key = SAVE_SNIFF_RESULT + '_' + \
                  package.check_type + '_' + package.ip
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
            package.interval = int(abs(package.end_time - package.start_time) * 1000)
        return self.send_packet


def ping_once(host, check_condition):
    """
    ping method
    :param check_condition:
    :param host:
    :return:
    """
    ip_id, icmp_id, icmp_seq = randint(1, 65535), randint(1, 65535), randint(1, 65535)
    ping_packet = IP(dst=host, ttl=64, id=ip_id) / ICMP(id=icmp_id, seq=icmp_seq) / b'rootkit'
    send(ping_packet, verbose=False)
    start_time = ping_packet.sent_time
    check_result = CheckCondition('ping', ip=host, port=None, start_time=start_time)
    check_condition.append(check_result)
