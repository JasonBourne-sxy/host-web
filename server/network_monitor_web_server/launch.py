# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     launch
   Description :
   Author :       'li'
   date：          2019/9/18
-------------------------------------------------
   Change Activity:
                   2019/9/18:
-------------------------------------------------
"""
import threading
import time

from common.log_util.log_utility import save_log_to_db
from network_monitor.monitor.monitor import Monitor
from network_monitor.packet_sniff.sniff_launch import launch_sniff
from web.app import launch_web

__author__ = 'li'


def __launch_sniff():
    """
    launch sniff
    :return:
    """
    threading.Thread(target=launch_sniff).start()


def __launch_monitor():
    """
    launch monitor
    :return:
    """
    master = Monitor()
    master.start()
    save_log_to_db(level='info', name='launch', description='launch monitor')
    print('monitor started ！')


def launch():
    __launch_sniff()
    time.sleep(2)
    __launch_monitor()
    launch_web()


if __name__ == '__main__':
    launch()
