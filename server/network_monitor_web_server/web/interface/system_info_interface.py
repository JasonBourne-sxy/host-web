# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     system_info_interface
   Description :
   Author :       'li'
   date：          2019/9/27
-------------------------------------------------
   Change Activity:
                   2019/9/27:
-------------------------------------------------
"""

import json

from db.mysql_relevant.service.system_info_service import SystemInfoService
from web.interface.interface_common import create_json_response

from web.web_launch import app, cross_origin, request


@app.route('/get_tree_info', methods=['GET', 'POST'])
@cross_origin()
def get_tree_info():
    """
    ocr interface for python
    :return:
    """
    sys_info_tree = SystemInfoService.get_system_info_tree()
    return create_json_response(sys_info_tree)


@app.route('/query_sys_info', methods=['POST'])
@cross_origin()
def get_sys_info():
    """
    ocr interface for python
    :return:
    """
    data_byte = request.data  # 获取 JSON 数据
    json_obj = json.loads(str(data_byte, encoding='utf8'))
    return_detail = SystemInfoService.query_sys_info(json_obj)
    return create_json_response(return_detail)


@app.route('/insert_or_update_system_info', methods=['POST'])
@cross_origin()
def insert_or_update_system_info():
    """
    ocr interface for python
    :return:
    """
    data_byte = request.data  # 获取 JSON 数据
    json_obj = json.loads(str(data_byte, encoding='utf8'))
    result = SystemInfoService.insert_or_update_system_info(json_obj)
    return create_json_response(result)


@app.route('/delete_sys_info', methods=['POST'])
@cross_origin()
def delete_sys_info():
    """
    ocr interface for python
    :return:
    """
    data_byte = request.data  # 获取 JSON 数据
    json_obj = json.loads(str(data_byte, encoding='utf8'))
    result = SystemInfoService.delete_system_info(json_obj)
    return create_json_response(result)
