# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     monitor_instance
   Description :
   Author :       'li'
   date：          2019/9/27
-------------------------------------------------
   Change Activity:
                   2019/9/27:
-------------------------------------------------
"""
__author__ = 'li'
INSERT_MONITOR_INSTANCE = """insert  into `monitor_instance`(`id`,`sys_id`,`sys_name`,`description`,`ip`,`port`,`type`,`interval`,`is_use`) values  ('%s','%s','%s','%s','%s',%s,'%s',%s,%s);"""
UPDATE_MONITOR_INSTANCE = """UPDATE   `monitor_instance` SET `id`='%s',`sys_id`='%s',`sys_name`='%s',`description`='%s',`ip`='%s',`port`=%s,`type`='%s',`interval`=%s,`is_use`=%s WHERE  `id`='%s';"""
DELETE_MONITOR_INSTANCE = """DELETE FROM monitor_instance WHERE `id`='%s'"""
QUERY_REAL_TIME_MONITOR_RESULT_BASE_SQL = """SELECT 
 * 
FROM(
  SELECT 
    a.*,b.check_result,b.start_time,b.interval AS response_time
  FROM
    (SELECT 
      * 
    FROM
      `monitor_instance` 
    WHERE is_use = 1) AS a LEFT JOIN
    (SELECT 
      * 
    FROM
      `monitor_visualization`) AS b ON a.ip = b.ip AND a.port = b.port  AND a.type = b.check_type
  WHERE a.ip = b.ip 
    AND a.port = b.port 
    AND a.type = b.check_type) AS t where 1=1  """
