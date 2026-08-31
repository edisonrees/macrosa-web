#!/usr/bin/env python3
"""Patch burst-100 WA/IG statuses in pipeline.md after deploy."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
path = ROOT / "leads" / "pipeline.md"
text = path.read_text(encoding="utf-8")

wa_sent = {
    "Michael McDonald Hair": "Sent (WhatsApp, 2026-08-31)",
    "Tash Maree Hair Design": "Sent (WhatsApp, 2026-08-31)",
    "The Little Brow Studio": "Sent (WhatsApp, 2026-08-31)",
    "Mat's Mobile Dog Grooming": "Sent (WhatsApp, 2026-08-31)",
    "Yorkshire Painting Service": "Sent (WhatsApp, 2026-08-31)",
    "Perth Hidden Beauty": "Sent (WhatsApp, 2026-08-31)",
    "Waggy Tails Doggy Wash": "Sent (WhatsApp, 2026-08-31)",
    "Manbun Mowing": "Sent (WhatsApp, 2026-08-31)",
}

wa_skipped = {
    "Leading Edge Mechanical": "Skipped — not on WhatsApp (+61 408 558 119)",
}

ig_sent = {
    "Luna Bakes": "Sent (IG DM, 2026-08-31)",
    "Fretzy Fadez": "Sent (IG DM, 2026-08-31)",
    "Haus of Solace": "Sent (IG DM, 2026-08-31)",
    "Niko's Confectionery": "Sent (IG DM, 2026-08-31)",
}

ig_skipped = {
    "Moey's Home Studio": "Skipped — no Instagram handle (Fresha only)",
}

for name, status in {**wa_sent, **wa_skipped, **ig_sent, **ig_skipped}.items():
    pattern = re.compile(rf"(\| {re.escape(name)} \|[^\n]*\| )[^|]+( \|)")
    text, n = pattern.subn(rf"\1{status}\2", text, count=1)
    if n == 0:
        print(f"WARN: no row for {name}")

path.write_text(text, encoding="utf-8")
print("patched", len(wa_sent) + len(ig_sent) + len(ig_skipped), "rows")
