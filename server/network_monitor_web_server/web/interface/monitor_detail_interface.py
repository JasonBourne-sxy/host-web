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
from web.service.monitor_visualization_service import get_monitor_visualization

__author__ = 'li'

import json

from web.interface.interface_common import create_json_response

from web.app import app, cross_origin, request


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
    return_detail = get_monitor_visualization(sys_id, check_type, check_result)
    return create_json_response(return_detail)
