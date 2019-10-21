# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     core
   Description :
   Author :       'li'
   date：          2019/10/11
-------------------------------------------------
   Change Activity:
                   2019/10/11:
-------------------------------------------------
"""
from common.utility.uuid_utility import get_uuid_str
from db.mysql_relevant.connection_pool.db_pool import DB_POOL
from db.mysql_relevant.sql_str.monitor_instance import INSERT_MONITOR_INSTANCE

port = """28087,22"""
ip = """
188.8.18.35
188.8.18.36
"""
description = """OPS,RDP"""

port = port.split(',')
new_ports = []
for p in port:
    new_pos = p.split(':')
    for n_p in new_pos:
        if len(n_p) > 1:
            new_ports.append(int(n_p))
new_ports.sort()
print(new_ports)

ips = ip.split('\n')
new_ips = []
for i in ips:
    if len(i) > 4:
        new_ips.append(i)
print(new_ips)
# 90012@fudian-bank.com
sys_id = '20bc37f8497240bbb3f9273bdabc2c84'
sys_name = '核心系统生产环境'
for ip in new_ips:
    for port in new_ports:
        sql = INSERT_MONITOR_INSTANCE % (get_uuid_str(),
                                         sys_id,
                                         sys_name,
                                         description,
                                         ip,
                                         str(port),
                                         '半连接',
                                         '600',
                                         '1')
        print(sql)
        DB_POOL.execute_sql_str(sql)
