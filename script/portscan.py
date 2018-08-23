#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author:Y4er

import socket
import threading

oport = []


class MyThread(threading.Thread):

    def __init__(self, host, port, timeout):
        super(MyThread, self).__init__()
        self.host = host
        self.port = port
        self.timeout = timeout

    def run(self):
        portscan(self.host, self.port, self.timeout)


def portscan(ip, port, timeout):
    # 开放端口
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket()
        s.connect((ip, port))
        print('[+] {} is open.'.format(port))
        oport.append(port)
        s.close()
        return oport
    except:
        pass


def_ports = [21, 22, 23, 25, 80, 110, 137, 138, 139, 443, 445, 873, 888, 1025, 1433, 1521, 2082, 2083, 2222, 3306,
             3311, 3312, 3389, 4899, 5432, 5900, 6379, 7001, 7002, 7778, 8000, 8080, 8888, 11211, 27017, 43958,
             50000, 65500]


def run(thread, ip, timeout):
    threads = []
    for index, port in enumerate(def_ports):
        # timeout 超时5秒
        t = MyThread(ip, port, 5)
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return list(set(oport))
