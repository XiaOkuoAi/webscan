# ! usr/bin/env python
#  -*- coding: utf-8 -*-
# @Author  : Y4er
# @File    : otherdomain.py
import requests, json, socket,re

API = 'http://www.webscan.cc/?action=query'
IP = 'http://www.webscan.cc/?action=getip'

def getip(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except:
        pass


def cduan(ip):
    cduaninfo = []
    a = ".".join(ip.split(".")[0:-1]) + "."
    for i in range(1, 5):
        ip = a + str(i)
        print(ip)
        cduaninfo.append(run(ip))
        print(cduaninfo)
    return cduaninfo


def run(ip):
    data = {
        'ip': ip,
    }
    try:
        req = requests.get(API, params=data,timeout=200).text
        if req.startswith(u'\ufeff'):
            req = req.encode('utf8')[3:].decode('utf8')
        info = json.loads(req)
        return info
    except:
        return info