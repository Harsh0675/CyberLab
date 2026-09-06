import socket

def analyze_dns(host,port=53):
    result={"target":host,"port":port,"available":False,"addresses":[]}
    try:
        result["addresses"]=sorted({i[4][0] for i in socket.getaddrinfo(host,None)}); result["available"]=True
    except socket.gaierror: pass
    return result
