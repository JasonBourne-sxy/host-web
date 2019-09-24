# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     app_run
   Description :
   Author :       'li'
   date：          2019/9/18
-------------------------------------------------
   Change Activity:
                   2019/9/18:
-------------------------------------------------
"""

from flask import request

from web.interface.query_data import *
from web.service.instance_service import query_instance_by_condition, insert_or_update_instance, delete_instance
from web.service.monitor_detail import get_monitor_history_data
from web.service.monitor_visualization_service import get_monitor_visualization

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/get_tree_info', methods=['GET', 'POST'])
@cross_origin()
def get_tree_info():
    """
    ocr interface for python
    :return:
    """
    sys_info_tree = get_system_info_tree()
    response = make_response()
    response.data = json.dumps(sys_info_tree)
    response.headers['Content-Type'] = 'application/json'
    return response


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
    response = make_response()
    response.data = json.dumps(return_detail)
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/get_monitor_history_data', methods=['POST'])
@cross_origin()
def get_monitor_history():
    """
    ocr interface for python
    :return:
    """
    data_byte = request.data  # 获取 JSON 数据
    json_obj = json.loads(str(data_byte, encoding='utf8'))
    result = get_monitor_history_data(json_obj)
    response = make_response()
    response.data = json.dumps(result)
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/insert_or_update_instance', methods=['POST'])
@cross_origin()
def insert_or_update_instance():
    """
    ocr interface for python
    :return:
    """
    data_byte = request.data  # 获取 JSON 数据
    json_obj = json.loads(str(data_byte, encoding='utf8'))
    result = insert_or_update_instance(json_obj)
    response = make_response()
    response.data = json.dumps(result)
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/delete_instance', methods=['POST'])
@cross_origin()
def delete_instance():
    """
    ocr interface for python
    :return:
    """
    data_byte = request.data  # 获取 JSON 数据
    json_obj = json.loads(str(data_byte, encoding='utf8'))
    result = delete_instance(json_obj)
    response = make_response()
    response.data = json.dumps(result)
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/get_monitor_instance', methods=['POST'])
@cross_origin()
def get_monitor_instance():
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
    return_detail = query_instance_by_condition(sys_id=sys_id, ip=ip,
                                                check_type=check_type,
                                                sys_name=sys_name)
    response = make_response()
    response.data = json.dumps(return_detail)
    response.headers['Content-Type'] = 'application/json'
    return response


def launch_web():
    """
    launch web
    :return:
    """
    app.run(host='0.0.0.0', port=5000)
    print('launch web finish')


if __name__ == '__main__':
    launch_web()
