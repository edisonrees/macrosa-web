#!/usr/bin/env python3
"""Quick lead research helper — scores businesses for outreach."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LEADS = ROOT / "leads" / "research.json"


def score_lead(lead: dict) -> int:
    s = 0
    if lead.get("phone"):
        s += 2
    if not lead.get("has_website"):
        s += 3
    elif lead.get("website_outdated"):
        s += 2
    if lead.get("email") or lead.get("facebook"):
        s += 1
    if lead.get("google_rating", 0) >= 4.0:
        s += 1
    if lead.get("active", True):
        s += 1
    return min(s, 5)


def main() -> None:
    if LEADS.exists():
        leads = json.loads(LEADS.read_text(encoding="utf-8"))
    else:
        leads = []

    if not leads:
        print("No leads in research.json yet. Add entries manually or via scrape.")
        return

    for lead in leads:
        lead["score"] = score_lead(lead)

    leads.sort(key=lambda x: x["score"], reverse=True)
    LEADS.write_text(json.dumps(leads, indent=2), encoding="utf-8")

    print(f"Scored {len(leads)} leads:\n")
    for l in leads:
        print(f"  [{l['score']}/5] {l['name']} — {l.get('phone', 'no phone')} — {l.get('niche', '?')}")


if __name__ == "__main__":
    main()
