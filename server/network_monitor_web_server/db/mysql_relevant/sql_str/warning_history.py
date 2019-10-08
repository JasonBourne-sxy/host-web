# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     warning_history
   Description :
   Author :       'li'
   date：          2019/9/27
-------------------------------------------------
   Change Activity:
                   2019/9/27:
-------------------------------------------------
"""
__author__ = 'li'
INSERT_WARNING_HISTORY = """insert  into `warning_history` (`id`,`sys_id`,`sys_name`,`description`,`check_type`,`ip`,`port`,`check_time`,`check_result`,`comment`,`warning_type`,`interval`) values  ('%s','%s','%s','%s','%s','%s',%s,'%s','%s','%s','%s','%s');"""
UPDATE_WARNING_HISTORY = """update `warning_history` set `id`='%s',`sys_id`='%s',`sys_name`='%s',`description`='%s',`check_type`='%s',`ip`='%s',`port`=%s,`check_time`='%s',`check_result`='%s',`comment`='%s',`warning_type`='%s',`interval`='%s' where id =='%s';"""
SELECT_WARNING_HISTORY_BASE = """SELECT * FROM `warning_history` where 1=1 """
