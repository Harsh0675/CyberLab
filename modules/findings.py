RULES={21:("MEDIUM","FTP exposed","Prefer SFTP/FTPS and restrict access."),23:("HIGH","Telnet exposed","Disable Telnet and use SSH."),25:("MEDIUM","SMTP exposed","Restrict mail service access and verify relay controls."),80:("INFO","HTTP exposed","Use HTTPS for sensitive communication."),110:("MEDIUM","POP3 exposed","Prefer encrypted mail protocols."),143:("MEDIUM","IMAP exposed","Prefer encrypted mail protocols."),445:("HIGH","SMB exposed","Restrict SMB to trusted hosts/networks."),3306:("HIGH","MySQL exposed","Restrict database access to trusted systems."),5432:("HIGH","PostgreSQL exposed","Restrict database access to trusted systems."),6379:("HIGH","Redis exposed","Restrict Redis to trusted systems and authenticate it.")}

def analyze_findings(open_ports,services=None):
    return [{"severity":RULES[p][0],"port":p,"title":RULES[p][1],"recommendation":RULES[p][2]} for p in open_ports if p in RULES]
def analyze(open_ports,services=None): return analyze_findings(open_ports,services)
