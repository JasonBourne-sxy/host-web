# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     query_data
   Description :
   Author :       'li'
   date：          2019/9/23
-------------------------------------------------
   Change Activity:
                   2019/9/23:
-------------------------------------------------
"""
from web.service.system_info_service import get_system_info_tree

__author__ = 'li'
import json

from flask import make_response
from flask import Flask

from flask_cors import *

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
