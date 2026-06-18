window.BENCHMARK_DATA = {
  "lastUpdate": 1781770366594,
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
      }
    ]
  }
}