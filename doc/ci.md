# CI build

The animations are rendered in CI by `.github/workflows/build.yml` and
deployed to GitHub Pages from `_site/`.

## System dependencies

The workflow installs the following on the Ubuntu runner before building:

- `ffmpeg` — manim shells out to it to encode the final mp4.
- `sox` — used by `manim-voiceover` to compute audio durations from the
  generated speech files.
- `libcairo2-dev`, `libpango1.0-dev`, `pkg-config` — manim's text and
  vector rendering backend (used by `Text(...)`, shapes, etc.).
- `texlive-latex-base`, `texlive-fonts-recommended`, `texlive-latex-extra` —
  required for manim's `Tex(...)` and `MathTex(...)` mobjects. **Keep these
  installed.** Removing the TeX packages would shave ~2 minutes off the
  workflow but break any animation that renders LaTeX (math formulas,
  typeset code labels, etc.). We use TeX support, so the cost is
  acceptable.

## Why not just use the rsconstruct repo's workflow as-is

`rsconstruct/.github/workflows/` contains workflows that release the
rsconstruct **tool itself** (Rust crate) — not workflows that *use*
rsconstruct to build a project. The pattern we copy from is
`teaching-slides/.github/workflows/build.yml`, which is the canonical
"build a project with rsconstruct + deploy to Pages" template. Differences
in our copy:

- No Node setup (the slides repo needs it for marp; we don't).
- No Ruby setup (the slides repo needs it for jekyll; we don't).
- Added the manim system deps listed above.
- Explicit `path: _site` on the upload-pages-artifact step.

## Render time on CI

GitHub-hosted runners have no GPU and limited cores, so manim renders
take noticeably longer than on a developer machine. Rough budget:

- 1080p60 voiceover scene of ~30 seconds: ~2 min locally, ~4–6 min on
  the runner.
- Time scales roughly linearly with the number of scenes built.

If render times become a problem, options are: lower the default quality
in `scripts/build_animation.py` (`-qm` for 720p, `-ql` for 480p), shard
animations across parallel jobs, or move to a self-hosted runner.
