#!/usr/bin/env python3
"""Generate ig.me deploy URLs for burst-100 IG-only leads."""
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
items = json.loads((ROOT / "scripts" / "ig_burst100.json").read_text(encoding="utf-8"))
out = []
for item in items:
    handle = item["profile"].split("instagram.com/")[-1].rstrip("/")
    out.append({
        "slug": item["slug"],
        "handle": handle,
        "ig_me": f"https://ig.me/m/{handle}",
        "body": item["body"],
    })
(ROOT / "scripts" / "ig_burst100_deploy.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print(len(out))
