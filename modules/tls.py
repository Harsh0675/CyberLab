"""TLS audit for authorized security assessments."""
import socket,ssl

def audit_tls(host,port=443,timeout=5):
    result={"host":host,"port":port,"status":"ok","protocol":None,"cipher":None,"certificate_verification":"NOT_COMPLETED"}
    try:
        ctx=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
        try: ctx.set_ciphers("DEFAULT:@SECLEVEL=1")
        except ssl.SSLError: pass
        with socket.create_connection((host,port),timeout=timeout) as raw:
            try:
                with ctx.wrap_socket(raw,server_hostname=host) as conn:
                    result["protocol"]=conn.version(); c=conn.cipher(); result["cipher"]=c[0] if c else None
                    if result["protocol"] in {"SSLv3","TLSv1","TLSv1.1"}: result["status"]="warning"; result["deprecated_protocol"]=True; result["finding"]="Deprecated TLS protocol negotiated."
                    return result
            except ssl.SSLError as exc:
                msg=str(exc)
                if "DH_KEY_TOO_SMALL" in msg or "dh key too small" in msg.lower():
                    return {"host":host,"port":port,"status":"warning","protocol":None,"cipher":None,"certificate_verification":"NOT_COMPLETED","finding":"Weak Diffie-Hellman parameters detected.","recommendation":"Upgrade or reconfigure the device to use sufficiently large DH parameters or modern ECDHE-based TLS.","error":msg}
                return {"host":host,"port":port,"status":"error","error":f"SSLError: {msg}"}
    except Exception as exc: return {"host":host,"port":port,"status":"error","error":f"{type(exc).__name__}: {exc}"}
