# coding=utf-8
"""
-------------------------------------------------
   File Name：     insert_sys_info_to_db
   Description :
   Author :       'li'
   date：          2019/9/11
-------------------------------------------------
   Change Activity:
                   2019/9/11:
-------------------------------------------------
"""
from network_monitor.object_mapping.monitor_instance import MONITOR_INSTANCE

__author__ = 'li'
from common.utility.file_path_utility import combine_file_path
from common.utility.uuid_utility import get_uuid_str
from db_utility.db_pool import DB_POOL
from db_utility.sql_str import INSERT_MONITOR_INSTANCE

import csv


def get_monitor_instance(row):
    """
    row
    :param row:
    :return:
    """
    ips = row[2]
    ports = row[3]
    first, second, threed, lasts = ips.split('.')
    instances = []
    if '/' in lasts:
        lasts = lasts.split('/')
    else:
        lasts = [lasts]
    for last in lasts:
        ip = first + '.' + second + '.' + threed + '.' + last
        if ports == '':
            instance = MONITOR_INSTANCE()
            instance.ip = ip
            instance.sys_name = row[0]
            instance.description = row[1]
            instances.append(instance)
            continue
        if '/' in ports:
            ports = ports.split('/')
        elif 'str' in str(type(ports)):
            ports = [ports]
        for port in ports:
            instance = MONITOR_INSTANCE()
            instance.ip = ip
            instance.sys_name = row[0]
            instance.description = row[1]
            instance.port = port
            instances.append(instance)
    return instances


def get_sys_infos():
    """
    get sys info
    :return:
    """
    file_name = combine_file_path('data_conversion/csv_to_db/fff.csv')
    all_items = []
    with open(file_name, mode='r', encoding='utf8')as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            items = get_monitor_instance(row)
            all_items = all_items + items
    return all_items


def insert_sys_infos(instances):
    """
    :param instances:
    :return:
    """
    sqls = []
    for info in instances:
        if info.port != '' and info.port is not None:
            port = int(info.port)
        else:
            port = 0
        value = (get_uuid_str(), info.sys_name, info.description,
                 info.ip, port)
        sql = INSERT_MONITOR_INSTANCE % value
        sqls = sqls.append(sql)
    DB_POOL.execute_sql_array(sqls)


def main():
    instances = get_sys_infos()
    insert_sys_infos(instances)
    pass


if __name__ == '__main__':
    main()
