# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     monitor
   Description :
   Author :       'li'
   date：          2019/10/3
-------------------------------------------------
   Change Activity:
                   2019/10/3:
-------------------------------------------------
"""
import threading
import time

from check_network.monitor.check_instances import CheckInstances
from check_network.monitor.half_connection_check import HalfConnectionCheck
from check_network.monitor.ping_instances_check import PingCheck
from check_network.warning_util.warning_operate import WarningOperate
from db.mysql_relevant.connection_pool.db_pool import DB_POOL
from db.mysql_relevant.object_mapping.monitor_visualization import MONITOR_VISUALIZATION
from db.mysql_relevant.service.monitor_detail_service import MonitorDetailService
from db.mysql_relevant.service.monitor_visualization_service import MonitorVisualizationService
from db.redis_relevant.connection_pool.redis_operate import delete_all_data_from_redis, \
    delete_all_instance_data_from_redis


class Monitor:
    """
    monitor class
    """

    def __init__(self):
        """
        start check network
        """
        delete_all_data_from_redis()
        self.__init_check_instances_to_redis()
        self.warning_operate = WarningOperate()

    def reload_redis_instances(self):
        """
        reload redis instance
        :return:
        """
        delete_all_instance_data_from_redis()
        self.__init_check_instances_to_redis()
        self.warning_operate = WarningOperate()

    @staticmethod
    def __init_check_instances_to_redis():
        """
        init check instances to redis
        :return:
        """
        ping_instances, half_connection_instances = CheckInstances.get_check_instances()
        CheckInstances.save_check_instances_to_redis(ping_instances, half_connection_instances)

    def start(self):
        """
        start monitoring
        :return:
        """
        current_second = 0
        while True:

            intervals = CheckInstances.get_all_interval()
            check_intervals = CheckInstances.get_check_interval(intervals, current_second)
            if len(check_intervals) > 0:
                threading.Thread(target=self.check_by_interval, args=(check_intervals,)).start()
                # self.check_by_interval(check_intervals)
            time.sleep(1)
            current_second = current_second + 1

    def check_by_interval(self, check_intervals):
        """

        :param check_intervals:
        :return:
        """
        ping_instances, half_instances = CheckInstances. \
            get_to_check_instances(check_intervals)
        ping_result = PingCheck(ping_instances).get_ping_result()
        half_connection_result = HalfConnectionCheck(half_instances). \
            get_half_connection_result()  # check condition
        for result in (ping_result, half_connection_result):
            MonitorDetailService.save_check_result_to_detail(result)
            self.update_monitor_visualization_db(result)
            to_warning_items = self.warning_operate. \
                save_warning_history_to_db(result)
            WarningOperate.send_warning_to_wechat(to_warning_items)

    @staticmethod
    def update_monitor_visualization_db(result):
        """

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
            sql, query_results = MonitorVisualizationService. \
                get_insert_or_update_visual(visual)
            WarningOperate.check_and_send_recover_info(visual, query_results)
            sqls.append(sql)
        if len(sqls) > 0:
            DB_POOL.execute_sql_array(sqls)


MASTER_MONITOR = Monitor()
