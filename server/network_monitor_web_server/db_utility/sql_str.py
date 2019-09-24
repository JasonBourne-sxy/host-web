# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     sql_str
   Description :
   Author :       'li'
   date：          2019/9/11
-------------------------------------------------
   Change Activity:
                   2019/9/11:
-------------------------------------------------
"""
from common.utility.uuid_utility import get_uuid_str
from config import *

__author__ = 'li'

GET_COLUMN_INFO = """SELECT * FROM information_schema.COLUMNS WHERE table_schema = '%s';""" % DB_NAME
INSERT_SYS_INFO = """ INSERT INTO system_info (id,name) VALUES ('%s','%s');"""
INSERT_MONITOR_INSTANCE = """INSERT INTO monitor_instance (id,sys_name,description,ip,PORT) VALUES('%s','%s','%s','%s','%d');"""
SELECT_MONITOR_INSTANCE = """SELECT * FROM monitor_instance"""
SELECT_SYSTEM_INFO = """SELECT * FROM system_info"""
UPDATE_SYSTEM_ID = """UPDATE monitor_instance SET sys_id ='%s' WHERE ID='%s'"""
SELECT_USED_MONITOR_INSTANCE = """SELECT * FROM monitor_instance WHERE is_use = 1"""
INSERT_PING_TO_MONITOR_DETAIL = """ INSERT INTO monitor_detail (id,ip,port,check_type,result,start_time,end_time,check_interval) VALUES 
 ('{}','{}',{},'{}','{}','{}','{}','{}'); """
SELECT_MONITOR_VISUAL_BY_UNIQUE_IDENTIFY = """SELECT * FROM monitor_visualization WHERE unique_identify = '%s';"""
INSERT_INTO_MONITOR_VISUAL = """insert  into `monitor_visualization`(`id`,`unique_identify`,`ip`,`port`,`check_type`,`interval`,`start_time`,`check_result`) values  ('%s','%s','%s',%s,'%s','%s','%s','%s');"""
UPDATE_MONITOR_VISUAL = """UPDATE  monitor_visualization as a SET a.id ='%s' ,a.unique_identify ='%s' ,a.ip ='%s' ,a.port ='%s' ,a.check_type ='%s' ,a.interval ='%s' ,a.start_time ='%s' ,a.check_result ='%s' WHERE a.unique_identify ='%s' ;"""
INSERT_LOG = """INSERT INTO `log` (`id`,`log_level`,`time`,`name`,`description`) VALUES ('%s','%s','%s','%s','%s');"""
SELECT_INSTANCE_FROM_SYS_ID = """SELECT * FROM `monitor_instance` WHERE sys_id ='%s';"""
SELECT_VISUAL_FROM_CHECK_TYPE = """SELECT * FROM `monitor_visualization` WHERE check_type ='%s';"""
QUERY_MONITOR_INSTANCE = """SELECT * FROM `monitor_instance` where 1=1 """
QUERY_MONITOR_DETAIL_HALF_CONNECTION = """SELECT * FROM `monitor_detail` WHERE start_time BETWEEN '%s' AND '%s' AND ip = '%s' AND PORT = %s AND check_type = '%s';"""
QUERY_MONITOR_DETAIL_PING = """SELECT * FROM `monitor_detail` WHERE start_time BETWEEN '%s' AND '$s' AND ip = '%s'  AND check_type = '%s';"""