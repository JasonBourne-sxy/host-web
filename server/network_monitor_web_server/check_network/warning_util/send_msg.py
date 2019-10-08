# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     send_msg
   Description :
   Author :       'li'
   date：          2019/10/4
-------------------------------------------------
   Change Activity:
                   2019/10/4:
-------------------------------------------------
"""
import json
import os
import threading

import requests


def __send_msg_to_qyweixin(touser_list, title, content):
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
        # parse json object
        res_dict = json.loads(res)
        return_code = res_dict["code"]
        # process the result
        if return_code == 'SUCCESS':
            print("Send Message To User " + touser + " Successfully")
        else:
            print("Send Message To User " + touser + " Fail")


def send_msg_to_qyweixin(touser_list, title, content):
    # threading.Thread(target=__send_msg_to_qyweixin,
    #                  args=(touser_list, title, content)).start()
    pass
