# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     tcp_check
   Description :
   Author :       'li'
   date：          2019/10/21
-------------------------------------------------
   Change Activity:
                   2019/10/21:
-------------------------------------------------
"""
import socket


def final_tcp_check(ip, port):
    """
    final tcp check
    :param ip:
    :param port:
    :return:
    """
    client = socket.socket()
    client.settimeout(2)
    is_connected = True
    try:
        client.connect((ip, port))
    except:
        is_connected = False
    return is_connected
