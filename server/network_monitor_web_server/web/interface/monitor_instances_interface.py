# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     monitor_instances_interface
   Description :
   Author :       'li'
   date：          2019/9/27
-------------------------------------------------
   Change Activity:
                   2019/9/27:
-------------------------------------------------
"""
from check_network.monitor.monitor import MASTER_MONITOR
from db.mysql_relevant.service.monitor_detail_service import MonitorDetailService
from db.mysql_relevant.service.monitor_instance_service import MonitorInstancesService

__author__ = 'li'

import json

from web.interface.interface_common import create_json_response

from web.web_launch import app, cross_origin, request


@app.route('/get_monitor_history_data', methods=['POST'])
@cross_origin()
def get_monitor_history():
    """
    ocr interface for python
    :return:
    """
    data_byte = request.data  # 获取 JSON 数据
    json_obj = json.loads(str(data_byte, encoding='utf8'))
    result = MonitorDetailService.get_monitor_history_data(json_obj)
    return create_json_response(result)


@app.route('/insert_or_update_instance', methods=['POST'])
@cross_origin()
def insert_or_update_instance():
    """
    ocr interface for python
    :return:
    """
    data_byte = request.data  # 获取 JSON 数据
    json_obj = json.loads(str(data_byte, encoding='utf8'))
    result = MonitorInstancesService.insert_or_update_monitor_instance(json_obj)
    MASTER_MONITOR.reload_redis_instances()
    return create_json_response(result)


@app.route('/delete_instance', methods=['POST'])
@cross_origin()
def delete_instance():
    """
    ocr interface for python
    :return:
    """
    data_byte = request.data  # 获取 JSON 数据
    json_obj = json.loads(str(data_byte, encoding='utf8'))
    result = MonitorInstancesService.delete_instance(json_obj)
    MASTER_MONITOR.reload_redis_instances()
    return create_json_response(result)


@app.route('/get_monitor_instance', methods=['POST'])
@cross_origin()
def get_monitor_instance():
    """
    ocr interface for python
    :return:
    """
    data_byte = request.data  # 获取 JSON 数据
    json_obj = json.loads(str(data_byte, encoding='utf8'))
    sys_id, ip, check_type, sys_name, description = json_obj.get('sys_id'), \
                                                    json_obj.get('ip'), \
                                                    json_obj.get('check_type'), \
                                                    json_obj.get('sys_name'), \
                                                    json_obj.get('description')
    return_detail = MonitorInstancesService. \
        query_instance_by_condition(sys_id=sys_id, ip=ip,
                                    check_type=check_type,
                                    sys_name=sys_name,
                                    description=description)
    return create_json_response(return_detail)
