import pyfofa
def fofa_api(domain):
    import pyfofa
    email = '1796900257@qq.com'
    key = '2bee09803e485cd94f1484249b70d74c'
    search = pyfofa.FofaAPI(email, key)
    r = search.get_data("cert="+"'"+domain+"'", 10, "host,ip")['results']
    list = ["Host: {} IP：{}".format(host,ip) for host,ip in r]
    return list
