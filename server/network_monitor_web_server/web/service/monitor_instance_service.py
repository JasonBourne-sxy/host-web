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
from common.utility.sql_parameter_type_change import TypeChange
from common.utility.uuid_utility import get_uuid_str
from db_utility.db_str.monitor_instance import INSERT_MONITOR_INSTANCE, UPDATE_MONITOR_INSTANCE, DELETE_MONITOR_INSTANCE
from db_utility.db_str.sql_str import QUERY_MONITOR_INSTANCE
from web.service.system_info_service import SystemInfoService

__author__ = 'li'
from db_utility.db_pool import DB_POOL


class MonitorInstancesService:
    @staticmethod
    def insert_or_update_instance(json_obj):
        """
        insert or update instance
        :param json_obj:
        :return:
        """
        print(json_obj)
        return {'is_success': True}

    @staticmethod
    def query_instance_by_condition(sys_id=None, sys_name=None,
                                    ip=None, check_type=None):
        """
        query instance by condition
        :param sys_id:
        :param sys_name:
        :param ip:
        :param check_type:
        :return:
        """
        base_sql = QUERY_MONITOR_INSTANCE
        if sys_id is not None and len(sys_id) > 0:
            base_sql = base_sql + """and sys_id = '%s'""" % sys_id
        if sys_name is not None and len(sys_name) > 0:
            base_sql = base_sql + "and sys_name like '%" + sys_name + "%'"
        if ip is not None and len(ip) > 0:
            base_sql = base_sql + "and ip like '%" + ip + "%'"
        if check_type is not None and len(check_type) > 0:
            base_sql = base_sql + "and `type` like '%" + check_type + "%'"
        base_sql = base_sql + 'order by sys_name limit 200;'
        result = DB_POOL.select(sql=base_sql)
        return result

    @staticmethod
    def delete_instance(json_obj):
        """
        insert or update instance
        :param json_obj:
        :return:
        """
        sql = DELETE_MONITOR_INSTANCE % (TypeChange.to_string(json_obj, 'id'))
        DB_POOL.execute_sql_str(sql)
        return {'is_success': True}

    @staticmethod
    def __insert_monitor_instance(json_obj):
        """
        insert monitor instance
        :param json_obj:
        :return:
        """
        sql = INSERT_MONITOR_INSTANCE % (get_uuid_str(),
                                         TypeChange.to_string(json_obj, 'sys_id'),
                                         TypeChange.to_string(json_obj, 'sys_name'),
                                         TypeChange.to_string(json_obj, 'description'),
                                         TypeChange.to_string(json_obj, 'ip'),
                                         TypeChange.to_int(json_obj, 'port'),
                                         TypeChange.to_string(json_obj, 'type'),
                                         TypeChange.to_int(json_obj, 'interval'),
                                         TypeChange.to_int(json_obj, 'is_use'))
        DB_POOL.execute_sql_str(sql)

    @staticmethod
    def __update_monitor_instance(json_obj):
        """
        UPDATE MONITOR INSTANCE
        :param json_obj:
        :return:
        """
        sys_name = SystemInfoService.get_system_name_by_id(json_obj['sys_id'])
        sql = UPDATE_MONITOR_INSTANCE % (TypeChange.to_string(json_obj, 'id'),
                                         TypeChange.to_string(json_obj, 'sys_id'),
                                         sys_name,
                                         TypeChange.to_string(json_obj, 'description'),
                                         TypeChange.to_string(json_obj, 'ip'),
                                         TypeChange.to_int(json_obj, 'port'),
                                         TypeChange.to_string(json_obj, 'type'),
                                         TypeChange.to_int(json_obj, 'interval'),
                                         TypeChange.to_int(json_obj, 'is_use'),
                                         TypeChange.to_string(json_obj, 'id'))
        DB_POOL.execute_sql_str(sql)

    @staticmethod
    def insert_or_update_monitor_instance(json_obj):
        """
        insert or update monitor instance
        :param json_obj:
        :return:
        """
        if 'id' in json_obj and (len(json_obj['id']) > 10):
            MonitorInstancesService.__update_monitor_instance(json_obj)

        else:
            MonitorInstancesService.__insert_monitor_instance(json_obj)
        return {'is_success': True}


def main():
    result = MonitorInstancesService.query_instance_by_condition(sys_id='6bd97c1ec2c0443ca937588fe601d53f', sys_name=None,
                                         ip='130', check_type=None)
    pass


if __name__ == '__main__':
    main()
