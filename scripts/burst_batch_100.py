#!/usr/bin/env python3
"""Burst batch: add 29 WA leads (71->100), WA/IG outreach drafts only (no FB)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = ROOT / "leads" / "targets.json"
LEADS_FILE = ROOT / "leads" / "burst100_leads.json"
OUTREACH = ROOT / "outreach"
DEMO_BASE = "https://edisonrees.github.io/macrosa-web/demos"


def is_real_mobile(lead: dict) -> bool:
    raw = lead.get("phone_raw", "")
    if not raw.startswith("+614"):
        return False
    if raw.startswith("+614000000"):
        return False
    return True


def wa_draft(lead: dict) -> str:
    slug = lead["slug"]
    name = lead["name"]
    city = lead.get("city", "Perth")
    return f"""DRAFT ONLY - DO NOT SEND WITHOUT EDISON APPROVAL ON DISCORD
CHANNEL: WhatsApp
MOBILE: {lead.get('phone_display', '')} ({lead.get('phone_raw', '')})
DEMO: {DEMO_BASE}/{slug}/

Hi, quick one from Edison at Caisson (web dev in Perth).

I came across {name} around {city}. You're doing great work but don't have a proper website when locals search Google.

Built a free preview:
{DEMO_BASE}/{slug}/ 

$180 one-off (Basic: mobile site, contact form, deployment) if you want it live. Medium is $250 if you want basic support, Google indexing and your own domain. Rebuilding previews with upgraded tooling tomorrow at 7pm Perth, so shout if you want this locked in. No stress if not for you.

Cheers,
Edison · Caisson · Perth
"""


def ig_draft(lead: dict) -> str:
    slug = lead["slug"]
    name = lead["name"]
    city = lead.get("city", "Perth")
    ig = lead.get("instagram", lead.get("source", ""))
    return f"""DRAFT ONLY - DO NOT SEND WITHOUT EDISON APPROVAL ON DISCORD
CHANNEL: Instagram DM
PROFILE: {ig}
DEMO: {DEMO_BASE}/{slug}/

Hi, quick one. I'm Edison from Caisson (web dev in Perth).

I came across {name} on Instagram. You're doing solid work in {city} but don't have a proper website when people search near me.

Built a free preview:
{DEMO_BASE}/{slug}/ 

$180 one-off (Basic: mobile site, contact form, deployment) if you want it live. Medium is $250 if you want basic support, Google indexing and your own domain. Rebuilding previews with upgraded tooling tomorrow at 7pm Perth, so shout if you want this one locked in. No stress if not for you.

Cheers,
Edison · Caisson · Perth
"""


def main() -> None:
    new_leads = json.loads(LEADS_FILE.read_text(encoding="utf-8"))
    existing = json.loads(TARGETS.read_text(encoding="utf-8"))
    slugs = {l["slug"] for l in existing}
    added = []
    for lead in new_leads:
        if lead["slug"] in slugs:
            print(f"SKIP duplicate: {lead['slug']}")
            continue
        existing.append(lead)
        added.append(lead)
        slugs.add(lead["slug"])

    TARGETS.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")
    print(f"Added {len(added)} leads to targets.json ({len(existing)} total)")

    wa_count = ig_count = 0
    for lead in added:
        slug = lead["slug"]
        if is_real_mobile(lead):
            (OUTREACH / f"wa-{slug}.txt").write_text(wa_draft(lead), encoding="utf-8")
            wa_count += 1
            print(f"Draft: wa-{slug}.txt")
        if lead.get("instagram"):
            (OUTREACH / f"ig-{slug}.txt").write_text(ig_draft(lead), encoding="utf-8")
            ig_count += 1
            print(f"Draft: ig-{slug}.txt")

    slugs_file = ROOT / "leads" / "burst100_slugs.txt"
    slugs_file.write_text("\n".join(l["slug"] for l in added), encoding="utf-8")
    print(f"WA drafts: {wa_count} | IG drafts: {ig_count} | Slugs: {slugs_file}")


if __name__ == "__main__":
    main()
