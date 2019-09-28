# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     interface_common
   Description :
   Author :       'li'
   date：          2019/9/27
-------------------------------------------------
   Change Activity:
                   2019/9/27:
-------------------------------------------------
"""
import json

from flask import make_response

__author__ = 'li'


def create_json_response(json_obj):
    """
    create json response
    :param json_obj:
    :return:
    """
    response = make_response()
    response.data = json.dumps(json_obj)
    response.headers['Content-Type'] = 'application/json'
    return response