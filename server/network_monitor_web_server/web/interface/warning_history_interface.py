# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     monitor_history_interface
   Description :
   Author :       'li'
   date：          2019/10/7
-------------------------------------------------
   Change Activity:
                   2019/10/7:
-------------------------------------------------
"""
from db.mysql_relevant.service.warning_history_service import WarningHistoryService

__author__ = 'li'

import json

from web.interface.interface_common import create_json_response

from web.web_launch import app, cross_origin, request


@app.route('/get_warning_history', methods=['POST'])
@cross_origin()
def get_warning_history():
    """
    ocr interface for python
    :return:
    """
    data_byte = request.data  # 获取 JSON 数据
    json_obj = json.loads(str(data_byte, encoding='utf8'))
    sys_id, ip, check_type, sys_name = json_obj.get('sys_id'), \
                                       json_obj.get('ip'), \
                                       json_obj.get('check_type'), \
                                       json_obj.get('sys_name')
    return_detail = WarningHistoryService. \
        query_warning_history_by_condition(sys_id=sys_id, ip=ip,
                                           check_type=check_type,
                                           sys_name=sys_name)
    return create_json_response(return_detail)
