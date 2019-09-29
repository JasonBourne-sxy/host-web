# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     monitor_visualization
   Description :
   Author :       'li'
   date：          2019/9/27
-------------------------------------------------
   Change Activity:
                   2019/9/27:
-------------------------------------------------
"""
__author__ = 'li'
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
