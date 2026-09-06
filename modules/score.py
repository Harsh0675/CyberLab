SEVERITY_POINTS={"HIGH":18,"MEDIUM":9,"LOW":4,"INFO":1}

def score_findings(findings,http=None,tls=None):
    deduction=sum(SEVERITY_POINTS.get(f["severity"],0) for f in findings)
    if http and http.get("available"):
        deduction += sum(2 for v in http.get("headers",{}).values() if v=="MISSING")
    if tls and tls.get("available") and tls.get("deprecated_protocol"): deduction += 10
    score=max(0,min(100,100-deduction)); grade="A" if score>=90 else "B" if score>=80 else "C" if score>=70 else "D" if score>=60 else "F"
    return {"score":score,"grade":grade,"method":"Rule-based indicators; not proof of compromise."}
