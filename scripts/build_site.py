#!/usr/bin/env python

"""
Generate index.html for the GitHub Pages site.

Scans _site/animations/ for rendered .mp4 files and groups them by source
animation file. Each source file becomes one entry on the index page;
the entry's videos play in a built-in player view.

Run via rsconstruct as the [processor.explicit.build_site] step,
or directly: scripts/build_site.py
"""

import ast
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
ANIMATIONS_DIR = ROOT / "animations"
SITE_DIR = ROOT / "_site"
VIDEOS_DIR = SITE_DIR / "animations"
RESOURCES_DIR = ROOT / "resources"

SUMMARY_SUFFIX = "_summary"


def humanize(slug: str) -> str:
    return slug.replace("_", " ").title()


def _first_voiceover_text(node: ast.AST) -> str:
    for sub in ast.walk(node):
        if not isinstance(sub, ast.Call):
            continue
        func = sub.func
        is_voiceover = (
            (isinstance(func, ast.Attribute) and func.attr == "voiceover") or
            (isinstance(func, ast.Name) and func.id == "voiceover")
        )
        if not is_voiceover:
            continue
        for kw in sub.keywords:
            if kw.arg == "text" and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                return " ".join(kw.value.value.split())
    return ""


def extract_description(py_path: Path) -> str:
    """Pull a short description from the source. Prefer the first voiceover
    text inside a show_title() method (convention used by every animation
    in this project). Fall back to the module docstring, then to the first
    voiceover anywhere."""
    if not py_path.exists():
        return ""
    try:
        tree = ast.parse(py_path.read_text(encoding="utf-8"))
    except SyntaxError:
        return ""

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "show_title":
            text = _first_voiceover_text(node)
            if text:
                return text

    doc = ast.get_docstring(tree)
    if doc:
        first = doc.strip().split("\n\n")[0]
        return " ".join(first.split())

    return _first_voiceover_text(tree)


def collect_entries() -> list[dict[str, Any]]:
    """Group rendered .mp4 files into topics. Each topic is a base slug
    plus its optional `<slug>_summary` companion. Both render to one .mp4
    each; together they form one entry on the index page."""
    if not VIDEOS_DIR.exists():
        return []

    available = {mp4.stem for mp4 in VIDEOS_DIR.iterdir() if mp4.is_file() and mp4.suffix == ".mp4"}

    base_slugs = sorted(s for s in available if not s.endswith(SUMMARY_SUFFIX))

    entries: list[dict[str, Any]] = []
    for slug in base_slugs:
        scenes = [{"label": "Animation", "path": f"animations/{slug}.mp4"}]
        summary_slug = f"{slug}{SUMMARY_SUFFIX}"
        if summary_slug in available:
            scenes.append({"label": "Summary", "path": f"animations/{summary_slug}.mp4"})

        py_path = ANIMATIONS_DIR / f"{slug}.py"
        description = extract_description(py_path)
        entries.append({
            "slug": slug,
            "title": humanize(slug),
            "description": description,
            "scenes": scenes,
        })
    return entries


def generate_index(entries: list[dict[str, Any]]) -> str:
    template = (RESOURCES_DIR / "index.html").read_text(encoding="utf-8")
    css = (RESOURCES_DIR / "index.css").read_text(encoding="utf-8")
    js = (RESOURCES_DIR / "index.js").read_text(encoding="utf-8")

    return (
        template
        .replace("{{CSS}}", css)
        .replace("{{JS}}", js)
        .replace("{{DATA_JSON}}", json.dumps(entries, ensure_ascii=False))
        .replace("{{TOTAL_COUNT}}", str(len(entries)))
    )


def main() -> None:
    if not SITE_DIR.exists():
        print(f"Error: {SITE_DIR} does not exist. Run 'rsconstruct build' first.", file=sys.stderr)
        sys.exit(1)

    entries = collect_entries()
    html = generate_index(entries)
    out = SITE_DIR / "index.html"
    out.write_text(html, encoding="utf-8")
    print(f"Site index built: {len(entries)} animations, written to {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
