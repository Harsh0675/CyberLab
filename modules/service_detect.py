import socket, ssl

def probe(host,port):
    try:
        if port==80:
            with socket.create_connection((host,port),timeout=2) as s:
                s.sendall(f"HEAD / HTTP/1.0\r\nHost: {host}\r\nConnection: close\r\n\r\n".encode())
                lines=s.recv(512).decode("utf-8","replace").splitlines(); return lines[0] if lines else "Connected (no banner)"
        if port==443:
            ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
            with socket.create_connection((host,port),timeout=2) as raw:
                with ctx.wrap_socket(raw,server_hostname=host) as s: return f"TLS {s.version()} | {s.cipher()[0]}"
        with socket.create_connection((host,port),timeout=2) as s:
            s.settimeout(1)
            try: s.sendall(b"\r\n"); data=s.recv(256)
            except socket.timeout: return "Connected (no banner)"
            if not data: return "Connected (no banner)"
            return "".join(c if c.isprintable() else "." for c in data.decode("utf-8","replace"))[:100]
    except ssl.SSLError as e: return f"TLS error: {type(e).__name__}"
    except (OSError,socket.timeout): return "No response"

def detect_services(host,ports): return [{"port":p,"details":probe(host,p)} for p in ports]
def run(host,ports): return detect_services(host,ports)
