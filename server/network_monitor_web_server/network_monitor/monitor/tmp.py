# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     tmp
   Description :
   Author :       'li'
   date：          2019/9/16
-------------------------------------------------
   Change Activity:
                   2019/9/16:
-------------------------------------------------
"""
__author__ = 'li'
from scapy.all import *


def haddle_tcp(x):
    """
    x
    :param x:
    :return:
    """
    src = x['IP'].src
    srcPort = x['IP'].dst
    des = x['IP'].dst
    ip = x['IP']
    sp = ip.sport
    dp = ip.dport
    tcp = x['TCP']
    ack = tcp.ack
    syn = tcp.flags
    print(syn)
    return dp


index = 1


def haddle_icmp(x):
    """
    x
    :param x:
    :return:
    """
    global index
    print(index)
    index = index + 1
    ip = x['ICMP']
    print(x)


#
dpkt = sniff(filter='tcp[tcpflags]&(tcp-syn)!=0 and tcp[tcpflags]&(tcp-ack)!=0', prn=haddle_tcp)
# dpkt = sniff(filter='icmp', prn=haddle_icmp)
