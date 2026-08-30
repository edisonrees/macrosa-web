#!/usr/bin/env python3
"""Serve Macrosa demos locally for preview."""

import http.server
import socketserver
import webbrowser
from pathlib import Path

PORT = 8765
ROOT = Path(__file__).resolve().parent

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}/site/index.html"
        print(f"Serving Macrosa at http://localhost:{PORT}/")
        print(f"Agency: {url}")
        print(f"Demo:   http://localhost:{PORT}/demos/historic-plumbing/index.html")
        webbrowser.open(url)
        httpd.serve_forever()
