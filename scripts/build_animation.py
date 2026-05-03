#!/usr/bin/env python

"""
Render a manim animation file.

For each input .py file, discovers Scene/VoiceoverScene subclasses and
renders each one with `manim -qh`, writing the final mp4 directly into
_site/animations/<slug>-<NN>-<Scene>.mp4. Manim's intermediate output
(Tex, partial movie chunks, logs, ...) goes to a scratch directory
configured in manim.cfg.

Usage:
    build_animation.py animations/syscall.py [animations/other.py ...]
"""

import argparse
import ast
import subprocess
import sys
from pathlib import Path

QUALITY_FLAG = "-qh"
OUTPUT_DIR = Path("_site/animations")
EXTRA_SUFFIXES = (".srt", ".wav")


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


def render(src: Path, scene: str, output_name: str) -> None:
    subprocess.run(
        ["manim", "--custom_folders", QUALITY_FLAG, "-o", output_name, str(src), scene],
        check=True,
    )


def main() -> None:
    if not Path(".git").exists():
        print("Error: script must be run from the root of the repository", file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Render manim animations.")
    parser.add_argument("paths", nargs="+", help=".py animation files")
    parser.add_argument(
        "--keep-extras",
        action="store_true",
        help="keep manim's .srt and .wav side files alongside each .mp4 "
             "(by default they are deleted to keep _site/ minimal)",
    )
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
            output_name = f"{src.stem}-{index:02d}-{scene}"
            try:
                render(src, scene, output_name)
            except subprocess.CalledProcessError as e:
                print(f"{src}::{scene}: manim failed (exit {e.returncode})", file=sys.stderr)
                failures += 1
                continue

            produced = OUTPUT_DIR / f"{output_name}.mp4"
            if not produced.exists():
                print(f"{src}::{scene}: expected output missing at {produced}", file=sys.stderr)
                failures += 1
                continue

            if not args.keep_extras:
                for suffix in EXTRA_SUFFIXES:
                    extra = OUTPUT_DIR / f"{output_name}{suffix}"
                    if extra.exists():
                        extra.unlink()

            print(f"{src}::{scene} -> {produced}")

    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
