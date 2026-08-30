#!/usr/bin/env python3
"""Update outreach drafts: Caisson branding, pricing, channel notes."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTREACH = ROOT / "outreach"

CHANNELS = {
    "kg-plumbing-gas": "Facebook preferred (corporate email may DMARC-block @gmail.com). Email fallback: info@kgplumbingandgas.com.au",
    "mh-plumbing-services": "Facebook only (no public phone or email)",
    "jaymichel-hair": "Facebook preferred (corporate email may DMARC-block @gmail.com)",
    "b-the-barber": "Instagram (Fresha booking only — no email found)",
    "bsparkz-electrics": "Facebook preferred",
    "canham-eatery": "Facebook only",
    "champion-barber-shop": "SMS preferred (0470 135 042). Facebook if listed",
    "cut-above-grooming": "Facebook preferred",
    "dagostino-electrical": "Facebook preferred",
    "kazzs-jamaican-kitchen": "Facebook preferred",
    "lash-generation": "Instagram (Fresha booking only)",
    "lumi-brow-studio": "Instagram (Fresha booking only)",
    "mech-mobile": "SMS (0407 878 188)",
    "megs-dog-walking": "SMS (0422 855 420)",
    "paws-in-the-park": "SMS (0406 540 024)",
    "that-girl-lashess": "Instagram (Fresha booking only)",
    "yundie-dc-gardening": "SMS (0436 438 748)",
}

DISCOUNT = (
    "Happy to do a good bloke discount if the price is the only thing holding you back — just ask."
)

SIGNATURE = """Cheers,
Edison Rees
Caisson · Perth
freddison200@gmail.com"""


def channel_type(note: str) -> str:
    low = note.lower()
    if low.startswith("sms"):
        return "SMS"
    if low.startswith("instagram"):
        return "Instagram"
    if "facebook only" in low or low.startswith("facebook"):
        return "Facebook"
    return "Email"


def fix_pricing_line(line: str) -> str:
    line = line.replace("`$650", "$650")
    if "$650" in line and DISCOUNT.split("—")[0].strip() not in line:
        if line.rstrip().endswith("."):
            return line.rstrip() + " " + DISCOUNT
        return line.rstrip() + ". " + DISCOUNT
    return line


def update_draft(path: Path, slug: str) -> bool:
    channel_note = CHANNELS.get(slug)
    if not channel_note:
        return False

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    out: list[str] = []
    i = 0

    # Header block
    out.append("DRAFT ONLY - DO NOT SEND WITHOUT EDISON APPROVAL ON DISCORD")
    out.append(f"CHANNEL: {channel_type(channel_note)}")
    out.append(f"PRIMARY: {channel_type(channel_note)} (prefer/simultaneous — not email backup)")
    out.append(f"CHANNEL NOTE: {channel_note}")

    # Preserve TO / DEMO / Subject from original header
    for line in lines[1:]:
        if line.startswith(("TO:", "DEMO:", "Subject:")):
            if line not in out:
                out.append(line)

    # Find body start after header block
    while i < len(lines):
        line = lines[i]
        if line.startswith(("DRAFT", "CHANNEL", "TO:", "DEMO:", "Subject:", "---", "Profile:")):
            i += 1
            continue
        if line.strip() == "":
            i += 1
            continue
        if line.startswith("Hi,") or line.startswith("Hi "):
            break
        i += 1

    body: list[str] = []
    while i < len(lines):
        line = lines[i]
        if line.startswith("Cheers,"):
            break
        if "`$650" in line or "$650" in line:
            line = fix_pricing_line(line)
        body.append(line)
        i += 1

    # Trim trailing blanks before signature
    while body and body[-1].strip() == "":
        body.pop()

    out.extend(body)
    out.append("")
    out.append(SIGNATURE)

    new_text = "\n".join(out) + "\n"
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def update_facebook_template() -> None:
    path = OUTREACH / "facebook-message-template.txt"
    text = """DRAFT ONLY - DO NOT SEND WITHOUT EDISON APPROVAL ON DISCORD
CHANNEL: Facebook
PRIMARY: Facebook (prefer/simultaneous — not email backup)
CHANNEL NOTE: Facebook Messenger PRIMARY — often beats email (corporate DMARC blocks @gmail.com)

Hi, quick one.

I am Edison from Caisson, web developer in Perth. I noticed you are on Facebook but do not have a proper website yet.

I built a free preview for you here:
https://edisonrees.github.io/caisson-web/demos/kg-plumbing-gas/

If you like it I can get it live for $650 one-off. Happy to do a good bloke discount if the price is the only thing holding you back — just ask. If not, ignore this and sorry for the bother.

Cheers,
Edison Rees
Caisson · Perth
"""
    path.write_text(text, encoding="utf-8")


def main() -> None:
    updated = []
    for path in sorted(OUTREACH.glob("email-*.txt")):
        slug = path.stem.replace("email-", "")
        if update_draft(path, slug):
            updated.append(path.name)

    update_facebook_template()
    updated.append("facebook-message-template.txt")

    print(f"Updated {len(updated)} outreach files:")
    for name in updated:
        print(f"  {name}")


if __name__ == "__main__":
    main()
