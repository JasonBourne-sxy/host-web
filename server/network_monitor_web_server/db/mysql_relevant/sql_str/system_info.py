# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     system_info
   Description :
   Author :       'li'
   date：          2019/9/27
-------------------------------------------------
   Change Activity:
                   2019/9/27:
-------------------------------------------------
"""
__author__ = 'li'

INSERT_SYSTEM_INFO = """insert  into `system_info`(`id`,`name`,`manager`,`telephone`,`job_number`) values  ('%s','%s','%s','%s','%s');"""
UPDATE_SYSTEM_INFO = """UPDATE `system_info` SET `id`='%s',`name`='%s',`manager`='%s',`telephone`='%s',`job_number`='%s' WHERE  `id`='%s';"""
DELETE_SYSTEM_INFO = """DELETE FROM system_info WHERE `id`='%s'"""
SELECT_BASE_SYSTEM_INFO = """SELECT * FROM `system_info` WHERE 1=1 """