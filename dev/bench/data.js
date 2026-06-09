window.BENCHMARK_DATA = {
  "lastUpdate": 1780988078073,
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
      },
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
          "id": "7bb3b09dcb2dce345f7beeb5c0297df70b8f5cd0",
          "message": "Merge pull request #170 from nbx-liz/develop\n\nrelease: v0.14.0",
          "timestamp": "2026-06-07T14:20:01Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/7bb3b09dcb2dce345f7beeb5c0297df70b8f5cd0"
        },
        "date": 1780906500403,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.4016030183056793,
            "unit": "iter/sec",
            "range": "stddev: 0.006668161081215834",
            "extra": "mean: 713.4687831999997 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.3120975540122783,
            "unit": "iter/sec",
            "range": "stddev: 0.008624133783932245",
            "extra": "mean: 762.1384529999987 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.8891954139127645,
            "unit": "iter/sec",
            "range": "stddev: 0.01854242447712921",
            "extra": "mean: 1.1246121880000004 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.17701558532924475,
            "unit": "iter/sec",
            "range": "stddev: 0.03753211709522367",
            "extra": "mean: 5.649220084999996 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.255602219697334,
            "unit": "iter/sec",
            "range": "stddev: 0.0014824158861224937",
            "extra": "mean: 190.27315199999842 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.225267903874943,
            "unit": "iter/sec",
            "range": "stddev: 0.00699634367775816",
            "extra": "mean: 449.3840935999941 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.7744761694355622,
            "unit": "iter/sec",
            "range": "stddev: 0.002734949823635605",
            "extra": "mean: 563.5465932000017 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.7080939659505466,
            "unit": "iter/sec",
            "range": "stddev: 0.01070848269610502",
            "extra": "mean: 1.4122419453999981 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.2800646059687384,
            "unit": "iter/sec",
            "range": "stddev: 0.03965205526204517",
            "extra": "mean: 3.5706047057999997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11765208496766008,
            "unit": "iter/sec",
            "range": "stddev: 0.0714706643761087",
            "extra": "mean: 8.499636876599999 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.07377503880092635,
            "unit": "iter/sec",
            "range": "stddev: 0.03351431124908835",
            "extra": "mean: 13.554720082199992 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 23.268392210494415,
            "unit": "iter/sec",
            "range": "stddev: 0.00025382311108583153",
            "extra": "mean: 42.97675537500112 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 15.076343574456997,
            "unit": "iter/sec",
            "range": "stddev: 0.0002080746314450648",
            "extra": "mean: 66.3290800625056 msec\nrounds: 16"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 5.966744374097541,
            "unit": "iter/sec",
            "range": "stddev: 0.0012841599785115025",
            "extra": "mean: 167.59558266667796 msec\nrounds: 6"
          }
        ]
      },
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
          "id": "7bb3b09dcb2dce345f7beeb5c0297df70b8f5cd0",
          "message": "Merge pull request #170 from nbx-liz/develop\n\nrelease: v0.14.0",
          "timestamp": "2026-06-07T14:20:01Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/7bb3b09dcb2dce345f7beeb5c0297df70b8f5cd0"
        },
        "date": 1780988077847,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.567054646288253,
            "unit": "iter/sec",
            "range": "stddev: 0.009779239137070853",
            "extra": "mean: 638.1398392000008 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.4522841144634753,
            "unit": "iter/sec",
            "range": "stddev: 0.01088272272229371",
            "extra": "mean: 688.5705008000002 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9423177606286539,
            "unit": "iter/sec",
            "range": "stddev: 0.011595527079132441",
            "extra": "mean: 1.0612131510000027 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.1745687902330202,
            "unit": "iter/sec",
            "range": "stddev: 0.017547872366022146",
            "extra": "mean: 5.728400813599997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 6.099938761494767,
            "unit": "iter/sec",
            "range": "stddev: 0.0008012141289330147",
            "extra": "mean: 163.9360720000005 msec\nrounds: 7"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.555584623626933,
            "unit": "iter/sec",
            "range": "stddev: 0.008732851494528468",
            "extra": "mean: 391.29989699999896 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.100235562714745,
            "unit": "iter/sec",
            "range": "stddev: 0.001321184694143462",
            "extra": "mean: 476.1370666000005 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.8265180750840299,
            "unit": "iter/sec",
            "range": "stddev: 0.011251004977050245",
            "extra": "mean: 1.209894895399998 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.3395702682619958,
            "unit": "iter/sec",
            "range": "stddev: 0.00847033384291585",
            "extra": "mean: 2.9448985775999943 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.1385580068493054,
            "unit": "iter/sec",
            "range": "stddev: 0.0071194188259323925",
            "extra": "mean: 7.217193886800004 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.08767818336123691,
            "unit": "iter/sec",
            "range": "stddev: 0.03412706489698097",
            "extra": "mean: 11.405345795999995 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 28.186412041241308,
            "unit": "iter/sec",
            "range": "stddev: 0.0002615581238463586",
            "extra": "mean: 35.478087758627716 msec\nrounds: 29"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 18.036027415663092,
            "unit": "iter/sec",
            "range": "stddev: 0.00032788059916291553",
            "extra": "mean: 55.444581944445616 msec\nrounds: 18"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.559425021493189,
            "unit": "iter/sec",
            "range": "stddev: 0.0008534327036843699",
            "extra": "mean: 152.45238671427938 msec\nrounds: 7"
          }
        ]
      }
    ]
  }
}