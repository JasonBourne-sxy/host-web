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

from config import SAVE_SNIFF_RESULT
from network_monitor.monitor.check_condition import CheckCondition
from network_monitor.monitor.executor_pool import EXECUTOR_POOL
from redis_utility.redis_operate import get_from_redis

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
        self.process_pool = EXECUTOR_POOL
        self.send_packet = []
        self.sleep_time = 5

    def get_ping_result(self):
        """
        get ping result
        :return:
        """
        self.__send_ping()
        time.sleep(self.sleep_time)
        return self.__get_ping_result()

    def __send_ping(self):
        """
        get ping result
        :return:
        """
        results = []
        for instance in self.ping_instances:
            ip = instance['ip']
            check_result = EXECUTOR_POOL.apply_async(ping_once, [ip])
            results.append(check_result)

        try:
            EXECUTOR_POOL.join()
        except Exception:
            pass
        new_result = []
        for res in results:
            new_result.append(res.get())
        self.send_packet = new_result

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


def ping_once(host):
    """
    ping method
    :param host:
    :return:
    """
    ip_id, icmp_id, icmp_seq = randint(1, 65535), randint(1, 65535), randint(1, 65535)
    ping_packet = IP(dst=host, ttl=64, id=ip_id) / ICMP(id=icmp_id, seq=icmp_seq) / b'rootkit'
    send(ping_packet, verbose=False)
    start_time = ping_packet.sent_time
    check_result = CheckCondition('ping', ip=host, port=None, start_time=start_time)
    return check_result


def main():
    a = ['14.215.177.38']
    resu = EXECUTOR_POOL.apply_async(ping_once, a)
    time.sleep(3)


if __name__ == '__main__':
    main()

    pass
