#!/usr/bin/env python3
"""One-shot: pivot outreach to Caisson tiered pricing (Aug 2026)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTREACH = ROOT / "outreach"

MEDIUM_SLUGS = {
    "b-the-barber",
    "canham-eatery",
    "jaymichel-hair",
    "kazzs-jamaican-kitchen",
    "lash-generation",
    "lumi-brow-studio",
    "that-girl-lashess",
}

EMAIL_MEDIUM = (
    "If you want it live, Medium is $250 one-off: everything in Basic plus basic support, "
    "Google indexing setup, and your own domain (you pay the domain cost upfront before I purchase it). "
    "Basic is $180 if you just need the site live. I am rebuilding previews with upgraded tooling "
    "tomorrow evening, so shout if you want this version locked in."
)

EMAIL_BASIC = (
    "If you want it live, Basic is $180 one-off: mobile-ready site, contact form, and deployment. "
    "Medium is $250 if you want basic support, Google indexing, and your own domain. "
    "I am rebuilding previews with upgraded tooling tomorrow evening, so shout if you want this version locked in."
)

FB_MEDIUM = (
    "If you like it I can get it live from $250 one-off (Medium: basic support, Google indexing, your own domain). "
    "Basic is $180 if you just need the site live. I am rebuilding previews with upgraded tooling tomorrow evening, "
    "so shout if you want this one locked in."
)

FB_BASIC = (
    "If you like it I can get it live from $180 one-off (Basic). Medium is $250 if you want basic support, "
    "Google indexing, and your own domain. I am rebuilding previews with upgraded tooling tomorrow evening, "
    "so shout if you want this one locked in."
)

IG_MEDIUM = (
    "$250 one-off (Medium: basic support, Google indexing, your own domain) if you want it live. "
    "Basic is $180. Rebuilding previews with upgraded tooling tomorrow evening, so shout if you want this one locked in."
)

IG_BASIC = (
    "$180 one-off (Basic) if you want it live. Medium is $250 with support, Google indexing, and your own domain. "
    "Rebuilding previews with upgraded tooling tomorrow evening, so shout if you want this one locked in."
)

PRICE_LINE = re.compile(
    r".*(\$650|good bloke|good-bloke).*",
    re.IGNORECASE,
)

DISCOUNT_FRAGMENT = re.compile(
    r"\s*Happy to do a good bloke discount[^.]*\.?\s*",
    re.IGNORECASE,
)


def slug_from_path(path: Path) -> str:
    name = path.stem
    for prefix in ("email-", "fb-", "ig-"):
        if name.startswith(prefix):
            return name[len(prefix) :]
    return name


def is_short(path: Path) -> bool:
    return path.name.startswith(("fb-", "ig-")) or path.name == "facebook-message-template.txt"


def rewrite_file(path: Path) -> bool:
    slug = slug_from_path(path)
    medium = slug in MEDIUM_SLUGS
    short = is_short(path)
    ig = path.name.startswith("ig-")

    if ig:
        new_price = IG_MEDIUM if medium else IG_BASIC
    elif short:
        new_price = FB_MEDIUM if medium else FB_BASIC
    else:
        new_price = EMAIL_MEDIUM if medium else EMAIL_BASIC

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    out: list[str] = []
    replaced = False
    skip_next_blank_after_price = False

    for line in lines:
        cleaned = DISCOUNT_FRAGMENT.sub("", line)
        cleaned = cleaned.replace("—", ", ").replace("–", ", ")
        if "$650" in cleaned or "good bloke" in cleaned.lower():
            if not replaced:
                if short and not ig:
                    suffix = ""
                    if "ignore this" in cleaned.lower() or "sorry for the bother" in cleaned.lower():
                        suffix = " If not, ignore this and sorry for the bother."
                    elif "no worries" in cleaned.lower():
                        suffix = " If not, no worries."
                    elif "no stress" in cleaned.lower():
                        suffix = " No stress if not for you."
                    out.append(new_price + suffix)
                elif ig:
                    tail = " No stress if not for you." if "no stress" in cleaned.lower() else ""
                    out.append(new_price + tail)
                else:
                    out.append(new_price)
                replaced = True
                skip_next_blank_after_price = False
            continue
        if "good bloke" in cleaned.lower():
            continue
        out.append(cleaned)

    new_text = "\n".join(out)
    if not new_text.endswith("\n"):
        new_text += "\n"

    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main() -> None:
    updated: list[str] = []
    patterns = ["email-*.txt", "fb-*.txt", "ig-*.txt", "facebook-message-template.txt"]
    for pattern in patterns:
        for path in sorted(OUTREACH.glob(pattern)):
            if rewrite_file(path):
                updated.append(path.name)
    print(f"Updated {len(updated)} outreach files:")
    for name in updated:
        print(f"  {name}")


if __name__ == "__main__":
    main()
