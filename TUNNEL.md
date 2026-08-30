# Macrosa preview tunnel

**Started:** 30 Aug 2026

Cloudflared quick tunnel pointing at local `serve.py` (port 8765).

| URL | Purpose |
|-----|---------|
| https://recreational-solutions-annie-achieved.trycloudflare.com/site/ | Agency landing page |
| https://recreational-solutions-annie-achieved.trycloudflare.com/demos/kg-plumbing-gas/ | KG Plumbing demo |
| https://recreational-solutions-annie-achieved.trycloudflare.com/demos/mh-plumbing-services/ | MH Plumbing demo |
| https://recreational-solutions-annie-achieved.trycloudflare.com/demos/jaymichel-hair/ | Jaymichel Hair demo |

**Note:** Quick tunnels expire when the cloudflared process stops. Restart with:

```
cd C:\Users\ediso\Downloads\Macrosa
python serve.py
cloudflared tunnel --url http://localhost:8765
```

Update this file with the new URL after restart.

**GitHub Pages (permanent):** https://edisonrees.github.io/macrosa-web/
