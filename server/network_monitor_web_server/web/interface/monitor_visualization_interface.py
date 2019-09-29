# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     monitor_visualization_interface
   Description :
   Author :       'li'
   date：          2019/9/28
-------------------------------------------------
   Change Activity:
                   2019/9/28:
-------------------------------------------------
"""

__author__ = 'li'
from web.service.monitor_visualization_service import MonitorVisualizationService

import json
from web.interface.interface_common import create_json_response
from web.app import app, cross_origin, request


@app.route('/get_real_time_monitor_result', methods=['POST'])
@cross_origin()
def get_real_time_monitor_result():
    """
    ocr interface for python
    :return:
    """
    data_byte = request.data  # 获取 JSON 数据
    json_obj = json.loads(str(data_byte, encoding='utf8'))
    results = MonitorVisualizationService.query_realtime_monitor_result(json_obj)
    return create_json_response(results)
