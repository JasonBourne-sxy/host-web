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
from multiprocessing.pool import ThreadPool  # 导入线程池


def create_executor_pool(threading_num=20):
    """
    create executor pool
    :param threading_num:
    :return:
    """
    pool = ThreadPool(threading_num)
    return pool
