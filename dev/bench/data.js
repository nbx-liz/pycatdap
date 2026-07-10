window.BENCHMARK_DATA = {
  "lastUpdate": 1783666201834,
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
      }
    ]
  }
}