import socket

COMMON_PORTS = {21:"FTP",22:"SSH",23:"Telnet",25:"SMTP",53:"DNS",80:"HTTP",110:"POP3",143:"IMAP",443:"HTTPS",445:"SMB",3306:"MySQL",5432:"PostgreSQL",6379:"Redis",8080:"HTTP-Alt"}

def scan_ports(host, ports, timeout=0.5):
    results=[]
    for port in ports:
        try:
            with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout); state="OPEN" if sock.connect_ex((host,port))==0 else "CLOSED"
        except (OSError,socket.gaierror): state="ERROR"
        results.append({"port":port,"state":state,"service":COMMON_PORTS.get(port,"Unknown")})
    return results

def scan(host): return scan_ports(host,list(COMMON_PORTS))
