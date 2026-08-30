#!/usr/bin/env python3
"""Download licensed stock photos for demo sites."""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Unsplash (free to use per Unsplash license)
IMAGE_SETS = {
    "plumber": {
        "hero": "https://images.unsplash.com/photo-1615529328331-f8917597711f?auto=format&fit=crop&w=1800&q=80",
        "about": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=1200&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1581578731548-c64695cc6952?auto=format&fit=crop&w=1200&q=80",
        ],
    },
    "salon": {
        "hero": "https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=1800&q=80",
        "about": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=1200&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1516975080664-ed2fc6a32937?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1519699047748-de8e457a634e?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1562322140-8baeececf3df?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1487412947147-5cebf100ffc2?auto=format&fit=crop&w=1200&q=80",
        ],
    },
}


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "MacrosaDemoBuilder/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        dest.write_bytes(resp.read())


def fetch_for_lead(lead: dict, out_dir: Path) -> dict:
    niche = lead.get("image_set", "plumber")
    pack = IMAGE_SETS[niche]
    assets = out_dir / "assets"
    mapping = {}

    download(pack["hero"], assets / "hero.jpg")
    download(pack["about"], assets / "about.jpg")
    mapping["hero"] = "assets/hero.jpg"
    mapping["about"] = "assets/about.jpg"

    gallery_paths = []
    for i, url in enumerate(pack["gallery"], start=1):
        path = assets / f"gallery-{i}.jpg"
        download(url, path)
        gallery_paths.append(f"assets/gallery-{i}.jpg")
    mapping["gallery"] = gallery_paths
    return mapping


def main() -> None:
    leads = json.loads((ROOT / "leads" / "targets.json").read_text(encoding="utf-8"))
    for lead in leads:
        out = ROOT / "demos" / lead["slug"]
        print(f"Images: {lead['name']}")
        fetch_for_lead(lead, out)


if __name__ == "__main__":
    main()
