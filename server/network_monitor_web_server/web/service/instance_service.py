# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     instance_service
   Description :
   Author :       'li'
   date：          2019/9/24
-------------------------------------------------
   Change Activity:
                   2019/9/24:
-------------------------------------------------
"""
from db_utility.sql_str import QUERY_MONITOR_INSTANCE

__author__ = 'li'
from db_utility.db_pool import DB_POOL


def insert_or_update_instance(json_obj):
    """
    insert or update instance
    :param json_obj:
    :return:
    """
    print(json_obj)
    return {'is_success': True}


def delete_instance(json_obj):
    """
    insert or update instance
    :param json_obj:
    :return:
    """
    print(json_obj)
    return {'is_success': True}


def query_instance_by_condition(sys_id=None, sys_name=None, ip=None, check_type=None):
    """
    query instance by condition
    :param sys_id:
    :param sys_name:
    :param ip:
    :param check_type:
    :return:
    """
    base_sql = QUERY_MONITOR_INSTANCE
    if sys_id is not None:
        base_sql = base_sql + """and sys_id = '%s'""" % sys_id
    if sys_name is not None:
        base_sql = base_sql + "and sys_name like '%" + sys_name + "%'"
    if ip is not None:
        base_sql = base_sql + "and ip like '%" + ip + "%'"
    if check_type is not None:
        base_sql = base_sql + "and sys_name like '%" + check_type + "%'"
    result = DB_POOL.select(sql=base_sql)
    return result


def main():
    result = query_instance_by_condition(sys_id='6bd97c1ec2c0443ca937588fe601d53f', sys_name=None,
                                         ip='130', check_type=None)
    pass


if __name__ == '__main__':
    main()
