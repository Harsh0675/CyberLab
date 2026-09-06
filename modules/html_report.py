from pathlib import Path
import html

def save_html(data,path):
    rows=''.join(f"<tr><td>{p['port']}</td><td>{html.escape(p['service'])}</td><td>{p['state']}</td></tr>" for p in data.get('ports',[]))
    findings=''.join(f"<li><b>{html.escape(f['severity'])}</b> — {html.escape(f['title'])}: {html.escape(f['recommendation'])}</li>" for f in data.get('findings',[])) or '<li>No rule-based findings.</li>'
    score=data.get('score',{}); page=f'''<!doctype html><html><head><meta charset="utf-8"><title>CyberLab Security Report</title><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{{font-family:system-ui;background:#10141a;color:#eee;margin:0;padding:24px}}main{{max-width:900px;margin:auto;background:#181e27;padding:24px;border-radius:16px}}table{{width:100%;border-collapse:collapse}}th,td{{padding:10px;border-bottom:1px solid #333;text-align:left}}.card{{margin:18px 0;padding:16px;background:#11161d;border-radius:12px}}</style></head><body><main><h1>🛡️ CyberLab Security Report</h1><div class="card"><b>Target:</b> {html.escape(data.get('target',''))}<br><b>Generated:</b> {html.escape(data.get('timestamp',''))}<br><b>Score:</b> {score.get('score','-')}/100 — Grade {score.get('grade','-')}</div><h2>Ports</h2><table><tr><th>Port</th><th>Service</th><th>State</th></tr>{rows}</table><h2>Findings</h2><ul>{findings}</ul><p><small>Rule-based assessment only; findings are indicators, not proof of compromise.</small></p></main></body></html>'''
    path=Path(path); path.write_text(page,encoding='utf-8'); return path

def save(target,open_ports): return save_html({"tool":"CyberLab","target":target,"open_ports":open_ports},Path(__file__).resolve().parents[1]/"reports"/"scan.html")
