window.BENCHMARK_DATA = {
  "lastUpdate": 1780818197649,
  "repoUrl": "https://github.com/nbx-liz/pycatdap",
  "entries": {
    "pycatdap benchmarks": [
      {
        "commit": {
          "author": {
            "name": "nbx-liz",
            "username": "nbx-liz",
            "email": "nobuyuki.tachibana.0305@gmail.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "9552d6eaa7ea76a5c1454982cc8ad9071b852083",
          "message": "ci(bench): nightly non-blocking benchmark workflow (#161, H-0022) (#162)\n\n* docs(history): add proposal H-0022 for nightly benchmark CI (#161)\n\n* ci(bench): add nightly non-blocking benchmark workflow (#161, H-0022)\n\nPhase 2 of #29: continuous benchmarking on a GitHub-hosted runner, never\nblocking a PR or commit.\n\n- .github/workflows/benchmarks.yml: schedule (03:00 UTC) + workflow_dispatch +\n  pull_request (validate-only). Runs `make bench` with --benchmark-json and feeds\n  benchmark-action/github-action-benchmark.\n- History + dashboard stored in the gh-pages BRANCH (dev/bench/). The public\n  Pages site is served from the Actions artifact (mkdocs, build_type=workflow),\n  so creating gh-pages does not change Pages and the chart is not public — view\n  it via the branch. Raw output.json uploaded as an artifact each run.\n- Non-blocking: alert-threshold 150% (above +20% because hosted runners are\n  noisy), comment-on-alert true, fail-on-alert false.\n- PR runs are side-effect-free: auto-push / save-data-file / comment-on-alert are\n  disabled for pull_request events (safe for forks; self-validates this PR).\n- Scheduled workflows fire from the default branch (main), so the nightly cadence\n  activates once this file reaches main; until then trigger via workflow_dispatch.\n- make ci is unchanged (benchmarks stay outside testpaths). Ignore local\n  output.json / .benchmarks/ artifacts.\n\nPR-delta comments on src changes (Phase 3) remain in #161.\n\n* ci(bench): skip gh-pages fetch on PR validation runs (#161)\n\n---------\n\nCo-authored-by: nbx <nbx@gmail.com>",
          "timestamp": "2026-06-07T07:38:47Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/9552d6eaa7ea76a5c1454982cc8ad9071b852083"
        },
        "date": 1780818197034,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.5369663444977186,
            "unit": "iter/sec",
            "range": "stddev: 0.01441036423141106",
            "extra": "mean: 650.6323340000008 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.4309364836623382,
            "unit": "iter/sec",
            "range": "stddev: 0.02222127755412346",
            "extra": "mean: 698.8430383999997 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9336351768640024,
            "unit": "iter/sec",
            "range": "stddev: 0.007968370620367522",
            "extra": "mean: 1.0710821793999998 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.17058717286215322,
            "unit": "iter/sec",
            "range": "stddev: 0.02311342295225814",
            "extra": "mean: 5.862105475000002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 6.067350658926542,
            "unit": "iter/sec",
            "range": "stddev: 0.0008821621098171829",
            "extra": "mean: 164.8165824285692 msec\nrounds: 7"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.5271986021943644,
            "unit": "iter/sec",
            "range": "stddev: 0.012786060938303359",
            "extra": "mean: 395.6950589999934 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.035259383900839,
            "unit": "iter/sec",
            "range": "stddev: 0.003306776791192697",
            "extra": "mean: 491.3378647999991 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.8057308496206101,
            "unit": "iter/sec",
            "range": "stddev: 0.007067273962949819",
            "extra": "mean: 1.2411092370000034 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.3330473695143393,
            "unit": "iter/sec",
            "range": "stddev: 0.027867294424100218",
            "extra": "mean: 3.002575884199996 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.13694469896602748,
            "unit": "iter/sec",
            "range": "stddev: 0.05755982224507407",
            "extra": "mean: 7.3022176656 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.08746965049464246,
            "unit": "iter/sec",
            "range": "stddev: 0.03439362015242657",
            "extra": "mean: 11.43253682099999 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 28.230309366519872,
            "unit": "iter/sec",
            "range": "stddev: 0.0001347389864441045",
            "extra": "mean: 35.42292034482499 msec\nrounds: 29"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 17.89600748166443,
            "unit": "iter/sec",
            "range": "stddev: 0.00021006815731180718",
            "extra": "mean: 55.87838522221015 msec\nrounds: 18"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.432090471211909,
            "unit": "iter/sec",
            "range": "stddev: 0.0014843887847191017",
            "extra": "mean: 155.4704499999957 msec\nrounds: 7"
          }
        ]
      }
    ]
  }
}