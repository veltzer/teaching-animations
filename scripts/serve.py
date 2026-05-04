#!/usr/bin/env python

"""
Serve _site/ over HTTP for local preview of the GitHub Pages site.

Run from the repo root. The build must have produced _site/ first
(e.g. via `rsconstruct build`).

Usage:
    scripts/serve.py            # serve on http://localhost:8000
    scripts/serve.py --port 9000
"""

import argparse
import http.server
import socketserver
import sys
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = ROOT / "_site"


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve _site/ for local preview.")
    parser.add_argument("--port", type=int, default=8000, help="port to listen on (default: 8000)")
    parser.add_argument("--no-open", action="store_true", help="do not open the browser automatically")
    args = parser.parse_args()

    if not SITE_DIR.exists():
        print(f"Error: {SITE_DIR.relative_to(ROOT)} does not exist. Run 'rsconstruct build' first.", file=sys.stderr)
        sys.exit(1)

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(SITE_DIR), **kw)

    url = f"http://localhost:{args.port}/"
    with socketserver.TCPServer(("", args.port), Handler) as httpd:
        print(f"Serving {SITE_DIR.relative_to(ROOT)}/ at {url}")
        print("Press Ctrl+C to stop.")
        if not args.no_open:
            webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped.")


if __name__ == "__main__":
    main()
