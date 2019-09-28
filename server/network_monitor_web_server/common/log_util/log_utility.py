# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     log_utility
   Description :
   Author :       'li'
   date：          2019/9/20
-------------------------------------------------
   Change Activity:
                   2019/9/20:
-------------------------------------------------
"""
import time

from common.utility.uuid_utility import get_uuid_str
from db_utility.check_result_handle import datestamp_to_datetime

from db_utility.db_pool import DB_POOL
from db_utility.db_str.sql_str import INSERT_LOG

__author__ = 'li'


def save_log_to_db(level, name, description):
    """
    insert log
    :param level:
    :param name:
    :param description:
    :return:
    """

    date_time = datestamp_to_datetime(time.time())
    log_id = get_uuid_str()
    sql = INSERT_LOG % (log_id, level, date_time, name, description)
    DB_POOL.execute_sql_str(sql)


if __name__ == '__main__':
    save_log_to_db(level='info', name='test', description='launch sniff')
