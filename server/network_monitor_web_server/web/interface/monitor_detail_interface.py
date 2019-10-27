# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     monitor_detail_interface
   Description :
   Author :       'li'
   date：          2019/9/27
-------------------------------------------------
   Change Activity:
                   2019/9/27:
-------------------------------------------------
"""
from db.mysql_relevant.service.monitor_detail_service import MonitorDetailService
from db.mysql_relevant.service.monitor_visualization_service import MonitorVisualizationService


import json

from web.interface.interface_common import create_json_response

from web.web_launch import app, cross_origin, request


@app.route('/get_detail', methods=['POST'])
@cross_origin()
def receive_image_interface():
    """
    ocr interface for python
    :return:
    """
    data_byte = request.data  # 获取 JSON 数据
    json_obj = json.loads(str(data_byte, encoding='utf8'))
    sys_id, check_type, check_result = json_obj.get('sys_id'), \
                                       json_obj.get('check_type'), \
                                       json_obj.get('check_result')
    return_detail = MonitorVisualizationService. \
        get_monitor_visualization(sys_id, check_type)
    return create_json_response(return_detail)


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
