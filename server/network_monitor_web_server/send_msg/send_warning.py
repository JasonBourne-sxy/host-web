# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     send_warning
   Description :
   Author :       'li'
   date：          2019/9/24
-------------------------------------------------
   Change Activity:
                   2019/9/24:
-------------------------------------------------
"""
import json
import os
import urllib

__author__ = 'li'
# !/usr/bin/python
# coding=UTF-8

import requests


def send_msg_to_qyweixin(touser_list, title, content):
    # set language environment
    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
    # start call API
    SOCKET_HOST = "172.24.19.2"
    SOCKET_PORT = "80"
    url = 'http://' + SOCKET_HOST + ':' + SOCKET_PORT + '/WeitSrv/api/v1/queue/push.do'
    title = str(title)
    content = str(content)
    for touser in touser_list:
        touser = str(touser)
        textmod = {"title": title, "touser": touser, "content": content}
        textmod = json.dumps(textmod)
        header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
                       "Content-Type": "application/json"}
        res = requests.post(url, data=textmod, headers=header_dict)
        print(res)
        # parse json object
        res_dict = json.loads(res)
        return_code = res_dict["code"]
        # process the result
        if return_code == 'SUCCESS':
            print("Send Message To User " + touser + " Successfully")
        else:
            print("Send Message To User " + touser + " Fail")


if __name__ == '__main__':
    touser_list = '01639'
    title = 'title test'
    content ="""t: 用于设定超时时间， 单位为秒，当发起一个get请求时可以设置一个timeout时间， 如果在timeout时间内请求内容没有返回， 将产生一个timeout的异常。t: 用于设定超时时间， 单位为秒，当发起一个get请求时可以设置一个timeout时间， 如果在timeout时间内请求内容没有返回， 将产生一个timeout的异常。t: 用于设定超时时间， 单位为秒，当发起一个get请求时可以设置一个timeout时间， 如果在timeout时"""
    print(len(content))
    # 弥补库
    title = title.replace("Problem:", "[告警]")
    title = title.replace("Resolved:", "[告警消除]")
    title = title.replace("Updated problem:", "[告警更新]")

    touser_list = touser_list.split(",")
    send_msg_to_qyweixin(touser_list, title, content)
