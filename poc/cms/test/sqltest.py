# ! usr/bin/env python
#  -*- coding: utf-8 -*-
# @Author  : Y4er
# @File    : sqltest.py
import requests


class sqltest:
    def __init__(self, url):
        self.url = url

    def run(self):
        url = self.url
        data = "'"
        try:
            req1 = requests.get(url,timeout=10).headers['Content-Length']
            req2 = requests.get(url + data,timeout=10).headers['Content-Length']
            if req1 != req2:
                return '[+] 存在注入'
            else:
                return '[-]不存在注入'
        except:
            return '[-]访问异常'
