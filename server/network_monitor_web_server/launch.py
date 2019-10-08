# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     launch
   Description :
   Author :       'li'
   date：          2019/10/4
-------------------------------------------------
   Change Activity:
                   2019/10/4:
-------------------------------------------------
"""
import threading
import time

from check_network.monitor.monitor import Monitor, MASTER_MONITOR
from check_network.packet_sniff.sniff_launch import launch_sniff
from common.log_util.log_utility import save_log_to_db
from web.web_launch import launch_web


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
    save_log_to_db(level='info', name='launch', description='launch monitor')
    print('monitor started ！')
    MASTER_MONITOR.start()


def launch():
    __launch_sniff()  # launch receive packet
    time.sleep(2)
    threading.Thread(target=launch_web).start()
    __launch_monitor()


if __name__ == '__main__':
    launch()
