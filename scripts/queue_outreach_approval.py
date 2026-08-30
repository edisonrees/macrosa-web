#!/usr/bin/env python3
"""Queue top-3 outreach approval bundles to Discord. Does NOT send outreach."""

import subprocess
import sys
from pathlib import Path

SEND = Path(r"C:\cursor-agent-tools\scripts\discord-bridge\send.py")
OUTREACH = Path(__file__).resolve().parent.parent / "outreach"


def read_body(path: Path) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    body: list[str] = []
    started = False
    for line in lines:
        if line.startswith(("Hi,", "Hi ")):
            started = True
        if started:
            body.append(line)
    return "\n".join(body).strip()


def queue(text: str) -> None:
    r = subprocess.run(
        [sys.executable, str(SEND), text],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    print(r.stdout or r.stderr or "(queued)")
    if r.returncode != 0:
        raise SystemExit(r.returncode)


MESSAGES = [
    """**OUTREACH APPROVAL 1/3 — Jaymichel Hair and Beauty**

**Channels found**
• Facebook: https://www.facebook.com/jaymichelhairandbeauty/ (PRIMARY)
• Instagram: https://www.instagram.com/jaymichelhairandbeauty/ (secondary)
• Email: hello.jaymichel@gmail.com (simultaneous)
• Phone: 0418 957 020 (not sending SMS unless you say)

**Demo:** https://edisonrees.github.io/macroa-web/demos/jaymichel-hair/
**Price:** $650 one-off + good bloke discount

---
**FB Messenger** (send first)
```
{fb_jay}
```

---
**Instagram DM** (same day, after FB)
```
{ig_jay}
```

---
**Email** → hello.jaymichel@gmail.com
**Subject:** website preview for Jaymichel Hair and Beauty
```
{email_jay}
```

Reply **approve jaymichel** / **edit jaymichel** / **skip jaymichel**""",
    """**OUTREACH APPROVAL 2/3 — KG Plumbing and Gas**

**Channels found**
• Facebook: https://www.facebook.com/KGPlumbingandGas (PRIMARY — 1K followers)
• Instagram: none found (business name tagged by others only)
• Email: admin@kgplumbingandgas.com.au (FB listing; draft has info@kgplumbingandgas.com.au)
• Phone: 0432 172 527 (FB; targets had old landline)

**Demo:** https://edisonrees.github.io/macroa-web/demos/kg-plumbing-gas/
**Price:** $650 one-off + good bloke discount

---
**FB Messenger** (send first)
```
{fb_kg}
```

---
**Email** → info@kgplumbingandgas.com.au (or admin@ if you prefer)
**Subject:** put together a website preview for KG Plumbing and Gas
```
{email_kg}
```

Reply **approve kg** / **edit kg** / **skip kg**""",
    """**OUTREACH APPROVAL 3/3 — D'Agostino Electrical**

**Channels found**
• Facebook: https://www.facebook.com/dagostinoelectrical (PRIMARY — 1K followers)
• Instagram: https://www.instagram.com/dagostinoelectrical/ (secondary)
• Email: dagostinoelectrical@bigpond.com (from FB — not in original draft)
• Phone: 0400 236 886 (no SMS draft)

**Demo:** https://edisonrees.github.io/macroa-web/demos/dagostino-electrical/
**Price:** $650 one-off + good bloke discount

---
**FB Messenger** (send first)
```
{fb_da}
```

---
**Instagram DM** (same day, after FB)
```
{ig_da}
```

---
**Email** → dagostinoelectrical@bigpond.com
**Subject:** website preview for D'Agostino Electrical
```
{email_da}
```

Reply **approve dagostino** / **edit dagostino** / **skip dagostino**""",
]


def main() -> None:
    fb_jay = read_body(OUTREACH / "fb-jaymichel-hair.txt")
    ig_jay = read_body(OUTREACH / "ig-jaymichel-hair.txt")
    email_jay = read_body(OUTREACH / "email-jaymichel-hair.txt")
    fb_kg = read_body(OUTREACH / "fb-kg-plumbing-gas.txt")
    email_kg = read_body(OUTREACH / "email-kg-plumbing-gas.txt")
    fb_da = read_body(OUTREACH / "fb-dagostino-electrical.txt")
    ig_da = read_body(OUTREACH / "ig-dagostino-electrical.txt")
    email_da = read_body(OUTREACH / "email-dagostino-electrical.txt")

    payloads = [
        MESSAGES[0].format(fb_jay=fb_jay, ig_jay=ig_jay, email_jay=email_jay),
        MESSAGES[1].format(fb_kg=fb_kg, email_kg=email_kg),
        MESSAGES[2].format(fb_da=fb_da, ig_da=ig_da, email_da=email_da),
    ]

    for i, msg in enumerate(payloads, 1):
        print(f"Queuing {i}/3...")
        queue(msg)

    print("All 3 approval bundles queued to Discord.")


if __name__ == "__main__":
    main()
