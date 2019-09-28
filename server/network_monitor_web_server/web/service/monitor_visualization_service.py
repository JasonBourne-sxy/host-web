# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     monitor_visualization_service
   Description :
   Author :       'li'
   date：          2019/9/24
-------------------------------------------------
   Change Activity:
                   2019/9/24:
-------------------------------------------------
"""

from db_utility.db_pool import DB_POOL
from db_utility.db_str.sql_str import SELECT_INSTANCE_FROM_SYS_ID, SELECT_VISUAL_FROM_CHECK_TYPE

__author__ = 'li'


def change_result(boole):
    """
    change result
    :param boole:
    :return:
    """
    if boole == 'True':
        return '正常'
    return '不正常'


def format_space_time(space_time):
    """
    format space time
    :param space_time:
    :return:
    """
    if str(space_time) == 'None':
        return '超时'
    return space_time


def get_monitor_visualization(sys_id, check_type, check_result=None):
    """
    get monitor visualization
    :param sys_id:
    :param check_type:
    :param check_result:
    :return:
    """
    if check_type == '半连接':
        new_check_type = 'half_connection'
    else:
        new_check_type = check_type
    sql = SELECT_INSTANCE_FROM_SYS_ID % sys_id
    instances = DB_POOL.select(sql)
    sql = SELECT_VISUAL_FROM_CHECK_TYPE % new_check_type
    visuals = DB_POOL.select(sql)
    new_result = []
    for instance in instances:
        if instance['type'] != check_type:
            continue
        for vis in visuals:
            if check_type == 'ping':
                if instance['ip'] == vis['ip']:
                    instance['start_time'] = str(vis['start_time'])
                    instance['check_result'] = change_result((vis['check_result']))
                    instance['space_time'] = format_space_time(vis['interval'])
                    new_result.append(instance)
            else:
                if instance['ip'] == vis['ip'] and instance['port'] == vis['port']:
                    instance['start_time'] = str(vis['start_time'])
                    instance['check_result'] = change_result((vis['check_result']))
                    instance['space_time'] = format_space_time(vis['interval'])
                    new_result.append(instance)
    return new_result


def main():
    get_monitor_visualization('675011c24208435396ee1ed460299d6c',
                              '半连接', check_result='True')


if __name__ == '__main__':
    main()
