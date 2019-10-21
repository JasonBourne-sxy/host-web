# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     ping
   Description :
   Author :       'li'
   date：          2019/10/21
-------------------------------------------------
   Change Activity:
                   2019/10/21:
-------------------------------------------------
"""
from random import randint

from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import sr1


def final_ping_check(host):
    """
    final ping check
    :param host:
    :return:
    """
    ip_id, icmp_id, icmp_seq = randint(1, 65535), randint(1, 65535), randint(1, 65535)
    ping_packet = IP(dst=host, ttl=64, id=ip_id) / ICMP(id=icmp_id, seq=icmp_seq) / b'rootkit'
    result = sr1(ping_packet, verbose=False, timeout=2)
    if result is None:
        return False
    return True
