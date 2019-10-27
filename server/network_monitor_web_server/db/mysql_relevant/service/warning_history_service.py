# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     warning_history_service
   Description :
   Author :       'li'
   date：          2019/10/4
-------------------------------------------------
   Change Activity:
                   2019/10/4:
-------------------------------------------------
"""
from common.utility.sql_parameter_type_change import TypeChange
from common.utility.uuid_utility import get_uuid_str
from db.mysql_relevant.connection_pool.db_pool import DB_POOL
from db.mysql_relevant.sql_str.warning_history import INSERT_WARNING_HISTORY, SELECT_WARNING_HISTORY_BASE


class WarningHistoryService:
    @staticmethod
    def save_items(items):
        """
        save items
        :param items:
        :return:
        """
        sqls = []
        for item in items:
            if item.port is None:
                item.port = 0
            sql = INSERT_WARNING_HISTORY % (
                get_uuid_str(),
                item.sys_id,
                item.sys_name,
                item.description,
                item.check_type,
                item.ip,
                item.port,
                TypeChange.date_stamp_to_datetime(item.start_time),
                item.is_success,
                item.comment,
                item.warning_type, item.interval)
            sqls.append(sql)
        DB_POOL.execute_sql_array(sqls)

    @staticmethod
    def save_recover_info(results):
        """
        save recover info
        :param results:
        :return:
        """
        sqls = []
        for item in results:
            if item['port'] is None or (str(item['port']) == ''):
                item['port'] = 0
            sql = INSERT_WARNING_HISTORY % (
                get_uuid_str(),
                item['sys_id'],
                item['sys_name'],
                item['description'],
                item['type'],
                item['ip'],
                str(item['port']),
                item['start_time'],
                item['check_result'],
                '',
                '异常恢复',
                str(item['interval']))
            sqls.append(sql)
        DB_POOL.execute_sql_array(sqls)

    @staticmethod
    def get_ping_last_state(item):
        """
        get ping last state
        :param item:
        :return:
        """
        ip = item.ip
        sql = SELECT_WARNING_HISTORY_BASE + """ and 
        check_type = 'ping' and ip = '%s' order by check_time desc;""" % ip
        res = DB_POOL.select(sql)
        return res

    @staticmethod
    def get_tcp_last_state(item):
        ip = item.ip
        sql = SELECT_WARNING_HISTORY_BASE + """ and
            check_type = 'half_connection' and ip = '%s' order by check_time desc;""" % ip
        res = DB_POOL.select(sql)
        return res

    @staticmethod
    def query_warning_history_by_condition(sys_id=None, sys_name=None,
                                           ip=None, check_type=None):
        """
        query instance by condition
        :param sys_id:
        :param sys_name:
        :param ip:
        :param check_type:
        :return:
        """
        base_sql = SELECT_WARNING_HISTORY_BASE
        if sys_id is not None and len(sys_id) > 0:
            base_sql = base_sql + """and sys_id = '%s'""" % sys_id
        if sys_name is not None and len(sys_name) > 0:
            base_sql = base_sql + "and sys_name like '%" + sys_name + "%'"
        if ip is not None and len(ip) > 0:
            base_sql = base_sql + "and ip like '%" + ip + "%'"
        if check_type is not None and len(check_type) > 0:
            base_sql = base_sql + "and `check_type` like '%" + check_type + "%'"
        base_sql = base_sql + 'ORDER BY check_time DESC limit 200;'
        print(base_sql)
        result = DB_POOL.select(sql=base_sql)
        for res in result:
            res['check_time'] = str(res['check_time'])
            if res['check_type'] == 'half_connection':
                res['check_type'] = '半连接'
        return result
