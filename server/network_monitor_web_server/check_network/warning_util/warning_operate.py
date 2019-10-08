# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     warning_operate
   Description :
   Author :       'li'
   date：          2019/10/4
-------------------------------------------------
   Change Activity:
                   2019/10/4:
-------------------------------------------------
"""
import copy

from check_network.warning_util.send_msg import send_msg_to_qyweixin
from common.utility.sql_parameter_type_change import TypeChange
from db.mysql_relevant.service.monitor_instance_service import MonitorInstancesService
from db.mysql_relevant.service.monitor_visualization_service import MonitorVisualizationService
from db.mysql_relevant.service.warning_history_service import WarningHistoryService


class WarningOperate:
    """
    warning
    """

    def __init__(self):
        """
        init method
        """
        self.format_monitor_instances = self.get_format_monitor_instances()

    def save_warning_history_to_db(self, check_result):
        large_delay, overtime = self.__get_warning_results(check_result)
        to_warning_items = self.get_to_warning_items(large_delay, overtime)
        self.__save_warning_to_mysql(to_warning_items)
        return to_warning_items

    @staticmethod
    def __save_warning_to_mysql(to_warning_items):
        """
        save warning to mysql
        (`id`,`sys_id`,`sys_name`,`description`,`check_type`,`ip`,`port`,
        `check_time`,`check_result`,`comment`,`warning_type`,`interval`)
        :return:
        """
        WarningHistoryService.save_items(to_warning_items)

    @staticmethod
    def get_format_monitor_instances():
        """
        get
        :return:
        """
        result = MonitorInstancesService.get_all_used_check_instances()
        mapping = {}
        for res in result:
            check_type = res['type']
            if check_type == '半连接':
                check_type = 'tcp'
            if check_type not in mapping:
                mapping[check_type] = {}
            if check_type == 'ping':
                ip = res['ip']
                if ip not in mapping[check_type]:
                    mapping[check_type][ip] = []
                mapping[check_type][ip].append(res)
            else:
                ip = res['ip']
                port = res['port']
                if ip not in mapping[check_type]:
                    mapping[check_type][ip] = {}
                if port not in mapping[check_type][ip]:
                    mapping[check_type][ip][port] = []
                mapping[check_type][ip][port].append(res)
        return mapping

    def __get_warning_results(self, check_result):
        """
        get warning result
        :param check_result:
        :return:
        """
        format_monitor_instances = self.format_monitor_instances
        large_delay, overtime = [], []
        for res in check_result:
            if not res.is_success:
                combine_res = self.__combine_result(format_monitor_instances, res)
                overtime = overtime + combine_res
                continue
            if res.end_time - res.start_time > 0.1:
                combine_res = self.__combine_result(format_monitor_instances, res)
                large_delay = large_delay + combine_res
        return large_delay, overtime

    @staticmethod
    def __combine_result(format_monitor_instances, res):
        """
        combine result
        :param format_monitor_instances:
        :param res:
        :return:
        """
        ret_res = []
        ip = res.ip
        port = res.port
        if res.comment is None:
            res.comment = ''
        if res.end_time is not None:
            res.interval = str(int(res.end_time - res.start_time))
        if res.check_type == 'ping':
            instances = format_monitor_instances['ping'][ip]
            for inst in instances:
                new_res = copy.deepcopy(res)
                if not new_res.is_success:
                    new_res.warning_type = '网络异常'
                else:
                    new_res.warning_type = '响应时间过长'
                new_res.sys_id = inst['sys_id']
                new_res.sys_name = inst['sys_name']
                new_res.description = inst['description']
                ret_res.append(new_res)
        else:
            instances = format_monitor_instances['tcp'][ip][int(port)]
            for inst in instances:
                new_res = copy.deepcopy(res)
                if not new_res.is_success:
                    new_res.warning_type = '网络异常'
                else:
                    new_res.warning_type = '响应时间过长'
                new_res.sys_id = inst['sys_id']
                new_res.sys_name = inst['sys_name']
                new_res.description = inst['description']
                ret_res.append(new_res)
        return ret_res

    def get_to_warning_items(self, large_delay, overtime):
        """
        get to warning items
        :param large_delay:
        :param overtime:
        :return:
        """
        to_send_warning_items = []
        all_items = overtime + large_delay
        for item in all_items:
            check_type = item.check_type
            if check_type == 'ping':
                last_states = WarningHistoryService.get_ping_last_state(item)
                if len(last_states) == 0 or self.check_not_in_valid_time(item, last_states):
                    to_send_warning_items.append(item)
            else:
                last_states = WarningHistoryService.get_tcp_last_state(item)
                if len(last_states) == 0 or self.check_not_in_valid_time(item,
                                                                         last_states):
                    to_send_warning_items.append(item)
        return to_send_warning_items

    @staticmethod
    def check_not_in_valid_time(item, last_states):
        """
        check in vaild time
        :param item:
        :param last_states:
        :return:
        """
        last = last_states[0]
        check_time = str(last['check_time'])
        check_time = TypeChange.datetime_to_date_stamp(check_time)
        if item.start_time - check_time > 600:
            return True
        return False

    @staticmethod
    def send_warning_to_wechat(to_warning_items):
        """
        send warning
        :param to_warning_items:
        :return:
        """
        for item in to_warning_items:
            title = item.sys_name + '_' + item.warning_type
            content = '系统名称：' + item.sys_name + '  描述：' + item.description + \
                      ' 地址：' + item.ip + '_' + str(item.port), ' 检查时间' + \
                      TypeChange.date_stamp_to_datetime(item.start_time) + ' 检查方式：' \
                      + item.check_type
            send_msg_to_qyweixin('01639', title, content)

    @staticmethod
    def check_and_send_recover_info(visual, query_results):
        """
        check and send recover info
        :param visual:
        :param query_results:
        :return:
        """
        if not visual.check_result or len(query_results) == 0 \
                or query_results[0]['check_result']:
            return
        results = MonitorVisualizationService.query_realtime_monitor_result(visual)
        if len(results) == 0:
            return
        WarningOperate.save_recover_info_to_mysql(results)
        WarningOperate.send_recover_info_to_wechart(results)

    @staticmethod
    def save_recover_info_to_mysql(results):
        """
        save recover info to mysql
        :param results:
        :return:
        """
        WarningHistoryService.save_recover_info(results)

    @classmethod
    def send_recover_info_to_wechart(cls, results):
        for item in results:
            title = item['sys_name'] + '_' + '异常恢复'
            content = '系统名称：' + item['sys_name'] + '  描述：' + item['description'] + \
                      ' 地址：' + item['ip'] + '_' + str(item['port']), ' 检查时间' + \
                      item['start_time'] + ' 检查方式：' \
                      + item['type'] + ' 异常恢复'
            send_msg_to_qyweixin('01639', title, content)
