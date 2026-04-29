#!/usr/bin/env python

"""
Render a manim animation file.

For each input .py file, discovers Scene/VoiceoverScene subclasses and
renders each one with `manim -qh`. Final mp4s are copied to _site/animations.

Usage:
    build_animation.py animations/syscall.py [animations/other.py ...]
"""

import argparse
import ast
import shutil
import subprocess
import sys
from pathlib import Path

QUALITY_FLAG = "-qh"
QUALITY_DIR = "1080p60"
OUTPUT_DIR = Path("_site/animations")


def find_scenes(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    scenes: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        for base in node.bases:
            name = base.id if isinstance(base, ast.Name) else (
                base.attr if isinstance(base, ast.Attribute) else None
            )
            if name and name.endswith("Scene"):
                scenes.append(node.name)
                break
    return scenes


def render(src: Path, scene: str) -> Path:
    subprocess.run(
        ["manim", QUALITY_FLAG, str(src), scene],
        check=True,
    )
    return Path("media/videos") / src.stem / QUALITY_DIR / f"{scene}.mp4"


def main() -> None:
    if not Path(".git").exists():
        print("Error: script must be run from the root of the repository", file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Render manim animations.")
    parser.add_argument("paths", nargs="+", help=".py animation files")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    failures = 0

    for path_str in args.paths:
        src = Path(path_str)
        scenes = find_scenes(src)
        if not scenes:
            print(f"{src}: no Scene subclass found", file=sys.stderr)
            failures += 1
            continue

        for index, scene in enumerate(scenes):
            try:
                produced = render(src, scene)
            except subprocess.CalledProcessError as e:
                print(f"{src}::{scene}: manim failed (exit {e.returncode})", file=sys.stderr)
                failures += 1
                continue

            if not produced.exists():
                print(f"{src}::{scene}: expected output missing at {produced}", file=sys.stderr)
                failures += 1
                continue

            dest = OUTPUT_DIR / f"{src.stem}-{index:02d}-{scene}.mp4"
            shutil.copy2(produced, dest)
            print(f"{src}::{scene} -> {dest}")

    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
