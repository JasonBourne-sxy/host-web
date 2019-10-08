# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     check_network_launch
   Description :
   Author :       'li'
   date：          2019/10/3
-------------------------------------------------
   Change Activity:
                   2019/10/3:
-------------------------------------------------
"""
from check_network.monitor.monitor import Monitor


class CheckNetworkLaunch:
    """
    launch class
    """

    def __init__(self):
        self.monitor = Monitor()

    def start_monitoring(self):
        self.monitor.start()


def main():
    monitor_launch = CheckNetworkLaunch()
    monitor_launch.start_monitoring()


if __name__ == '__main__':
    main()
