# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     executor_pool
   Description :
   Author :       'li'
   date：          2019/9/12
-------------------------------------------------
   Change Activity:
                   2019/9/12:
-------------------------------------------------
"""
import time

__author__ = 'li'
from multiprocessing.pool import ThreadPool  # 导入线程池

EXECUTOR_POOL = ThreadPool(10)
