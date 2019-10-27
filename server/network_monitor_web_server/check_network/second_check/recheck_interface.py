# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     recheck_interface
   Description :
   Author :       'li'
   date：          2019/10/25
-------------------------------------------------
   Change Activity:
                   2019/10/25:
-------------------------------------------------
"""
from check_network.second_check.ping_check import final_ping_check
from check_network.second_check.tcp_check import final_tcp_check


def get_success_and_fail_result(results):
    """
    recheck result
    :param results:
    :return:
    """
    success_results = []
    fail_results = []
    for res in results:
        is_success = res.is_success
        if is_success:
            success_results.append(res)
        else:
            fail_results.append(res)
    return success_results, fail_results


def recheck_failed_results(fail_results):
    """
    recheck failed results
    :param fail_results:
    :return:
    """
    for res in fail_results:
        check_type = res.check_type
        ip = res.ip
        if check_type == 'ping':
            recheck_res = final_ping_check(ip)
        else:
            port = int(res.port)
            recheck_res = final_tcp_check(ip, port)
        if recheck_res:
            res.is_success = True
            res.interval = 99
    return fail_results
