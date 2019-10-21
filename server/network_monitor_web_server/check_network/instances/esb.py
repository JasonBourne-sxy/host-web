# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     esb
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

port = """:1098
:1099
:3098
:3099
:5005"""
ip = """188.8.26.33
188.8.29.33
188.8.26.48
188.8.27.32
172.16.133.202
188.10.23.11
188.8.12.35
188.8.12.37
172.16.135.45
172.17.3.41
188.8.12.39
172.17.36.5
10.40.22.31
188.8.20.12
172.16.133.232
172.17.28.3
172.36.0.164
188.8.12.42
172.16.1.112
188.8.28.19
188.8.12.38
188.8.23.15
10.40.22.27
172.36.0.167
172.17.34.70
172.17.28.2
172.16.135.19
188.8.26.32
172.16.133.239
188.8.25.13
172.16.135.21
188.8.20.11
188.8.26.16
172.16.133.238
172.17.28.6
188.8.26.17
188.8.23.14
188.8.12.41
188.8.23.13
188.8.29.32
188.8.28.32
172.17.28.7
172.36.0.163
172.16.133.246
172.36.0.172
188.8.12.36
172.16.133.231
188.8.28.16
188.8.20.13
172.16.135.18
172.16.133.203
188.8.19.11
172.36.0.171
172.16.135.20
172.16.1.124
172.16.134.230
172.36.0.166
188.8.28.17
172.16.135.44
10.40.22.28
188.8.24.11
172.17.34.153
188.8.24.12
188.8.27.33
188.8.19.12
188.8.12.40
172.16.135.59
188.8.19.13
172.16.135.58
172.17.36.6
188.8.28.18
172.16.1.91
188.8.25.12
172.16.134.231
188.8.27.34
"""
description = """接入ESB的终端"""

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

sys_id = '675011c24208435396ee1ed460299d6c'
sys_name = 'ESB系统'
for ip in new_ips:
    for port in new_ports:
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
sys_id = '675011c24208435396ee1ed460299d6c'
sys_name = 'ESB系统'
for ip in new_ips:
    for port in new_ports:
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
