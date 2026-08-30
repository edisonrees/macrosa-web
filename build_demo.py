#!/usr/bin/env python3
"""Generate demo websites from template + lead data."""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
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
    "electrician": {
        "theme_color": "#0c1218",
        "theme_vars": """
  --ink: #0c1218;
  --accent: #e8b84a;
  --accent-deep: #b8860b;
  --cream: #eef1f4;
  --muted: #8a9aab;
""".strip(),
    },
    "gardener": {
        "theme_color": "#0e140f",
        "theme_vars": """
  --ink: #0e140f;
  --accent: #6b9e5a;
  --accent-deep: #3d6b32;
  --cream: #eef2eb;
  --muted: #8fa088;
""".strip(),
    },
    "mechanic": {
        "theme_color": "#101014",
        "theme_vars": """
  --ink: #101014;
  --accent: #c44b3f;
  --accent-deep: #8b2e26;
  --cream: #eeedec;
  --muted: #9a9590;
""".strip(),
    },
    "pet": {
        "theme_color": "#14100c",
        "theme_vars": """
  --ink: #14100c;
  --accent: #c9a06c;
  --accent-deep: #8b6b3f;
  --cream: #f5f0e8;
  --muted: #a89a88;
""".strip(),
    },
    "cafe": {
        "theme_color": "#120e0c",
        "theme_vars": """
  --ink: #120e0c;
  --accent: #b8734a;
  --accent-deep: #7a4a2e;
  --cream: #f4ede6;
  --muted: #a89888;
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
    return f"""<figure class="carousel-slide shield img-loading">
  <img src="{src}" alt="{caption}" draggable="false" loading="lazy" data-img-load />
  <iframe class="img-shield" src="data:text/html," title="" tabindex="-1" aria-hidden="true" sandbox loading="lazy"></iframe>
  <figcaption>{caption}</figcaption>
</figure>"""


def gallery_thumb(src: str, caption: str, index: int) -> str:
    active = " is-active" if index == 0 else ""
    return f"""<button type="button" class="gallery-thumb{active}" data-gallery-thumb aria-label="{caption}">
  <img src="{src}" alt="" loading="lazy" />
  <span>{caption}</span>
</button>"""


def faq_item(question: str, answer: str) -> str:
    return f"""<div class="reveal">
  <dt>{question}</dt>
  <dd>{answer}</dd>
</div>"""


DEFAULT_FAQ = [
    (
        "Do you offer free quotes?",
        "Yes. We can usually give you a ballpark over the phone and confirm after seeing the job if needed.",
    ),
    (
        "What areas do you cover?",
        "We work across our local service area. Call or message with your suburb and we will confirm availability.",
    ),
    (
        "Are you licensed and insured?",
        "Yes. We carry the licences and insurance required for this trade and can talk you through it on request.",
    ),
]


def apply(content: str, mapping: dict[str, str]) -> str:
    for key, value in mapping.items():
        content = content.replace(key, value)
    return content


def build_site(lead: dict) -> Path:
    slug = lead["slug"]
    out = DEMOS / slug
    assets_backup: Path | None = None
    if out.exists():
        assets_src = out / "assets"
        if assets_src.is_dir():
            backup_root = Path(tempfile.mkdtemp())
            assets_backup = backup_root / "assets"
            shutil.copytree(assets_src, assets_backup)
        shutil.rmtree(out)
    shutil.copytree(TEMPLATE, out)
    if assets_backup is not None:
        dst_assets = out / "assets"
        if dst_assets.exists():
            shutil.rmtree(dst_assets)
        shutil.copytree(assets_backup, dst_assets)
        shutil.rmtree(assets_backup.parent)

    theme_key = lead.get("theme", lead.get("image_set", "plumber"))
    theme = THEMES.get(theme_key, THEMES["plumber"])

    services_html = "\n        ".join(
        service_item(i + 1, s["title"], s["desc"]) for i, s in enumerate(lead.get("services", []))
    )

    gallery = lead.get("gallery_captions", [])
    gallery_paths = [f"assets/gallery-{i}.jpg" for i in range(1, 5)]
    gallery_captions = [
        gallery[i] if i < len(gallery) else f"Recent work by {lead['name']}"
        for i in range(len(gallery_paths))
    ]
    gallery_html = "\n              ".join(
        gallery_slide(path, caption) for path, caption in zip(gallery_paths, gallery_captions)
    )
    gallery_thumbs_html = "\n          ".join(
        gallery_thumb(path, caption, i) for i, (path, caption) in enumerate(zip(gallery_paths, gallery_captions))
    )

    faq_entries = lead.get("faq") or DEFAULT_FAQ
    faq_html = "\n        ".join(faq_item(q, a) for q, a in faq_entries)

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
        "{{GALLERY_THUMBS_HTML}}": gallery_thumbs_html,
        "{{FAQ_HTML}}": faq_html,
    }

    for fname in ("index.html", "privacy.html", "terms.html"):
        path = out / fname
        if path.exists():
            path.write_text(apply(path.read_text(encoding="utf-8"), mapping), encoding="utf-8")

    return out


def main() -> None:
    leads_file = ROOT / "leads" / "targets.json"
    slug_filter: set[str] = set()
    args = sys.argv[1:]
    if args and not args[0].endswith(".json"):
        slug_filter = set(args)
    elif args:
        leads_file = Path(args[0])

    leads = json.loads(leads_file.read_text(encoding="utf-8"))
    if slug_filter:
        leads = [lead for lead in leads if lead["slug"] in slug_filter]
    built = []
    for lead in leads:
        path = build_site(lead)
        built.append({"slug": lead["slug"], "path": str(path), "name": lead["name"]})
        print(f"Built: {lead['name']} -> {path}")

    (ROOT / "leads" / "built.json").write_text(json.dumps(built, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
