# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     zonghe
   Description :
   Author :       'li'
   date：          2019/10/12
-------------------------------------------------
   Change Activity:
                   2019/10/12:
-------------------------------------------------
"""

import csv

from common.utility.uuid_utility import get_uuid_str
from db.mysql_relevant.connection_pool.db_pool import DB_POOL
from db.mysql_relevant.sql_str.monitor_instance import INSERT_MONITOR_INSTANCE

sys_id = 'f6f7aa8239a24499962ee7f45a763bc5'
sys_name = '综合运营平台'
with open('1.csv', 'r', encoding='utf8') as f:
    reader = csv.reader(f)
    print(type(reader))
    for row in reader:
        description = str(row[0]).replace(' ', '')
        ip = row[1].replace(' ', '')
        ports = row[2].replace(' ', '')
        ports = str(ports).split('/')
        for port in ports:
            if len(port) < 2:
                continue
            sql = INSERT_MONITOR_INSTANCE % (get_uuid_str(),
                                             sys_id,
                                             sys_name,
                                             description,
                                             ip,
                                             str(port),
                                             '半连接',
                                             '60',
                                             '1')
            print(sql)
            DB_POOL.execute_sql_str(sql)
        print(row)
