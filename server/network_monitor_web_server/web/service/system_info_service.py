# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     system_info_service
   Description :
   Author :       'li'
   date：          2019/9/23
-------------------------------------------------
   Change Activity:
                   2019/9/23:
-------------------------------------------------
"""
from db_utility.db_pool import DB_POOL
from db_utility.sql_str import SELECT_SYSTEM_INFO

__author__ = 'li'


def get_system_info_tree():
    """
    get system info tree
    :return:
    """
    system_info = DB_POOL.select(SELECT_SYSTEM_INFO)
    half_connection = []
    ping = []
    for sys in system_info:
        half_connection.append({'id': sys['id'], 'name': sys['name'], 'type': '半连接'})
        ping.append({'id': sys['id'], 'name': sys['name'], 'type': 'ping'})
    return_data = {'results': {'data': [{'id': 1, 'name': '半连接', 'children': half_connection},
                                        {'id': 2, 'name': 'ping', 'children': ping}]}}
    return return_data


if __name__ == '__main__':
    get_system_info_tree()
