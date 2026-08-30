#!/usr/bin/env python3
"""Generate demo websites from template + lead data."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "template"
DEMOS = ROOT / "demos"

THEMES = {
    "plumber": {
        "theme_color": "#0a1014",
        "theme_vars": """
  --ink: #0a1014;
  --accent: #c87533;
  --accent-deep: #8b4513;
  --cream: #eef2f0;
  --muted: #9aa8a0;
""".strip(),
    },
    "salon": {
        "theme_color": "#120c0e",
        "theme_vars": """
  --ink: #120c0e;
  --accent: #d4a5a5;
  --accent-deep: #9e6b6b;
  --cream: #f7efe6;
  --muted: #b9a59a;
""".strip(),
    },
}


def service_item(num: int, title: str, desc: str) -> str:
    return f"""<li class="reveal">
  <span class="service-mark">{num:02d}</span>
  <div>
    <h3>{title}</h3>
    <p>{desc}</p>
  </div>
</li>"""


def gallery_slide(src: str, caption: str) -> str:
    return f"""<figure class="carousel-slide shield">
  <img src="{src}" alt="{caption}" draggable="false" loading="lazy" />
  <iframe class="img-shield" src="data:text/html," title="" tabindex="-1" aria-hidden="true" sandbox loading="lazy"></iframe>
  <figcaption>{caption}</figcaption>
</figure>"""


def apply(content: str, mapping: dict[str, str]) -> str:
    for key, value in mapping.items():
        content = content.replace(key, value)
    return content


def build_site(lead: dict) -> Path:
    slug = lead["slug"]
    out = DEMOS / slug
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(TEMPLATE, out)

    theme_key = lead.get("theme", lead.get("image_set", "plumber"))
    theme = THEMES.get(theme_key, THEMES["plumber"])

    services_html = "\n        ".join(
        service_item(i + 1, s["title"], s["desc"]) for i, s in enumerate(lead.get("services", []))
    )

    gallery = lead.get("gallery_captions", [])
    gallery_paths = [f"assets/gallery-{i}.jpg" for i in range(1, 5)]
    gallery_html = "\n            ".join(
        gallery_slide(path, gallery[i] if i < len(gallery) else f"Recent work by {lead['name']}")
        for i, path in enumerate(gallery_paths)
    )

    logo = lead.get("logo_text") or lead["name"].split()[0].upper()

    mapping = {
        "{{BUSINESS_NAME}}": lead["name"],
        "{{LOGO_TEXT}}": logo,
        "{{TAGLINE}}": lead.get("tagline", f"{lead.get('industry', 'Services')} in {lead.get('city', 'Perth')}"),
        "{{META_DESCRIPTION}}": lead.get(
            "meta",
            f"{lead['name']}. {lead.get('industry', 'Local services')} in {lead.get('city', 'Perth')}.",
        ),
        "{{THEME_COLOR}}": theme["theme_color"],
        "{{THEME_VARS}}": theme["theme_vars"],
        "{{CITY}}": lead.get("city", "Perth"),
        "{{INDUSTRY}}": lead.get("industry", "Local services"),
        "{{HERO_HEADLINE}}": lead.get("hero_headline", lead["name"]),
        "{{HERO_SUBHEAD}}": lead.get(
            "hero_subhead",
            "Fast response, fair pricing, and work you can trust. Call now for a free quote.",
        ),
        "{{CTA_PRIMARY}}": lead.get("cta", f"Call {lead.get('phone_display', 'now')}"),
        "{{PHONE_RAW}}": lead.get("phone_raw", ""),
        "{{PHONE_DISPLAY}}": lead.get("phone_display", ""),
        "{{EMAIL}}": lead.get("email", f"hello@{slug.replace('-', '')}.com.au"),
        "{{YEARS}}": str(lead.get("years", 10)),
        "{{RATING}}": str(lead.get("rating", "4.9")),
        "{{ABOUT_HEADLINE}}": lead.get("about_headline", f"Local {lead.get('industry', 'experts')} you can trust"),
        "{{ABOUT_TEXT}}": lead.get(
            "about",
            f"{lead['name']} serves {lead.get('city', 'Perth')} with reliable, professional work.",
        ),
        "{{SERVICE_AREA}}": lead.get("service_area", "Perth metro and surrounds"),
        "{{HOURS}}": lead.get("hours", "Mon-Fri 7am-6pm, Sat 8am-2pm, 24/7 emergencies"),
        "{{ADDRESS}}": lead.get("address", "Perth, WA"),
        "{{HERO_IMAGE}}": "assets/hero.jpg",
        "{{ABOUT_IMAGE}}": "assets/about.jpg",
        "{{GALLERY_HEADLINE}}": lead.get("gallery_headline", "Work we stand behind"),
        "{{GALLERY_SUBHEAD}}": lead.get(
            "gallery_subhead",
            "A sample of the kind of jobs we take on every week across the local area.",
        ),
        "{{BAND_HEADLINE}}": lead.get("band_headline", "We answer the phone"),
        "{{BAND_TEXT}}": lead.get(
            "band_text",
            "Blocked drain, burst pipe, or planning a renovation? Call now and we will talk you through the next step.",
        ),
        "{{SERVICES_HTML}}": services_html,
        "{{GALLERY_HTML}}": gallery_html,
    }

    for fname in ("index.html", "privacy.html", "terms.html"):
        path = out / fname
        if path.exists():
            path.write_text(apply(path.read_text(encoding="utf-8"), mapping), encoding="utf-8")

    return out


def main() -> None:
    leads_file = ROOT / "leads" / "targets.json"
    if len(sys.argv) > 1:
        leads_file = Path(sys.argv[1])

    leads = json.loads(leads_file.read_text(encoding="utf-8"))
    built = []
    for lead in leads:
        path = build_site(lead)
        built.append({"slug": lead["slug"], "path": str(path), "name": lead["name"]})
        print(f"Built: {lead['name']} -> {path}")

    (ROOT / "leads" / "built.json").write_text(json.dumps(built, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
