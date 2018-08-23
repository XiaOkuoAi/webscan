from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from .forms import DomainForm, PortForm, OtherdomainForm, FuckcmsForm
from script import portscan, otherdomain
import requests
import json, os
from poc.main import *
from script.awvs import *
from script.fofa_api import *


def index(request):
    return render(request, 'index.html')


# cms识别
class Whatcms(View):
    form = DomainForm()

    def get(self, request):
        return render(request, 'whatcms.html', context={'form': self.form})

    def post(self, request):
        domain = request.POST['domain']
        info = self.cmsinfo(domain)
        msg = '查询失败，请检查域名是否有效，如果是第一次查询请等两分钟后再查下试试'
        if type(info) == dict:
            return render(request, 'whatcms.html', context={'form': self.form, 'info': info})
        else:
            return render(request, 'whatcms.html', context={'form': self.form, 'msg': msg})

    def cmsinfo(self, url):
        API = 'http://api.yunsee.cn/fingerApi/?token=KvblfJojHIecEfzaotSVA3kxO4Stnz&id=409'
        payload = {'level': '2', 'url': url}
        try:
            req = requests.get(API, params=payload, timeout=100)
            code = json.loads(req.text)['code']
            if code == 200:
                info = json.loads(req.text)['data']
                return info
        except:
            return None


# 端口扫描
class Portscan(View):
    form = PortForm()

    def get(self, request):
        return render(request, 'portscan.html', context={'form': self.form})

    def post(self, request):
        ip = request.POST['ip']
        num = request.POST['num']
        timeout = request.POST['timeout']
        ports = portscan.run(num, ip, timeout)
        return render(request, 'portscan.html', context={'form': self.form, 'ports': ports})


class Otherdomain(View):
    form = OtherdomainForm()

    def get(self, request):
        return render(request, 'otherdomain.html', context={'form': self.form})

    def post(self, request):
        domain = request.POST['domain']
        ip = otherdomain.getip(domain)
        info = otherdomain.run(ip)
        cduan = otherdomain.cduan(ip)
        return render(request, 'otherdomain.html',
                      context={'form': self.form, 'domain': domain, 'info': info, 'ip': ip, 'cduan': cduan})


class Fuckcms(View):
    def get(self, request):
        data = json.dumps(list(poclist.keys()))
        print(data)
        return render(request, 'fuckcms.html', context={'data': data})

    def post(self, request):
        return render(request, 'fuckcms.html')


@csrf_exempt
def api_cms(request):
    if request.method == 'POST':
        url = request.POST['url']
        type = request.POST['type']
        print(url, type)
        result = list(poclist.values())[int(type)](url).run()
        if '[+]' in result:
            status = 1
            return HttpResponse(json.dumps({"status": status, "pocresult": result}))
        else:
            result = '[-]没洞'
            status = 0
            return HttpResponse(json.dumps({"status": status, "pocresult": result}))


class Awvs(View):
    def get(self, request):
        scan_list = getscans()
        return render(request, 'awvs.html', context={'scan_list': scan_list})

    def post(self, request):
        return render(request, 'awvs.html')

@csrf_exempt
def del_scan(request):
    if request.method == 'POST':
        if scan_del(scan_id=request.POST['scanid']):
            print("删除成功")
            return HttpResponse(json.dumps({'code': 1}))
    else:
        print("删除失败")
        return HttpResponse(json.dumps({'code': 0}))

@csrf_exempt
def stop_scan(request):
    if request.method == 'POST':
        if scan_stop(scan_id=request.POST['scanid']):
            print("停止成功")
            return HttpResponse(json.dumps({'code': 1}))
    else:
        print("停止失败")
        return HttpResponse(json.dumps({'code': 0}))

@csrf_exempt
def add_scan(request):
    if request.method == 'POST':
        target= request.POST['target']
        print(target)
        if scan_add(target):
            print("添加成功")
            return HttpResponse(1)
    else:
        print("添加失败")
        return HttpResponse(0)
@csrf_exempt
def Presentation(request):
    if request.method == 'POST':
        scan_id = request.POST['scanid']
        print(scan_id)
        if bg(scan_id):
            print("导出成功")
            return HttpResponse(1)
        else:
            print("导出失败")
            return HttpResponse(0)

@csrf_exempt
def get_vluns(request):
    if request.method == 'POST':
        scan_id = request.POST['scanid']
        session_id = api_getsessionid(scan_id)
        vulns = api_getvulns(scan_id,session_id)
        return HttpResponse(json.dumps(vulns))

#fofa搜索
@csrf_exempt
def fofa(request):
    if request.method == 'POST':
        domain = request.POST['domain']
        fofa_content = fofa_api(domain)
        return render(request, 'fofa.html', context={'list': fofa_content})
    else:
        return render(request, 'fofa.html')