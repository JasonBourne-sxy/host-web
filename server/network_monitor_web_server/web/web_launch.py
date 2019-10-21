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

from flask import Flask
from flask_cors import CORS
from flask_cors import cross_origin
from flask import request

app = Flask(__name__)
CORS(app, supports_credentials=True)
from web.interface.monitor_detail_interface import *
from web.interface.monitor_instances_interface import *
from web.interface.system_info_interface import *
from web.interface.monitor_visualization_interface import *
from web.interface.warning_history_interface import *


def launch_web():
    """
    launch web
    :return:
    """
    app.run(host='0.0.0.0', port=5000)
    print('launch web finish')


if __name__ == '__main__':
    launch_web()
