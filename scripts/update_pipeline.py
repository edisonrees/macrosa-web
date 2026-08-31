#!/usr/bin/env python3
"""Regenerate pipeline.md table from targets.json."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = json.loads((ROOT / "leads" / "targets.json").read_text(encoding="utf-8"))
OUTREACH = ROOT / "outreach"


def is_real_mobile(lead: dict) -> bool:
    raw = lead.get("phone_raw", "")
    if not raw.startswith("+614"):
        return False
    if raw.startswith("+614000000"):
        return False
    return True


def primary_channel(lead: dict) -> str:
    if is_real_mobile(lead):
        return "WhatsApp"
    if lead.get("instagram"):
        return "Instagram"
    return "Email"


BURST100 = set(
    (ROOT / "leads" / "burst100_slugs.txt").read_text(encoding="utf-8").strip().splitlines()
) if (ROOT / "leads" / "burst100_slugs.txt").exists() else set()

# Status from prior session + new batch defaults
STATUS = {
    "kg-plumbing-gas": "Sent (FB Messenger, 2026-08-30)",
    "jaymichel-hair": "Sent (FB Messenger, 2026-08-30)",
    "dagostino-electrical": "Closed — already engaged another provider (2026-08-30)",
    "bsparkz-electrics": "Sent (FB Messenger, 2026-08-30)",
    "champion-barber-shop": "Sent (FB Messenger, 2026-08-30)",
    "kazzs-jamaican-kitchen": "Sent (FB Messenger, 2026-08-30)",
    "cut-above-grooming": "Sent (FB Messenger, 2026-08-30)",
    "canham-eatery": "Skipped — working site",
    "mh-plumbing-services": "Skipped — working site / wrong lead",
    "mech-mobile": "Skipped — no FB page found",
    "yundie-dc-gardening": "Sent (FB Messenger, 2026-08-30)",
    "paws-in-the-park": "Skipped — working site",
    "megs-dog-walking": "Skipped — no FB page found",
    "lumi-brow-studio": "Sent (IG DM, 2026-08-30)",
    "that-girl-lashess": "Sent (IG DM, 2026-08-30)",
    "lash-generation": "Sent (IG DM, 2026-08-30)",
    "b-the-barber": "Sent (IG DM, 2026-08-30)",
    "pureflow-plumbing": "Sent (IG DM, 2026-08-30)",
    "lashes-by-monique": "Sent (IG DM, 2026-08-30)",
    "amy-j-lash-beauty": "Sent (IG DM, 2026-08-30)",
    "lashes-by-aimee-tahlia": "Sent (IG DM, 2026-08-30)",
    "alexandria-gardens": "Sent (IG DM, 2026-08-30)",
    "larissas-barbershop": "Sent (IG DM, 2026-08-30)",
    "miiso-nail-studio": "Sent (IG DM, 2026-08-30)",
    "studio-b-nails": "Sent (IG DM, 2026-08-30)",
    "thp-auto-mobile": "Skipped — FB page unavailable",
    "jds-pressure-cleaning": "Skipped — working site (jdspressurewashingandcleaning.com)",
    "ace-mobile-mechanic": "Skipped — FB page unavailable",
    "cambos-mobile-mechanic": "Skipped — FB page unavailable",
    "perth-mech-mobile": "Skipped — working site (perthmech.com.au)",
}

IG_SLUGS = {
    "halo-lashes", "flick-and-flutter-lash", "kikididit", "studio-eire", "lilly-c-nails",
    "fluffy-dog-grooming", "pampered-with-love-pet", "pimp-my-paws", "sash-hair-studio",
    "a-blended-place", "lisas-mane-studio", "prep-perth", "juicy-beauty", "pooches-beauty-bar",
    "belashed-by-km", "md-beauty-studio", "white-feather-beauty", "tay-luxe-studio",
    "gelato-nails-subiaco", "salty-dog-pet-salon",
}

FB_NEW = {
    "one-and-all-cleaning",
}

rows = []
for lead in TARGETS:
    slug = lead["slug"]
    name = lead["name"]
    phone = lead.get("phone_display", "Contact via social")
    website = "Yes" if lead.get("has_website") else "No"
    demo = "✅"
    draft = "✅"
    if slug in STATUS:
        status = STATUS[slug]
        if "IG" in status or "Instagram" in status:
            ch = "Instagram"
        elif "FB" in status or "Facebook" in status:
            ch = "Facebook"
        else:
            ch = "Instagram" if lead.get("instagram") else ("Facebook" if "facebook" in lead.get("source", "") else "Email")
    elif slug in FB_NEW:
        ch = "Facebook"
        status = "Ready — draft in outreach/fb-*.txt"
    elif slug in IG_SLUGS:
        ch = "Instagram"
        ig = lead.get("instagram", "")
        handle = ig.split("instagram.com/")[-1].rstrip("/") if ig else slug
        status = f"Ready — draft in outreach/ig-{slug}.txt (@{handle})"
    elif slug in BURST100:
        ch = primary_channel(lead)
        if ch == "WhatsApp":
            status = f"Ready — draft in outreach/wa-{slug}.txt"
        elif ch == "Instagram":
            ig = lead.get("instagram", "")
            handle = ig.split("instagram.com/")[-1].rstrip("/") if ig else slug
            status = f"Ready — draft in outreach/ig-{slug}.txt (@{handle})"
        else:
            status = "Ready — no WA/IG channel"
    else:
        ch = primary_channel(lead) if is_real_mobile(lead) or lead.get("instagram") else (
            "Facebook" if "facebook" in lead.get("source", "") else "Instagram"
        )
        status = "Ready"

    rows.append(f"| {name} | {phone} | {website} | {demo} | {draft} | {ch} | {status} |")

n = len(TARGETS)
body = f"""# Lead pipeline tracker — Caisson

**{n} leads in targets.json | All demos built | Drafts in outreach/**

**Burst-100 batch (2026-08-31):** +29 Perth/WA leads (71→100). Demos built. WA-first outreach; Instagram for IG-handle leads without real mobile. Facebook suspended — no FB sends.

| Business | Phone | Website? | Demo | Draft | Channel | Status |
|----------|-------|----------|------|-------|---------|--------|
"""
body += "\n".join(rows)
body += """

## Contact channel priority

1. **WhatsApp** — PRIMARY when real WA mobile (+614, not placeholder)
2. **Instagram** — for IG-handle leads without WhatsApp mobile
3. **Email** — when found via Facebook About or ABN lookup; fallback only
4. **Phone call** — highest conversion, needs Edison
5. **Facebook** — SUSPENDED (account banned). Do not send.

## Pricing (Caisson)

- **Basic:** $180 one-off
- **Medium:** $250 one-off (support, Google indexing, custom URL)
- **Advanced:** $400 one-off (3-day sprint scope)
- Goal: $1,000 to $2,000 AUD in 3 days via volume + upsells

## Revenue tracker

| Date | Client | Amount | Status |
|------|--------|--------|--------|
| — | — | $0 / $1,000 | — |
"""

(ROOT / "leads" / "pipeline.md").write_text(body, encoding="utf-8")
print(f"pipeline.md updated: {n} leads")
