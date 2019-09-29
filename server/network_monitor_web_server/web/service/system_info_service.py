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
from common.utility.sql_parameter_type_change import TypeChange
from common.utility.uuid_utility import get_uuid_str
from db_utility.db_pool import DB_POOL
from db_utility.db_str.sql_str import SELECT_SYSTEM_INFO, QUERY_SYS_INFO
from db_utility.db_str.system_info import *

__author__ = 'li'


class SystemInfoService:
    @staticmethod
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

    @staticmethod
    def query_sys_info(json_object):
        """
        query sys info
        :param json_object:
        :return:
        """
        sys_name, manager, job_number = json_object.get('name'), \
                                        json_object.get('manager'), \
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

    @staticmethod
    def delete_system_info(json_obj):
        """
        insert or update instance
        :param json_obj:
        :return:
        """
        sql = DELETE_SYSTEM_INFO % (TypeChange.to_string(json_obj, 'id'))
        DB_POOL.execute_sql_str(sql)
        return {'is_success': True}

    @staticmethod
    def __insert_system_info(json_obj):
        """
        insert monitor instance
        :param json_obj:
        :return:
        """
        sql = INSERT_SYSTEM_INFO % (get_uuid_str(),
                                    TypeChange.to_string(json_obj, 'name'),
                                    TypeChange.to_string(json_obj, 'manager'),
                                    TypeChange.to_string(json_obj, 'telephone'),
                                    TypeChange.to_string(json_obj, 'job_number'),)
        DB_POOL.execute_sql_str(sql)

    @staticmethod
    def __update_system_info(json_obj):
        """
        UPDATE MONITOR INSTANCE
        :param json_obj:
        :return:
        """
        sql = UPDATE_SYSTEM_INFO % (TypeChange.to_string(json_obj, 'id'),
                                    TypeChange.to_string(json_obj, 'name'),
                                    TypeChange.to_string(json_obj, 'manager'),
                                    TypeChange.to_string(json_obj, 'telephone'),
                                    TypeChange.to_string(json_obj, 'job_number'),
                                    TypeChange.to_string(json_obj, 'id'))
        DB_POOL.execute_sql_str(sql)

    @staticmethod
    def insert_or_update_system_info(json_obj):
        """
        insert or update monitor instance
        :param json_obj:
        :return:
        """
        if 'id' in json_obj and (len(json_obj['id']) > 10):
            SystemInfoService.__update_system_info(json_obj)
        else:
            SystemInfoService.__insert_system_info(json_obj)
        return {'is_success': True}

    @staticmethod
    def get_system_name_by_id(sys_id):
        """
        get system name by id
        :param sys_id:
        :return:
        """
        sql = SELECT_BASE_SYSTEM_INFO + """ and id ='%s'""" % sys_id
        sys_name = DB_POOL.select(sql)[0]['name']
        return sys_name


if __name__ == '__main__':
    SystemInfoService.get_system_info_tree()
