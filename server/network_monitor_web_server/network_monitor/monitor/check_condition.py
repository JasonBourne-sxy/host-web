# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     check_condition
   Description :
   Author :       'li'
   date：          2019/9/16
-------------------------------------------------
   Change Activity:
                   2019/9/16:
-------------------------------------------------
"""
__author__ = 'li'


class CheckCondition(object):
    """

    """

    def __init__(self, check_type, ip, port, start_time,
                 end_time=None, is_success=None, interval=None):
        """
        init
        :param check_type:
        """
        self.interval = interval
        self.is_success = is_success
        self.end_time = end_time
        self.check_type = check_type
        self.ip = ip
        self.port = port
        self.start_time = start_time
