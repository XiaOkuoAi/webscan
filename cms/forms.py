# ! usr/bin/env python
#  -*- coding: utf-8 -*-
# @Author  : Y4er
# @File    : forms.py

from django import forms


class DomainForm(forms.Form):
    domain = forms.CharField(label="域名")


class PortForm(forms.Form):
    ip = forms.CharField(label="IP")
    num = forms.CharField(label="线程数")
    timeout = forms.CharField(label="超时数")


class OtherdomainForm(forms.Form):
    domain = forms.CharField(label="请输入你要查询的IP或域名")


class FuckcmsForm(forms.Form):
    domain = forms.CharField(label="请输入IP或域名")
