#!/usr/bin/env python3
"""Queue top-3 outreach approval messages to Discord. Does not send outreach."""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SEND = Path(r"C:\cursor-agent-tools\scripts\discord-bridge\send.py")
OUTBOX = Path(r"C:\cursor-agent-tools\scripts\discord-bridge\data\outbox.jsonl")

DEMO = "https://edisonrees.github.io/macroa-web/demos/{slug}/"

FB_JAY = """Hi, quick one.

I am Edison from Caisson, web developer in Perth. I came across Jaymichel Hair and Beauty on Facebook. You have great reviews but no standalone website yet.

I built a free preview for you here:
{DEMO}

If you like it I can get it live for $650 one-off. Happy to do a good bloke discount if the price is the only thing holding you back, just ask. If not, ignore this and sorry for the bother.

Cheers,
Edison Rees
Caisson · Perth"""

FB_KG = """Hi, quick one.

I am Edison from Caisson, web developer in Perth. I found KG Plumbing and Gas on Facebook. You are getting good work in Mandurah and Peel but do not have a proper website yet.

I built a free preview for you here:
{DEMO}

If you like it I can get it live for $650 one-off. Happy to do a good bloke discount if the price is the only thing holding you back, just ask. If not, ignore this and sorry for the bother.

Cheers,
Edison Rees
Caisson · Perth"""

FB_DAG = """Hi, quick one.

I am Edison from Caisson, web developer in Perth. I found D'Agostino Electrical on Facebook. You have good hipages reviews around Wanneroo but no proper website yet.

I built a free preview for you here:
{DEMO}

If you like it I can get it live for $650 one-off. Happy to do a good bloke discount if the price is the only thing holding you back, just ask. If not, ignore this and sorry for the bother.

Cheers,
Edison Rees
Caisson · Perth"""

EMAIL_JAY = """Hi Helen,

I am Edison, a web developer based in Perth.

I came across Jaymichel Hair and Beauty on Facebook. You have great reviews but no standalone website, which makes it harder for new clients to find you outside Facebook.

I made a preview site for you:

{DEMO}

It includes your phone number, email, services and a contact form. Happy for you to click through and tell me what you think.

If you want it live I charge $650 one-off. I can usually turn it around in a few days. Happy to do a good bloke discount if the price is the only thing holding you back, just ask.

No worries if you are not interested.

Cheers,
Edison Rees
Caisson · Perth
freddison200@gmail.com"""

EMAIL_KG = """Hi,

My name is Edison. I am a web developer in Perth.

I found KG Plumbing and Gas on Facebook and noticed you are getting good work in the Mandurah and Peel area but do not have a proper website yet.

I built a preview site for you anyway, no charge to look at it:

{DEMO}

It has your services, phone number, contact form and works on mobile.

If you want it live properly I can do that for $650 one-off. That includes hosting setup and any small changes you want. Happy to do a good bloke discount if the price is the only thing holding you back, just ask.

If it is not for you, no stress at all.

Cheers,
Edison Rees
Caisson · Perth
freddison200@gmail.com"""

EMAIL_DAG = """Hi Peter,

I am Edison, a web developer in Perth.

I found D'Agostino Electrical on Facebook. You have good hipages reviews around Wanneroo but no proper website, so people searching Google still land on directories instead of you.

I built a preview site for your business:

{DEMO}

Services, phone number, mobile layout and a contact form. Free to look at.

If you want it live I charge $650 one-off. I handle hosting and any small text changes. Happy to do a good bloke discount if the price is the only thing holding you back, just ask.

Let me know what you think or ignore this if it is not useful.

Cheers,
Edison Rees
Caisson · Perth
freddison200@gmail.com"""

LEADS = [
    {
        "name": "Jaymichel Hair and Beauty",
        "slug": "jaymichel-hair",
        "channels": [
            ("Facebook Messenger", "https://www.facebook.com/jaymichelhairandbeauty/", FB_JAY),
            ("Instagram DM", "https://www.instagram.com/jaymichelhairandbeauty/", FB_JAY),
            ("Email", "hello.jaymichel@gmail.com", EMAIL_JAY, "website preview for Jaymichel Hair and Beauty"),
        ],
    },
    {
        "name": "KG Plumbing and Gas",
        "slug": "kg-plumbing-gas",
        "channels": [
            ("Facebook Messenger", "https://www.facebook.com/KGPlumbingandGas", FB_KG),
            ("Email", "info@kgplumbingandgas.com.au", EMAIL_KG, "put together a website preview for KG Plumbing and Gas"),
        ],
    },
    {
        "name": "D'Agostino Electrical",
        "slug": "dagostino-electrical",
        "channels": [
            ("Facebook Messenger", "https://www.facebook.com/dagostinoelectrical", FB_DAG),
            ("Instagram DM", "https://www.instagram.com/dagostinoelectrical/", FB_DAG),
            ("Email", "dagostinoelectrical@bigpond.com", EMAIL_DAG, "website preview for D'Agostino Electrical"),
        ],
    },
]


def queue(text: str) -> None:
    subprocess.run([sys.executable, str(SEND), text], check=True)


def main() -> None:
    before = OUTBOX.stat().st_size if OUTBOX.exists() else 0
    queued = 0

    queue("**OUTREACH APPROVAL QUEUE (top 3)**\nCaisson · $650 one-off · good bloke discount available\nReply APPROVE + lead name + channel to send. Nothing sent yet.")

    for lead in LEADS:
        demo = DEMO.format(slug=lead["slug"])
        queue(f"\n---\n**{lead['name']}** (`{lead['slug']}`)\nDemo: {demo}\nChannels found below. Awaiting your approval per channel.")

        for ch in lead["channels"]:
            kind, target, body = ch[0], ch[1], ch[2]
            subject = ch[3] if len(ch) > 3 else None
            copy = body.format(DEMO=demo)
            header = f"**[{lead['name']}] {kind}**\nTarget: {target}"
            if subject:
                header += f"\nSubject: {subject}"
            header += "\n\n```\n" + copy + "\n```\n\nReply: `APPROVE {lead['slug']} {kind.split()[0].lower()}`"
            queue(header)
            queued += 1

    after = OUTBOX.stat().st_size if OUTBOX.exists() else 0
    print(f"Queued {queued + 1} Discord messages (outbox +{after - before} bytes)")


if __name__ == "__main__":
    main()
