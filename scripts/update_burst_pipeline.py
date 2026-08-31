#!/usr/bin/env python3
"""Append burst-70 rows to pipeline.md and fix channel priority."""

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent
slugs = (ROOT / "leads" / "burst70_slugs.txt").read_text(encoding="utf-8").strip().splitlines()
targets = {t["slug"]: t for t in json.loads((ROOT / "leads" / "targets.json").read_text(encoding="utf-8"))}

new_rows = []
for slug in slugs:
    t = targets[slug]
    phone = t.get("phone_display", "Contact via social")
    website = "Yes" if t.get("has_website") else "No"
    pr = t.get("phone_raw", "")
    wa_ok = pr.startswith("+614") and "4000000" not in pr and not pr.startswith("+618")
    ig = t.get("instagram")
    if wa_ok:
        ch = "WhatsApp"
        status = "Ready (WA draft)"
    elif ig:
        ch = "Instagram"
        status = f"Ready (IG draft)"
    else:
        ch = "Facebook"
        status = "Ready (FB draft)"
    new_rows.append(f"| {t['name']} | {phone} | {website} | ✅ | ✅ | {ch} | {status} |")

path = ROOT / "leads" / "pipeline.md"
text = path.read_text(encoding="utf-8")
text = text.replace("**51 leads in targets.json", "**70 leads in targets.json")
text = text.replace(
    "**Deploy (2026-08-31):** Light off-white theme live on all 51 demos + agency (`a7f7a70`). No outreach resend needed.",
    "**Burst batch (2026-08-31):** +19 WA leads (51→70), demos built and pushed. WA-first outreach on confirmed mobiles.\n\n**Deploy (2026-08-31):** Light off-white theme live on all demos + agency (`a7f7a70`).",
)
text = text.replace(
    """## Contact channel priority

1. **Instagram / Facebook** — PRIMARY. DM first or simultaneously; not as email backup.
2. **SMS** — listed mobile numbers (requires Edison approval)
3. **Email** — when found via Facebook About or ABN lookup; fallback only
4. **Phone** — highest conversion, needs Edison""",
    """## Contact channel priority

1. **WhatsApp** — PRIMARY when real AU mobile documented
2. **Facebook** — Messenger for FB-page leads
3. **Instagram** — DM when IG handle confirmed
4. **Email** — fallback when found via Facebook About or ABN lookup""",
)
insert_before = "\n## Contact channel priority"
if new_rows[0].split("|")[1].strip() not in text:
    text = text.replace(insert_before, "\n".join(new_rows) + insert_before)

path.write_text(text, encoding="utf-8")
print(f"Updated pipeline with {len(new_rows)} rows")
