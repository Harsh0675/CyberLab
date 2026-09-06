import json
from pathlib import Path

def save_json(data,path):
    path=Path(path); path.write_text(json.dumps(data,indent=2),encoding="utf-8"); return path

def save(target,open_ports):
    from datetime import datetime
    base=Path(__file__).resolve().parents[1]/"reports"; base.mkdir(exist_ok=True)
    return save_json({"tool":"CyberLab","target":target,"open_ports":open_ports},base/f"scan_{datetime.now():%Y%m%d_%H%M%S}.json")
