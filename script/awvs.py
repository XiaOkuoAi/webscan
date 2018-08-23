# ! usr/bin/env python
#  -*- coding: utf-8 -*-
import requests, json
import requests.packages.urllib3.exceptions
import time

requests.packages.urllib3.disable_warnings()

API = 'https://localhost:3443/api/v1'
headers = {
    'X-Auth': '1986ad8c0a5b3df4d7028d5f3c06e936c99948011f94043849aea5e8a54b92363',
    'content-type': 'application/json'
}


def gettarget():
    # 获取全部目标
    req = requests.get(API + '/targets', headers=headers, verify=False)
    infos = json.loads(req.text)
    targets = []
    for info in infos['targets']:
        print(info['target_id'], info['address'], info['description'], info['last_scan_date'])


def getscans():
    req = requests.get(API + '/scans', headers=headers, verify=False)
    scans = json.loads(req.text)
    scan_list = []
    for scan in scans['scans']:
        scanid = scan['scan_id']
        address = scan['target']['address']
        description = scan['target']['description']
        status = scan['current_session']['status']
        scan_dict = {'scanid': scanid, 'address': address, 'description': description, 'status': status}
        scan_list.append(scan_dict)
    return scan_list


def scan_del(scan_id):
    req = requests.delete(API + '/scans/' + scan_id, headers=headers, verify=False)
    if req.status_code == 204:
        return True
    else:
        return False

#停止扫描
def scan_stop(scan_id):
    req = requests.post(API + '/scans/' + scan_id + '/abort', headers=headers, verify=False)
    print(req.text)
    if req.status_code == 204:
        return True
    else:
        return False
#添加扫描
def scan_add(target):
    data = {'address': target, 'description': '', 'criticality': 10}
    r = requests.post(url=API + '/targets', timeout=10,
                      verify=False, headers=headers, data=json.dumps(data))
    if r.status_code == 201:
        target_id =  json.loads(r.text)['target_id']
        data = {'target_id': target_id, 'profile_id': "11111111-1111-1111-1111-111111111111",
                'schedule': {'disable': False, 'start_date': None, 'time_sensitive': False}}
        try:
            r = requests.post(url=API + '/scans', timeout=10,
                              verify=False, headers=headers, data=json.dumps(data))
            if r.status_code == 201:
                print('[-] OK, 扫描任务已经启动...')
                return True
            else:
                return False
        except Exception as e:
            print(e)

#生成
def bg(scanid):
    #生成报告
    try:
        data = {'template_id': '11111111-1111-1111-1111-111111111111',
                'source': {'list_type': 'scans', 'id_list': [scanid]}}
        r = requests.post(url=API + '/reports', timeout=10,
                          verify=False, headers=headers, data=json.dumps(data))
        if r.status_code == 201:
            download(r.headers['Location'])
            return True
        else:
            return False
    except Exception as e:
        print(e)

def download(path):
    # 下载报告
    try:
        r = requests.get(url=API.replace('/api/v1', '') + path,
                         timeout=10, verify=False, headers=headers)
        response = json.loads(r.text)
        report_id = response['report_id']
        target = response['source']['description']
        url = API.replace('/api/v1', '') + '/reports/download/'
        print('[-] 报告生成中...')
        # 等待报告生成
        while True:
            time.sleep(5)
            _r = request('/reports/' + report_id)
            name = json.loads(_r.text)['source']['description'].replace(';','')
            if json.loads(_r.text)['status'] == 'completed':
                res = requests.get(url=url + report_id + '.pdf', verify=False, timeout=10)
                if res.status_code == 200:
                    print('[-] OK, 报告下载成功.')
                    name = name.replace(':','_').replace('/','_')
                    with open('报告'+'/'+name + '.pdf', 'wb') as f:
                        f.write(res.content)
                    break
    except Exception as e:
        print(e)

def request(path):
    try:
        return requests.get(url=API + path, timeout=10,
                            verify=False, headers=headers)
    except Exception as e:
        print(e)

def api_getsessionid(scan_id):
    r = request('/scans/'+scan_id)
    req = json.loads(r.text)
    return req['current_session']['scan_session_id']


def api_getvulns(scan_id,scan_session_id):
    r = request("/scans/"+scan_id+"/results/"+scan_session_id+"/vulnerabilities")
    req = json.loads(r.text)
    print(req)
    return req['vulnerabilities']