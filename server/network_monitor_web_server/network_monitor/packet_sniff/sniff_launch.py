# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     sniff_utility
   Description :
   Author :       'li'
   date：          2019/9/16
-------------------------------------------------
   Change Activity:
                   2019/9/16:
-------------------------------------------------
"""
import json
import time

from scapy.all import sniff

from common.log_util.log_utility import save_log_to_db
from config import LOCAL_IP, SAVE_SNIFF_RESULT
from redis_utility.redis_operate import insert_to_redis, get_from_redis

__author__ = 'li'


def handle_ICMP(package):
    """

    :param package:
    :return:
    """
    src_ip = package['IP'].src
    receive_time = package.time
    check_type = 'ping'
    key = SAVE_SNIFF_RESULT + '_' + check_type + '_' + src_ip
    value = {'src_ip': src_ip, 'receive_time': receive_time,
             'check_type': check_type}
    value_str = json.dumps(value)
    insert_to_redis(key, value_str)


def handle_TCP(package):
    """
    handle tcp
    :param package:
    :return:
    """
    src_ip = package['IP'].src
    src_port = package['IP'].sport
    check_type = 'half_connection'
    receive_time = package.time
    key = SAVE_SNIFF_RESULT + '_' + check_type + '_' + src_ip + '_' + str(src_port)
    value = get_from_redis(key)
    if value is None:
        value = {'src_ip': src_ip, 'src_port': src_port, 'check_type': check_type,
                 'receive_time': receive_time}
        value_str = json.dumps(value)
        insert_to_redis(key, value_str)
    elif abs(receive_time - value['receive_time']) < 10:
        return
    value = {'src_ip': src_ip, 'src_port': src_port, 'check_type': check_type,
             'receive_time': receive_time}
    value_str = json.dumps(value)
    insert_to_redis(key, value_str)


def handle_package(package):
    """
    handle package
    :param package:
    :return:
    """
    try:
        if 'ICMP' in package:
            handle_ICMP(package)
        elif 'TCP' in package:
            handle_TCP(package)
    except Exception as e:
        save_log_to_db(level='error', name='sniff error',
                       description=str(e).replace('\'', '"'))
        print(e)
    pass


def launch_sniff():
    """

    :return:
    """
    filter_condition = 'icmp or (tcp[tcpflags]&(tcp-syn)!=0 and ' \
                       'tcp[tcpflags]&(tcp-ack)!=0)'  # + ' and dst host ' + LOCAL_IP
    print('launch sniff:' + LOCAL_IP)
    save_log_to_db(level='info', name='端口监听',
                   description='开启端口监听,本机IP :' + LOCAL_IP)
    sniff(filter=filter_condition, prn=handle_package)


if __name__ == '__main__':
    launch_sniff()
