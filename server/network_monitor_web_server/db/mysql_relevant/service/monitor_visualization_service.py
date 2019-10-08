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
from common.utility.sql_parameter_type_change import TypeChange
from common.utility.uuid_utility import get_uuid_str
from db.mysql_relevant.connection_pool.db_pool import DB_POOL
from db.mysql_relevant.object_mapping.monitor_visualization import MONITOR_VISUALIZATION
from db.mysql_relevant.sql_str.monitor_visualization import QUERY_REAL_TIME_MONITOR_RESULT_BASE_SQL
from db.mysql_relevant.sql_str.sql_str import SELECT_INSTANCE_FROM_SYS_ID, SELECT_VISUAL_FROM_CHECK_TYPE, \
    SELECT_MONITOR_VISUAL_BY_UNIQUE_IDENTIFY, UPDATE_MONITOR_VISUAL, INSERT_INTO_MONITOR_VISUAL


class MonitorVisualizationService:
    @staticmethod
    def change_result(boole):
        """
        change result
        :param boole:
        :return:
        """
        if boole == 'True':
            return '正常'
        return '不正常'

    @staticmethod
    def format_space_time(space_time):
        """
        format space time
        :param space_time:
        :return:
        """
        if str(space_time) == 'None':
            return '超时'
        return space_time

    @staticmethod
    def get_monitor_visualization(sys_id, check_type):
        """
        get monitor visualization
        :param sys_id:
        :param check_type:
        :return:
        """
        sql = SELECT_INSTANCE_FROM_SYS_ID % sys_id
        instances = DB_POOL.select(sql)
        sql = SELECT_VISUAL_FROM_CHECK_TYPE % check_type
        visuals = DB_POOL.select(sql)
        new_result = []
        for instance in instances:
            if instance['type'] != check_type:
                continue
            for vis in visuals:
                if check_type == 'ping':
                    if instance['ip'] == vis['ip']:
                        instance['start_time'] = str(vis['start_time'])
                        instance['check_result'] = \
                            MonitorVisualizationService.change_result((vis['check_result']))
                        instance['space_time'] = \
                            MonitorVisualizationService.format_space_time(vis['interval'])
                        new_result.append(instance)
                else:
                    if instance['ip'] == vis['ip'] and instance['port'] == vis['port']:
                        instance['start_time'] = str(vis['start_time'])
                        instance['check_result'] = \
                            MonitorVisualizationService.change_result((vis['check_result']))
                        instance['space_time'] = \
                            MonitorVisualizationService.format_space_time(vis['interval'])
                        new_result.append(instance)
        return new_result

    @staticmethod
    def query_realtime_monitor_result(json_obj):
        """
        query real time monitor result
        :param json_obj:
        :return:
        """
        ip, check_type, port = json_obj.ip, \
                               json_obj.check_type, \
                               json_obj.port
        base_sql = QUERY_REAL_TIME_MONITOR_RESULT_BASE_SQL
        if ip is not None and len(ip) > 0:
            base_sql = base_sql + " and ip like '%" + ip + "%'"
        if port is not None:
            base_sql = base_sql + " and port = " + str(port) + ""
        if check_type is not None and len(check_type) > 0:
            base_sql = base_sql + " and type like '%" + check_type + "%'"
        base_sql = base_sql + ' order by t.sys_name ;'
        results = DB_POOL.select(base_sql)
        return MonitorVisualizationService.format_monitor_result(results)

    @staticmethod
    def query_realtime_monitor(json_obj):
        """
        query real time monitor result
        :param json_obj:
        :return:
        """
        ip, check_type, sys_name, check_result = json_obj['ip'], \
                                             json_obj['check_type'], \
                                             json_obj['sys_name'], \
                                             json_obj['check_result']
        base_sql = QUERY_REAL_TIME_MONITOR_RESULT_BASE_SQL
        if ip is not None and len(ip) > 0:
            base_sql = base_sql + " and ip like '%" + ip + "%'"
        if sys_name is not None and len(sys_name) > 0:
            base_sql = base_sql + " and sys_name like '%" + sys_name + "%'"
        if check_type is not None and len(check_type) > 0:
            base_sql = base_sql + " and type like '%" + check_type + "%'"
        if check_result is not None and len(check_result) > 0:
            base_sql = base_sql + " and check_result = '" + check_result + "'"
        base_sql = base_sql + ' order by t.sys_name ;'
        results = DB_POOL.select(base_sql)
        return MonitorVisualizationService.format_monitor_result(results)

    @staticmethod
    def format_monitor_result(results):
        """
        format monitor result
        :param results:
        :return:
        """
        for result in results:
            if 'None' == result['response_time']:
                result['response_time'] = '超时'
            if 'True' == result['check_result']:
                result['check_result'] = '正常'
            else:
                result['check_result'] = '异常'
            if result['type'] == 'ping':
                result['port'] = '0'
            result['start_time'] = str(result['start_time'])
        return results

    @staticmethod
    def update_monitor_visualization_db(result):
        """
        update monitor visualization
        :param result:
        :return:
        """
        sqls = []
        for item in result:
            visual = MONITOR_VISUALIZATION()
            visual.unique_identify = item.check_type + '_' + item.ip + '_' + str(item.port)
            visual.check_type = item.check_type
            visual.ip = item.ip
            visual.check_result = item.is_success
            visual.port = item.port
            visual.start_time = item.start_time
            if item.is_success:
                visual.interval = item.interval
            sql = MonitorVisualizationService.get_insert_or_update_visual(visual)
            sqls.append(sql)
        if len(sqls) > 0:
            DB_POOL.execute_sql_array(sqls)

    @staticmethod
    def get_insert_or_update_visual(visual):
        """
        insert or update visual
        :param visual:
        :return:
        """
        sql = SELECT_MONITOR_VISUAL_BY_UNIQUE_IDENTIFY % visual.unique_identify
        query_results = DB_POOL.select(sql)
        count = len(query_results)
        if visual.port is None:
            visual.port = 0
        if visual.check_type == 'half_connection':
            visual.check_type = '半连接'
        if count == 0:
            sql = INSERT_INTO_MONITOR_VISUAL % \
                  (get_uuid_str(), visual.unique_identify, visual.ip, visual.port,
                   visual.check_type, visual.interval,
                   TypeChange.date_stamp_to_datetime(visual.start_time),
                   visual.check_result)
        else:
            sql = UPDATE_MONITOR_VISUAL % \
                  (get_uuid_str(), visual.unique_identify, visual.ip, visual.port,
                   visual.check_type, visual.interval,
                   TypeChange.date_stamp_to_datetime(visual.start_time),
                   visual.check_result, visual.unique_identify)
        return sql, query_results

    @staticmethod
    def get_real_time_monitor_result(visual):
        """
        get real time monitor result
        :param visual:
        :return:
        """
        base_sql = QUERY_REAL_TIME_MONITOR_RESULT_BASE_SQL
        if visual.check_type == 'ping':
            if visual.ip is not None and len(visual.ip) > 0:
                base_sql = base_sql + "and ip like '%" + visual.ip + "%'"
            if visual.check_type is not None and len(visual.check_type) > 0:
                base_sql = base_sql + "and type like '%" + visual.check_type + "%'"
        else:
            if visual.ip is not None and len(visual.ip) > 0:
                base_sql = base_sql + "and ip like '%" + visual.ip + "%'"
            if visual.port is not None and len(visual.port) > 0:
                base_sql = base_sql + "and ip = " + str(visual.port) + ""
            if visual.check_type is not None and len(visual.check_type) > 0:
                base_sql = base_sql + "and type like '%" + visual.check_type + "%'"
        base_sql = base_sql + 'order by sys_name ;'
        results = DB_POOL.select(base_sql)
        return results
