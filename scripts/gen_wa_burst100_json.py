#!/usr/bin/env python3
"""Generate WhatsApp send URLs for burst-100 WA drafts."""
import json
import re
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTREACH = ROOT / "outreach"
slugs_file = ROOT / "leads" / "burst100_slugs.txt"
slugs = slugs_file.read_text(encoding="utf-8").strip().splitlines()
items = []
for slug in slugs:
    p = OUTREACH / f"wa-{slug}.txt"
    if not p.exists():
        continue
    lines = p.read_text(encoding="utf-8").splitlines()
    mobile = None
    for line in lines:
        m = re.search(r"\(\+(\d+)\)", line)
        if m:
            mobile = m.group(1)
            break
    body = "\n".join(lines[5:]).strip()
    url = f"https://web.whatsapp.com/send?phone={mobile}&text={urllib.parse.quote(body)}"
    items.append({"slug": slug, "mobile": mobile, "url": url})
(ROOT / "scripts" / "wa_burst100_urls.json").write_text(json.dumps(items, indent=2), encoding="utf-8")
print(len(items))
