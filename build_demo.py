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


def service_item(title: str, desc: str) -> str:
    return f"""<article class="service-item">
  <h3>{title}</h3>
  <p>{desc}</p>
</article>"""


def review_item(text: str, author: str, source: str = "") -> str:
    source_line = f' <span>({source})</span>' if source else ""
    return f"""<blockquote class="review-item">
  <p>"{text}"</p>
  <cite>{author}{source_line}</cite>
</blockquote>"""


def apply_replacements(content: str, lead: dict) -> str:
    replacements = {
        "{{BUSINESS_NAME}}": lead["name"],
        "{{TAGLINE}}": lead.get("tagline", f"Trusted {lead.get('industry', 'local')} in Perth"),
        "{{META_DESCRIPTION}}": lead.get(
            "meta",
            f"{lead['name']}. Professional {lead.get('industry', 'services')} in {lead.get('city', 'Perth')}.",
        ),
        "{{CITY}}": lead.get("city", "Perth"),
        "{{INDUSTRY}}": lead.get("industry", "Local services"),
        "{{HERO_HEADLINE}}": lead.get("hero_headline", f"Trusted local {lead.get('industry', 'service')}"),
        "{{HERO_SUBHEAD}}": lead.get(
            "hero_subhead",
            "Fast response, fair pricing, and work you can trust. Call now for a free quote.",
        ),
        "{{CTA_PRIMARY}}": lead.get("cta", f"Call {lead.get('phone_display', 'now')}"),
        "{{PHONE_RAW}}": lead.get("phone_raw", ""),
        "{{PHONE_DISPLAY}}": lead.get("phone_display", ""),
        "{{EMAIL}}": lead.get("email", f"hello@{lead['slug'].replace('-', '')}.com.au"),
        "{{YEARS}}": str(lead.get("years", 10)),
        "{{RATING}}": str(lead.get("rating", "4.9")),
        "{{ABOUT_TEXT}}": lead.get(
            "about",
            f"{lead['name']} has been serving {lead.get('city', 'Perth')} with reliable, professional service. "
            "We are fully licensed, locally owned, and proud of our reputation for honest work.",
        ),
        "{{SERVICE_AREA}}": lead.get("service_area", "Perth metro and surrounds"),
        "{{HOURS}}": lead.get("hours", "Mon-Fri 7am-6pm, Sat 8am-2pm, 24/7 emergencies"),
        "{{ADDRESS}}": lead.get("address", "Perth, WA"),
    }
    for key, value in replacements.items():
        content = content.replace(key, value)
    return content


def build_site(lead: dict) -> Path:
    slug = lead["slug"]
    out = DEMOS / slug
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(TEMPLATE, out)

    services_html = "\n          ".join(
        service_item(s["title"], s["desc"]) for s in lead.get("services", [])
    )

    reviews = lead.get("reviews", [])
    if reviews:
        reviews_html = '<div class="review-list">\n          ' + "\n          ".join(
            review_item(r["text"], r["author"], r.get("source", "")) for r in reviews
        ) + "\n        </div>"
    else:
        reviews_html = ""

    html_path = out / "index.html"
    html = html_path.read_text(encoding="utf-8")
    html = apply_replacements(html, lead)
    html = html.replace("{{SERVICES_HTML}}", services_html)
    html = html.replace("{{REVIEWS_HTML}}", reviews_html)
    html_path.write_text(html, encoding="utf-8")

    for legal in ("privacy.html", "terms.html"):
        legal_path = out / legal
        legal_path.write_text(apply_replacements(legal_path.read_text(encoding="utf-8"), lead), encoding="utf-8")

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
