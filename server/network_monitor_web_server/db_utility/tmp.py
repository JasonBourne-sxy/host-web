# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     tmp
   Description :
   Author :       'li'
   date：          2019/9/18
-------------------------------------------------
   Change Activity:
                   2019/9/18:
-------------------------------------------------
"""
import json
import time

from db_utility.check_result_handle import datestamp_to_datetime
from db_utility.db_pool import DB_POOL

__author__ = 'li'

sql = """SELECT * FROM `monitor_instance` """

results = DB_POOL.select(sql)
content = []
for result in results:
    sys_name = result['sys_name']
    sys_id = result['sys_id']
    id = result['id']
    description = result['description']
    ip = result['ip']
    port = result['port']
    type = result['type']
    interval = result['interval']
    is_used = result['is_use']
    check_time = datestamp_to_datetime(time.time())
    check_result = '正常'
    item_json = {
        "id": id,
        "isParent": False,
        "sys_name": sys_name,
        "sys_id": sys_id,
        "description": description,
        "ip": ip,
        "port": port,
        "type": type,
        "interval": interval,
        "is_used": is_used,
        "check_time": check_time,
        "check_result": check_result
    }
    content.append(item_json)
print(content)
