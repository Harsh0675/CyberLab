import json
from pathlib import Path
HISTORY=Path(__file__).resolve().parents[1]/"scans"/"history.jsonl"
HISTORY.parent.mkdir(exist_ok=True)
def record(data,read_only=False):
    if read_only:
        if not HISTORY.exists(): return []
        return [json.loads(line) for line in HISTORY.read_text().splitlines() if line.strip()]
    with HISTORY.open("a",encoding="utf-8") as f: f.write(json.dumps(data)+"\n")
    return data
