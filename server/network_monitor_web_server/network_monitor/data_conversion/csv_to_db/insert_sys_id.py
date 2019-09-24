# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     insert_sys_id
   Description :
   Author :       'li'
   date：          2019/9/12
-------------------------------------------------
   Change Activity:
                   2019/9/12:
-------------------------------------------------
"""
from db_utility.db_pool import DB_POOL
from db_utility.sql_str import SELECT_MONITOR_INSTANCE, SELECT_SYSTEM_INFO, UPDATE_SYSTEM_ID

__author__ = 'li'


def main():
    monitor_instance = DB_POOL.select(SELECT_MONITOR_INSTANCE)
    system_info = DB_POOL.select(SELECT_SYSTEM_INFO)
    for instance in monitor_instance:
        sys_name = instance['sys_name']
        for info in system_info:
            name = info['name']
            if sys_name == name:
                instance['sys_id'] = info['id']
                sql = UPDATE_SYSTEM_ID % (info['id'], instance['id'])
                count = DB_POOL.execute_sql_str(sql)
                print(count)


if __name__ == '__main__':
    main()
