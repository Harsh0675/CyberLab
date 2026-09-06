import http.client
HEADER_MAP={"HSTS":"Strict-Transport-Security","CSP":"Content-Security-Policy","X-Content-Type-Options":"X-Content-Type-Options","X-Frame-Options":"X-Frame-Options","Referrer-Policy":"Referrer-Policy"}

def audit_http(host,port=80):
    result={"available":False,"status":None,"headers":{}}
    try:
        conn=http.client.HTTPConnection(host,port,timeout=3); conn.request("HEAD","/"); resp=conn.getresponse(); headers={k.lower():v for k,v in resp.getheaders()}
        result["available"]=True; result["status"]=f"HTTP {resp.status} {resp.reason}"; result["headers"]={n:headers.get(h.lower(),"MISSING") for n,h in HEADER_MAP.items()}; conn.close()
    except (OSError,TimeoutError): pass
    return result
