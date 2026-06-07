# pycatdap benchmark data (gh-pages)

This branch stores **performance benchmark history** for pycatdap, written by the
`Benchmarks` workflow (`.github/workflows/benchmarks.yml`, see HISTORY H-0022 /
issue #161) via
[`github-action-benchmark`](https://github.com/benchmark-action/github-action-benchmark).

- Data + interactive dashboard live under `dev/bench/` (`data.js`, `index.html`).
- This branch is **not** the published documentation site. GitHub Pages for this
  repo is served from the GitHub Actions artifact (mkdocs; see `docs.yml`,
  `build_type: workflow`), so this branch is data-only and not web-served.
- To view the trend chart, open `dev/bench/index.html` from a local checkout of
  this branch.

Do not edit by hand — the workflow appends to it automatically.
