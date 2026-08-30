#!/usr/bin/env python3
"""Serve Caisson demos locally for preview."""

import http.server
import socketserver
import webbrowser
from pathlib import Path

PORT = 8765
HOST = "127.0.0.1"
ROOT = Path(__file__).resolve().parent

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

if __name__ == "__main__":
    with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
        url = f"http://{HOST}:{PORT}/site/index.html"
        print(f"Serving Caisson at http://{HOST}:{PORT}/")
        print(f"Agency: {url}")
        print(f"KG demo: http://{HOST}:{PORT}/demos/kg-plumbing-gas/")
        webbrowser.open(url)
        httpd.serve_forever()
