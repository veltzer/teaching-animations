#!/usr/bin/env python

"""
Render manim animation files as a generator-style processor.

Invoked by rsconstruct's [processor.generator.manim] in batched mode:
the argv is a flat list of (input, output) pairs. For each pair, this
script discovers the single Scene/VoiceoverScene subclass in the input
file, renders it with `manim --custom_folders -qh`, and the rendered
mp4 lands directly at the output path (manim.cfg's [custom_folders]
points video_dir at _site/animations/).

Each input .py file must contain exactly one Scene subclass.

Usage:
    build_animation.py IN1 OUT1 [IN2 OUT2 ...]
"""

import argparse
import ast
import subprocess
import sys
from pathlib import Path

QUALITY_FLAG = "-qh"
EXTRA_SUFFIXES = (".srt", ".wav")


def find_scene(path: Path) -> str:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    scenes: list[str] = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        for base in node.bases:
            name = base.id if isinstance(base, ast.Name) else (
                base.attr if isinstance(base, ast.Attribute) else None
            )
            if name and name.endswith("Scene"):
                scenes.append(node.name)
                break
    if len(scenes) != 1:
        raise SystemExit(
            f"{path}: expected exactly one Scene subclass, found {len(scenes)}: {scenes}"
        )
    return scenes[0]


def render(src: Path, scene: str, output_stem: str) -> None:
    subprocess.run(
        ["manim", "--custom_folders", QUALITY_FLAG, "-o", output_stem, str(src), scene],
        check=True,
    )


def main() -> None:
    if not Path(".git").exists():
        print("Error: script must be run from the root of the repository", file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Render manim animations.")
    parser.add_argument("pairs", nargs="+", help="alternating input and output paths")
    parser.add_argument(
        "--keep-extras",
        action="store_true",
        help="keep manim's .srt and .wav side files alongside each .mp4",
    )
    args = parser.parse_args()

    if len(args.pairs) % 2 != 0:
        print("Error: argv must be an even number of input/output paths", file=sys.stderr)
        sys.exit(1)

    failures = 0
    for i in range(0, len(args.pairs), 2):
        src = Path(args.pairs[i])
        out = Path(args.pairs[i + 1])

        scene = find_scene(src)
        # Manim writes <video_dir>/<output_stem>.mp4. video_dir comes from
        # manim.cfg, which we configured to match the parent of `out`.
        # The output stem is whatever -o is set to.
        output_stem = out.stem

        try:
            render(src, scene, output_stem)
        except subprocess.CalledProcessError as e:
            print(f"{src}: manim failed (exit {e.returncode})", file=sys.stderr)
            failures += 1
            continue

        if not out.exists():
            print(f"{src}: expected output missing at {out}", file=sys.stderr)
            failures += 1
            continue

        if not args.keep_extras:
            for suffix in EXTRA_SUFFIXES:
                extra = out.with_suffix(suffix)
                if extra.exists():
                    extra.unlink()

        print(f"{src} -> {out}")

    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
