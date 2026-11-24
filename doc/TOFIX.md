# TOFIX

Findings from a code scan on 2026-10-04.

## Medium

- `pyproject.toml:25` - config-level ruff ignore of `F403`/`F405` for all of `animations/*.py`, needed only because all 24 animations use `from manim import *` (e.g. `animations/clock.py:4`); per the lint policy, replace the star imports with explicit imports and delete the per-file-ignores.
- `doc/ci.md:30` - the "Why not just use the rsconstruct repo's workflow" section describes a hand-adapted copy of `teaching-slides`' workflow ("Added the manim system deps", "Explicit `path: _site` on the upload-pages-artifact step"), but `.github/workflows/build.yml` is now the fleet-shared generic workflow (uploads `steps.pages.outputs.dir`, line 71); also line 10 cites `rsconstruct tool install-deps --yes` while the workflow runs it without `--yes` (line 42). Rewrite the section to describe the current setup.
- `README.md:1` - README is only the title; describe what the repo is, how to build (`rsconstruct build`, system deps from `rsconstruct.toml:2`, the `shared/shared-themes` submodule), preview (`scripts/serve.py`) and where the published site lives.

## Low

- `scripts/play.py:9` - usage example points to `_site/animations/clock-00-ClockAnimation.mp4`, but `scripts/build_animation.py:83` names outputs after the source slug (`_site/animations/clock.mp4`); update the example.
- `scripts/serve.py:40` - binds `("", port)`, i.e. all interfaces, while advertising `http://localhost:...`; bind to `"127.0.0.1"` for a local preview server.
- `pyproject.toml:15` - dev group declares `mypy` and `pytest` but `rsconstruct.toml` runs neither and the repo has no tests; add a `[processor.mypy]` for `scripts/` or drop the unused tools.
- `doc/animation_ideas.md:130` - the implemented `animations/bitcoin_ledger.py` has no entry in the ideas list (every other implemented animation is struck through with a ✅); add/tick it so the list stays an accurate tracker.
