#!/usr/bin/env python3
"""Generate IG deploy list for burst-100 (IG-only, no real WA mobile)."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTREACH = ROOT / "outreach"
TARGETS = json.loads((ROOT / "leads" / "targets.json").read_text(encoding="utf-8"))
slugs = set((ROOT / "leads" / "burst100_slugs.txt").read_text(encoding="utf-8").strip().splitlines())
by_slug = {l["slug"]: l for l in TARGETS}

def is_real_mobile(lead):
    raw = lead.get("phone_raw", "")
    return raw.startswith("+614") and not raw.startswith("+614000000")

items = []
for slug in slugs:
    if is_real_mobile(by_slug[slug]):
        continue
    p = OUTREACH / f"ig-{slug}.txt"
    if not p.exists():
        continue
    lines = p.read_text(encoding="utf-8").splitlines()
    profile = lines[2].split("PROFILE:", 1)[1].strip() if len(lines) > 2 else ""
    body = "\n".join(lines[5:]).strip()
    items.append({"slug": slug, "profile": profile, "body": body})

(ROOT / "scripts" / "ig_burst100.json").write_text(json.dumps(items, indent=2), encoding="utf-8")
print(len(items))
