#!/usr/bin/env python3
"""Generate a demo website for a local business lead."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "template"
DEMOS = ROOT / "demos"


def service_card(icon: str, title: str, desc: str) -> str:
    return f"""<article class="service-card">
  <div class="service-icon">{icon}</div>
  <h3>{title}</h3>
  <p>{desc}</p>
</article>"""


def review_card(stars: int, text: str, author: str) -> str:
    return f"""<blockquote class="review-card">
  <div class="stars">{"★" * stars}{"☆" * (5 - stars)}</div>
  <p>"{text}"</p>
  <cite>— {author}</cite>
</blockquote>"""


def build_site(lead: dict) -> Path:
    slug = lead["slug"]
    out = DEMOS / slug
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(TEMPLATE, out)

    services_html = "\n          ".join(
        service_card(s["icon"], s["title"], s["desc"]) for s in lead.get("services", [])
    )
    reviews_html = "\n          ".join(
        review_card(r.get("stars", 5), r["text"], r["author"]) for r in lead.get("reviews", [])
    )

    replacements = {
        "{{BUSINESS_NAME}}": lead["name"],
        "{{TAGLINE}}": lead.get("tagline", f"Trusted {lead.get('industry', 'local')} in Perth"),
        "{{META_DESCRIPTION}}": lead.get(
            "meta",
            f"{lead['name']} — professional {lead.get('industry', 'services')} in {lead.get('city', 'Perth')}.",
        ),
        "{{CITY}}": lead.get("city", "Perth"),
        "{{INDUSTRY}}": lead.get("industry", "Local services"),
        "{{HERO_HEADLINE}}": lead.get("hero_headline", f"Perth's trusted {lead.get('industry', 'team')}"),
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
        "{{ABOUT_TEXT}}": lead.get(
            "about",
            f"{lead['name']} has been serving {lead.get('city', 'Perth')} with reliable, professional service. "
            "We're fully licensed, locally owned, and proud of our reputation for honest work.",
        ),
        "{{SERVICE_AREA}}": lead.get("service_area", "Perth metro & surrounds"),
        "{{HOURS}}": lead.get("hours", "Mon–Fri 7am–6pm · Sat 8am–2pm · 24/7 emergencies"),
        "{{ADDRESS}}": lead.get("address", "Perth, WA"),
        "{{SERVICES_HTML}}": services_html,
        "{{REVIEWS_HTML}}": reviews_html,
    }

    html_path = out / "index.html"
    html = html_path.read_text(encoding="utf-8")
    for k, v in replacements.items():
        html = html.replace(k, v)
    html_path.write_text(html, encoding="utf-8")
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
