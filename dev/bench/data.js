window.BENCHMARK_DATA = {
  "lastUpdate": 1787197809057,
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
        "date": 1781075626412,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.5059686531516474,
            "unit": "iter/sec",
            "range": "stddev: 0.015441627280601349",
            "extra": "mean: 664.0244455999991 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.4064963494179106,
            "unit": "iter/sec",
            "range": "stddev: 0.013001867618207432",
            "extra": "mean: 710.9865591999991 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.8742993562113823,
            "unit": "iter/sec",
            "range": "stddev: 0.024853273724189204",
            "extra": "mean: 1.1437730028000004 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.16020808773842013,
            "unit": "iter/sec",
            "range": "stddev: 0.018487372147264924",
            "extra": "mean: 6.2418821304000005 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.548923138381696,
            "unit": "iter/sec",
            "range": "stddev: 0.0037370507322316434",
            "extra": "mean: 180.21514716667042 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.3220061021131504,
            "unit": "iter/sec",
            "range": "stddev: 0.014442198920982046",
            "extra": "mean: 430.66208959999983 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.8794551528224803,
            "unit": "iter/sec",
            "range": "stddev: 0.004291751013803326",
            "extra": "mean: 532.0690938000013 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.7578109084822336,
            "unit": "iter/sec",
            "range": "stddev: 0.023601775221526206",
            "extra": "mean: 1.319590400200005 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.31812728229566556,
            "unit": "iter/sec",
            "range": "stddev: 0.05240968105123127",
            "extra": "mean: 3.1433959162000007 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.13339162268011318,
            "unit": "iter/sec",
            "range": "stddev: 0.07586098749766274",
            "extra": "mean: 7.496722657000004 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.08383594139651608,
            "unit": "iter/sec",
            "range": "stddev: 0.07220243856421882",
            "extra": "mean: 11.928058340400009 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 27.085143666847802,
            "unit": "iter/sec",
            "range": "stddev: 0.0015681337331550007",
            "extra": "mean: 36.920609035720176 msec\nrounds: 28"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 17.52399379388861,
            "unit": "iter/sec",
            "range": "stddev: 0.00035017190154247385",
            "extra": "mean: 57.06461733333552 msec\nrounds: 18"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.371997379998068,
            "unit": "iter/sec",
            "range": "stddev: 0.001189853570162619",
            "extra": "mean: 156.9366621428685 msec\nrounds: 7"
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
        "date": 1781165296651,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.5444495800035651,
            "unit": "iter/sec",
            "range": "stddev: 0.013718174153237514",
            "extra": "mean: 647.4798614000023 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.4362298996386844,
            "unit": "iter/sec",
            "range": "stddev: 0.023010731982609597",
            "extra": "mean: 696.2673596000002 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9313767691425344,
            "unit": "iter/sec",
            "range": "stddev: 0.019371025786226688",
            "extra": "mean: 1.0736793456000016 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.1729176296585634,
            "unit": "iter/sec",
            "range": "stddev: 0.054864322204031805",
            "extra": "mean: 5.783100323400004 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.947293567841943,
            "unit": "iter/sec",
            "range": "stddev: 0.001953926619282539",
            "extra": "mean: 168.14370916666613 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.541864238381351,
            "unit": "iter/sec",
            "range": "stddev: 0.011525163247030231",
            "extra": "mean: 393.41204179999636 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.0093920826546605,
            "unit": "iter/sec",
            "range": "stddev: 0.005246541968745935",
            "extra": "mean: 497.6629541999955 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.8099696679497027,
            "unit": "iter/sec",
            "range": "stddev: 0.021003113497344697",
            "extra": "mean: 1.2346141338000052 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.33612389630505357,
            "unit": "iter/sec",
            "range": "stddev: 0.029839099560523143",
            "extra": "mean: 2.975093443199995 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.13932054300666571,
            "unit": "iter/sec",
            "range": "stddev: 0.03606546301411425",
            "extra": "mean: 7.177692380600007 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.08874371140431933,
            "unit": "iter/sec",
            "range": "stddev: 0.04812491815773372",
            "extra": "mean: 11.268404083799993 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 28.562191418027428,
            "unit": "iter/sec",
            "range": "stddev: 0.00021082930719621714",
            "extra": "mean: 35.01131917240902 msec\nrounds: 29"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 18.15999225191679,
            "unit": "iter/sec",
            "range": "stddev: 0.00012633813227897852",
            "extra": "mean: 55.06610278946841 msec\nrounds: 19"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.561715089691955,
            "unit": "iter/sec",
            "range": "stddev: 0.0008768997383630215",
            "extra": "mean: 152.39918014284675 msec\nrounds: 7"
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
        "date": 1781249269541,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.380170097898843,
            "unit": "iter/sec",
            "range": "stddev: 0.008911048408523038",
            "extra": "mean: 724.5483738000047 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.3011208417275024,
            "unit": "iter/sec",
            "range": "stddev: 0.010016034308932113",
            "extra": "mean: 768.5681206000027 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9014440279118836,
            "unit": "iter/sec",
            "range": "stddev: 0.008541932068675671",
            "extra": "mean: 1.109331216399994 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.18104970800427103,
            "unit": "iter/sec",
            "range": "stddev: 0.021215142074419723",
            "extra": "mean: 5.523345003000003 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.1825023604678755,
            "unit": "iter/sec",
            "range": "stddev: 0.001059352450576013",
            "extra": "mean: 192.95697916666654 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.18619052215961,
            "unit": "iter/sec",
            "range": "stddev: 0.0086132776518995",
            "extra": "mean: 457.41667519999964 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.7815235607591875,
            "unit": "iter/sec",
            "range": "stddev: 0.004260051127573428",
            "extra": "mean: 561.3173028000006 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.7045461838884647,
            "unit": "iter/sec",
            "range": "stddev: 0.00958247809005471",
            "extra": "mean: 1.4193533693999938 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.2825099498314916,
            "unit": "iter/sec",
            "range": "stddev: 0.03491786685237782",
            "extra": "mean: 3.5396983384000067 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11912929744658722,
            "unit": "iter/sec",
            "range": "stddev: 0.014460046621511576",
            "extra": "mean: 8.394240723600001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.07420215642578504,
            "unit": "iter/sec",
            "range": "stddev: 0.09963647601447301",
            "extra": "mean: 13.476697284399984 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 23.114359100655346,
            "unit": "iter/sec",
            "range": "stddev: 0.00022092810016681845",
            "extra": "mean: 43.26315065216961 msec\nrounds: 23"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 14.995573216814174,
            "unit": "iter/sec",
            "range": "stddev: 0.000291062816507777",
            "extra": "mean: 66.68634706666126 msec\nrounds: 15"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 5.921993722094741,
            "unit": "iter/sec",
            "range": "stddev: 0.0008083639740584754",
            "extra": "mean: 168.86204999999185 msec\nrounds: 6"
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
        "date": 1781334162086,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.5533189698860184,
            "unit": "iter/sec",
            "range": "stddev: 0.017620650717333604",
            "extra": "mean: 643.7827769999999 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.4504423840568708,
            "unit": "iter/sec",
            "range": "stddev: 0.007839743397810814",
            "extra": "mean: 689.4448280000006 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9407086094933184,
            "unit": "iter/sec",
            "range": "stddev: 0.010107761596527529",
            "extra": "mean: 1.0630284340000002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.17634741961864278,
            "unit": "iter/sec",
            "range": "stddev: 0.0029966188925201935",
            "extra": "mean: 5.6706245102 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 6.156843088557241,
            "unit": "iter/sec",
            "range": "stddev: 0.000318215797533035",
            "extra": "mean: 162.42090071428703 msec\nrounds: 7"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.5791877611276575,
            "unit": "iter/sec",
            "range": "stddev: 0.009595681076224785",
            "extra": "mean: 387.7189613999974 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.132667496114797,
            "unit": "iter/sec",
            "range": "stddev: 0.0028988025564256063",
            "extra": "mean: 468.8963478000005 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.8284727388678352,
            "unit": "iter/sec",
            "range": "stddev: 0.018664488690290023",
            "extra": "mean: 1.2070403201999966 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.3381943923924753,
            "unit": "iter/sec",
            "range": "stddev: 0.03171898957952835",
            "extra": "mean: 2.9568793052000046 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.1388098242627804,
            "unit": "iter/sec",
            "range": "stddev: 0.027287403969778586",
            "extra": "mean: 7.204101044799995 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.0887158763051329,
            "unit": "iter/sec",
            "range": "stddev: 0.022517304284998287",
            "extra": "mean: 11.271939608200006 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 28.326299418287988,
            "unit": "iter/sec",
            "range": "stddev: 0.00013520583016162489",
            "extra": "mean: 35.30288179310783 msec\nrounds: 29"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 17.979742637499264,
            "unit": "iter/sec",
            "range": "stddev: 0.0002603721891410501",
            "extra": "mean: 55.618148722238125 msec\nrounds: 18"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.478756234662739,
            "unit": "iter/sec",
            "range": "stddev: 0.0024991633310253746",
            "extra": "mean: 154.35061357144215 msec\nrounds: 7"
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
        "date": 1781422052980,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.3641465121433614,
            "unit": "iter/sec",
            "range": "stddev: 0.006103495914850314",
            "extra": "mean: 733.0590894000011 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.30475544121718,
            "unit": "iter/sec",
            "range": "stddev: 0.008696215827888378",
            "extra": "mean: 766.4271544000002 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.8964391971919496,
            "unit": "iter/sec",
            "range": "stddev: 0.010849004536586089",
            "extra": "mean: 1.1155246257999978 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.1812297496263203,
            "unit": "iter/sec",
            "range": "stddev: 0.035087491328688845",
            "extra": "mean: 5.517857868600004 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.249855502320975,
            "unit": "iter/sec",
            "range": "stddev: 0.0006709182101167692",
            "extra": "mean: 190.48143316666474 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.2179248528441513,
            "unit": "iter/sec",
            "range": "stddev: 0.007600591387873817",
            "extra": "mean: 450.87190339999665 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.7912186026027705,
            "unit": "iter/sec",
            "range": "stddev: 0.0022166214800038854",
            "extra": "mean: 558.2791506000035 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.7164445951046547,
            "unit": "iter/sec",
            "range": "stddev: 0.009872947814521674",
            "extra": "mean: 1.3957813442000002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.28484145647255305,
            "unit": "iter/sec",
            "range": "stddev: 0.019048537441384603",
            "extra": "mean: 3.5107249217999934 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11894578197096796,
            "unit": "iter/sec",
            "range": "stddev: 0.051397475386908226",
            "extra": "mean: 8.4071917762 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.0751147342347893,
            "unit": "iter/sec",
            "range": "stddev: 0.04307933253333077",
            "extra": "mean: 13.312967291800003 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 23.505896051485887,
            "unit": "iter/sec",
            "range": "stddev: 0.0001325452642481964",
            "extra": "mean: 42.542517750000286 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 15.096573317326463,
            "unit": "iter/sec",
            "range": "stddev: 0.0005475710525962592",
            "extra": "mean: 66.24019762499955 msec\nrounds: 16"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.0275787525965505,
            "unit": "iter/sec",
            "range": "stddev: 0.0009045076054371309",
            "extra": "mean: 165.9040953333412 msec\nrounds: 6"
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
        "date": 1781515662607,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.35374701487852,
            "unit": "iter/sec",
            "range": "stddev: 0.01865910901647196",
            "extra": "mean: 738.6904561999984 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.2816275444373364,
            "unit": "iter/sec",
            "range": "stddev: 0.012834343660085363",
            "extra": "mean: 780.2578871999998 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.8880279392501115,
            "unit": "iter/sec",
            "range": "stddev: 0.006485634763890429",
            "extra": "mean: 1.126090695800002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.17599369044654314,
            "unit": "iter/sec",
            "range": "stddev: 0.03632207643317729",
            "extra": "mean: 5.682021880799999 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.185316424903833,
            "unit": "iter/sec",
            "range": "stddev: 0.003199566800593483",
            "extra": "mean: 192.8522616666631 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.168075627108896,
            "unit": "iter/sec",
            "range": "stddev: 0.021125733441359904",
            "extra": "mean: 461.23852299999726 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.7217340074227163,
            "unit": "iter/sec",
            "range": "stddev: 0.011802979906344914",
            "extra": "mean: 580.8098090000044 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.6854859632035735,
            "unit": "iter/sec",
            "range": "stddev: 0.02085097820881598",
            "extra": "mean: 1.458819076800006 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.2733657091907924,
            "unit": "iter/sec",
            "range": "stddev: 0.023824183375820648",
            "extra": "mean: 3.6581032893999947 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11425638822259906,
            "unit": "iter/sec",
            "range": "stddev: 0.06373975550588866",
            "extra": "mean: 8.752245852999994 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.0715610474150019,
            "unit": "iter/sec",
            "range": "stddev: 0.04858774204370525",
            "extra": "mean: 13.974082774400006 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 23.381397163480816,
            "unit": "iter/sec",
            "range": "stddev: 0.0002278274573594772",
            "extra": "mean: 42.76904382608455 msec\nrounds: 23"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 15.102455009475404,
            "unit": "iter/sec",
            "range": "stddev: 0.001048708338140235",
            "extra": "mean: 66.21440020000666 msec\nrounds: 15"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 5.882349896194873,
            "unit": "iter/sec",
            "range": "stddev: 0.00349973328027722",
            "extra": "mean: 170.00008800001373 msec\nrounds: 6"
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
        "date": 1781599847889,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.5650064311591707,
            "unit": "iter/sec",
            "range": "stddev: 0.00926867250850703",
            "extra": "mean: 638.9750100000028 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.448406973486431,
            "unit": "iter/sec",
            "range": "stddev: 0.01045697787115363",
            "extra": "mean: 690.4136877999974 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9389762712872669,
            "unit": "iter/sec",
            "range": "stddev: 0.00843103719029636",
            "extra": "mean: 1.064989638800003 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.17231263752217962,
            "unit": "iter/sec",
            "range": "stddev: 0.05068790742094373",
            "extra": "mean: 5.803404871400002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 6.110871326340148,
            "unit": "iter/sec",
            "range": "stddev: 0.0007510408043570215",
            "extra": "mean: 163.64278457142842 msec\nrounds: 7"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.552311663001765,
            "unit": "iter/sec",
            "range": "stddev: 0.012465601977800386",
            "extra": "mean: 391.80168100000117 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.0798710404746763,
            "unit": "iter/sec",
            "range": "stddev: 0.004894437825780572",
            "extra": "mean: 480.79904020000015 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.8212280331448217,
            "unit": "iter/sec",
            "range": "stddev: 0.012210688517978092",
            "extra": "mean: 1.217688583000006 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.3361320633006676,
            "unit": "iter/sec",
            "range": "stddev: 0.03562172202603424",
            "extra": "mean: 2.9750211573999934 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.13735003303688043,
            "unit": "iter/sec",
            "range": "stddev: 0.08664447781585327",
            "extra": "mean: 7.280668070399997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.08741614186906312,
            "unit": "iter/sec",
            "range": "stddev: 0.027817282992861094",
            "extra": "mean: 11.439534834400002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 28.109896003857227,
            "unit": "iter/sec",
            "range": "stddev: 0.0002520312913289806",
            "extra": "mean: 35.5746602499981 msec\nrounds: 28"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 17.864441917199652,
            "unit": "iter/sec",
            "range": "stddev: 0.00021796729896069697",
            "extra": "mean: 55.977119500005934 msec\nrounds: 18"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.547163345564505,
            "unit": "iter/sec",
            "range": "stddev: 0.0009733149401585757",
            "extra": "mean: 152.737903000002 msec\nrounds: 7"
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
        "date": 1781685196706,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.3465210778238454,
            "unit": "iter/sec",
            "range": "stddev: 0.0130802315896136",
            "extra": "mean: 742.6545461999979 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.2752761843952927,
            "unit": "iter/sec",
            "range": "stddev: 0.0129617646975131",
            "extra": "mean: 784.1438679999953 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.8525861987061482,
            "unit": "iter/sec",
            "range": "stddev: 0.014719330083408914",
            "extra": "mean: 1.1729019323999865 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.17238649397826217,
            "unit": "iter/sec",
            "range": "stddev: 0.021200909119176832",
            "extra": "mean: 5.800918487999991 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.089776726637133,
            "unit": "iter/sec",
            "range": "stddev: 0.0010188709392472046",
            "extra": "mean: 196.47227249999824 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.111091206054358,
            "unit": "iter/sec",
            "range": "stddev: 0.016724579243743563",
            "extra": "mean: 473.68867679999767 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.7040834235021598,
            "unit": "iter/sec",
            "range": "stddev: 0.00589906869159046",
            "extra": "mean: 586.8257305999975 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.6947518075652708,
            "unit": "iter/sec",
            "range": "stddev: 0.013897818755067804",
            "extra": "mean: 1.4393629337999982 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.2764955596045196,
            "unit": "iter/sec",
            "range": "stddev: 0.028223528343068367",
            "extra": "mean: 3.616694609599995 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11662761045096583,
            "unit": "iter/sec",
            "range": "stddev: 0.0653534547013984",
            "extra": "mean: 8.57429896860001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.07309171657064857,
            "unit": "iter/sec",
            "range": "stddev: 0.037510565085314675",
            "extra": "mean: 13.681440892599994 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 23.630927565253607,
            "unit": "iter/sec",
            "range": "stddev: 0.0001907282136494098",
            "extra": "mean: 42.31742479166911 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 15.037151357557097,
            "unit": "iter/sec",
            "range": "stddev: 0.002583112690613982",
            "extra": "mean: 66.50195746666061 msec\nrounds: 15"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 5.999437948655349,
            "unit": "iter/sec",
            "range": "stddev: 0.0011115441639002097",
            "extra": "mean: 166.68228066666302 msec\nrounds: 6"
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
        "date": 1781770366358,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.3741288570636636,
            "unit": "iter/sec",
            "range": "stddev: 0.0075513838713935095",
            "extra": "mean: 727.7337891999963 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.299959093537227,
            "unit": "iter/sec",
            "range": "stddev: 0.008365735644639657",
            "extra": "mean: 769.2549749999984 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.8962399472437486,
            "unit": "iter/sec",
            "range": "stddev: 0.015102519032546767",
            "extra": "mean: 1.115772626599997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.1878357593712455,
            "unit": "iter/sec",
            "range": "stddev: 0.03522408673771772",
            "extra": "mean: 5.3237999162 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.16884026637034,
            "unit": "iter/sec",
            "range": "stddev: 0.000479460074715152",
            "extra": "mean: 193.46699616666996 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.180182269446909,
            "unit": "iter/sec",
            "range": "stddev: 0.008090183934669665",
            "extra": "mean: 458.67724639999494 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.765252845324037,
            "unit": "iter/sec",
            "range": "stddev: 0.0035254200438659205",
            "extra": "mean: 566.4910851999991 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.7042965887367276,
            "unit": "iter/sec",
            "range": "stddev: 0.00889940869248152",
            "extra": "mean: 1.419856372999996 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.27988526451310763,
            "unit": "iter/sec",
            "range": "stddev: 0.025958135811769652",
            "extra": "mean: 3.5728926341999965 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11777857297755866,
            "unit": "iter/sec",
            "range": "stddev: 0.06103813264388162",
            "extra": "mean: 8.490508712399992 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.07405310931628417,
            "unit": "iter/sec",
            "range": "stddev: 0.022270901669490535",
            "extra": "mean: 13.503821908800006 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 22.66575361652939,
            "unit": "iter/sec",
            "range": "stddev: 0.0016131687493469678",
            "extra": "mean: 44.119424260869614 msec\nrounds: 23"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 14.778067620784809,
            "unit": "iter/sec",
            "range": "stddev: 0.0015003093034121533",
            "extra": "mean: 67.66784573333098 msec\nrounds: 15"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 5.978984139802795,
            "unit": "iter/sec",
            "range": "stddev: 0.000795416352945045",
            "extra": "mean: 167.25249250000238 msec\nrounds: 6"
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
        "date": 1781858199909,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.374906503745425,
            "unit": "iter/sec",
            "range": "stddev: 0.014411993384030469",
            "extra": "mean: 727.322183199999 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.2965026911214605,
            "unit": "iter/sec",
            "range": "stddev: 0.015744569941712513",
            "extra": "mean: 771.3057650000025 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.8788454924415716,
            "unit": "iter/sec",
            "range": "stddev: 0.006905026068077541",
            "extra": "mean: 1.1378564361999992 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.17593576671970815,
            "unit": "iter/sec",
            "range": "stddev: 0.03980651637438312",
            "extra": "mean: 5.683892585599997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.165140856223285,
            "unit": "iter/sec",
            "range": "stddev: 0.0009033277755697676",
            "extra": "mean: 193.60556233333645 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.179366037134887,
            "unit": "iter/sec",
            "range": "stddev: 0.013967994087819928",
            "extra": "mean: 458.8490335999978 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.7232128081946967,
            "unit": "iter/sec",
            "range": "stddev: 0.005817821197098235",
            "extra": "mean: 580.3113784000004 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.6894571106906924,
            "unit": "iter/sec",
            "range": "stddev: 0.01631787948577744",
            "extra": "mean: 1.4504165443999966 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.27904093434198585,
            "unit": "iter/sec",
            "range": "stddev: 0.02522644794205471",
            "extra": "mean: 3.583703596600003 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11667225835771232,
            "unit": "iter/sec",
            "range": "stddev: 0.06892477209631893",
            "extra": "mean: 8.571017773 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.07399260082021465,
            "unit": "iter/sec",
            "range": "stddev: 0.23363317082346416",
            "extra": "mean: 13.514864850200018 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 22.5209004972287,
            "unit": "iter/sec",
            "range": "stddev: 0.0013298724359259786",
            "extra": "mean: 44.403197826084025 msec\nrounds: 23"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 14.547882550021441,
            "unit": "iter/sec",
            "range": "stddev: 0.0013033956772792214",
            "extra": "mean: 68.73852579999871 msec\nrounds: 15"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 5.7676558387081425,
            "unit": "iter/sec",
            "range": "stddev: 0.0034953925537055384",
            "extra": "mean: 173.38066416667175 msec\nrounds: 6"
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
        "date": 1781939112674,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.565150550665432,
            "unit": "iter/sec",
            "range": "stddev: 0.010365218747117329",
            "extra": "mean: 638.9161729999998 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.4626342422930092,
            "unit": "iter/sec",
            "range": "stddev: 0.008059258450283194",
            "extra": "mean: 683.6979274000001 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9364197599770848,
            "unit": "iter/sec",
            "range": "stddev: 0.010752702810505499",
            "extra": "mean: 1.0678971575999967 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.16947060273822329,
            "unit": "iter/sec",
            "range": "stddev: 0.07143495638174809",
            "extra": "mean: 5.900728408600005 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 6.132677971769023,
            "unit": "iter/sec",
            "range": "stddev: 0.00022917241715682954",
            "extra": "mean: 163.06090171428676 msec\nrounds: 7"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.5878146593973796,
            "unit": "iter/sec",
            "range": "stddev: 0.00824698421195294",
            "extra": "mean: 386.4264376000051 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.1104491989227343,
            "unit": "iter/sec",
            "range": "stddev: 0.0017557328680348067",
            "extra": "mean: 473.83277480000174 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.8362986508433582,
            "unit": "iter/sec",
            "range": "stddev: 0.010829531385051503",
            "extra": "mean: 1.1957450834000014 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.341468870373902,
            "unit": "iter/sec",
            "range": "stddev: 0.021047416680796443",
            "extra": "mean: 2.928524637999999 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.13736898027340694,
            "unit": "iter/sec",
            "range": "stddev: 0.03449318161103714",
            "extra": "mean: 7.2796638514 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.08681667557043067,
            "unit": "iter/sec",
            "range": "stddev: 0.12545354073634868",
            "extra": "mean: 11.5185244474 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 28.459855563095157,
            "unit": "iter/sec",
            "range": "stddev: 0.00019791701737338388",
            "extra": "mean: 35.13721275861756 msec\nrounds: 29"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 18.084371459561332,
            "unit": "iter/sec",
            "range": "stddev: 0.00016732679292830679",
            "extra": "mean: 55.29636472221947 msec\nrounds: 18"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.48502014681236,
            "unit": "iter/sec",
            "range": "stddev: 0.0009711008088068505",
            "extra": "mean: 154.20152557144158 msec\nrounds: 7"
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
        "date": 1782029119324,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.3617433173469353,
            "unit": "iter/sec",
            "range": "stddev: 0.02698088400602681",
            "extra": "mean: 734.3527868000009 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.3092482119023718,
            "unit": "iter/sec",
            "range": "stddev: 0.012086330779651829",
            "extra": "mean: 763.7971096000001 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.8936093878674715,
            "unit": "iter/sec",
            "range": "stddev: 0.017315680143044358",
            "extra": "mean: 1.1190571781999978 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.18225969943172723,
            "unit": "iter/sec",
            "range": "stddev: 0.03787807288799207",
            "extra": "mean: 5.486676446399993 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.281584481259652,
            "unit": "iter/sec",
            "range": "stddev: 0.0010040738321366852",
            "extra": "mean: 189.33712100000358 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.181003152836348,
            "unit": "iter/sec",
            "range": "stddev: 0.01057973066938427",
            "extra": "mean: 458.50460999999996 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.7543363584356233,
            "unit": "iter/sec",
            "range": "stddev: 0.004550255417129796",
            "extra": "mean: 570.0161176000023 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.6951835594530629,
            "unit": "iter/sec",
            "range": "stddev: 0.024902836771668452",
            "extra": "mean: 1.4384690006000027 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.2807994578420214,
            "unit": "iter/sec",
            "range": "stddev: 0.03344046253381707",
            "extra": "mean: 3.561260437199999 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11646530717855726,
            "unit": "iter/sec",
            "range": "stddev: 0.020291917158618784",
            "extra": "mean: 8.586247907000006 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.07369804560922408,
            "unit": "iter/sec",
            "range": "stddev: 0.06614307027815652",
            "extra": "mean: 13.568880853399993 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 23.247906916837923,
            "unit": "iter/sec",
            "range": "stddev: 0.0009244642869287839",
            "extra": "mean: 43.01462508333268 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 15.083562787001613,
            "unit": "iter/sec",
            "range": "stddev: 0.001278047216529245",
            "extra": "mean: 66.29733400001214 msec\nrounds: 16"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.066434304639651,
            "unit": "iter/sec",
            "range": "stddev: 0.0007488409252164399",
            "extra": "mean: 164.84147850001327 msec\nrounds: 6"
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
        "date": 1782118981998,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.3771057542704086,
            "unit": "iter/sec",
            "range": "stddev: 0.015673223225342977",
            "extra": "mean: 726.160643 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.3082607583636257,
            "unit": "iter/sec",
            "range": "stddev: 0.013110960357160608",
            "extra": "mean: 764.3736109999978 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.8745546214711685,
            "unit": "iter/sec",
            "range": "stddev: 0.022924852513870234",
            "extra": "mean: 1.1434391579999983 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.17060900144001023,
            "unit": "iter/sec",
            "range": "stddev: 0.019382344174929435",
            "extra": "mean: 5.861355447599999 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.290661155424849,
            "unit": "iter/sec",
            "range": "stddev: 0.0011319815293038473",
            "extra": "mean: 189.01229366666902 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.1993573967703557,
            "unit": "iter/sec",
            "range": "stddev: 0.009019935812897461",
            "extra": "mean: 454.6782625999981 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.7433359316511705,
            "unit": "iter/sec",
            "range": "stddev: 0.011970602829727455",
            "extra": "mean: 573.6129118000036 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.6918809396544766,
            "unit": "iter/sec",
            "range": "stddev: 0.030869391117632674",
            "extra": "mean: 1.4453353787999959 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.27913741104177786,
            "unit": "iter/sec",
            "range": "stddev: 0.041636555347878045",
            "extra": "mean: 3.582464981200002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11620927793976907,
            "unit": "iter/sec",
            "range": "stddev: 0.10360064961347709",
            "extra": "mean: 8.605164903600013 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.07205384528982291,
            "unit": "iter/sec",
            "range": "stddev: 0.08694170683791803",
            "extra": "mean: 13.878509828000016 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 23.598606580946953,
            "unit": "iter/sec",
            "range": "stddev: 0.00029516531035849185",
            "extra": "mean: 42.37538333332699 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 15.159422441201901,
            "unit": "iter/sec",
            "range": "stddev: 0.0015534982999905692",
            "extra": "mean: 65.96557381250179 msec\nrounds: 16"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 5.800561593551635,
            "unit": "iter/sec",
            "range": "stddev: 0.008932151209831821",
            "extra": "mean: 172.39710050000667 msec\nrounds: 6"
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
        "date": 1782197742912,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.420988932967874,
            "unit": "iter/sec",
            "range": "stddev: 0.006273848850239575",
            "extra": "mean: 703.7352486000032 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.339609197373513,
            "unit": "iter/sec",
            "range": "stddev: 0.009482330048636443",
            "extra": "mean: 746.4863648000005 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9091176847555491,
            "unit": "iter/sec",
            "range": "stddev: 0.005837166614974198",
            "extra": "mean: 1.0999676023999996 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.18393186420459104,
            "unit": "iter/sec",
            "range": "stddev: 0.06387003686661183",
            "extra": "mean: 5.4367958718000065 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.386738628419711,
            "unit": "iter/sec",
            "range": "stddev: 0.0005073251570050437",
            "extra": "mean: 185.64108433331702 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.263976906280032,
            "unit": "iter/sec",
            "range": "stddev: 0.005965132085477895",
            "extra": "mean: 441.70061859999805 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.788557775747502,
            "unit": "iter/sec",
            "range": "stddev: 0.009151044010943073",
            "extra": "mean: 559.1096991999962 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.7204355769405347,
            "unit": "iter/sec",
            "range": "stddev: 0.012292953780224736",
            "extra": "mean: 1.38804916360001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.28355417977562875,
            "unit": "iter/sec",
            "range": "stddev: 0.023120615462930507",
            "extra": "mean: 3.5266628789999914 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11916796512427062,
            "unit": "iter/sec",
            "range": "stddev: 0.07382256192668472",
            "extra": "mean: 8.391516956399993 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.07519502491653891,
            "unit": "iter/sec",
            "range": "stddev: 0.04099624829672298",
            "extra": "mean: 13.298752159600031 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 23.55566959291728,
            "unit": "iter/sec",
            "range": "stddev: 0.00017903059971028441",
            "extra": "mean: 42.452624666661144 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 15.202321136001707,
            "unit": "iter/sec",
            "range": "stddev: 0.00046955681653302385",
            "extra": "mean: 65.77942874998399 msec\nrounds: 16"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 5.972201004871817,
            "unit": "iter/sec",
            "range": "stddev: 0.0008929603715213122",
            "extra": "mean: 167.4424553333438 msec\nrounds: 6"
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
        "date": 1782284045429,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.3646232768061917,
            "unit": "iter/sec",
            "range": "stddev: 0.010366185077730673",
            "extra": "mean: 732.8029772000023 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.2752092586003052,
            "unit": "iter/sec",
            "range": "stddev: 0.010757504281077343",
            "extra": "mean: 784.1850215999997 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.8641927368990213,
            "unit": "iter/sec",
            "range": "stddev: 0.022152040941214104",
            "extra": "mean: 1.1571492762000006 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.17264452119483245,
            "unit": "iter/sec",
            "range": "stddev: 0.0576634677761352",
            "extra": "mean: 5.792248679999998 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.011949007677003,
            "unit": "iter/sec",
            "range": "stddev: 0.0014255868117947557",
            "extra": "mean: 199.52317919999984 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.106836376527973,
            "unit": "iter/sec",
            "range": "stddev: 0.017138133761704113",
            "extra": "mean: 474.64530760000514 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.6946463747499843,
            "unit": "iter/sec",
            "range": "stddev: 0.007699824048259915",
            "extra": "mean: 590.0936118000033 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.6741779234586026,
            "unit": "iter/sec",
            "range": "stddev: 0.01472650673652319",
            "extra": "mean: 1.4832879647999988 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.27527533085939926,
            "unit": "iter/sec",
            "range": "stddev: 0.04529770158047664",
            "extra": "mean: 3.6327265391999988 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11260861688352351,
            "unit": "iter/sec",
            "range": "stddev: 0.07229345042403139",
            "extra": "mean: 8.880315092 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.07052976979976075,
            "unit": "iter/sec",
            "range": "stddev: 0.034028689858146506",
            "extra": "mean: 14.178410093199995 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 22.80126117502925,
            "unit": "iter/sec",
            "range": "stddev: 0.0011512886470885714",
            "extra": "mean: 43.85722317391583 msec\nrounds: 23"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 14.860687430573774,
            "unit": "iter/sec",
            "range": "stddev: 0.0005008446742368728",
            "extra": "mean: 67.29163806666443 msec\nrounds: 15"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 5.844935383946755,
            "unit": "iter/sec",
            "range": "stddev: 0.0036078979404643033",
            "extra": "mean: 171.0882900000096 msec\nrounds: 6"
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
        "date": 1782370379112,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.4086347096142884,
            "unit": "iter/sec",
            "range": "stddev: 0.008794847387200388",
            "extra": "mean: 709.9072549999988 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.3176536689432194,
            "unit": "iter/sec",
            "range": "stddev: 0.009208638573423857",
            "extra": "mean: 758.9247642000017 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.898732924388321,
            "unit": "iter/sec",
            "range": "stddev: 0.006230567661939416",
            "extra": "mean: 1.1126776073999978 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.1832863443128273,
            "unit": "iter/sec",
            "range": "stddev: 0.037344469719628653",
            "extra": "mean: 5.455943833400004 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.267006662831878,
            "unit": "iter/sec",
            "range": "stddev: 0.0017821581858023662",
            "extra": "mean: 189.8611610000008 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.2488936642956325,
            "unit": "iter/sec",
            "range": "stddev: 0.007609551755270321",
            "extra": "mean: 444.66308740000215 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.7767169555171967,
            "unit": "iter/sec",
            "range": "stddev: 0.008128795949923722",
            "extra": "mean: 562.8358512000034 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.7161978598482742,
            "unit": "iter/sec",
            "range": "stddev: 0.011148556014219673",
            "extra": "mean: 1.3962622007999983 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.28167188630106965,
            "unit": "iter/sec",
            "range": "stddev: 0.031770542911589615",
            "extra": "mean: 3.5502300677999985 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11684824797193774,
            "unit": "iter/sec",
            "range": "stddev: 0.0480781107709898",
            "extra": "mean: 8.558108635399993 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.07414043739266939,
            "unit": "iter/sec",
            "range": "stddev: 0.034845260047283576",
            "extra": "mean: 13.487916111199997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 23.585665218000543,
            "unit": "iter/sec",
            "range": "stddev: 0.00017828559153556115",
            "extra": "mean: 42.39863454166226 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 15.3236444451531,
            "unit": "iter/sec",
            "range": "stddev: 0.00032192196946911184",
            "extra": "mean: 65.25862718749664 msec\nrounds: 16"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 5.902629010006459,
            "unit": "iter/sec",
            "range": "stddev: 0.009307862810060644",
            "extra": "mean: 169.4160345000076 msec\nrounds: 6"
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
        "date": 1782457199283,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.3684097134701376,
            "unit": "iter/sec",
            "range": "stddev: 0.014467220304932813",
            "extra": "mean: 730.7752862000001 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.2753465055494053,
            "unit": "iter/sec",
            "range": "stddev: 0.01215776555709689",
            "extra": "mean: 784.1006311999977 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.8738436296609069,
            "unit": "iter/sec",
            "range": "stddev: 0.01774360817860788",
            "extra": "mean: 1.1443695028000007 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.17382031517685312,
            "unit": "iter/sec",
            "range": "stddev: 0.018618553807534476",
            "extra": "mean: 5.7530674650000035 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.141169254392623,
            "unit": "iter/sec",
            "range": "stddev: 0.0016861697911637061",
            "extra": "mean: 194.5082821666683 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.1691763733621703,
            "unit": "iter/sec",
            "range": "stddev: 0.009684790895710074",
            "extra": "mean: 461.00446800000157 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.734852988495299,
            "unit": "iter/sec",
            "range": "stddev: 0.005466883106435996",
            "extra": "mean: 576.4177176000004 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.6925105984031099,
            "unit": "iter/sec",
            "range": "stddev: 0.01884502663642581",
            "extra": "mean: 1.4440212211999977 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.2788761798732811,
            "unit": "iter/sec",
            "range": "stddev: 0.028678665920486075",
            "extra": "mean: 3.5858207769999977 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11583066383616694,
            "unit": "iter/sec",
            "range": "stddev: 0.05460262714728211",
            "extra": "mean: 8.633292488200004 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.07293356272520596,
            "unit": "iter/sec",
            "range": "stddev: 0.04332032445703162",
            "extra": "mean: 13.711108612199997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 22.698412839239527,
            "unit": "iter/sec",
            "range": "stddev: 0.00037858785206318346",
            "extra": "mean: 44.055943782609575 msec\nrounds: 23"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 14.72765542995456,
            "unit": "iter/sec",
            "range": "stddev: 0.0003558346400862156",
            "extra": "mean: 67.89947013331812 msec\nrounds: 15"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 5.846889999888824,
            "unit": "iter/sec",
            "range": "stddev: 0.0013681604982913292",
            "extra": "mean: 171.03109516666373 msec\nrounds: 6"
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
        "date": 1782542029164,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.3992060293816089,
            "unit": "iter/sec",
            "range": "stddev: 0.007141075085071302",
            "extra": "mean: 714.6910312000003 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.3166575193070502,
            "unit": "iter/sec",
            "range": "stddev: 0.010549740262399831",
            "extra": "mean: 759.4989474000002 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9105064895882949,
            "unit": "iter/sec",
            "range": "stddev: 0.00680845501595466",
            "extra": "mean: 1.0982898106000007 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.18677767581266091,
            "unit": "iter/sec",
            "range": "stddev: 0.0013291384338197023",
            "extra": "mean: 5.353958901400003 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.248480707200192,
            "unit": "iter/sec",
            "range": "stddev: 0.0006197543737695994",
            "extra": "mean: 190.53132816667073 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.2152746375367527,
            "unit": "iter/sec",
            "range": "stddev: 0.00819360531009651",
            "extra": "mean: 451.41129820000003 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.8022308515943022,
            "unit": "iter/sec",
            "range": "stddev: 0.000997934515093486",
            "extra": "mean: 554.8678733999992 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.7208324518807885,
            "unit": "iter/sec",
            "range": "stddev: 0.009753044469714584",
            "extra": "mean: 1.3872849334000024 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.2876039327590352,
            "unit": "iter/sec",
            "range": "stddev: 0.021759252951439698",
            "extra": "mean: 3.477003914400001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11980497872025193,
            "unit": "iter/sec",
            "range": "stddev: 0.009680851071612321",
            "extra": "mean: 8.346898523599998 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.07599723617963289,
            "unit": "iter/sec",
            "range": "stddev: 0.056349386301284235",
            "extra": "mean: 13.158373255000004 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 23.30332039146818,
            "unit": "iter/sec",
            "range": "stddev: 0.00013689434214284488",
            "extra": "mean: 42.91233966667344 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 15.048924776798337,
            "unit": "iter/sec",
            "range": "stddev: 0.0003860861518453042",
            "extra": "mean: 66.44993013333078 msec\nrounds: 15"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.0743188784239095,
            "unit": "iter/sec",
            "range": "stddev: 0.0010443418363749975",
            "extra": "mean: 164.62751133333123 msec\nrounds: 6"
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
        "date": 1782630397953,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.5361538492145754,
            "unit": "iter/sec",
            "range": "stddev: 0.014651319529760265",
            "extra": "mean: 650.9764633999993 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.4159178048251027,
            "unit": "iter/sec",
            "range": "stddev: 0.019050260451915785",
            "extra": "mean: 706.2556856000001 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9224227988412836,
            "unit": "iter/sec",
            "range": "stddev: 0.013143977945207523",
            "extra": "mean: 1.0841015651999997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.1709229434209456,
            "unit": "iter/sec",
            "range": "stddev: 0.053498736992913194",
            "extra": "mean: 5.850589628200001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.957919055992594,
            "unit": "iter/sec",
            "range": "stddev: 0.004294609804726594",
            "extra": "mean: 167.84383785714243 msec\nrounds: 7"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.517980017790997,
            "unit": "iter/sec",
            "range": "stddev: 0.013475466294006077",
            "extra": "mean: 397.143739400002 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.044120353396025,
            "unit": "iter/sec",
            "range": "stddev: 0.0036953563245921014",
            "extra": "mean: 489.20798539999737 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.7849378291271885,
            "unit": "iter/sec",
            "range": "stddev: 0.007312837103566059",
            "extra": "mean: 1.2739862482000006 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.33334393627058917,
            "unit": "iter/sec",
            "range": "stddev: 0.02643677069118602",
            "extra": "mean: 2.9999045766000023 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.13486703252741242,
            "unit": "iter/sec",
            "range": "stddev: 0.08960616520517552",
            "extra": "mean: 7.414710483799996 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.08344338950663079,
            "unit": "iter/sec",
            "range": "stddev: 0.16532643156693005",
            "extra": "mean: 11.984172813599997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 27.904654400182665,
            "unit": "iter/sec",
            "range": "stddev: 0.000364497457216125",
            "extra": "mean: 35.83631553571414 msec\nrounds: 28"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 17.61269026584664,
            "unit": "iter/sec",
            "range": "stddev: 0.000299538390583622",
            "extra": "mean: 56.77724327777077 msec\nrounds: 18"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.333095574449979,
            "unit": "iter/sec",
            "range": "stddev: 0.0010943419432212925",
            "extra": "mean: 157.90066457142464 msec\nrounds: 7"
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
        "date": 1782721003629,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.5184273579099699,
            "unit": "iter/sec",
            "range": "stddev: 0.010666702090560436",
            "extra": "mean: 658.5761214000015 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.4140392998218585,
            "unit": "iter/sec",
            "range": "stddev: 0.011928426929740062",
            "extra": "mean: 707.1939231999991 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.931840668260187,
            "unit": "iter/sec",
            "range": "stddev: 0.01441962555736024",
            "extra": "mean: 1.0731448348000001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.16958601035562856,
            "unit": "iter/sec",
            "range": "stddev: 0.05272760712414627",
            "extra": "mean: 5.896712812000002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 6.092759684608835,
            "unit": "iter/sec",
            "range": "stddev: 0.0006751076739648198",
            "extra": "mean: 164.12923728571474 msec\nrounds: 7"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.546151020345335,
            "unit": "iter/sec",
            "range": "stddev: 0.011462259746181442",
            "extra": "mean: 392.7496806000022 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.054393850708118,
            "unit": "iter/sec",
            "range": "stddev: 0.003223456228848803",
            "extra": "mean: 486.76158160000114 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.808177695884275,
            "unit": "iter/sec",
            "range": "stddev: 0.010246669142383515",
            "extra": "mean: 1.2373516432000031 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.3295179047397038,
            "unit": "iter/sec",
            "range": "stddev: 0.02703556544412661",
            "extra": "mean: 3.034736460799999 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.1340047017669567,
            "unit": "iter/sec",
            "range": "stddev: 0.06960110878045915",
            "extra": "mean: 7.462424727000013 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.08504393324986148,
            "unit": "iter/sec",
            "range": "stddev: 0.031131768787302005",
            "extra": "mean: 11.758628296999996 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 28.20511024116295,
            "unit": "iter/sec",
            "range": "stddev: 0.000196440987588557",
            "extra": "mean: 35.45456803570955 msec\nrounds: 28"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 17.951635439815345,
            "unit": "iter/sec",
            "range": "stddev: 0.0004065161422619944",
            "extra": "mean: 55.705231055554805 msec\nrounds: 18"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.344566551861849,
            "unit": "iter/sec",
            "range": "stddev: 0.0011227971437725943",
            "extra": "mean: 157.61518014284906 msec\nrounds: 7"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1782802848685,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.4150536410779793,
            "unit": "iter/sec",
            "range": "stddev: 0.008715102485723838",
            "extra": "mean: 706.6869911999987 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.3220466079054636,
            "unit": "iter/sec",
            "range": "stddev: 0.010996460848983355",
            "extra": "mean: 756.4029846000011 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9146379673531123,
            "unit": "iter/sec",
            "range": "stddev: 0.008268983987350305",
            "extra": "mean: 1.0933287658000013 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.18290863600206406,
            "unit": "iter/sec",
            "range": "stddev: 0.05103525377178078",
            "extra": "mean: 5.467210416399996 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.300595208253089,
            "unit": "iter/sec",
            "range": "stddev: 0.00401434999911183",
            "extra": "mean: 188.65805833333363 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.2584437422000274,
            "unit": "iter/sec",
            "range": "stddev: 0.007621177420242767",
            "extra": "mean: 442.78278060000105 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.7687175593410434,
            "unit": "iter/sec",
            "range": "stddev: 0.007955709308948898",
            "extra": "mean: 565.3813943999978 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.713581006251513,
            "unit": "iter/sec",
            "range": "stddev: 0.01938263762496021",
            "extra": "mean: 1.4013825918000038 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.27937259528184305,
            "unit": "iter/sec",
            "range": "stddev: 0.02997609533202591",
            "extra": "mean: 3.5794491545999962 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11601488045772779,
            "unit": "iter/sec",
            "range": "stddev: 0.07225541685540202",
            "extra": "mean: 8.619583936600003 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.07331211544586401,
            "unit": "iter/sec",
            "range": "stddev: 0.06476880444455971",
            "extra": "mean: 13.640310253199988 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 23.665720794477185,
            "unit": "iter/sec",
            "range": "stddev: 0.00018208933627597248",
            "extra": "mean: 42.25520991667272 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 15.301924915304642,
            "unit": "iter/sec",
            "range": "stddev: 0.00020861447768024262",
            "extra": "mean: 65.35125518749751 msec\nrounds: 16"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.048974865661106,
            "unit": "iter/sec",
            "range": "stddev: 0.0010468015582352323",
            "extra": "mean: 165.31726816667933 msec\nrounds: 6"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1782890191748,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.398533642287017,
            "unit": "iter/sec",
            "range": "stddev: 0.008725225122325764",
            "extra": "mean: 715.0346404000004 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.328474210058224,
            "unit": "iter/sec",
            "range": "stddev: 0.009114870813713824",
            "extra": "mean: 752.7432541999985 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9157644574920374,
            "unit": "iter/sec",
            "range": "stddev: 0.007062934821054733",
            "extra": "mean: 1.091983852200002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.17866673547003528,
            "unit": "iter/sec",
            "range": "stddev: 0.09418389239957861",
            "extra": "mean: 5.597012770000004 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.338372866459487,
            "unit": "iter/sec",
            "range": "stddev: 0.0006648058256081089",
            "extra": "mean: 187.32299616666145 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.2481435248926442,
            "unit": "iter/sec",
            "range": "stddev: 0.007258848031932145",
            "extra": "mean: 444.81145839999385 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.797553846519073,
            "unit": "iter/sec",
            "range": "stddev: 0.005177129569557903",
            "extra": "mean: 556.311568600006 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.7205312236573345,
            "unit": "iter/sec",
            "range": "stddev: 0.006392976353545258",
            "extra": "mean: 1.3878649074000067 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.28573888933482755,
            "unit": "iter/sec",
            "range": "stddev: 0.00974918835412327",
            "extra": "mean: 3.4996986316000003 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11902549299913988,
            "unit": "iter/sec",
            "range": "stddev: 0.05091069541283066",
            "extra": "mean: 8.401561504199998 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.07264758831180602,
            "unit": "iter/sec",
            "range": "stddev: 0.09309248551001392",
            "extra": "mean: 13.765081859399993 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 22.9903597963199,
            "unit": "iter/sec",
            "range": "stddev: 0.00022976783395979003",
            "extra": "mean: 43.49649195834123 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 14.89738452121943,
            "unit": "iter/sec",
            "range": "stddev: 0.00031844669514439057",
            "extra": "mean: 67.12587693333869 msec\nrounds: 15"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 5.939102057004145,
            "unit": "iter/sec",
            "range": "stddev: 0.00217635895936834",
            "extra": "mean: 168.37562149999977 msec\nrounds: 6"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1782974754154,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.3490021592503665,
            "unit": "iter/sec",
            "range": "stddev: 0.0223984152337704",
            "extra": "mean: 741.2886577999956 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.2944599083501616,
            "unit": "iter/sec",
            "range": "stddev: 0.015043333959149047",
            "extra": "mean: 772.5229600000034 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.857610237030765,
            "unit": "iter/sec",
            "range": "stddev: 0.020932323583701246",
            "extra": "mean: 1.1660308573999998 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.1707048973210448,
            "unit": "iter/sec",
            "range": "stddev: 0.06699695466494943",
            "extra": "mean: 5.8580627485999965 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.037490855707369,
            "unit": "iter/sec",
            "range": "stddev: 0.003561502346157759",
            "extra": "mean: 198.51152659999798 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.1640011757468747,
            "unit": "iter/sec",
            "range": "stddev: 0.0120805659751059",
            "extra": "mean: 462.1069577999947 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.6690673814181898,
            "unit": "iter/sec",
            "range": "stddev: 0.007759686166399901",
            "extra": "mean: 599.1369858000041 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.6709899948589234,
            "unit": "iter/sec",
            "range": "stddev: 0.011819631717963816",
            "extra": "mean: 1.490335187800008 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.2741616215392981,
            "unit": "iter/sec",
            "range": "stddev: 0.03541951757188716",
            "extra": "mean: 3.6474835332 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11355337348369036,
            "unit": "iter/sec",
            "range": "stddev: 0.12313128762783825",
            "extra": "mean: 8.806431454399984 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.07119541716650044,
            "unit": "iter/sec",
            "range": "stddev: 0.141035681729654",
            "extra": "mean: 14.045847890200013 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 23.91051287317453,
            "unit": "iter/sec",
            "range": "stddev: 0.0005363233063453831",
            "extra": "mean: 41.82260770834034 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 15.46862967702324,
            "unit": "iter/sec",
            "range": "stddev: 0.0007049853856034595",
            "extra": "mean: 64.64696749999632 msec\nrounds: 16"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.093240273792189,
            "unit": "iter/sec",
            "range": "stddev: 0.0011126742073098107",
            "extra": "mean: 164.11629200002645 msec\nrounds: 6"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1783060614176,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.5439672100914963,
            "unit": "iter/sec",
            "range": "stddev: 0.008305413518470913",
            "extra": "mean: 647.6821485999949 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.3949311357859724,
            "unit": "iter/sec",
            "range": "stddev: 0.03579539821556179",
            "extra": "mean: 716.8812670000023 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9308282433623478,
            "unit": "iter/sec",
            "range": "stddev: 0.015841011321574776",
            "extra": "mean: 1.0743120518000069 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.17667548512869435,
            "unit": "iter/sec",
            "range": "stddev: 0.02466384601333734",
            "extra": "mean: 5.6600948302 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 6.1097750492634315,
            "unit": "iter/sec",
            "range": "stddev: 0.00040187434833853606",
            "extra": "mean: 163.67214700000383 msec\nrounds: 7"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.5447431020943267,
            "unit": "iter/sec",
            "range": "stddev: 0.010299942636263054",
            "extra": "mean: 392.9669753999917 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.079544022009042,
            "unit": "iter/sec",
            "range": "stddev: 0.0053695018244658025",
            "extra": "mean: 480.8746481999947 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.8018082678971711,
            "unit": "iter/sec",
            "range": "stddev: 0.032968266158201164",
            "extra": "mean: 1.2471809534000045 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.3335183396250241,
            "unit": "iter/sec",
            "range": "stddev: 0.059758219433777515",
            "extra": "mean: 2.9983358670000086 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.13699843965681927,
            "unit": "iter/sec",
            "range": "stddev: 0.02816849705650151",
            "extra": "mean: 7.299353208000014 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.08653798196626714,
            "unit": "iter/sec",
            "range": "stddev: 0.18731549492781452",
            "extra": "mean: 11.5556195936 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 28.38816867860001,
            "unit": "iter/sec",
            "range": "stddev: 0.00011806495458593019",
            "extra": "mean: 35.22594258620968 msec\nrounds: 29"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 18.001119327598424,
            "unit": "iter/sec",
            "range": "stddev: 0.0002289503324896709",
            "extra": "mean: 55.55210105556322 msec\nrounds: 18"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.598127517392387,
            "unit": "iter/sec",
            "range": "stddev: 0.0014327772075009093",
            "extra": "mean: 151.55814999998742 msec\nrounds: 7"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1783146231258,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.5609025494051847,
            "unit": "iter/sec",
            "range": "stddev: 0.007455731854948521",
            "extra": "mean: 640.6549853999991 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.4553266162950649,
            "unit": "iter/sec",
            "range": "stddev: 0.015710595063524704",
            "extra": "mean: 687.1309772000018 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.954295112963784,
            "unit": "iter/sec",
            "range": "stddev: 0.009670037642439148",
            "extra": "mean: 1.047893870999998 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.19510601546268616,
            "unit": "iter/sec",
            "range": "stddev: 0.014591402780011404",
            "extra": "mean: 5.1254185968 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 6.537796095711119,
            "unit": "iter/sec",
            "range": "stddev: 0.0006010510623917697",
            "extra": "mean: 152.95674342857117 msec\nrounds: 7"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.7391057122575693,
            "unit": "iter/sec",
            "range": "stddev: 0.009613495006867388",
            "extra": "mean: 365.08266019999667 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.3895604652994398,
            "unit": "iter/sec",
            "range": "stddev: 0.0017278243404012974",
            "extra": "mean: 418.48700399999643 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.9366837218188617,
            "unit": "iter/sec",
            "range": "stddev: 0.008222626890938646",
            "extra": "mean: 1.0675962191999986 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.38487537539212324,
            "unit": "iter/sec",
            "range": "stddev: 0.01897340994856302",
            "extra": "mean: 2.598243649599999 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.15644768742004886,
            "unit": "iter/sec",
            "range": "stddev: 0.01770349987997008",
            "extra": "mean: 6.391912954999995 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.10040530453250798,
            "unit": "iter/sec",
            "range": "stddev: 0.17064266835716152",
            "extra": "mean: 9.959633155399995 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 35.387812274465006,
            "unit": "iter/sec",
            "range": "stddev: 0.0003433468816269313",
            "extra": "mean: 28.25831651428692 msec\nrounds: 35"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 22.497344310771567,
            "unit": "iter/sec",
            "range": "stddev: 0.0004030630841459677",
            "extra": "mean: 44.449690869566645 msec\nrounds: 23"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 8.13182442018416,
            "unit": "iter/sec",
            "range": "stddev: 0.000611465089455839",
            "extra": "mean: 122.97363400000133 msec\nrounds: 9"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1783233889605,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.487923462645479,
            "unit": "iter/sec",
            "range": "stddev: 0.007812197222141856",
            "extra": "mean: 672.0775800000041 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.3960148287442524,
            "unit": "iter/sec",
            "range": "stddev: 0.008373872372035109",
            "extra": "mean: 716.324769199997 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9773201004079682,
            "unit": "iter/sec",
            "range": "stddev: 0.008397651815450586",
            "extra": "mean: 1.023206214199999 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.20682156378789568,
            "unit": "iter/sec",
            "range": "stddev: 0.06545798508412667",
            "extra": "mean: 4.835085769999992 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.809684079895513,
            "unit": "iter/sec",
            "range": "stddev: 0.0006545290220772816",
            "extra": "mean: 172.1263989999926 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.454575945243269,
            "unit": "iter/sec",
            "range": "stddev: 0.006382507170929724",
            "extra": "mean: 407.40234659999146 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.9611164137934172,
            "unit": "iter/sec",
            "range": "stddev: 0.004395850600698427",
            "extra": "mean: 509.9136353999938 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.7835034080759947,
            "unit": "iter/sec",
            "range": "stddev: 0.01042529175945426",
            "extra": "mean: 1.2763186345999997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.3026313221670801,
            "unit": "iter/sec",
            "range": "stddev: 0.018983882953994117",
            "extra": "mean: 3.3043506298000067 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.12813984718912458,
            "unit": "iter/sec",
            "range": "stddev: 0.07193257460003781",
            "extra": "mean: 7.8039737204 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.08037314754148896,
            "unit": "iter/sec",
            "range": "stddev: 0.016373627731470584",
            "extra": "mean: 12.441966385399997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 27.361962259831454,
            "unit": "iter/sec",
            "range": "stddev: 0.000676860749925737",
            "extra": "mean: 36.54708644445589 msec\nrounds: 27"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 17.423413459878724,
            "unit": "iter/sec",
            "range": "stddev: 0.0010542193603112603",
            "extra": "mean: 57.39403488889946 msec\nrounds: 18"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.8899688239145,
            "unit": "iter/sec",
            "range": "stddev: 0.002458311828778565",
            "extra": "mean: 145.13853771429044 msec\nrounds: 7"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1783322219009,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.538865946276753,
            "unit": "iter/sec",
            "range": "stddev: 0.009791953172581722",
            "extra": "mean: 649.8291826000013 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.43846546032918,
            "unit": "iter/sec",
            "range": "stddev: 0.012334854508225279",
            "extra": "mean: 695.185270399999 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9356673386176009,
            "unit": "iter/sec",
            "range": "stddev: 0.011735826083561945",
            "extra": "mean: 1.0687559121999997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.16640869174206135,
            "unit": "iter/sec",
            "range": "stddev: 0.024890272678658423",
            "extra": "mean: 6.0093014946 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 6.010112741051801,
            "unit": "iter/sec",
            "range": "stddev: 0.000578280937223221",
            "extra": "mean: 166.38622985714488 msec\nrounds: 7"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.524408138779113,
            "unit": "iter/sec",
            "range": "stddev: 0.013859175141402228",
            "extra": "mean: 396.1324575999953 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.061022137506796,
            "unit": "iter/sec",
            "range": "stddev: 0.0017851401016608865",
            "extra": "mean: 485.1961469999992 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.8091497855068546,
            "unit": "iter/sec",
            "range": "stddev: 0.012524598834608637",
            "extra": "mean: 1.2358651239999972 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.3274043471872037,
            "unit": "iter/sec",
            "range": "stddev: 0.022400465704598915",
            "extra": "mean: 3.054327190800001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.13360921247489274,
            "unit": "iter/sec",
            "range": "stddev: 0.042822071339509236",
            "extra": "mean: 7.484513840599993 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.08506257080303233,
            "unit": "iter/sec",
            "range": "stddev: 0.037157366180478976",
            "extra": "mean: 11.756051933999998 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 28.603889533428354,
            "unit": "iter/sec",
            "range": "stddev: 0.0001497829696714179",
            "extra": "mean: 34.96028044827034 msec\nrounds: 29"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 18.080030551063217,
            "unit": "iter/sec",
            "range": "stddev: 0.00020595969129872226",
            "extra": "mean: 55.309641052636046 msec\nrounds: 19"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.382625079414416,
            "unit": "iter/sec",
            "range": "stddev: 0.006973635547394764",
            "extra": "mean: 156.67534714286344 msec\nrounds: 7"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1783407069978,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.391854506713697,
            "unit": "iter/sec",
            "range": "stddev: 0.007889507905475494",
            "extra": "mean: 718.4658994000002 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.3090197115183178,
            "unit": "iter/sec",
            "range": "stddev: 0.01180198851790007",
            "extra": "mean: 763.9304368000012 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9001446029736224,
            "unit": "iter/sec",
            "range": "stddev: 0.006697182642935841",
            "extra": "mean: 1.110932617600001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.17988494979182332,
            "unit": "iter/sec",
            "range": "stddev: 0.012719232232616675",
            "extra": "mean: 5.559108758999999 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.289415798236041,
            "unit": "iter/sec",
            "range": "stddev: 0.00046840526362785395",
            "extra": "mean: 189.05679533333122 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.228920237495979,
            "unit": "iter/sec",
            "range": "stddev: 0.008440739328258456",
            "extra": "mean: 448.6477277999967 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.786235081052464,
            "unit": "iter/sec",
            "range": "stddev: 0.0017820899419984126",
            "extra": "mean: 559.8367261999982 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.7138957863449323,
            "unit": "iter/sec",
            "range": "stddev: 0.011030850652145128",
            "extra": "mean: 1.400764676199995 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.28173740422314125,
            "unit": "iter/sec",
            "range": "stddev: 0.023874981019241803",
            "extra": "mean: 3.5494044631999997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.1167951760332871,
            "unit": "iter/sec",
            "range": "stddev: 0.029272143035372063",
            "extra": "mean: 8.561997455400007 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.07307281357891632,
            "unit": "iter/sec",
            "range": "stddev: 0.05721633004406516",
            "extra": "mean: 13.684980104400001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 23.151213651972824,
            "unit": "iter/sec",
            "range": "stddev: 0.00025221838483437494",
            "extra": "mean: 43.19427979166809 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 15.007941527298593,
            "unit": "iter/sec",
            "range": "stddev: 0.00029966558506101977",
            "extra": "mean: 66.63138966666793 msec\nrounds: 15"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 5.9295364426270964,
            "unit": "iter/sec",
            "range": "stddev: 0.0010440187153807098",
            "extra": "mean: 168.64724749999974 msec\nrounds: 6"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1783490151779,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.2804516955000136,
            "unit": "iter/sec",
            "range": "stddev: 0.01967788803250027",
            "extra": "mean: 780.9744041999977 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.2224765992007387,
            "unit": "iter/sec",
            "range": "stddev: 0.018976285873631274",
            "extra": "mean: 818.0115682000007 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.8104086692952639,
            "unit": "iter/sec",
            "range": "stddev: 0.025456861830886218",
            "extra": "mean: 1.2339453387999981 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.16894858720977626,
            "unit": "iter/sec",
            "range": "stddev: 0.03337892335912065",
            "extra": "mean: 5.918960415800001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 4.716530512080673,
            "unit": "iter/sec",
            "range": "stddev: 0.0045451393766261575",
            "extra": "mean: 212.02025459999732 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 1.9821587657579514,
            "unit": "iter/sec",
            "range": "stddev: 0.017307974553871737",
            "extra": "mean: 504.5004554000059 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.5683376413733305,
            "unit": "iter/sec",
            "range": "stddev: 0.009180952621315453",
            "extra": "mean: 637.6178022000033 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.6316717478739986,
            "unit": "iter/sec",
            "range": "stddev: 0.02843129916690098",
            "extra": "mean: 1.5831007218000082 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.25880971658373214,
            "unit": "iter/sec",
            "range": "stddev: 0.040178184779487945",
            "extra": "mean: 3.8638425681999933 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11039154541491031,
            "unit": "iter/sec",
            "range": "stddev: 0.06554808263399373",
            "extra": "mean: 9.0586647396 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.06769693870449048,
            "unit": "iter/sec",
            "range": "stddev: 0.0636626435430666",
            "extra": "mean: 14.771716700000024 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 22.9359342704031,
            "unit": "iter/sec",
            "range": "stddev: 0.00015090372673461143",
            "extra": "mean: 43.59970639131174 msec\nrounds: 23"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 14.78157463752947,
            "unit": "iter/sec",
            "range": "stddev: 0.00030670777296088283",
            "extra": "mean: 67.65179113333868 msec\nrounds: 15"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 5.758460725672425,
            "unit": "iter/sec",
            "range": "stddev: 0.005379922866868172",
            "extra": "mean: 173.65751850000302 msec\nrounds: 6"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1783579802373,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.3735237721552762,
            "unit": "iter/sec",
            "range": "stddev: 0.010861630288290009",
            "extra": "mean: 728.0543812000004 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.2965506431330218,
            "unit": "iter/sec",
            "range": "stddev: 0.011126320090401659",
            "extra": "mean: 771.277238799999 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.8932772955140584,
            "unit": "iter/sec",
            "range": "stddev: 0.023848361806364463",
            "extra": "mean: 1.1194732084000023 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.17812497243805506,
            "unit": "iter/sec",
            "range": "stddev: 0.10260120408907047",
            "extra": "mean: 5.6140359563999995 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.1668563580381575,
            "unit": "iter/sec",
            "range": "stddev: 0.0008002895211606099",
            "extra": "mean: 193.54128133333623 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.168900807070144,
            "unit": "iter/sec",
            "range": "stddev: 0.011259827180700644",
            "extra": "mean: 461.06304020000266 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.7055663204913212,
            "unit": "iter/sec",
            "range": "stddev: 0.005366356654439318",
            "extra": "mean: 586.3155176000021 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.6838782789337202,
            "unit": "iter/sec",
            "range": "stddev: 0.017003465583998154",
            "extra": "mean: 1.462248518200002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.276911472144368,
            "unit": "iter/sec",
            "range": "stddev: 0.04033376286681594",
            "extra": "mean: 3.611262445199992 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11415256250729021,
            "unit": "iter/sec",
            "range": "stddev: 0.09164319410600007",
            "extra": "mean: 8.760206324200004 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.07280416796528764,
            "unit": "iter/sec",
            "range": "stddev: 0.0729397909080469",
            "extra": "mean: 13.735477349000002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 22.46406831983506,
            "unit": "iter/sec",
            "range": "stddev: 0.002526292261325116",
            "extra": "mean: 44.51553413043317 msec\nrounds: 23"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 14.852174465869158,
            "unit": "iter/sec",
            "range": "stddev: 0.0008974357803684474",
            "extra": "mean: 67.3302082666775 msec\nrounds: 15"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 5.883779451967152,
            "unit": "iter/sec",
            "range": "stddev: 0.0018504752580987469",
            "extra": "mean: 169.9587838333514 msec\nrounds: 6"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1783666201359,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.5370737642191306,
            "unit": "iter/sec",
            "range": "stddev: 0.012181702596129223",
            "extra": "mean: 650.5868640000003 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.4281826727593279,
            "unit": "iter/sec",
            "range": "stddev: 0.010327277802912782",
            "extra": "mean: 700.1905422000008 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9295257272348904,
            "unit": "iter/sec",
            "range": "stddev: 0.011865904079844674",
            "extra": "mean: 1.0758174525999977 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.16825513689144073,
            "unit": "iter/sec",
            "range": "stddev: 0.035343053308368635",
            "extra": "mean: 5.943354945799999 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.932669598783087,
            "unit": "iter/sec",
            "range": "stddev: 0.00367592352112137",
            "extra": "mean: 168.55818166666836 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.5180871797347053,
            "unit": "iter/sec",
            "range": "stddev: 0.009225440468520488",
            "extra": "mean: 397.1268382000005 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.0295436916478247,
            "unit": "iter/sec",
            "range": "stddev: 0.009559367385341204",
            "extra": "mean: 492.72159260000024 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.8175684587470194,
            "unit": "iter/sec",
            "range": "stddev: 0.015210488438555369",
            "extra": "mean: 1.2231391625999977 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.3344589043618569,
            "unit": "iter/sec",
            "range": "stddev: 0.01603907849096664",
            "extra": "mean: 2.989903952200007 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.13619448314491328,
            "unit": "iter/sec",
            "range": "stddev: 0.033073830718630494",
            "extra": "mean: 7.3424413156000075 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.08670030336963121,
            "unit": "iter/sec",
            "range": "stddev: 0.018709047940887236",
            "extra": "mean: 11.53398501659999 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 28.054569897763006,
            "unit": "iter/sec",
            "range": "stddev: 0.0001392813942154078",
            "extra": "mean: 35.64481664285779 msec\nrounds: 28"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 17.858358571989257,
            "unit": "iter/sec",
            "range": "stddev: 0.00020763561942737722",
            "extra": "mean: 55.9961877777779 msec\nrounds: 18"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.403701002527333,
            "unit": "iter/sec",
            "range": "stddev: 0.0009203088601132194",
            "extra": "mean: 156.1596957142959 msec\nrounds: 7"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1783748714010,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.4063668298810883,
            "unit": "iter/sec",
            "range": "stddev: 0.009171060289413916",
            "extra": "mean: 711.0520375999997 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.3268597160493854,
            "unit": "iter/sec",
            "range": "stddev: 0.008428134325122547",
            "extra": "mean: 753.6591757999986 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9080608949573498,
            "unit": "iter/sec",
            "range": "stddev: 0.013516223984661733",
            "extra": "mean: 1.1012477308000015 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.18607084968812274,
            "unit": "iter/sec",
            "range": "stddev: 0.017941059590279366",
            "extra": "mean: 5.374296950199996 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.276778338127037,
            "unit": "iter/sec",
            "range": "stddev: 0.0004750615268270162",
            "extra": "mean: 189.50957116666464 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.2165525949422493,
            "unit": "iter/sec",
            "range": "stddev: 0.00727863250413513",
            "extra": "mean: 451.1510362000024 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.771946508780737,
            "unit": "iter/sec",
            "range": "stddev: 0.003598065466211614",
            "extra": "mean: 564.3511217999986 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.7032755004955837,
            "unit": "iter/sec",
            "range": "stddev: 0.015649644749270705",
            "extra": "mean: 1.4219178675999955 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.2763040294942924,
            "unit": "iter/sec",
            "range": "stddev: 0.025229456977162213",
            "extra": "mean: 3.619201652000001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.1145719413585591,
            "unit": "iter/sec",
            "range": "stddev: 0.02014196961026703",
            "extra": "mean: 8.728140486599994 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.07351456505936695,
            "unit": "iter/sec",
            "range": "stddev: 0.03921823309296281",
            "extra": "mean: 13.6027466012 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 23.15350572377221,
            "unit": "iter/sec",
            "range": "stddev: 0.0011234223782064206",
            "extra": "mean: 43.190003791662456 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 15.105122605364299,
            "unit": "iter/sec",
            "range": "stddev: 0.00021761695293076087",
            "extra": "mean: 66.20270660000263 msec\nrounds: 15"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.02825096411,
            "unit": "iter/sec",
            "range": "stddev: 0.0008597829495339263",
            "extra": "mean: 165.88559533331212 msec\nrounds: 6"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1783836061201,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.828072018851028,
            "unit": "iter/sec",
            "range": "stddev: 0.0071831893373507615",
            "extra": "mean: 547.0244003999994 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.7158777164165246,
            "unit": "iter/sec",
            "range": "stddev: 0.01114054713701552",
            "extra": "mean: 582.7921129999993 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 1.118382182905637,
            "unit": "iter/sec",
            "range": "stddev: 0.01200759535079138",
            "extra": "mean: 894.1487224000014 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.23413904490680915,
            "unit": "iter/sec",
            "range": "stddev: 0.01723026136401018",
            "extra": "mean: 4.270966426800003 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 7.590515204929146,
            "unit": "iter/sec",
            "range": "stddev: 0.005827145877277249",
            "extra": "mean: 131.743363 msec\nrounds: 8"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 3.2514804749823067,
            "unit": "iter/sec",
            "range": "stddev: 0.007733354090035447",
            "extra": "mean: 307.55220820000204 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.881438630664155,
            "unit": "iter/sec",
            "range": "stddev: 0.0038935082012776685",
            "extra": "mean: 347.0488628000055 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 1.135337842624881,
            "unit": "iter/sec",
            "range": "stddev: 0.0076709790128164194",
            "extra": "mean: 880.7950924000011 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.4738047227575493,
            "unit": "iter/sec",
            "range": "stddev: 0.010964006241865753",
            "extra": "mean: 2.1105741499999993 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.19384374695157078,
            "unit": "iter/sec",
            "range": "stddev: 0.02450688757493839",
            "extra": "mean: 5.158794213000002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.12199639813481315,
            "unit": "iter/sec",
            "range": "stddev: 0.023214394871752735",
            "extra": "mean: 8.1969633144 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 41.4443625595945,
            "unit": "iter/sec",
            "range": "stddev: 0.00015995493669723916",
            "extra": "mean: 24.12873399999964 msec\nrounds: 41"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 26.198298480286283,
            "unit": "iter/sec",
            "range": "stddev: 0.00015559936543408815",
            "extra": "mean: 38.17041785184946 msec\nrounds: 27"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 9.622975903489278,
            "unit": "iter/sec",
            "range": "stddev: 0.0001786093437082459",
            "extra": "mean: 103.91795739999736 msec\nrounds: 10"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1783923747912,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.568803842608804,
            "unit": "iter/sec",
            "range": "stddev: 0.008502431884819294",
            "extra": "mean: 637.4283214000002 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.4580598576823496,
            "unit": "iter/sec",
            "range": "stddev: 0.008248981840624432",
            "extra": "mean: 685.8428991999987 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9331500504702589,
            "unit": "iter/sec",
            "range": "stddev: 0.0177239877096957",
            "extra": "mean: 1.0716390140000016 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.17265313442193483,
            "unit": "iter/sec",
            "range": "stddev: 0.022501777164404695",
            "extra": "mean: 5.791959719399999 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 6.082928682301353,
            "unit": "iter/sec",
            "range": "stddev: 0.001132232654501688",
            "extra": "mean: 164.39449683333626 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.5627620805118108,
            "unit": "iter/sec",
            "range": "stddev: 0.010434102185750754",
            "extra": "mean: 390.2039941999959 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.1042110683083077,
            "unit": "iter/sec",
            "range": "stddev: 0.001983494979083378",
            "extra": "mean: 475.2374963999955 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.8205189269914019,
            "unit": "iter/sec",
            "range": "stddev: 0.015737312818410412",
            "extra": "mean: 1.2187409298000005 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.34120703557568366,
            "unit": "iter/sec",
            "range": "stddev: 0.023223033788481996",
            "extra": "mean: 2.9307719235999996 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.13764755138217497,
            "unit": "iter/sec",
            "range": "stddev: 0.02706987227319822",
            "extra": "mean: 7.264931268000003 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.08714941373791614,
            "unit": "iter/sec",
            "range": "stddev: 0.08257098274031598",
            "extra": "mean: 11.474546495599999 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 27.879052516630818,
            "unit": "iter/sec",
            "range": "stddev: 0.00014435644156499754",
            "extra": "mean: 35.86922473077108 msec\nrounds: 26"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 17.806007818264177,
            "unit": "iter/sec",
            "range": "stddev: 0.0006162407845563009",
            "extra": "mean: 56.16081999999286 msec\nrounds: 18"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.462798661540691,
            "unit": "iter/sec",
            "range": "stddev: 0.001300115228391762",
            "extra": "mean: 154.7317272857153 msec\nrounds: 7"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1784007281178,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.3700293968248924,
            "unit": "iter/sec",
            "range": "stddev: 0.014008705518459208",
            "extra": "mean: 729.9113451999986 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.2912556529765074,
            "unit": "iter/sec",
            "range": "stddev: 0.013649806082574704",
            "extra": "mean: 774.4399783999967 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.8888900931966937,
            "unit": "iter/sec",
            "range": "stddev: 0.015379858097737632",
            "extra": "mean: 1.1249984757999996 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.1762884285724577,
            "unit": "iter/sec",
            "range": "stddev: 0.032171418796069946",
            "extra": "mean: 5.672522059999997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.216594499023191,
            "unit": "iter/sec",
            "range": "stddev: 0.0008897627041613402",
            "extra": "mean: 191.69594266666698 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.199115280352976,
            "unit": "iter/sec",
            "range": "stddev: 0.009720218564686465",
            "extra": "mean: 454.72832140000037 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.749756353951668,
            "unit": "iter/sec",
            "range": "stddev: 0.0017860806338149595",
            "extra": "mean: 571.5081403999989 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.6962994892781786,
            "unit": "iter/sec",
            "range": "stddev: 0.014597424099224699",
            "extra": "mean: 1.4361636270000049 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.27936153932261343,
            "unit": "iter/sec",
            "range": "stddev: 0.02340491977040602",
            "extra": "mean: 3.579590814200003 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11615190338435126,
            "unit": "iter/sec",
            "range": "stddev: 0.0575689955319566",
            "extra": "mean: 8.609415522800003 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.07240336598562526,
            "unit": "iter/sec",
            "range": "stddev: 0.08139722541287642",
            "extra": "mean: 13.811512577999991 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 23.227870667524527,
            "unit": "iter/sec",
            "range": "stddev: 0.00019953015272452553",
            "extra": "mean: 43.0517292916619 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 14.949583301154437,
            "unit": "iter/sec",
            "range": "stddev: 0.001994087538923005",
            "extra": "mean: 66.89149656250137 msec\nrounds: 16"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 5.918162360716862,
            "unit": "iter/sec",
            "range": "stddev: 0.005150350539567346",
            "extra": "mean: 168.97136966665963 msec\nrounds: 6"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1784093624881,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.9367470138715446,
            "unit": "iter/sec",
            "range": "stddev: 0.009901272538635132",
            "extra": "mean: 516.3296976000013 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.810264853923964,
            "unit": "iter/sec",
            "range": "stddev: 0.008941578365881591",
            "extra": "mean: 552.4053554000019 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 1.1994814980217612,
            "unit": "iter/sec",
            "range": "stddev: 0.010626606698762467",
            "extra": "mean: 833.693559800001 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.255816744927377,
            "unit": "iter/sec",
            "range": "stddev: 0.017407735272338555",
            "extra": "mean: 3.909048253600001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 7.9648698344780176,
            "unit": "iter/sec",
            "range": "stddev: 0.006239406894608225",
            "extra": "mean: 125.55132987500173 msec\nrounds: 8"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 3.4215002066648266,
            "unit": "iter/sec",
            "range": "stddev: 0.007121182907718831",
            "extra": "mean: 292.2694547999953 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.9305743833888487,
            "unit": "iter/sec",
            "range": "stddev: 0.0017046721081919133",
            "extra": "mean: 341.2300352000017 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 1.1563963783520275,
            "unit": "iter/sec",
            "range": "stddev: 0.013056593766494996",
            "extra": "mean: 864.7553890000012 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.4627394876404943,
            "unit": "iter/sec",
            "range": "stddev: 0.018776757197391157",
            "extra": "mean: 2.1610431500000002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.18998676099978382,
            "unit": "iter/sec",
            "range": "stddev: 0.006853326042964838",
            "extra": "mean: 5.263524651600003 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.12062413170317061,
            "unit": "iter/sec",
            "range": "stddev: 0.04671234196259007",
            "extra": "mean: 8.290215116000002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 41.74637673455344,
            "unit": "iter/sec",
            "range": "stddev: 0.00014444536170023507",
            "extra": "mean: 23.954174666667562 msec\nrounds: 42"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 26.617428787352097,
            "unit": "iter/sec",
            "range": "stddev: 0.0005293099531976099",
            "extra": "mean: 37.569368851854456 msec\nrounds: 27"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 9.860045877768217,
            "unit": "iter/sec",
            "range": "stddev: 0.0006427526816585912",
            "extra": "mean: 101.41940639999802 msec\nrounds: 10"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1784180700031,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.3646712956098925,
            "unit": "iter/sec",
            "range": "stddev: 0.0116305875101597",
            "extra": "mean: 732.7771919999861 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.2789775029565962,
            "unit": "iter/sec",
            "range": "stddev: 0.01907198811496585",
            "extra": "mean: 781.8745815999989 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.8784195262673361,
            "unit": "iter/sec",
            "range": "stddev: 0.015010867789122567",
            "extra": "mean: 1.1384082094000063 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.17015135510992443,
            "unit": "iter/sec",
            "range": "stddev: 0.03385466857630355",
            "extra": "mean: 5.8771203988000025 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.0425583181618565,
            "unit": "iter/sec",
            "range": "stddev: 0.002320135736561483",
            "extra": "mean: 198.31203466666616 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.1327222077562973,
            "unit": "iter/sec",
            "range": "stddev: 0.014673738600039832",
            "extra": "mean: 468.8843190000057 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.6976983492658504,
            "unit": "iter/sec",
            "range": "stddev: 0.004473222797909542",
            "extra": "mean: 589.032792799992 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.6764317971715986,
            "unit": "iter/sec",
            "range": "stddev: 0.015556175185983795",
            "extra": "mean: 1.4783456427999908 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.2689768430407762,
            "unit": "iter/sec",
            "range": "stddev: 0.03302856901647382",
            "extra": "mean: 3.7177921663999998 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.1136071901103575,
            "unit": "iter/sec",
            "range": "stddev: 0.18027270402794773",
            "extra": "mean: 8.802259778000007 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.07221418405272954,
            "unit": "iter/sec",
            "range": "stddev: 0.2814514112632692",
            "extra": "mean: 13.847695063200012 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 22.84202276602889,
            "unit": "iter/sec",
            "range": "stddev: 0.0005745115997896764",
            "extra": "mean: 43.77895995652451 msec\nrounds: 23"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 14.78083265136615,
            "unit": "iter/sec",
            "range": "stddev: 0.0006494726507795971",
            "extra": "mean: 67.65518719999666 msec\nrounds: 15"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 5.798201197178036,
            "unit": "iter/sec",
            "range": "stddev: 0.001798669351108719",
            "extra": "mean: 172.46728183332038 msec\nrounds: 6"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1784267093806,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 2.1697421161339783,
            "unit": "iter/sec",
            "range": "stddev: 0.009224938921836751",
            "extra": "mean: 460.8842647999978 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 2.032738866115589,
            "unit": "iter/sec",
            "range": "stddev: 0.00866317645695686",
            "extra": "mean: 491.94710480000055 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 1.3555423416926617,
            "unit": "iter/sec",
            "range": "stddev: 0.012578558140309302",
            "extra": "mean: 737.7121091999996 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.2966406914983471,
            "unit": "iter/sec",
            "range": "stddev: 0.013816379431433564",
            "extra": "mean: 3.3710816777999995 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 8.710320108919161,
            "unit": "iter/sec",
            "range": "stddev: 0.0059617744407722524",
            "extra": "mean: 114.80634322222254 msec\nrounds: 9"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 3.721950059338593,
            "unit": "iter/sec",
            "range": "stddev: 0.009241890906806563",
            "extra": "mean: 268.67636160000075 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 3.2655468057775976,
            "unit": "iter/sec",
            "range": "stddev: 0.0010941618677235713",
            "extra": "mean: 306.2274282000004 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 1.2032162124332506,
            "unit": "iter/sec",
            "range": "stddev: 0.06256152743752243",
            "extra": "mean: 831.1058226000057 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.5099741873505237,
            "unit": "iter/sec",
            "range": "stddev: 0.09995955972628853",
            "extra": "mean: 1.9608835599999963 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.21119745789736663,
            "unit": "iter/sec",
            "range": "stddev: 0.15867242351226038",
            "extra": "mean: 4.734905476400002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.1336560430621328,
            "unit": "iter/sec",
            "range": "stddev: 0.16612285269491883",
            "extra": "mean: 7.481891406400001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 43.446674434370216,
            "unit": "iter/sec",
            "range": "stddev: 0.0001290157014906537",
            "extra": "mean: 23.016721372094484 msec\nrounds: 43"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 28.059012311742144,
            "unit": "iter/sec",
            "range": "stddev: 0.0000989402862841885",
            "extra": "mean: 35.63917321428737 msec\nrounds: 28"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 10.786914260161163,
            "unit": "iter/sec",
            "range": "stddev: 0.00032411062922449414",
            "extra": "mean: 92.7049178181805 msec\nrounds: 11"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1784352650848,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.344838652503903,
            "unit": "iter/sec",
            "range": "stddev: 0.012814309531911254",
            "extra": "mean: 743.5836248 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.2670578502515928,
            "unit": "iter/sec",
            "range": "stddev: 0.010251674021078891",
            "extra": "mean: 789.2299470000012 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.8573012434006096,
            "unit": "iter/sec",
            "range": "stddev: 0.033476404970546304",
            "extra": "mean: 1.1664511251999996 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.17752285747920715,
            "unit": "iter/sec",
            "range": "stddev: 0.07544731844332252",
            "extra": "mean: 5.633077420000001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 4.716929004818407,
            "unit": "iter/sec",
            "range": "stddev: 0.011643119479453012",
            "extra": "mean: 212.0023428333321 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.1324185737588266,
            "unit": "iter/sec",
            "range": "stddev: 0.010353205860586277",
            "extra": "mean: 468.95108319999963 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.6499288762849285,
            "unit": "iter/sec",
            "range": "stddev: 0.007135690519908097",
            "extra": "mean: 606.0867316000042 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.6586422438774986,
            "unit": "iter/sec",
            "range": "stddev: 0.02577759112820461",
            "extra": "mean: 1.5182749197999983 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.25701846156304997,
            "unit": "iter/sec",
            "range": "stddev: 0.05937560576046647",
            "extra": "mean: 3.890771090599992 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.10595098063542856,
            "unit": "iter/sec",
            "range": "stddev: 0.04528115531687348",
            "extra": "mean: 9.438326988599988 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.06698380138770434,
            "unit": "iter/sec",
            "range": "stddev: 0.09029724189682253",
            "extra": "mean: 14.928982519400005 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 23.730229318879818,
            "unit": "iter/sec",
            "range": "stddev: 0.00019253329275549652",
            "extra": "mean: 42.140342875001124 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 15.278391150805298,
            "unit": "iter/sec",
            "range": "stddev: 0.0008330420985765472",
            "extra": "mean: 65.45191768750414 msec\nrounds: 16"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 5.903758203081404,
            "unit": "iter/sec",
            "range": "stddev: 0.001978779062286447",
            "extra": "mean: 169.38363083333266 msec\nrounds: 6"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1784440624347,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.3970051152979601,
            "unit": "iter/sec",
            "range": "stddev: 0.011584009678726843",
            "extra": "mean: 715.8169923999992 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.321940143558674,
            "unit": "iter/sec",
            "range": "stddev: 0.009579376952738887",
            "extra": "mean: 756.4639026000009 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9043463740621263,
            "unit": "iter/sec",
            "range": "stddev: 0.026239981470715847",
            "extra": "mean: 1.1057710062000012 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.18289462727445832,
            "unit": "iter/sec",
            "range": "stddev: 0.015234914755298173",
            "extra": "mean: 5.4676291748 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.253027026619158,
            "unit": "iter/sec",
            "range": "stddev: 0.0008704954820953765",
            "extra": "mean: 190.3664296666676 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.213820598895523,
            "unit": "iter/sec",
            "range": "stddev: 0.007224016330138511",
            "extra": "mean: 451.7077854000007 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.7523578787476428,
            "unit": "iter/sec",
            "range": "stddev: 0.00413382817932122",
            "extra": "mean: 570.6596877999999 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.7014143053620135,
            "unit": "iter/sec",
            "range": "stddev: 0.013288896025329752",
            "extra": "mean: 1.425690910999998 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.2730390997714863,
            "unit": "iter/sec",
            "range": "stddev: 0.020941995771454853",
            "extra": "mean: 3.662479113200001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11308528280239834,
            "unit": "iter/sec",
            "range": "stddev: 0.034764431262434954",
            "extra": "mean: 8.842883664600004 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.07114832680668676,
            "unit": "iter/sec",
            "range": "stddev: 0.029747544396483194",
            "extra": "mean: 14.055144300400002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 23.969643932076202,
            "unit": "iter/sec",
            "range": "stddev: 0.00024752223941963556",
            "extra": "mean: 41.719434916669705 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 15.422698401674603,
            "unit": "iter/sec",
            "range": "stddev: 0.0002513274128945018",
            "extra": "mean: 64.83949656250942 msec\nrounds: 16"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.06365448633766,
            "unit": "iter/sec",
            "range": "stddev: 0.0004996510789167801",
            "extra": "mean: 164.91704833333642 msec\nrounds: 6"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1784528557614,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.363518145001772,
            "unit": "iter/sec",
            "range": "stddev: 0.018865265249920292",
            "extra": "mean: 733.3969141999944 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.2695058333526492,
            "unit": "iter/sec",
            "range": "stddev: 0.014068151758346957",
            "extra": "mean: 787.7080779999972 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.882745206040561,
            "unit": "iter/sec",
            "range": "stddev: 0.04481062760459397",
            "extra": "mean: 1.1328297148000046 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.19056798849915824,
            "unit": "iter/sec",
            "range": "stddev: 0.0238693834532901",
            "extra": "mean: 5.2474710357999985 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.4702672462867294,
            "unit": "iter/sec",
            "range": "stddev: 0.0009512739554906616",
            "extra": "mean: 182.8064251666698 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.2857392245659867,
            "unit": "iter/sec",
            "range": "stddev: 0.007027554391970578",
            "extra": "mean: 437.495226599998 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.8188290309655588,
            "unit": "iter/sec",
            "range": "stddev: 0.003666345423325987",
            "extra": "mean: 549.8042878000092 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.7247189401130364,
            "unit": "iter/sec",
            "range": "stddev: 0.012628801058491559",
            "extra": "mean: 1.3798452677999933 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.2851893164074135,
            "unit": "iter/sec",
            "range": "stddev: 0.020806035822836678",
            "extra": "mean: 3.5064427118000028 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.1169166162772069,
            "unit": "iter/sec",
            "range": "stddev: 0.02296728872477963",
            "extra": "mean: 8.553104185199993 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.07469992930568553,
            "unit": "iter/sec",
            "range": "stddev: 0.2519337177759339",
            "extra": "mean: 13.386893525800009 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 26.343452475633583,
            "unit": "iter/sec",
            "range": "stddev: 0.0015597676092441407",
            "extra": "mean: 37.96009657143275 msec\nrounds: 28"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 16.376478170785607,
            "unit": "iter/sec",
            "range": "stddev: 0.0010794853535350207",
            "extra": "mean: 61.06319011763617 msec\nrounds: 17"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.460919384195113,
            "unit": "iter/sec",
            "range": "stddev: 0.0009538412799195106",
            "extra": "mean: 154.7767338571394 msec\nrounds: 7"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1784613254167,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.5246391440316769,
            "unit": "iter/sec",
            "range": "stddev: 0.018872410605233897",
            "extra": "mean: 655.8929067999998 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.429882373737856,
            "unit": "iter/sec",
            "range": "stddev: 0.01037068984702103",
            "extra": "mean: 699.3582258000004 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9338222849727199,
            "unit": "iter/sec",
            "range": "stddev: 0.013097659461794173",
            "extra": "mean: 1.070867568800003 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.17475247154625018,
            "unit": "iter/sec",
            "range": "stddev: 0.008892961914455086",
            "extra": "mean: 5.722379724599998 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 6.06338083166443,
            "unit": "iter/sec",
            "range": "stddev: 0.0011586237468836278",
            "extra": "mean: 164.92449142857066 msec\nrounds: 7"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.548711562867538,
            "unit": "iter/sec",
            "range": "stddev: 0.00956113416617126",
            "extra": "mean: 392.35510780000027 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.070479138016607,
            "unit": "iter/sec",
            "range": "stddev: 0.00487164660970212",
            "extra": "mean: 482.9799931999986 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.8221552825693184,
            "unit": "iter/sec",
            "range": "stddev: 0.013597707964349158",
            "extra": "mean: 1.2163152402000008 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.33137417017339144,
            "unit": "iter/sec",
            "range": "stddev: 0.02525095237240862",
            "extra": "mean: 3.017736715799998 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.13549231114412524,
            "unit": "iter/sec",
            "range": "stddev: 0.040272869283517226",
            "extra": "mean: 7.3804926018 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.0863319206053357,
            "unit": "iter/sec",
            "range": "stddev: 0.03596387325548624",
            "extra": "mean: 11.583201126400002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 27.969573830530173,
            "unit": "iter/sec",
            "range": "stddev: 0.0002193343444289409",
            "extra": "mean: 35.75313682142881 msec\nrounds: 28"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 17.751201747974207,
            "unit": "iter/sec",
            "range": "stddev: 0.0003964667511499116",
            "extra": "mean: 56.334214111116246 msec\nrounds: 18"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.332071826022916,
            "unit": "iter/sec",
            "range": "stddev: 0.0005986590108247306",
            "extra": "mean: 157.92619342855525 msec\nrounds: 7"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1784699702905,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.3640921285179715,
            "unit": "iter/sec",
            "range": "stddev: 0.011147878754234635",
            "extra": "mean: 733.0883149999977 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.2917754980526623,
            "unit": "iter/sec",
            "range": "stddev: 0.01092332875637405",
            "extra": "mean: 774.1283230000022 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.8838621245759254,
            "unit": "iter/sec",
            "range": "stddev: 0.006729533168452316",
            "extra": "mean: 1.131398181000003 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.1732917821142052,
            "unit": "iter/sec",
            "range": "stddev: 0.04331791440836001",
            "extra": "mean: 5.770614092599994 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.14594650448974,
            "unit": "iter/sec",
            "range": "stddev: 0.000693965232658301",
            "extra": "mean: 194.3277100000008 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.161415572304147,
            "unit": "iter/sec",
            "range": "stddev: 0.009997386883889972",
            "extra": "mean: 462.6597554000057 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.6705152163271948,
            "unit": "iter/sec",
            "range": "stddev: 0.004616253790320679",
            "extra": "mean: 598.6177139999995 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.6702906323837408,
            "unit": "iter/sec",
            "range": "stddev: 0.020662487760598165",
            "extra": "mean: 1.491890161799995 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.25992634069700354,
            "unit": "iter/sec",
            "range": "stddev: 0.025620613229025032",
            "extra": "mean: 3.8472437895999976 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.10991930259429036,
            "unit": "iter/sec",
            "range": "stddev: 0.0893892858185123",
            "extra": "mean: 9.097583194199995 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.06637679968072946,
            "unit": "iter/sec",
            "range": "stddev: 0.07016322241512615",
            "extra": "mean: 15.065504887399992 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 22.85772399419317,
            "unit": "iter/sec",
            "range": "stddev: 0.0005273191136903994",
            "extra": "mean: 43.7488876956447 msec\nrounds: 23"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 14.811928544132543,
            "unit": "iter/sec",
            "range": "stddev: 0.0008438570055720023",
            "extra": "mean: 67.51315313333257 msec\nrounds: 15"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 5.7625344382502455,
            "unit": "iter/sec",
            "range": "stddev: 0.0028538326049890234",
            "extra": "mean: 173.53475466667115 msec\nrounds: 6"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1784786285261,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.3968018509144386,
            "unit": "iter/sec",
            "range": "stddev: 0.00852380672061673",
            "extra": "mean: 715.9211589999927 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.3174146106930429,
            "unit": "iter/sec",
            "range": "stddev: 0.010465400731401207",
            "extra": "mean: 759.0624788000014 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9069605432046988,
            "unit": "iter/sec",
            "range": "stddev: 0.008941734962732331",
            "extra": "mean: 1.1025837976000048 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.17295008910866985,
            "unit": "iter/sec",
            "range": "stddev: 0.10069534418762145",
            "extra": "mean: 5.782014945199995 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.171810568277439,
            "unit": "iter/sec",
            "range": "stddev: 0.00239499797100779",
            "extra": "mean: 193.35588316666966 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.1118133618411115,
            "unit": "iter/sec",
            "range": "stddev: 0.015188787659956399",
            "extra": "mean: 473.5266941999953 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.7286017362542956,
            "unit": "iter/sec",
            "range": "stddev: 0.0021835345127140257",
            "extra": "mean: 578.5022536000099 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.7113139529133994,
            "unit": "iter/sec",
            "range": "stddev: 0.01208922910867918",
            "extra": "mean: 1.4058489867999924 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.2789142512224068,
            "unit": "iter/sec",
            "range": "stddev: 0.04324301932373491",
            "extra": "mean: 3.5853313182000077 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11525683749379793,
            "unit": "iter/sec",
            "range": "stddev: 0.09031748853490197",
            "extra": "mean: 8.676274846199998 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.0723283384720569,
            "unit": "iter/sec",
            "range": "stddev: 0.3396602154345196",
            "extra": "mean: 13.82583951360001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 23.45286953114196,
            "unit": "iter/sec",
            "range": "stddev: 0.0001774971771458392",
            "extra": "mean: 42.638705625004526 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 15.15278327876297,
            "unit": "iter/sec",
            "range": "stddev: 0.00029483841126796994",
            "extra": "mean: 65.99447650000556 msec\nrounds: 16"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 5.902228226021808,
            "unit": "iter/sec",
            "range": "stddev: 0.00345904132222829",
            "extra": "mean: 169.42753849998363 msec\nrounds: 6"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1784872475929,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.29489157197323,
            "unit": "iter/sec",
            "range": "stddev: 0.01631429725170181",
            "extra": "mean: 772.2654325999997 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.2449387311557831,
            "unit": "iter/sec",
            "range": "stddev: 0.012822298677902754",
            "extra": "mean: 803.2523809999986 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.8135704413962095,
            "unit": "iter/sec",
            "range": "stddev: 0.027016919956268204",
            "extra": "mean: 1.2291498672000045 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.16609095781495994,
            "unit": "iter/sec",
            "range": "stddev: 0.042603824564566774",
            "extra": "mean: 6.0207973579999985 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.125917772831017,
            "unit": "iter/sec",
            "range": "stddev: 0.0021379863825223347",
            "extra": "mean: 195.08701549999805 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.1761908776085535,
            "unit": "iter/sec",
            "range": "stddev: 0.010380260130875014",
            "extra": "mean: 459.51851480000414 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.6972495805437033,
            "unit": "iter/sec",
            "range": "stddev: 0.009639904282282851",
            "extra": "mean: 589.1885385999956 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.7034344061071346,
            "unit": "iter/sec",
            "range": "stddev: 0.0097828798817193",
            "extra": "mean: 1.4215966568000056 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.2747633467045353,
            "unit": "iter/sec",
            "range": "stddev: 0.02458826793452422",
            "extra": "mean: 3.6394956314000013 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11517965050134442,
            "unit": "iter/sec",
            "range": "stddev: 0.07334910343261727",
            "extra": "mean: 8.6820892028 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.06939452632466711,
            "unit": "iter/sec",
            "range": "stddev: 0.07993399085157159",
            "extra": "mean: 14.410358467200002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 23.083735220362946,
            "unit": "iter/sec",
            "range": "stddev: 0.0025772971151254336",
            "extra": "mean: 43.32054541666489 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 15.21570858342496,
            "unit": "iter/sec",
            "range": "stddev: 0.0002115954529233199",
            "extra": "mean: 65.72155312499461 msec\nrounds: 16"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.066224702093151,
            "unit": "iter/sec",
            "range": "stddev: 0.001275189484393906",
            "extra": "mean: 164.84717416665262 msec\nrounds: 6"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1784958404710,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.542386306997415,
            "unit": "iter/sec",
            "range": "stddev: 0.00955045698762259",
            "extra": "mean: 648.3460047999998 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.4384727074718064,
            "unit": "iter/sec",
            "range": "stddev: 0.009004537911236293",
            "extra": "mean: 695.1817680000019 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9362583745198552,
            "unit": "iter/sec",
            "range": "stddev: 0.00853163782243773",
            "extra": "mean: 1.0680812339999988 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.1732346403036096,
            "unit": "iter/sec",
            "range": "stddev: 0.03392665829742202",
            "extra": "mean: 5.772517541800002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 6.0014157579829295,
            "unit": "iter/sec",
            "range": "stddev: 0.000258263130114276",
            "extra": "mean: 166.62734933333448 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.5343181833012096,
            "unit": "iter/sec",
            "range": "stddev: 0.00898221776014794",
            "extra": "mean: 394.5834452000014 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.079555568497047,
            "unit": "iter/sec",
            "range": "stddev: 0.002250516324464244",
            "extra": "mean: 480.8719781999997 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.8081622409245286,
            "unit": "iter/sec",
            "range": "stddev: 0.018409835377988935",
            "extra": "mean: 1.2373753057999977 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.3278097641793863,
            "unit": "iter/sec",
            "range": "stddev: 0.019172320440147182",
            "extra": "mean: 3.050549767800001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.131817077687422,
            "unit": "iter/sec",
            "range": "stddev: 0.11921133477069482",
            "extra": "mean: 7.5862704404 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.07972253545298523,
            "unit": "iter/sec",
            "range": "stddev: 0.20870322848943984",
            "extra": "mean: 12.543504723200005 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 27.64095011141641,
            "unit": "iter/sec",
            "range": "stddev: 0.00018763443065631654",
            "extra": "mean: 36.17820646429136 msec\nrounds: 28"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 17.466311676688733,
            "unit": "iter/sec",
            "range": "stddev: 0.0001553004563372445",
            "extra": "mean: 57.25307200000569 msec\nrounds: 18"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.28398210322608,
            "unit": "iter/sec",
            "range": "stddev: 0.0005372479156134381",
            "extra": "mean: 159.1347625714304 msec\nrounds: 7"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1785046178930,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.4897360542239289,
            "unit": "iter/sec",
            "range": "stddev: 0.019650292805827817",
            "extra": "mean: 671.2598498000006 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.4268088549035887,
            "unit": "iter/sec",
            "range": "stddev: 0.012294920673186835",
            "extra": "mean: 700.8647280000033 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.924934733835001,
            "unit": "iter/sec",
            "range": "stddev: 0.011767523300618919",
            "extra": "mean: 1.0811573654 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.17174930579438966,
            "unit": "iter/sec",
            "range": "stddev: 0.010652566651431716",
            "extra": "mean: 5.822439836800004 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.936754936327673,
            "unit": "iter/sec",
            "range": "stddev: 0.0011150058038831854",
            "extra": "mean: 168.44218950000567 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.503600179561838,
            "unit": "iter/sec",
            "range": "stddev: 0.012213492300674528",
            "extra": "mean: 399.4247995999956 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.0221771144969463,
            "unit": "iter/sec",
            "range": "stddev: 0.005622278177947783",
            "extra": "mean: 494.5165252000038 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.8009777595744645,
            "unit": "iter/sec",
            "range": "stddev: 0.014889917190812023",
            "extra": "mean: 1.2484741156000012 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.32776640216006053,
            "unit": "iter/sec",
            "range": "stddev: 0.025654078920211217",
            "extra": "mean: 3.050953341800002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.13264815202060712,
            "unit": "iter/sec",
            "range": "stddev: 0.038998391923219626",
            "extra": "mean: 7.538740530999997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.08476972245294069,
            "unit": "iter/sec",
            "range": "stddev: 0.09545264185765359",
            "extra": "mean: 11.796664788599998 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 27.75741972062115,
            "unit": "iter/sec",
            "range": "stddev: 0.0001391050326770129",
            "extra": "mean: 36.0264033928591 msec\nrounds: 28"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 17.559628229500046,
            "unit": "iter/sec",
            "range": "stddev: 0.00020216592781241167",
            "extra": "mean: 56.94881388889586 msec\nrounds: 18"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.341916803348914,
            "unit": "iter/sec",
            "range": "stddev: 0.0019044786155748518",
            "extra": "mean: 157.68103414285406 msec\nrounds: 7"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1785134110125,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.3898670263402393,
            "unit": "iter/sec",
            "range": "stddev: 0.009070866496212726",
            "extra": "mean: 719.4932903999984 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.3152456670189638,
            "unit": "iter/sec",
            "range": "stddev: 0.007986220399133066",
            "extra": "mean: 760.3142326000011 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.8998713491726695,
            "unit": "iter/sec",
            "range": "stddev: 0.006087173359019391",
            "extra": "mean: 1.1112699619999986 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.18337842263872328,
            "unit": "iter/sec",
            "range": "stddev: 0.02001593577752522",
            "extra": "mean: 5.453204284400002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.245544057198659,
            "unit": "iter/sec",
            "range": "stddev: 0.0004952606567642109",
            "extra": "mean: 190.6379946666661 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.2140472130397484,
            "unit": "iter/sec",
            "range": "stddev: 0.007210889622662216",
            "extra": "mean: 451.6615518000009 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.7595205657236441,
            "unit": "iter/sec",
            "range": "stddev: 0.0030863112527775025",
            "extra": "mean: 568.3366363999994 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.6986849380044274,
            "unit": "iter/sec",
            "range": "stddev: 0.010081914206434605",
            "extra": "mean: 1.4312602800000007 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.2697908046293452,
            "unit": "iter/sec",
            "range": "stddev: 0.02092628535829628",
            "extra": "mean: 3.7065755498000015 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11319544427361149,
            "unit": "iter/sec",
            "range": "stddev: 0.01781757804092764",
            "extra": "mean: 8.834277796400006 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.07144514299680572,
            "unit": "iter/sec",
            "range": "stddev: 0.08813749554612664",
            "extra": "mean: 13.996752725999993 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 22.920344194371737,
            "unit": "iter/sec",
            "range": "stddev: 0.00028212881409912674",
            "extra": "mean: 43.62936226086682 msec\nrounds: 23"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 14.850477727395074,
            "unit": "iter/sec",
            "range": "stddev: 0.00031385782357970147",
            "extra": "mean: 67.3379010666622 msec\nrounds: 15"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 5.952131541535151,
            "unit": "iter/sec",
            "range": "stddev: 0.0014124796637307443",
            "extra": "mean: 168.00703966668115 msec\nrounds: 6"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1785217828968,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.3523382633276404,
            "unit": "iter/sec",
            "range": "stddev: 0.008824785100110007",
            "extra": "mean: 739.4599614 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.2868363861227055,
            "unit": "iter/sec",
            "range": "stddev: 0.011169688386095385",
            "extra": "mean: 777.0995681999977 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.875223167575952,
            "unit": "iter/sec",
            "range": "stddev: 0.010324406928986968",
            "extra": "mean: 1.1425657330000007 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.17324934047072915,
            "unit": "iter/sec",
            "range": "stddev: 0.03061822435572385",
            "extra": "mean: 5.772027745 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.0071213031665005,
            "unit": "iter/sec",
            "range": "stddev: 0.0017518475621509974",
            "extra": "mean: 199.71555300000432 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.1363542800252873,
            "unit": "iter/sec",
            "range": "stddev: 0.009606458621782527",
            "extra": "mean: 468.0871563999972 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.6924936629906253,
            "unit": "iter/sec",
            "range": "stddev: 0.003176052983541143",
            "extra": "mean: 590.8441619999962 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.678450880561219,
            "unit": "iter/sec",
            "range": "stddev: 0.013335997098220647",
            "extra": "mean: 1.4739460565999907 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.2661392391189858,
            "unit": "iter/sec",
            "range": "stddev: 0.0504945578688019",
            "extra": "mean: 3.7574316485999986 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.10924087219149399,
            "unit": "iter/sec",
            "range": "stddev: 0.06057586607945498",
            "extra": "mean: 9.154082899000002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.06942750856992831,
            "unit": "iter/sec",
            "range": "stddev: 0.04785431013550585",
            "extra": "mean: 14.403512679599999 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 23.093711539045643,
            "unit": "iter/sec",
            "range": "stddev: 0.00022104745646855427",
            "extra": "mean: 43.30183125000294 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 14.983278107251403,
            "unit": "iter/sec",
            "range": "stddev: 0.0005199674681262563",
            "extra": "mean: 66.74106913333162 msec\nrounds: 15"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 5.963156838222746,
            "unit": "iter/sec",
            "range": "stddev: 0.0010460515491853568",
            "extra": "mean: 167.69641099998958 msec\nrounds: 6"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1785304587041,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.3684855793483681,
            "unit": "iter/sec",
            "range": "stddev: 0.022496335299627218",
            "extra": "mean: 730.7347736000039 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.3034365489387234,
            "unit": "iter/sec",
            "range": "stddev: 0.012904154197063578",
            "extra": "mean: 767.2026696000003 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.904690424956028,
            "unit": "iter/sec",
            "range": "stddev: 0.006831074269604252",
            "extra": "mean: 1.1053504849999982 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.18720534245551962,
            "unit": "iter/sec",
            "range": "stddev: 0.04156143413504264",
            "extra": "mean: 5.341727895599999 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.255557487294094,
            "unit": "iter/sec",
            "range": "stddev: 0.0007573459642965327",
            "extra": "mean: 190.27477150000038 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.223835358786831,
            "unit": "iter/sec",
            "range": "stddev: 0.008331404897561557",
            "extra": "mean: 449.67357680000646 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.7714478475952262,
            "unit": "iter/sec",
            "range": "stddev: 0.004357731487094425",
            "extra": "mean: 564.5099861999995 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.7017306204909207,
            "unit": "iter/sec",
            "range": "stddev: 0.008656654918269153",
            "extra": "mean: 1.4250482604000012 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.27339820857858993,
            "unit": "iter/sec",
            "range": "stddev: 0.011237849428882488",
            "extra": "mean: 3.6576684434000013 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11291965355653527,
            "unit": "iter/sec",
            "range": "stddev: 0.03441518391819756",
            "extra": "mean: 8.855854304400003 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.07227039323810687,
            "unit": "iter/sec",
            "range": "stddev: 0.09145071165768286",
            "extra": "mean: 13.836924848399997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 24.12939283149613,
            "unit": "iter/sec",
            "range": "stddev: 0.000165963769265776",
            "extra": "mean: 41.44323095833139 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 15.467640802185384,
            "unit": "iter/sec",
            "range": "stddev: 0.0009706931349254349",
            "extra": "mean: 64.65110050000078 msec\nrounds: 16"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.08472843175543,
            "unit": "iter/sec",
            "range": "stddev: 0.0011642089694290543",
            "extra": "mean: 164.34587199999365 msec\nrounds: 6"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1785390283945,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.5361430273917844,
            "unit": "iter/sec",
            "range": "stddev: 0.014046761423586697",
            "extra": "mean: 650.9810494000021 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.4424888844460786,
            "unit": "iter/sec",
            "range": "stddev: 0.014493904140320101",
            "extra": "mean: 693.2462431999979 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.942239238942271,
            "unit": "iter/sec",
            "range": "stddev: 0.01161023042749222",
            "extra": "mean: 1.0613015873999998 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.16847405478202274,
            "unit": "iter/sec",
            "range": "stddev: 0.05156539017808955",
            "extra": "mean: 5.935632054999999 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 6.0010014951375785,
            "unit": "iter/sec",
            "range": "stddev: 0.0017585516343800866",
            "extra": "mean: 166.6388519999984 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.5309158995182957,
            "unit": "iter/sec",
            "range": "stddev: 0.01027506943197597",
            "extra": "mean: 395.1138796000009 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.0644318503467405,
            "unit": "iter/sec",
            "range": "stddev: 0.003411031406520812",
            "extra": "mean: 484.39477420000117 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.8133645783128296,
            "unit": "iter/sec",
            "range": "stddev: 0.01257038387016215",
            "extra": "mean: 1.2294609657999984 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.32835670016892926,
            "unit": "iter/sec",
            "range": "stddev: 0.04794530290808485",
            "extra": "mean: 3.045468539199996 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.13435617238472858,
            "unit": "iter/sec",
            "range": "stddev: 0.047346283287097564",
            "extra": "mean: 7.442903308800004 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.08617914983420076,
            "unit": "iter/sec",
            "range": "stddev: 0.019269137739282106",
            "extra": "mean: 11.603734800399986 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 28.131393750895196,
            "unit": "iter/sec",
            "range": "stddev: 0.00017298313247223984",
            "extra": "mean: 35.54747442857068 msec\nrounds: 28"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 17.770425911251934,
            "unit": "iter/sec",
            "range": "stddev: 0.0002394877688254115",
            "extra": "mean: 56.27327138888757 msec\nrounds: 18"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.4448974270265476,
            "unit": "iter/sec",
            "range": "stddev: 0.0006879401092602776",
            "extra": "mean: 155.16150742857755 msec\nrounds: 7"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1785478643467,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.5350025924305761,
            "unit": "iter/sec",
            "range": "stddev: 0.01613305975119461",
            "extra": "mean: 651.4646977999987 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.444771047782205,
            "unit": "iter/sec",
            "range": "stddev: 0.01313937431719479",
            "extra": "mean: 692.1511899999999 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.951933246026864,
            "unit": "iter/sec",
            "range": "stddev: 0.008628611396619029",
            "extra": "mean: 1.0504938284000005 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.18863931245475618,
            "unit": "iter/sec",
            "range": "stddev: 0.038236908091195745",
            "extra": "mean: 5.301121950600001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 6.434509194969793,
            "unit": "iter/sec",
            "range": "stddev: 0.006457632025923787",
            "extra": "mean: 155.4120088571409 msec\nrounds: 7"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.736426010084957,
            "unit": "iter/sec",
            "range": "stddev: 0.0147980817544474",
            "extra": "mean: 365.4401750000005 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.289046968580256,
            "unit": "iter/sec",
            "range": "stddev: 0.004884688791793745",
            "extra": "mean: 436.86303240000086 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.9034250127626938,
            "unit": "iter/sec",
            "range": "stddev: 0.012386703940363336",
            "extra": "mean: 1.1068987308000005 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.3651286672035894,
            "unit": "iter/sec",
            "range": "stddev: 0.02601749506807565",
            "extra": "mean: 2.7387605789999983 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.15102820838852782,
            "unit": "iter/sec",
            "range": "stddev: 0.08869289216523334",
            "extra": "mean: 6.621279631600004 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.09664787039708253,
            "unit": "iter/sec",
            "range": "stddev: 0.2414752196771623",
            "extra": "mean: 10.346839468799994 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 35.15674370505907,
            "unit": "iter/sec",
            "range": "stddev: 0.0004798443895154731",
            "extra": "mean: 28.444044999995253 msec\nrounds: 35"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 22.419747366506602,
            "unit": "iter/sec",
            "range": "stddev: 0.000338857530337167",
            "extra": "mean: 44.60353560869842 msec\nrounds: 23"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 7.9484595529028095,
            "unit": "iter/sec",
            "range": "stddev: 0.0006965595642469226",
            "extra": "mean: 125.8105414444483 msec\nrounds: 9"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "dependabot[bot]",
            "username": "dependabot[bot]",
            "email": "49699333+dependabot[bot]@users.noreply.github.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "93dd3a250689f07bb28c41bee47ce4b1dad332b4",
          "message": "build(deps): bump actions/checkout from 6 to 7 (#172)\n\nBumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.\n- [Release notes](https://github.com/actions/checkout/releases)\n- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/actions/checkout/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/checkout\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-06-30T03:14:38Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/93dd3a250689f07bb28c41bee47ce4b1dad332b4"
        },
        "date": 1785563945682,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.3579746296400665,
            "unit": "iter/sec",
            "range": "stddev: 0.011670357364991907",
            "extra": "mean: 736.390782400001 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.2610651598121057,
            "unit": "iter/sec",
            "range": "stddev: 0.021220829543216038",
            "extra": "mean: 792.9804357999999 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.8737951922930458,
            "unit": "iter/sec",
            "range": "stddev: 0.029176430448961746",
            "extra": "mean: 1.1444329389999992 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.174785896968965,
            "unit": "iter/sec",
            "range": "stddev: 0.01864827740635757",
            "extra": "mean: 5.721285397399998 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.062556286766457,
            "unit": "iter/sec",
            "range": "stddev: 0.006042589233847744",
            "extra": "mean: 197.52866799999916 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.1588833006180157,
            "unit": "iter/sec",
            "range": "stddev: 0.010387147186139872",
            "extra": "mean: 463.20243420000224 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.6755695642643555,
            "unit": "iter/sec",
            "range": "stddev: 0.002772640234354519",
            "extra": "mean: 596.8119864000045 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.6671905737056896,
            "unit": "iter/sec",
            "range": "stddev: 0.022036737771730333",
            "extra": "mean: 1.4988221348000024 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.26675446893568394,
            "unit": "iter/sec",
            "range": "stddev: 0.04349367424780827",
            "extra": "mean: 3.7487656870000023 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.10969878072904649,
            "unit": "iter/sec",
            "range": "stddev: 0.03941986458907832",
            "extra": "mean: 9.1158716018 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.06930316757814102,
            "unit": "iter/sec",
            "range": "stddev: 0.0380222153617224",
            "extra": "mean: 14.429354890200011 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 23.01969376236774,
            "unit": "iter/sec",
            "range": "stddev: 0.00017892071942953952",
            "extra": "mean: 43.44106443478347 msec\nrounds: 23"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 14.783057507564079,
            "unit": "iter/sec",
            "range": "stddev: 0.00020515169612526696",
            "extra": "mean: 67.64500506666687 msec\nrounds: 15"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 5.876337524569346,
            "unit": "iter/sec",
            "range": "stddev: 0.0014520797051940102",
            "extra": "mean: 170.17402350000074 msec\nrounds: 6"
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
          "id": "24529c169c190ccabdcfa10d9a64965b0b073380",
          "message": "feat(policy): promote managed Git safeguards\n\nPromote the independently reviewed policy-only patch to the default branch for Issue #147 acceptance.",
          "timestamp": "2026-08-01T22:48:30Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/24529c169c190ccabdcfa10d9a64965b0b073380"
        },
        "date": 1785650430112,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.8008962916771991,
            "unit": "iter/sec",
            "range": "stddev: 0.010960021642324746",
            "extra": "mean: 555.2790599999995 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.6700695586476288,
            "unit": "iter/sec",
            "range": "stddev: 0.01320207201571407",
            "extra": "mean: 598.7774549999998 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 1.110518462697378,
            "unit": "iter/sec",
            "range": "stddev: 0.006895910124441612",
            "extra": "mean: 900.4803014000004 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.2306021580440648,
            "unit": "iter/sec",
            "range": "stddev: 0.012478874614920357",
            "extra": "mean: 4.3364728608000025 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 7.488079503935261,
            "unit": "iter/sec",
            "range": "stddev: 0.0063533983942015365",
            "extra": "mean: 133.54559062500115 msec\nrounds: 8"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 3.2199077468095223,
            "unit": "iter/sec",
            "range": "stddev: 0.008440213901365954",
            "extra": "mean: 310.56790400000125 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.7744639703425666,
            "unit": "iter/sec",
            "range": "stddev: 0.0009718973882913528",
            "extra": "mean: 360.42998239999804 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 1.092737487883674,
            "unit": "iter/sec",
            "range": "stddev: 0.01010145142203425",
            "extra": "mean: 915.1328759999984 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.4386618814003587,
            "unit": "iter/sec",
            "range": "stddev: 0.019436271875245423",
            "extra": "mean: 2.2796601263999916 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.17966576105658316,
            "unit": "iter/sec",
            "range": "stddev: 0.013652575894822123",
            "extra": "mean: 5.565890763599995 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.11322339968481566,
            "unit": "iter/sec",
            "range": "stddev: 0.06311154862432877",
            "extra": "mean: 8.832096570000004 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 42.2645448595839,
            "unit": "iter/sec",
            "range": "stddev: 0.00006756810346480094",
            "extra": "mean: 23.660493761906444 msec\nrounds: 42"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 26.75900736284502,
            "unit": "iter/sec",
            "range": "stddev: 0.00007692962844911818",
            "extra": "mean: 37.37059400000404 msec\nrounds: 27"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 9.554187837472687,
            "unit": "iter/sec",
            "range": "stddev: 0.00047495379932518034",
            "extra": "mean: 104.66614400000367 msec\nrounds: 10"
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
          "id": "24529c169c190ccabdcfa10d9a64965b0b073380",
          "message": "feat(policy): promote managed Git safeguards\n\nPromote the independently reviewed policy-only patch to the default branch for Issue #147 acceptance.",
          "timestamp": "2026-08-01T22:48:30Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/24529c169c190ccabdcfa10d9a64965b0b073380"
        },
        "date": 1785738423114,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.3846667127618435,
            "unit": "iter/sec",
            "range": "stddev: 0.009430821629146737",
            "extra": "mean: 722.1954502000045 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.308652997327031,
            "unit": "iter/sec",
            "range": "stddev: 0.009162636351819178",
            "extra": "mean: 764.1445074000018 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9004047749496722,
            "unit": "iter/sec",
            "range": "stddev: 0.008144573790711217",
            "extra": "mean: 1.1106116135999997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.18262599009840408,
            "unit": "iter/sec",
            "range": "stddev: 0.010744291325877866",
            "extra": "mean: 5.475671888000013 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.258773885596372,
            "unit": "iter/sec",
            "range": "stddev: 0.0004466516101843518",
            "extra": "mean: 190.15839466666762 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.1952057894481967,
            "unit": "iter/sec",
            "range": "stddev: 0.01693101169847626",
            "extra": "mean: 455.53815719999875 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.7422900004316182,
            "unit": "iter/sec",
            "range": "stddev: 0.004419233619315976",
            "extra": "mean: 573.9572629999998 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.7049329696855445,
            "unit": "iter/sec",
            "range": "stddev: 0.013709472944947072",
            "extra": "mean: 1.418574592199991 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.27949411563058535,
            "unit": "iter/sec",
            "range": "stddev: 0.021801275092075967",
            "extra": "mean: 3.577892857399996 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11712223543414363,
            "unit": "iter/sec",
            "range": "stddev: 0.04050976330750559",
            "extra": "mean: 8.538088402200003 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.07195423836964021,
            "unit": "iter/sec",
            "range": "stddev: 0.1176240297478164",
            "extra": "mean: 13.897721978000003 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 23.49120486304472,
            "unit": "iter/sec",
            "range": "stddev: 0.00018854089590978227",
            "extra": "mean: 42.56912345833541 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 15.194089335153917,
            "unit": "iter/sec",
            "range": "stddev: 0.00029469480598848577",
            "extra": "mean: 65.81506649999369 msec\nrounds: 16"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.0124112160516,
            "unit": "iter/sec",
            "range": "stddev: 0.0009741176277778041",
            "extra": "mean: 166.3226223333254 msec\nrounds: 6"
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
          "id": "24529c169c190ccabdcfa10d9a64965b0b073380",
          "message": "feat(policy): promote managed Git safeguards\n\nPromote the independently reviewed policy-only patch to the default branch for Issue #147 acceptance.",
          "timestamp": "2026-08-01T22:48:30Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/24529c169c190ccabdcfa10d9a64965b0b073380"
        },
        "date": 1785822601254,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.5230616215282144,
            "unit": "iter/sec",
            "range": "stddev: 0.015860535671396263",
            "extra": "mean: 656.5722527999995 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.406834310253991,
            "unit": "iter/sec",
            "range": "stddev: 0.015640781977044896",
            "extra": "mean: 710.8157603999998 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9047820569468077,
            "unit": "iter/sec",
            "range": "stddev: 0.017234186147971238",
            "extra": "mean: 1.1052385404000007 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.1668524222893109,
            "unit": "iter/sec",
            "range": "stddev: 0.03027247746434208",
            "extra": "mean: 5.9933202424 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.828001269878836,
            "unit": "iter/sec",
            "range": "stddev: 0.0015426994576945034",
            "extra": "mean: 171.5854121666638 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.5240699487649865,
            "unit": "iter/sec",
            "range": "stddev: 0.013306677562620127",
            "extra": "mean: 396.1855338000021 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.951592985022272,
            "unit": "iter/sec",
            "range": "stddev: 0.007524617905189817",
            "extra": "mean: 512.4019238000017 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.7986750009847038,
            "unit": "iter/sec",
            "range": "stddev: 0.015310314356761157",
            "extra": "mean: 1.2520737455999977 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.3170114799265782,
            "unit": "iter/sec",
            "range": "stddev: 0.02796864089361153",
            "extra": "mean: 3.154459896 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.12859332576001334,
            "unit": "iter/sec",
            "range": "stddev: 0.06002175383095424",
            "extra": "mean: 7.776453358600003 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.08373117457819988,
            "unit": "iter/sec",
            "range": "stddev: 0.08764688204074102",
            "extra": "mean: 11.942983065000004 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 27.921009593155095,
            "unit": "iter/sec",
            "range": "stddev: 0.00018508111998388768",
            "extra": "mean: 35.815323821426304 msec\nrounds: 28"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 17.6955542533005,
            "unit": "iter/sec",
            "range": "stddev: 0.00021860277845206234",
            "extra": "mean: 56.5113692222149 msec\nrounds: 18"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.370337205518268,
            "unit": "iter/sec",
            "range": "stddev: 0.0020177929420621236",
            "extra": "mean: 156.977561428578 msec\nrounds: 7"
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
          "id": "24529c169c190ccabdcfa10d9a64965b0b073380",
          "message": "feat(policy): promote managed Git safeguards\n\nPromote the independently reviewed policy-only patch to the default branch for Issue #147 acceptance.",
          "timestamp": "2026-08-01T22:48:30Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/24529c169c190ccabdcfa10d9a64965b0b073380"
        },
        "date": 1785908984749,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.3834891767483466,
            "unit": "iter/sec",
            "range": "stddev: 0.010518399655120468",
            "extra": "mean: 722.8101359999996 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.321066478600066,
            "unit": "iter/sec",
            "range": "stddev: 0.00682134453287452",
            "extra": "mean: 756.9641771999998 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9116264146434556,
            "unit": "iter/sec",
            "range": "stddev: 0.008587575508559896",
            "extra": "mean: 1.0969405711999998 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.18961876712680112,
            "unit": "iter/sec",
            "range": "stddev: 0.011922400797314683",
            "extra": "mean: 5.273739594199998 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.313873498747573,
            "unit": "iter/sec",
            "range": "stddev: 0.0005208767552706403",
            "extra": "mean: 188.1866401666675 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.246524939309117,
            "unit": "iter/sec",
            "range": "stddev: 0.005254758106384746",
            "extra": "mean: 445.1319380000001 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.8021670611251734,
            "unit": "iter/sec",
            "range": "stddev: 0.0034087695088895254",
            "extra": "mean: 554.8875138 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.7181450909452883,
            "unit": "iter/sec",
            "range": "stddev: 0.003028224492561131",
            "extra": "mean: 1.3924762734000011 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.28147247518292384,
            "unit": "iter/sec",
            "range": "stddev: 0.013845031801521109",
            "extra": "mean: 3.5527452528000056 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11617982280257147,
            "unit": "iter/sec",
            "range": "stddev: 0.05723476287817789",
            "extra": "mean: 8.607346575999998 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.07351824365263984,
            "unit": "iter/sec",
            "range": "stddev: 0.05435384570518205",
            "extra": "mean: 13.60206596779999 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 23.887632790340568,
            "unit": "iter/sec",
            "range": "stddev: 0.00033777511361692426",
            "extra": "mean: 41.86266629167079 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 15.34228793000071,
            "unit": "iter/sec",
            "range": "stddev: 0.0001909783967474614",
            "extra": "mean: 65.1793268750076 msec\nrounds: 16"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.091544265010852,
            "unit": "iter/sec",
            "range": "stddev: 0.0011796498849019601",
            "extra": "mean: 164.16198528571613 msec\nrounds: 7"
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
          "id": "24529c169c190ccabdcfa10d9a64965b0b073380",
          "message": "feat(policy): promote managed Git safeguards\n\nPromote the independently reviewed policy-only patch to the default branch for Issue #147 acceptance.",
          "timestamp": "2026-08-01T22:48:30Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/24529c169c190ccabdcfa10d9a64965b0b073380"
        },
        "date": 1785995535900,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.4825248526026116,
            "unit": "iter/sec",
            "range": "stddev: 0.01672110154243759",
            "extra": "mean: 674.5249486000006 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.3917143473568914,
            "unit": "iter/sec",
            "range": "stddev: 0.02054455475452774",
            "extra": "mean: 718.5382560000007 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9087484913375565,
            "unit": "iter/sec",
            "range": "stddev: 0.017012933053449072",
            "extra": "mean: 1.1004144816000008 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.16670793066933423,
            "unit": "iter/sec",
            "range": "stddev: 0.031490947423887326",
            "extra": "mean: 5.998514863600002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.988420104783525,
            "unit": "iter/sec",
            "range": "stddev: 0.0016002192461456028",
            "extra": "mean: 166.988952428572 msec\nrounds: 7"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.499125441048407,
            "unit": "iter/sec",
            "range": "stddev: 0.014613775991873868",
            "extra": "mean: 400.1399784 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.0041772850701496,
            "unit": "iter/sec",
            "range": "stddev: 0.012649037414022086",
            "extra": "mean: 498.9578554000019 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.8090267679410151,
            "unit": "iter/sec",
            "range": "stddev: 0.015590226349303673",
            "extra": "mean: 1.2360530449999998 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.3187723530944066,
            "unit": "iter/sec",
            "range": "stddev: 0.03420988627268714",
            "extra": "mean: 3.1370349099999997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.12970253774777307,
            "unit": "iter/sec",
            "range": "stddev: 0.11788924949057164",
            "extra": "mean: 7.709949376200001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.08237921196492869,
            "unit": "iter/sec",
            "range": "stddev: 0.1256386680675086",
            "extra": "mean: 12.138984777199983 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 28.10495673205441,
            "unit": "iter/sec",
            "range": "stddev: 0.0003601104624143556",
            "extra": "mean: 35.58091227585754 msec\nrounds: 29"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 17.803433659828325,
            "unit": "iter/sec",
            "range": "stddev: 0.00023524529287861283",
            "extra": "mean: 56.16894016666012 msec\nrounds: 18"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.494255326930428,
            "unit": "iter/sec",
            "range": "stddev: 0.0008852173466445108",
            "extra": "mean: 153.9822427142943 msec\nrounds: 7"
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
          "id": "24529c169c190ccabdcfa10d9a64965b0b073380",
          "message": "feat(policy): promote managed Git safeguards\n\nPromote the independently reviewed policy-only patch to the default branch for Issue #147 acceptance.",
          "timestamp": "2026-08-01T22:48:30Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/24529c169c190ccabdcfa10d9a64965b0b073380"
        },
        "date": 1786078695797,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.582127359812024,
            "unit": "iter/sec",
            "range": "stddev: 0.009458948134937046",
            "extra": "mean: 632.0603672000288 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.4683773815272116,
            "unit": "iter/sec",
            "range": "stddev: 0.011036174970718961",
            "extra": "mean: 681.0238379999646 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9514209760463093,
            "unit": "iter/sec",
            "range": "stddev: 0.008513719423465642",
            "extra": "mean: 1.0510594417999528 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.1792686350890822,
            "unit": "iter/sec",
            "range": "stddev: 0.015324655019804373",
            "extra": "mean: 5.578220637999948 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 6.131193337579365,
            "unit": "iter/sec",
            "range": "stddev: 0.00029413071503446315",
            "extra": "mean: 163.10038600002892 msec\nrounds: 7"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.5728733124220775,
            "unit": "iter/sec",
            "range": "stddev: 0.007905247101599787",
            "extra": "mean: 388.6705167999935 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.091730883292576,
            "unit": "iter/sec",
            "range": "stddev: 0.00586559261567738",
            "extra": "mean: 478.0729720000636 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.8295316228106606,
            "unit": "iter/sec",
            "range": "stddev: 0.012711466971509464",
            "extra": "mean: 1.2054995524001242 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.33264781719132197,
            "unit": "iter/sec",
            "range": "stddev: 0.02556856760239914",
            "extra": "mean: 3.0061823596000066 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.13650174842815507,
            "unit": "iter/sec",
            "range": "stddev: 0.03316149095033538",
            "extra": "mean: 7.325913488399965 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.08773246452591962,
            "unit": "iter/sec",
            "range": "stddev: 0.04583037001523848",
            "extra": "mean: 11.398289166999984 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 27.81857357282674,
            "unit": "iter/sec",
            "range": "stddev: 0.00013325681193436742",
            "extra": "mean: 35.947206185179915 msec\nrounds: 27"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 17.687467438256327,
            "unit": "iter/sec",
            "range": "stddev: 0.0004529309973583689",
            "extra": "mean: 56.537206555478605 msec\nrounds: 18"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.435808787133135,
            "unit": "iter/sec",
            "range": "stddev: 0.002992100098752812",
            "extra": "mean: 155.38062628573763 msec\nrounds: 7"
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
          "id": "24529c169c190ccabdcfa10d9a64965b0b073380",
          "message": "feat(policy): promote managed Git safeguards\n\nPromote the independently reviewed policy-only patch to the default branch for Issue #147 acceptance.",
          "timestamp": "2026-08-01T22:48:30Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/24529c169c190ccabdcfa10d9a64965b0b073380"
        },
        "date": 1786162381544,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 2.176941680463843,
            "unit": "iter/sec",
            "range": "stddev: 0.008733002906934878",
            "extra": "mean: 459.3600319999979 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 2.034763103130982,
            "unit": "iter/sec",
            "range": "stddev: 0.00858499467786044",
            "extra": "mean: 491.45770260000035 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 1.3372925405292284,
            "unit": "iter/sec",
            "range": "stddev: 0.0402145191603463",
            "extra": "mean: 747.7795393999983 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.3009754364688292,
            "unit": "iter/sec",
            "range": "stddev: 0.032302415299850507",
            "extra": "mean: 3.322530276000002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 8.857151009376814,
            "unit": "iter/sec",
            "range": "stddev: 0.0063011765463672174",
            "extra": "mean: 112.90312188889276 msec\nrounds: 9"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 3.790536407616184,
            "unit": "iter/sec",
            "range": "stddev: 0.0074851835960469204",
            "extra": "mean: 263.8149044000045 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 3.265093422802288,
            "unit": "iter/sec",
            "range": "stddev: 0.0014432735477190794",
            "extra": "mean: 306.2699501999987 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 1.2470095205932117,
            "unit": "iter/sec",
            "range": "stddev: 0.056045628654650334",
            "extra": "mean: 801.918496600004 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.5305448888288342,
            "unit": "iter/sec",
            "range": "stddev: 0.012216438308223953",
            "extra": "mean: 1.8848546486000033 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.21215412442500692,
            "unit": "iter/sec",
            "range": "stddev: 0.10553514518929832",
            "extra": "mean: 4.713554368600003 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.13384020755667855,
            "unit": "iter/sec",
            "range": "stddev: 0.28267500935975237",
            "extra": "mean: 7.471596303199999 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 46.202164361887036,
            "unit": "iter/sec",
            "range": "stddev: 0.00006614387764447151",
            "extra": "mean: 21.644007673911428 msec\nrounds: 46"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 29.53168648616985,
            "unit": "iter/sec",
            "range": "stddev: 0.00021676877647403624",
            "extra": "mean: 33.86193336666755 msec\nrounds: 30"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 11.210758488089892,
            "unit": "iter/sec",
            "range": "stddev: 0.00020957356237616902",
            "extra": "mean: 89.20003058333492 msec\nrounds: 12"
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
          "id": "24529c169c190ccabdcfa10d9a64965b0b073380",
          "message": "feat(policy): promote managed Git safeguards\n\nPromote the independently reviewed policy-only patch to the default branch for Issue #147 acceptance.",
          "timestamp": "2026-08-01T22:48:30Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/24529c169c190ccabdcfa10d9a64965b0b073380"
        },
        "date": 1786249316576,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.3841840407977932,
            "unit": "iter/sec",
            "range": "stddev: 0.01153106671158395",
            "extra": "mean: 722.4472833999996 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.313734785565192,
            "unit": "iter/sec",
            "range": "stddev: 0.008712417387515794",
            "extra": "mean: 761.1886440000006 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9081323372673671,
            "unit": "iter/sec",
            "range": "stddev: 0.0057152304953700436",
            "extra": "mean: 1.1011610961999978 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.18359608725119894,
            "unit": "iter/sec",
            "range": "stddev: 0.015178927494060933",
            "extra": "mean: 5.446739170599997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.251486461469687,
            "unit": "iter/sec",
            "range": "stddev: 0.0005240562317014232",
            "extra": "mean: 190.42227516666563 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.2097060816377536,
            "unit": "iter/sec",
            "range": "stddev: 0.010178367904592889",
            "extra": "mean: 452.54887440000005 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.7387038868735818,
            "unit": "iter/sec",
            "range": "stddev: 0.006059638197981681",
            "extra": "mean: 575.1410620000001 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.6960728612719468,
            "unit": "iter/sec",
            "range": "stddev: 0.013355055797140771",
            "extra": "mean: 1.4366312144000006 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.2724365635363104,
            "unit": "iter/sec",
            "range": "stddev: 0.013039214070574063",
            "extra": "mean: 3.670579260799991 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11248608180744621,
            "unit": "iter/sec",
            "range": "stddev: 0.048234354739492724",
            "extra": "mean: 8.889988734000008 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.07059364074187457,
            "unit": "iter/sec",
            "range": "stddev: 0.05358710580197798",
            "extra": "mean: 14.165581906399996 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 23.708197677458656,
            "unit": "iter/sec",
            "range": "stddev: 0.00025955323339286334",
            "extra": "mean: 42.17950320832623 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 15.309950202112342,
            "unit": "iter/sec",
            "range": "stddev: 0.00021603043782259302",
            "extra": "mean: 65.31699886666047 msec\nrounds: 15"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.053156689607225,
            "unit": "iter/sec",
            "range": "stddev: 0.0013774455515567358",
            "extra": "mean: 165.20305871429335 msec\nrounds: 7"
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
          "id": "24529c169c190ccabdcfa10d9a64965b0b073380",
          "message": "feat(policy): promote managed Git safeguards\n\nPromote the independently reviewed policy-only patch to the default branch for Issue #147 acceptance.",
          "timestamp": "2026-08-01T22:48:30Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/24529c169c190ccabdcfa10d9a64965b0b073380"
        },
        "date": 1786336806754,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 2.0359259202864157,
            "unit": "iter/sec",
            "range": "stddev: 0.007439788279546037",
            "extra": "mean: 491.17700699999887 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.9046791335742903,
            "unit": "iter/sec",
            "range": "stddev: 0.006854686899185533",
            "extra": "mean: 525.0228148000004 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 1.2095735163069643,
            "unit": "iter/sec",
            "range": "stddev: 0.00938033318691029",
            "extra": "mean: 826.7376777999999 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.23221489193482436,
            "unit": "iter/sec",
            "range": "stddev: 0.01542436376863104",
            "extra": "mean: 4.306356029399998 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 7.816267440906479,
            "unit": "iter/sec",
            "range": "stddev: 0.005269094459614699",
            "extra": "mean: 127.93830400000061 msec\nrounds: 8"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 3.3337559669122645,
            "unit": "iter/sec",
            "range": "stddev: 0.00732378146999445",
            "extra": "mean: 299.9619678000016 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.7114009487617805,
            "unit": "iter/sec",
            "range": "stddev: 0.004155905355161649",
            "extra": "mean: 368.81303020000473 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 1.0708134945510808,
            "unit": "iter/sec",
            "range": "stddev: 0.00808923743688347",
            "extra": "mean: 933.8694414000003 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.4261848888661971,
            "unit": "iter/sec",
            "range": "stddev: 0.031421904253045425",
            "extra": "mean: 2.3463994762 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.1739694335552846,
            "unit": "iter/sec",
            "range": "stddev: 0.016547383697692836",
            "extra": "mean: 5.7481362074 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.10955236097488466,
            "unit": "iter/sec",
            "range": "stddev: 0.03877458243358262",
            "extra": "mean: 9.128055215799998 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 36.951594962564705,
            "unit": "iter/sec",
            "range": "stddev: 0.00009876354490771907",
            "extra": "mean: 27.062431297298264 msec\nrounds: 37"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 23.297262967362855,
            "unit": "iter/sec",
            "range": "stddev: 0.000529852205686092",
            "extra": "mean: 42.923497125001354 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 8.568101748881048,
            "unit": "iter/sec",
            "range": "stddev: 0.00029144877281150195",
            "extra": "mean: 116.71196600000637 msec\nrounds: 9"
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
          "id": "24529c169c190ccabdcfa10d9a64965b0b073380",
          "message": "feat(policy): promote managed Git safeguards\n\nPromote the independently reviewed policy-only patch to the default branch for Issue #147 acceptance.",
          "timestamp": "2026-08-01T22:48:30Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/24529c169c190ccabdcfa10d9a64965b0b073380"
        },
        "date": 1786422211560,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.3837783934807504,
            "unit": "iter/sec",
            "range": "stddev: 0.007000751949944769",
            "extra": "mean: 722.6590649999991 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.3051140017733074,
            "unit": "iter/sec",
            "range": "stddev: 0.01023483729767256",
            "extra": "mean: 766.2165900000019 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9011991497555174,
            "unit": "iter/sec",
            "range": "stddev: 0.014941910455200711",
            "extra": "mean: 1.1096326491999975 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.18259845076793452,
            "unit": "iter/sec",
            "range": "stddev: 0.00984855578216748",
            "extra": "mean: 5.476497723800001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.312458172969308,
            "unit": "iter/sec",
            "range": "stddev: 0.00031642386221610426",
            "extra": "mean: 188.2367761666662 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.2395008431393717,
            "unit": "iter/sec",
            "range": "stddev: 0.00871734383907002",
            "extra": "mean: 446.5280747999998 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.7820064197700818,
            "unit": "iter/sec",
            "range": "stddev: 0.001084564257326005",
            "extra": "mean: 561.165206199999 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.7125570182835309,
            "unit": "iter/sec",
            "range": "stddev: 0.007814198053457597",
            "extra": "mean: 1.4033964641999972 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.2793494425460892,
            "unit": "iter/sec",
            "range": "stddev: 0.02762865633731656",
            "extra": "mean: 3.5797458225999947 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11548935501089462,
            "unit": "iter/sec",
            "range": "stddev: 0.049646993666610593",
            "extra": "mean: 8.658806691799999 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.07309123936076534,
            "unit": "iter/sec",
            "range": "stddev: 0.03369980984674848",
            "extra": "mean: 13.681530218199999 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 23.43703721006837,
            "unit": "iter/sec",
            "range": "stddev: 0.00024545779220495206",
            "extra": "mean: 42.6675091666624 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 15.175071273824049,
            "unit": "iter/sec",
            "range": "stddev: 0.00024882764108246144",
            "extra": "mean: 65.89754881250087 msec\nrounds: 16"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 5.953316508982646,
            "unit": "iter/sec",
            "range": "stddev: 0.0008113016112711268",
            "extra": "mean: 167.9735990000116 msec\nrounds: 6"
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
          "id": "24529c169c190ccabdcfa10d9a64965b0b073380",
          "message": "feat(policy): promote managed Git safeguards\n\nPromote the independently reviewed policy-only patch to the default branch for Issue #147 acceptance.",
          "timestamp": "2026-08-01T22:48:30Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/24529c169c190ccabdcfa10d9a64965b0b073380"
        },
        "date": 1786510149031,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.619990766409018,
            "unit": "iter/sec",
            "range": "stddev: 0.028691185912532047",
            "extra": "mean: 617.2874690000043 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.5946674305812543,
            "unit": "iter/sec",
            "range": "stddev: 0.00974851225447549",
            "extra": "mean: 627.0900006000005 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 1.035902301338239,
            "unit": "iter/sec",
            "range": "stddev: 0.009006394812997727",
            "extra": "mean: 965.3420006000005 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.22338741170630738,
            "unit": "iter/sec",
            "range": "stddev: 0.043994897387732664",
            "extra": "mean: 4.476527984999993 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 6.993033057948603,
            "unit": "iter/sec",
            "range": "stddev: 0.008143567164437353",
            "extra": "mean: 142.99946699999566 msec\nrounds: 8"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 3.0509651444189396,
            "unit": "iter/sec",
            "range": "stddev: 0.009118756255428608",
            "extra": "mean: 327.7651342000013 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.5940422225529023,
            "unit": "iter/sec",
            "range": "stddev: 0.011309279048996156",
            "extra": "mean: 385.4987367999968 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.9835800381243038,
            "unit": "iter/sec",
            "range": "stddev: 0.04485096111817021",
            "extra": "mean: 1.0166940780000062 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.4109694138472986,
            "unit": "iter/sec",
            "range": "stddev: 0.036496301275670225",
            "extra": "mean: 2.4332711055999994 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.16993164142799147,
            "unit": "iter/sec",
            "range": "stddev: 0.16505375843977893",
            "extra": "mean: 5.884719241199997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.11471652201830365,
            "unit": "iter/sec",
            "range": "stddev: 0.03524038862492968",
            "extra": "mean: 8.717140150399995 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 38.12523441814819,
            "unit": "iter/sec",
            "range": "stddev: 0.0015283195012288045",
            "extra": "mean: 26.229346921050926 msec\nrounds: 38"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 23.71646205937787,
            "unit": "iter/sec",
            "range": "stddev: 0.0018295312570637088",
            "extra": "mean: 42.16480508333594 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 8.843209688822734,
            "unit": "iter/sec",
            "range": "stddev: 0.0037260197741961483",
            "extra": "mean: 113.08111366667441 msec\nrounds: 9"
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
          "id": "24529c169c190ccabdcfa10d9a64965b0b073380",
          "message": "feat(policy): promote managed Git safeguards\n\nPromote the independently reviewed policy-only patch to the default branch for Issue #147 acceptance.",
          "timestamp": "2026-08-01T22:48:30Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/24529c169c190ccabdcfa10d9a64965b0b073380"
        },
        "date": 1786596811265,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.662434830193988,
            "unit": "iter/sec",
            "range": "stddev: 0.012957844954729413",
            "extra": "mean: 601.527339200004 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.5656924022838798,
            "unit": "iter/sec",
            "range": "stddev: 0.012329876850575938",
            "extra": "mean: 638.6950581999997 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 1.0322946817534029,
            "unit": "iter/sec",
            "range": "stddev: 0.023201632348493425",
            "extra": "mean: 968.715636799999 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.21539739475165787,
            "unit": "iter/sec",
            "range": "stddev: 0.046011433827609936",
            "extra": "mean: 4.642581685599998 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 6.938909200680799,
            "unit": "iter/sec",
            "range": "stddev: 0.006076918051251384",
            "extra": "mean: 144.11487037499882 msec\nrounds: 8"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.9337870737809837,
            "unit": "iter/sec",
            "range": "stddev: 0.008316161654003371",
            "extra": "mean: 340.85636579999914 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.5555787979768425,
            "unit": "iter/sec",
            "range": "stddev: 0.01309631729885268",
            "extra": "mean: 391.30078899999603 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 1.0145667574752322,
            "unit": "iter/sec",
            "range": "stddev: 0.023535738271236506",
            "extra": "mean: 985.6423864000021 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.41371332948651557,
            "unit": "iter/sec",
            "range": "stddev: 0.054084555889392906",
            "extra": "mean: 2.417132658600002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.16890747268148545,
            "unit": "iter/sec",
            "range": "stddev: 0.0830001265555604",
            "extra": "mean: 5.920401176600007 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.10603753987329227,
            "unit": "iter/sec",
            "range": "stddev: 0.059791058979684834",
            "extra": "mean: 9.430622411600012 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 37.71673220223294,
            "unit": "iter/sec",
            "range": "stddev: 0.0006821403222655949",
            "extra": "mean: 26.513431615393156 msec\nrounds: 39"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 23.706614524762443,
            "unit": "iter/sec",
            "range": "stddev: 0.000673452678253315",
            "extra": "mean: 42.18231999999252 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 8.618435692774307,
            "unit": "iter/sec",
            "range": "stddev: 0.00294740469770908",
            "extra": "mean: 116.03033724999534 msec\nrounds: 8"
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
          "id": "24529c169c190ccabdcfa10d9a64965b0b073380",
          "message": "feat(policy): promote managed Git safeguards\n\nPromote the independently reviewed policy-only patch to the default branch for Issue #147 acceptance.",
          "timestamp": "2026-08-01T22:48:30Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/24529c169c190ccabdcfa10d9a64965b0b073380"
        },
        "date": 1786683036046,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.9928011413872277,
            "unit": "iter/sec",
            "range": "stddev: 0.013723632921443333",
            "extra": "mean: 501.8062159999971 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.8631338983920098,
            "unit": "iter/sec",
            "range": "stddev: 0.013891220581364482",
            "extra": "mean: 536.7300766 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 1.1625221034309163,
            "unit": "iter/sec",
            "range": "stddev: 0.01604565759291673",
            "extra": "mean: 860.1986982 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.21487348277740348,
            "unit": "iter/sec",
            "range": "stddev: 0.048038966170690305",
            "extra": "mean: 4.653901389199999 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 7.506107924090157,
            "unit": "iter/sec",
            "range": "stddev: 0.010175090043120616",
            "extra": "mean: 133.2248363749997 msec\nrounds: 8"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 3.250542767504877,
            "unit": "iter/sec",
            "range": "stddev: 0.008161934961949276",
            "extra": "mean: 307.640930000008 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.5683521688208337,
            "unit": "iter/sec",
            "range": "stddev: 0.0048116952940229695",
            "extra": "mean: 389.35470459999806 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.9854696930346574,
            "unit": "iter/sec",
            "range": "stddev: 0.014845725476821043",
            "extra": "mean: 1.0147445498000025 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.3986244056304521,
            "unit": "iter/sec",
            "range": "stddev: 0.053732728716374724",
            "extra": "mean: 2.5086271334 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.1685759497765713,
            "unit": "iter/sec",
            "range": "stddev: 0.06339148141523714",
            "extra": "mean: 5.932044288200001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.10667371370173383,
            "unit": "iter/sec",
            "range": "stddev: 0.18401470957418137",
            "extra": "mean: 9.374380672600006 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 36.90550183869347,
            "unit": "iter/sec",
            "range": "stddev: 0.00026951464252688163",
            "extra": "mean: 27.096230918923663 msec\nrounds: 37"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 23.197310673141008,
            "unit": "iter/sec",
            "range": "stddev: 0.00010515888436108683",
            "extra": "mean: 43.10844537499984 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 8.333390548232662,
            "unit": "iter/sec",
            "range": "stddev: 0.00097493979558701",
            "extra": "mean: 119.99917611110631 msec\nrounds: 9"
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
          "id": "24529c169c190ccabdcfa10d9a64965b0b073380",
          "message": "feat(policy): promote managed Git safeguards\n\nPromote the independently reviewed policy-only patch to the default branch for Issue #147 acceptance.",
          "timestamp": "2026-08-01T22:48:30Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/24529c169c190ccabdcfa10d9a64965b0b073380"
        },
        "date": 1786765287396,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.5728054246652865,
            "unit": "iter/sec",
            "range": "stddev: 0.011606794925612621",
            "extra": "mean: 635.806555800005 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.4729484315422128,
            "unit": "iter/sec",
            "range": "stddev: 0.007743577727628429",
            "extra": "mean: 678.9103939999961 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9542397696474362,
            "unit": "iter/sec",
            "range": "stddev: 0.01010287939309507",
            "extra": "mean: 1.0479546459999995 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.1810035540634291,
            "unit": "iter/sec",
            "range": "stddev: 0.005838513495210233",
            "extra": "mean: 5.524753396000003 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 6.172313749140693,
            "unit": "iter/sec",
            "range": "stddev: 0.0004488425739813487",
            "extra": "mean: 162.01379914286105 msec\nrounds: 7"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.593773613034078,
            "unit": "iter/sec",
            "range": "stddev: 0.008566632420827057",
            "extra": "mean: 385.53865880000444 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.1399092756788276,
            "unit": "iter/sec",
            "range": "stddev: 0.002153622157446203",
            "extra": "mean: 467.3095309999894 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.8416863328698378,
            "unit": "iter/sec",
            "range": "stddev: 0.010577850448857475",
            "extra": "mean: 1.1880910512000014 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.3379660731270438,
            "unit": "iter/sec",
            "range": "stddev: 0.024385376400096515",
            "extra": "mean: 2.9588768800000027 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.13783841976862343,
            "unit": "iter/sec",
            "range": "stddev: 0.0310672496241341",
            "extra": "mean: 7.254871331799995 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.08855024249080208,
            "unit": "iter/sec",
            "range": "stddev: 0.023317295063084657",
            "extra": "mean: 11.293023845799997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 28.40120153496554,
            "unit": "iter/sec",
            "range": "stddev: 0.00012582237217652998",
            "extra": "mean: 35.209777965515684 msec\nrounds: 29"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 17.91093800406369,
            "unit": "iter/sec",
            "range": "stddev: 0.0003313799353816809",
            "extra": "mean: 55.83180511110678 msec\nrounds: 18"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.598674098436045,
            "unit": "iter/sec",
            "range": "stddev: 0.001336250391461181",
            "extra": "mean: 151.54559614286913 msec\nrounds: 7"
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
          "id": "24529c169c190ccabdcfa10d9a64965b0b073380",
          "message": "feat(policy): promote managed Git safeguards\n\nPromote the independently reviewed policy-only patch to the default branch for Issue #147 acceptance.",
          "timestamp": "2026-08-01T22:48:30Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/24529c169c190ccabdcfa10d9a64965b0b073380"
        },
        "date": 1786852328823,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.339828046891841,
            "unit": "iter/sec",
            "range": "stddev: 0.016447299640959145",
            "extra": "mean: 746.3644326000036 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.2526638118306404,
            "unit": "iter/sec",
            "range": "stddev: 0.01914471895258506",
            "extra": "mean: 798.2987858000001 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.8414676207490408,
            "unit": "iter/sec",
            "range": "stddev: 0.019657478884259297",
            "extra": "mean: 1.1883998568000038 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.1697147310104974,
            "unit": "iter/sec",
            "range": "stddev: 0.03161038498007953",
            "extra": "mean: 5.8922404322 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.116597968280245,
            "unit": "iter/sec",
            "range": "stddev: 0.0008326881146175546",
            "extra": "mean: 195.44236350000213 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.123858297406264,
            "unit": "iter/sec",
            "range": "stddev: 0.020269539247503958",
            "extra": "mean: 470.8412049999936 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.6460874801662086,
            "unit": "iter/sec",
            "range": "stddev: 0.006311072233451475",
            "extra": "mean: 607.5011274000019 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.6595564444366689,
            "unit": "iter/sec",
            "range": "stddev: 0.024509816055780387",
            "extra": "mean: 1.5161704633999988 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.26045677219384705,
            "unit": "iter/sec",
            "range": "stddev: 0.02972019841316648",
            "extra": "mean: 3.8394087110000044 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11156866752802522,
            "unit": "iter/sec",
            "range": "stddev: 0.08479532450088023",
            "extra": "mean: 8.963089926200002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.06956013620989644,
            "unit": "iter/sec",
            "range": "stddev: 0.055580851905595995",
            "extra": "mean: 14.376050055199983 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 23.012122049503528,
            "unit": "iter/sec",
            "range": "stddev: 0.0005425190308763125",
            "extra": "mean: 43.45535791305149 msec\nrounds: 23"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 14.76167854550866,
            "unit": "iter/sec",
            "range": "stddev: 0.0008088150731870252",
            "extra": "mean: 67.74297359999461 msec\nrounds: 15"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 5.769398281491139,
            "unit": "iter/sec",
            "range": "stddev: 0.001812271750770486",
            "extra": "mean: 173.3283006666587 msec\nrounds: 6"
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
          "id": "24529c169c190ccabdcfa10d9a64965b0b073380",
          "message": "feat(policy): promote managed Git safeguards\n\nPromote the independently reviewed policy-only patch to the default branch for Issue #147 acceptance.",
          "timestamp": "2026-08-01T22:48:30Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/24529c169c190ccabdcfa10d9a64965b0b073380"
        },
        "date": 1786938765089,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 2.026659653062355,
            "unit": "iter/sec",
            "range": "stddev: 0.00760538823654611",
            "extra": "mean: 493.4227601999993 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.8912611539457551,
            "unit": "iter/sec",
            "range": "stddev: 0.008936720594489826",
            "extra": "mean: 528.7477077999995 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 1.2232239467610473,
            "unit": "iter/sec",
            "range": "stddev: 0.005307700470049701",
            "extra": "mean: 817.5117913999983 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.22734079853298625,
            "unit": "iter/sec",
            "range": "stddev: 0.008888759024127202",
            "extra": "mean: 4.398682534999999 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 7.79598209544371,
            "unit": "iter/sec",
            "range": "stddev: 0.004941673198226141",
            "extra": "mean: 128.27120274999615 msec\nrounds: 8"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 3.316187969450544,
            "unit": "iter/sec",
            "range": "stddev: 0.006862148684356102",
            "extra": "mean: 301.5510607999971 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.6985360186817178,
            "unit": "iter/sec",
            "range": "stddev: 0.003021717944766258",
            "extra": "mean: 370.57129979999957 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 1.068084805757555,
            "unit": "iter/sec",
            "range": "stddev: 0.009593145420513306",
            "extra": "mean: 936.2552436000016 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.42325363932432375,
            "unit": "iter/sec",
            "range": "stddev: 0.017004922393993344",
            "extra": "mean: 2.362649501600001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.17288413110074283,
            "unit": "iter/sec",
            "range": "stddev: 0.038699437812364554",
            "extra": "mean: 5.784220874600001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.10851644724009112,
            "unit": "iter/sec",
            "range": "stddev: 0.027033676045215144",
            "extra": "mean: 9.215192953999997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 36.63473346327488,
            "unit": "iter/sec",
            "range": "stddev: 0.00007930353688224416",
            "extra": "mean: 27.296499945945214 msec\nrounds: 37"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 23.32499607265216,
            "unit": "iter/sec",
            "range": "stddev: 0.00016119122146828017",
            "extra": "mean: 42.87246166666966 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 8.46760445868984,
            "unit": "iter/sec",
            "range": "stddev: 0.0010037141753528758",
            "extra": "mean: 118.0971554444486 msec\nrounds: 9"
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
          "id": "24529c169c190ccabdcfa10d9a64965b0b073380",
          "message": "feat(policy): promote managed Git safeguards\n\nPromote the independently reviewed policy-only patch to the default branch for Issue #147 acceptance.",
          "timestamp": "2026-08-01T22:48:30Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/24529c169c190ccabdcfa10d9a64965b0b073380"
        },
        "date": 1787024843631,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.5063789203103934,
            "unit": "iter/sec",
            "range": "stddev: 0.019544826223271788",
            "extra": "mean: 663.8435963999996 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.4395605244217462,
            "unit": "iter/sec",
            "range": "stddev: 0.013029136029208068",
            "extra": "mean: 694.6564475999978 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9175438303411636,
            "unit": "iter/sec",
            "range": "stddev: 0.011247833246288618",
            "extra": "mean: 1.0898661915999994 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.17081295024319715,
            "unit": "iter/sec",
            "range": "stddev: 0.12735546743311008",
            "extra": "mean: 5.854357053000004 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 6.05512554812361,
            "unit": "iter/sec",
            "range": "stddev: 0.0003170197943781893",
            "extra": "mean: 165.14934199999942 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.5137654600999952,
            "unit": "iter/sec",
            "range": "stddev: 0.010403557604338693",
            "extra": "mean: 397.80958720000115 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.0033449409743485,
            "unit": "iter/sec",
            "range": "stddev: 0.005327537425315794",
            "extra": "mean: 499.16516100000194 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.7716471314127913,
            "unit": "iter/sec",
            "range": "stddev: 0.007380479767192821",
            "extra": "mean: 1.2959291356000022 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.3186128870166488,
            "unit": "iter/sec",
            "range": "stddev: 0.029675871419467738",
            "extra": "mean: 3.138604999200004 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.12957638359097762,
            "unit": "iter/sec",
            "range": "stddev: 0.07395462858980574",
            "extra": "mean: 7.7174556989999985 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.08347005203665009,
            "unit": "iter/sec",
            "range": "stddev: 0.17512640630047777",
            "extra": "mean: 11.980344753600003 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 28.151486031368908,
            "unit": "iter/sec",
            "range": "stddev: 0.001023125707855636",
            "extra": "mean: 35.52210348276856 msec\nrounds: 29"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 17.886861096077112,
            "unit": "iter/sec",
            "range": "stddev: 0.0002613168449959921",
            "extra": "mean: 55.906958444448186 msec\nrounds: 18"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.535076295690728,
            "unit": "iter/sec",
            "range": "stddev: 0.0004413958347530618",
            "extra": "mean: 153.0204017142702 msec\nrounds: 7"
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
          "id": "24529c169c190ccabdcfa10d9a64965b0b073380",
          "message": "feat(policy): promote managed Git safeguards\n\nPromote the independently reviewed policy-only patch to the default branch for Issue #147 acceptance.",
          "timestamp": "2026-08-01T22:48:30Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/24529c169c190ccabdcfa10d9a64965b0b073380"
        },
        "date": 1787111358679,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.5682023508048926,
            "unit": "iter/sec",
            "range": "stddev: 0.011526039364393545",
            "extra": "mean: 637.6728101999987 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.4559549934819704,
            "unit": "iter/sec",
            "range": "stddev: 0.012504637024035667",
            "extra": "mean: 686.8344175999994 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.9481493209653129,
            "unit": "iter/sec",
            "range": "stddev: 0.009174893079749943",
            "extra": "mean: 1.0546861954000009 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.17395565167943144,
            "unit": "iter/sec",
            "range": "stddev: 0.05447690883542592",
            "extra": "mean: 5.7485916114 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 6.104370723740925,
            "unit": "iter/sec",
            "range": "stddev: 0.0003516711601747309",
            "extra": "mean: 163.8170493333296 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.56789768247429,
            "unit": "iter/sec",
            "range": "stddev: 0.008841711922864202",
            "extra": "mean: 389.4236156000005 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 2.0835039853316553,
            "unit": "iter/sec",
            "range": "stddev: 0.006198364275342356",
            "extra": "mean: 479.96068499999467 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.8169253422231182,
            "unit": "iter/sec",
            "range": "stddev: 0.01435033501207979",
            "extra": "mean: 1.2241020669999982 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.3288229192002185,
            "unit": "iter/sec",
            "range": "stddev: 0.02772586427248292",
            "extra": "mean: 3.0411505452 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.13373478525536758,
            "unit": "iter/sec",
            "range": "stddev: 0.061702000824701494",
            "extra": "mean: 7.477486116200003 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.08415583990214899,
            "unit": "iter/sec",
            "range": "stddev: 0.048661059481559646",
            "extra": "mean: 11.882716649999997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 28.110166958559326,
            "unit": "iter/sec",
            "range": "stddev: 0.0014005392387229567",
            "extra": "mean: 35.57431734483198 msec\nrounds: 29"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 17.824366693742675,
            "unit": "iter/sec",
            "range": "stddev: 0.0002671712232342084",
            "extra": "mean: 56.1029750555488 msec\nrounds: 18"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.5030363192173475,
            "unit": "iter/sec",
            "range": "stddev: 0.001187877372155049",
            "extra": "mean: 153.7743218571401 msec\nrounds: 7"
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
          "id": "24529c169c190ccabdcfa10d9a64965b0b073380",
          "message": "feat(policy): promote managed Git safeguards\n\nPromote the independently reviewed policy-only patch to the default branch for Issue #147 acceptance.",
          "timestamp": "2026-08-01T22:48:30Z",
          "url": "https://github.com/nbx-liz/pycatdap/commit/24529c169c190ccabdcfa10d9a64965b0b073380"
        },
        "date": 1787197808389,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100]",
            "value": 1.3634603555306772,
            "unit": "iter/sec",
            "range": "stddev: 0.009576185886887356",
            "extra": "mean: 733.4279987999992 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[1000]",
            "value": 1.2923458299182624,
            "unit": "iter/sec",
            "range": "stddev: 0.01759569418786666",
            "extra": "mean: 773.7866883999984 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[10000]",
            "value": 0.8859619462510822,
            "unit": "iter/sec",
            "range": "stddev: 0.012425202498324258",
            "extra": "mean: 1.1287166499999983 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap1.py::test_catdap1_categorical[100000]",
            "value": 0.17997963278627518,
            "unit": "iter/sec",
            "range": "stddev: 0.016826018268448654",
            "extra": "mean: 5.556184244400001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-5]",
            "value": 5.227513557040193,
            "unit": "iter/sec",
            "range": "stddev: 0.0011506333841967123",
            "extra": "mean: 191.29553450000003 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[100-10]",
            "value": 2.1943359206113193,
            "unit": "iter/sec",
            "range": "stddev: 0.008627323716841339",
            "extra": "mean: 455.71873960000175 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-5]",
            "value": 1.7323979332923656,
            "unit": "iter/sec",
            "range": "stddev: 0.0035368949132840695",
            "extra": "mean: 577.2345838000007 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[1000-10]",
            "value": 0.6914864539206713,
            "unit": "iter/sec",
            "range": "stddev: 0.010022639300669534",
            "extra": "mean: 1.4461599273999979 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-5]",
            "value": 0.2723188744080922,
            "unit": "iter/sec",
            "range": "stddev: 0.019979682995466153",
            "extra": "mean: 3.6721655895999987 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_catdap2.py::test_catdap2_mixed[10000-10]",
            "value": 0.11204767526968926,
            "unit": "iter/sec",
            "range": "stddev: 0.045238986542296",
            "extra": "mean: 8.924772402400004 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_discovery.py::test_discover_error_slices_adult_like",
            "value": 0.07036965963039658,
            "unit": "iter/sec",
            "range": "stddev: 0.03655351800073941",
            "extra": "mean: 14.210669843400012 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[1000]",
            "value": 23.495535279999796,
            "unit": "iter/sec",
            "range": "stddev: 0.00019878204659173958",
            "extra": "mean: 42.56127762499773 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[10000]",
            "value": 15.158422813211542,
            "unit": "iter/sec",
            "range": "stddev: 0.0007964416267437197",
            "extra": "mean: 65.96992393749801 msec\nrounds: 16"
          },
          {
            "name": "benchmarks/bench_pooling.py::test_optimal_binning_bottom_up[100000]",
            "value": 6.051114643670996,
            "unit": "iter/sec",
            "range": "stddev: 0.0011298107319540037",
            "extra": "mean: 165.2588091428616 msec\nrounds: 7"
          }
        ]
      }
    ]
  }
}