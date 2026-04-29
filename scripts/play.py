#!/usr/bin/env python

"""
Play one or more animation files with a configured video player.

Change PLAYER below to switch players globally.

Usage:
    play.py _site/animations/clock-00-ClockAnimation.mp4
    play.py _site/animations/*.mp4
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

PLAYER = ["mpv"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Play animation files.")
    parser.add_argument("paths", nargs="+", help="video files to play")
    args = parser.parse_args()

    if shutil.which(PLAYER[0]) is None:
        print(f"Error: player {PLAYER[0]!r} not found in PATH", file=sys.stderr)
        sys.exit(1)

    missing = [p for p in args.paths if not Path(p).exists()]
    if missing:
        for p in missing:
            print(f"Error: file not found: {p}", file=sys.stderr)
        sys.exit(1)

    sys.exit(subprocess.run([*PLAYER, *args.paths]).returncode)


if __name__ == "__main__":
    main()
