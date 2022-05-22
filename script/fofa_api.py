import pyfofa
def fofa_api(domain):
    import pyfofa
    email = ''
    key = ''
    search = pyfofa.FofaAPI(email, key)
    r = search.get_data("cert="+"'"+domain+"'", 10, "host,ip")['results']
    list = ["Host: {} IP：{}".format(host,ip) for host,ip in r]
    return list
