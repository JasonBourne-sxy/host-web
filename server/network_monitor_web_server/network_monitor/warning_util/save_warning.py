# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     save_warning_to_db
   Description :
   Author :       'li'
   date：          2019/9/28
-------------------------------------------------
   Change Activity:
                   2019/9/28:
-------------------------------------------------
"""
from db_utility.db_pool import DB_POOL
from db_utility.db_str.sql_str import QUERY_MONITOR_INSTANCE

__author__ = 'li'


def get_monitor_instances_mapping():
    """
    get instances mapping
    :return:
    """
    mapping = {}


def save_warning_to_db(results):
    """
    save warning to db
    :param results:
    :return:
    """
    instance_mapping = get_monitor_instances_mapping()
    pass
