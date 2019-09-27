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
from db_utility.sql_str import SELECT_SYSTEM_INFO, QUERY_SYS_INFO

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


def query_sys_info(json_object):
    """
    query sys info
    :param json_object:
    :return:
    """
    sys_name, manager, job_number = json_object.get('sys_name'), \
                                 json_object.get('name'), \
                                 json_object.get('job_number')
    base_sql = QUERY_SYS_INFO
    if sys_name is not None and len(sys_name) > 0:
        base_sql = base_sql + "and name like '%" + sys_name + "%'"
    if manager is not None and len(manager) > 0:
        base_sql = base_sql + "and manager like '%" + manager + "%'"
    if job_number is not None and len(job_number) > 0:
        base_sql = base_sql + "and job_number like '%" + job_number + "%'"
    base_sql = base_sql + 'order by name limit 200;'
    result = DB_POOL.select(sql=base_sql)
    return result


if __name__ == '__main__':
    get_system_info_tree()
