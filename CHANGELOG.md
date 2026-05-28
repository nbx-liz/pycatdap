# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.7.0] — 2026-05-28

このリリースは **H-0010 Phase G** に対応し、ML 誤差分析 arc の基盤となる
**誤差ラベリングユーティリティ** と、Phase G チュートリアル用に
**D3 demo データセット** を同梱する。BLUEPRINT.md §3.1 / §5.8 を参照。

主要な追加:
- `pycatdap.error.error_label / confusion_label / residual_label / abs_residual_pool`
  — 予測結果を categorical Series にラベル付け
- `pycatdap.error._detect_task` — task auto-detection ヒューリスティック
- `pycatdap.datasets.load_german_credit / load_heart_disease / load_penguins`
  — D3 demo データセット(UCI / Palmer Penguins)

### Added — Phase G error labeling (`pycatdap.error`)
- `error_label(y_true, y_pred)` — 任意 task で予測の正誤を
  `pd.Series("correct" | "incorrect")` で返す。
- `confusion_label(y_true, y_pred, *, positive=None)` — 二値分類で
  TP/FP/FN/TN を `pd.Series` で返す。`positive=None` の時は 2 ユニーク値の
  片方(大きい方)を自動選択。**multiclass は `NotImplementedError`**(H-0010 §C
  により one-vs-rest は v0.8.0+ 後続)。
- `residual_label(y_true, y_pred, *, method="aic_pool", n_bins=4)` —
  回帰残差を 3 つの method(`aic_pool` / `quantile` / `equal_width`)で
  ビン化。`aic_pool` は `pycatdap._pooling.equal_pooling` を再利用。
- `abs_residual_pool(y_true, y_pred, *, n_bins=4)` — `|y_true - y_pred|` を
  AIC pooling で binned categorical に。
- `_detect_task(y_true, y_pred)` — 文字列/object → classification、
  両方 int で <= 20 ユニーク → classification、float in [0,1] vs binary
  y_true → classification、それ以外 → regression。

Phase G は **意図的に新規 dataclass を導入していない**。H-0009 で対処した
shallow-freeze pattern の再発を防ぐため、すべて `pd.Series` で返す。
`ErrorAnalysisResult` は Phase H(v0.8.0)で v0.6.1 immutable pattern を
最初から適用して導入する。

### Added — D3 demo datasets (`pycatdap.datasets`)
- `load_german_credit()` — UCI Statlog German Credit(1000 × 21)。
  Binary classification benchmark。`class` ラベルは `"good"` / `"bad"`、
  700/300 split。Public domain via OpenML id `credit-g` v1。
- `load_heart_disease()` — UCI Cleveland Heart Disease processed
  subset(303 × 14)。Binary classification、`target` ラベルは 0/1。
  全列 numeric。CC BY 4.0 via OpenML id `heart-disease` v1。
- `load_penguins()` — Palmer Penguins(344 × 7)。3 クラス分類
  `species ∈ {Adelie, Chinstrap, Gentoo}`。CC0 1.0 via OpenML id
  `penguins` v1。

データセット issue は **独立リリースとして扱わず、それを使う Phase に同梱**
する方針(2026-05-28 architect レビュー、PLAN.md §3.3 で文書化)。D3 は
v0.5.0 → v0.6.0 と 2 回スリップしたが、Phase G が demo データを必要とする
ため自然な fold-in タイミングとして v0.7.0 にまとめた。

### Added — Tutorial
- `docs/tutorials/10-phase-g-error-labeling.ipynb` — German Credit と
  合成回帰データで Phase G API を体系的にデモ。Phase H への接続を解説。

### Changed
- BLUEPRINT.md §3.1 の `error/` ツリーを更新(`_labels.py` 実装済を反映)。
- BLUEPRINT.md §5.8 の Phase G セクションを「v0.7.0 で実装済」に格上げ。

### References
- HISTORY.md H-0010 (Phase G + D3 dataset folding decision)
- Issue #16 (Phase G)、Issue #23 (D3 datasets)

## [0.6.1] — 2026-05-28

### Changed — API hardening (breaking for callers that mutated result objects)
H-0009: 4 `@dataclass(frozen=True)` types shipped in v0.6.0 had mutable
internal fields (`list` / `dict` / `pd.DataFrame`) despite `frozen=True`.
This contradicted the "NEVER mutate" rule and allowed silent corruption
of result objects. Fixed in v0.6.1 before Phase G (v0.7.0) inherits the
same shallow-freeze pattern:

- `SuiteResult.checks` is now `tuple[CheckResult, ...]` instead of
  `list[CheckResult]`. Call `list(result.checks)` to get a mutable copy.
- `CheckResult.affected_columns` is now `tuple[str, ...]` instead of
  `list[str]`. Call `list(...)` to get a mutable copy.
- `TargetAnalysisResult.top_summaries` is now a read-only
  `Mapping[str, ...]` (`types.MappingProxyType`). Reads, iteration, and
  `.items()` work as before; `__setitem__` / `__delitem__` raise
  `TypeError`. Call `dict(...)` to get a mutable copy.
- `TargetAnalysisResult.ranking` is documented read-only and the
  underlying numpy buffer is frozen via `__post_init__` setting
  `.flags.writeable = False`. Element assignment (`df.values[i] = x`)
  raises; DataFrame-level operations (`drop`, `assign(inplace=False)`)
  still allocate new buffers and remain available. Call `.copy()`
  before mutating in place.

Pre-v0.6.0 result objects with the same pattern
(`QualityReport.warnings`, `ProfileResult.variables`,
`EDADescribe.summary`, etc.) are deferred to a follow-up issue for
staged migration before v1.0 — fixing them all together would inflate
this patch beyond a focused release.

### CI / Release infrastructure
- `auto-release.yml` now dispatches `release.yml` automatically via
  `workflow_dispatch` after creating the tag and GitHub Release.
  Previously the default `GITHUB_TOKEN`-pushed tag did not fire
  `release.yml`'s `push: tags: [v*]` trigger (recursive-trigger
  suppression), forcing a manual `gh workflow run "Release to PyPI"`
  step on every release from v0.3.0 through v0.6.0. The new step uses
  `workflow_dispatch`, which is exempt from the recursive-trigger
  restriction and works with `GITHUB_TOKEN` (no PAT required).
  Requires `permissions: actions: write` on `auto-release.yml`.

## [0.6.0] — 2026-05-28

このリリースは H-0008 Phase D に対応し、**target 駆動分析と CI 統合可能な
品質スイート** を追加する。v0.5.0 の flagship `profile()` を補完する 4 つの
新規公開 API（`quality_report` / `target_analysis` / `pycatdap.measures` /
`pycatdap.suite`）と、`association_matrix(measure=...)` の non-AIC 拡張を
含む。詳細は HISTORY.md H-0008 および以下の節を参照。

主要な追加:
- `pycatdap.quality_report(df).passed` — CI gate 用の高速データ品質スキャン
- `pycatdap.target_analysis(df, response)` — ΔAIC ランキング + 上位 K の TargetSummary
- `pycatdap.measures.{aic, cramers_v, mutual_info, register}` — pluggable interestingness 指標
- `pycatdap.association_matrix(df, measure="cramers_v")` — 非 AIC 関連度行列
- `pycatdap.suite.AICIndependenceSuite(df, response).run().passed` — deepchecks 風 CI スイート

### Added
- Tutorial Notebook 09 — `docs/tutorials/09-phase-d-target-analysis-and-suite.ipynb`
  walks through every Phase D API on the Titanic dataset:
  `quality_report` → `target_analysis` → `pycatdap.measures.*` →
  `pycatdap.suite.AICIndependenceSuite` with the
  `assert suite_result.passed, suite_result.summary()` CI idiom
  (H-0008 PR-D6).
- `pycatdap.suite` subpackage — deepchecks-style CI-integrable suite
  per Issue #15 (H-0008 PR-D5). Public API:
  - `pycatdap.suite.AICIndependenceSuite(df, response=...).run() ->
    SuiteResult` — default bundle of the 4 standard checks
  - Individual checks: `ConstantColumnCheck`, `HighCardinalityCheck`,
    `IndependenceCheck`, `PoolingSuggestionCheck` (all
    `@dataclass(frozen=True)` so thresholds are immutable; no
    `eval()` / string DSL anywhere — safe on untrusted DataFrames)
  - `SuiteResult` with `.passed` boolean for `assert suite_result.passed`,
    `.failures` (all non-passing checks including `"info"`-severity),
    `.summary()`, `.show()`, `.to_html(path)`, `.to_dict()`,
    `.to_plotly_json()`
- `association_matrix(df, measure=...)` extension — dispatch on any
  registered :mod:`pycatdap.measures` measure. ``measure="aic"``
  (default) keeps the existing :func:`target_summary`-based path;
  ``"cramers_v"`` / ``"mutual_info"`` / custom measures use a generic
  crosstab path with uniform ``pd.qcut`` binning of continuous columns
  (H-0008 PR-D5).
- `pycatdap.measures` subpackage with a pluggable interestingness-
  measure registry (BLUEPRINT §5.11, H-0008 PR-D4). Each measure has
  the uniform signature `Callable[[npt.NDArray[np.float64]], float]`.
  Standard measures shipped:
  - `pycatdap.measures.aic(cross_freq)` — ΔAIC (negative = informative)
  - `pycatdap.measures.cramers_v(cross_freq)` — Cramér's V (0..1,
    pure-numpy, no scipy dependency)
  - `pycatdap.measures.mutual_info(cross_freq)` — mutual information
    in nats (pure-numpy)
  - `pycatdap.measures.register(name, fn)` / `get(name)` /
    `list_measures()` for custom measures (pysubgroup / DivExplorer
    interop, Issues #31 / #32)
- `pycatdap.target_analysis(df, response)` — target-driven ΔAIC ranking
  of every non-response column. Keeps the full `TargetSummary` /
  `RegressionTargetSummary` for the top-K most informative columns
  (`top_k=5` by default). Exposes `.show()`, `.to_html(path)`,
  `.to_dict()`, and `.to_plotly_json()` matching the
  `ProfileResult` 4-method contract; HTML report embeds each top-K
  cross-tab inline via Plotly (H-0008 PR-D3).
- `pycatdap.TargetAnalysisResult` re-export.
- `pycatdap.quality_report(df)` — focused data-quality scan returning
  a `QualityReport` dataclass. Shares the warning logic of `profile()`
  via the new `src/pycatdap/_quality.py` helper but skips
  `association_matrix` / `catdap2`, so it stays fast on wide CI frames.
  Exposes `.passed` (boolean for `assert qr.passed`), `.by_severity()`,
  `.by_kind()`, `.show()`, `.to_html(path)`, `.to_dict()`, and
  `.to_plotly_json()` (H-0008 PR-D2).
- `pycatdap.QualityReport` re-export.

### Changed
- Internal refactor: `_scan_quality` lifted from `pycatdap.profile`
  into `pycatdap._quality` so `quality_report` / `profile` /
  `pycatdap.suite` share one helper. Public surface unchanged
  (H-0008 PR-D1).
- `BLUEPRINT.md` §3.1 / §5.10 / §5.11 updated to reflect the shipped
  Phase D module structure and APIs (H-0008 PR-D6).
- `README.md` Quickstart now shows the target-analysis / quality
  report / suite / measures workflow (H-0008 PR-D6).
- `SuiteResult.warnings` → `SuiteResult.failures` (rename, H-0008
  PR-D6 quality pass). The previous name was misleading because the
  property returned ALL non-passing checks regardless of severity,
  including `"info"`-severity findings that do not flip `.passed`
  to `False`. The list semantics are unchanged. Pre-release rename;
  no users yet depend on `.warnings` since v0.6.0 is not yet
  published.

### Fixed
- `quality_report(df)` and `profile(df)` no longer raise
  `ZeroDivisionError` on a 0-row DataFrame — `_scan_quality` skips
  columns with `n_obs == 0` and returns an empty warnings list
  (H-0008 PR-D6 quality pass; caught by python-reviewer).
- `pycatdap.measures.cramers_v` no longer emits
  `RuntimeWarning: invalid value encountered in divide` on tables
  with an all-zero marginal row or column — switched to
  `np.divide(..., where=...)` for side-effect-free masked division.
  The returned numeric value is unchanged (H-0008 PR-D6 quality pass).

## [0.5.0] — 2026-05-28

このリリースは EDA レイヤの **フラッグシップ API** `pycatdap.profile()` を導入:
H-0007（Phase C）に対応し、`describe` + `association_matrix` + `target_summary` +
`catdap2` を 1 コールに統合、jinja2 + インライン Plotly による
self-contained HTML レポートを生成する。`ydata-profiling` / `skrub.TableReport`
の pycatdap 版に相当。詳細は HISTORY.md H-0007 および以下の節を参照。

### Added

- ワンコール EDA レポート API（H-0007 Phase C、Issue #14）:
  - `pycatdap.profile(df, *, response=None, bins=None, criterion="bic", top_k_subsets=5, quality_thresholds=None) -> ProfileResult`
    — `describe` + `association_matrix` + `target_summary` + `catdap2` を 1 コールに統合
  - `ProfileResult` frozen dataclass — `overview` / `variables` / `association` /
    `top_subsets` / `quality_warnings` / `response` / `n_rows` / `n_cols` を保持。
    `.show / .to_dict / .to_plotly_json / .to_html` を提供
  - `VariableCard` frozen dataclass — 列ごとの type / cardinality / missing /
    top / continuous 統計量 / ΔAIC vs response / AIC binning 境界
  - `QualityWarning` frozen dataclass — 4 種類の警告（`high_cardinality` /
    `constant` / `id_candidate` / `high_missing`、`quality_thresholds=` で上書き可）
  - `ProfileResult.to_html(path=None)` — jinja2 テンプレート（`src/pycatdap/templates/profile.html.j2`）
    で単一の self-contained HTML を生成。Plotly figure は `include_plotlyjs="inline"`
    で同梱（オフライン閲覧可）。`path` 指定時は `_io.atomic_write_text` 経由で原子的書き込み。
    `jinja2` が無い場合は `pycatdap[plotly]` extras を促す `ImportError`
  - チュートリアル `docs/tutorials/08-profile-titanic.ipynb`
    — Titanic データセットで `profile()` の全機能（quality thresholds の上書き、
    `to_html` / `to_dict` / `to_plotly_json` 各シリアライズ）をデモ
  - `BLUEPRINT.md` §3.1 / §5.9 — H-0007 で追加したモジュール（`profile.py` / `templates/`）と
    `ProfileResult` / `VariableCard` / `QualityWarning` の確定 API を反映
  - `README.md` Quickstart — v0.5+ One-call EDA report 節を `pycatdap.profile()` の
    動く例に置き換え（v0.3+ プレースホルダから昇格）

### Fixed

- `pycatdap.profile(df, quality_thresholds={})` が空 dict を `None` 同等に黙って
  落としていた falsy trap を修正（PR #75）。空 dict は「上書き無し」として明示的に
  扱う（`is not None` チェック、`feedback_python_falsy_or_default_trap`）
- `ProfileResult.to_dict()` が `+/-inf` をそのまま emit していたため、`json.dumps`
  の strict モードや JavaScript の `JSON.parse` で reject される RFC 8259 違反だった。
  `_scalar_to_json` ヘルパーで `NaN` と統一して `None` に変換（PR #75）

### Changed

- `ProfileResult.show()` の Jupyter 経路を `IPython.display.HTML` ラッパーを使わない
  形に変更し、`DescribeResult` / `TargetSummary` の慣習と揃えた（local mypy noise が
  5 errors → 3 errors に減少、機能変更なし、PR #75）
- `ProfileResult.to_html(path)` が `_io.atomic_write_text(..., encoding="utf-8")` を
  明示指定（PR #75、コードベース既存 3 call site と整合）

## [0.4.0] — 2026-05-27

このリリースは EDA レイヤを **ペア・全列ペア** まで広げる minor 拡張:
H-0004(`target_summary` / `plot_target`)+ H-0005(連続目的変数 Gaussian 回帰 AIC)
+ H-0006(Phase B 二変量 API: `plot_pair` / `aic_heatmap` / `association_matrix` /
`association_plot`)の 3 つの HISTORY エントリと、それを支える 5 本のチュートリアル
ノートブック(03 / 04 / 05 / 06 / 07)を含む。詳細は HISTORY.md および以下の各節を参照。

### Fixed

- `DescribeResult.to_html(path)` / `TargetSummary.to_html(path)` を atomic write
  化（`pycatdap._io.atomic_write_text` 経由）。同時に読み取るプロセス（mkdocs
  serve の watcher 等）が空ファイルや書き込み途中の状態を観測するリスクを排除

### Added

- Phase B 二変量 API（H-0006、Issue #13）— 段階的に追加:
  - `pycatdap.plot_pair(df, x, y, *, kind="auto", bins=None, backend=...)`
    — 対称ラッパー。dtype に基づき (target, explanatory) を決定し `plot_target` に委譲
    （連続 × カテゴリ → カテゴリが target、連続 × 連続 → `y` が target、両カテゴリ → `y` が target）
  - `pycatdap.association_matrix(df, *, measure="aic", bins=None, criterion="bic")`
    — 全列ペアの ΔAIC 行列を返す（非対称、対角 NaN）。`target_summary` を全 `(i, j)` ペアで
    呼び出し、`M.loc[i, j]` に `target=i, explanatory=j` の `delta_aic` を格納。
    `measure="cramers_v"` / `"mutual_info"` は H-0007 で別途追加予定
  - `pycatdap.aic_heatmap(result, *, threshold=0.0, backend=...)`
    — `Catdap1Result` または `pd.DataFrame` を受け取り、diverging colormap
    （`RdYlGn_r`、中心 0）で ΔAIC ヒートマップを描画。`threshold` 未満のセルに `*` 注釈
  - `pycatdap.association_plot(table, *, threshold=2.0, backend=...)`
    — vcd `assoc(shade=TRUE)` 風 Pearson 標準化残差ヒートマップ。
    `TargetSummary` または `pd.DataFrame`（クロス頻度表）を受け取り、
    diverging colormap（`RdBu_r`、中心 0）で描画。
    `RegressionTargetSummary` は `TypeError`（`plot_target(kind="scatter")` を推奨）
  - チュートリアル `docs/tutorials/07-bivariate-phase-b.ipynb`
    — Phase B の 4 つの API を Titanic データセットで通しデモ
- 目的変数 × 説明変数ペア分析 API（H-0004）:
  - `pycatdap.target_summary(df, target, explanatory, *, bins=None) -> TargetSummary`
    — counts / row_prop / col_prop / expected / pearson_residuals / delta_aic を保持し、
    `.show / .to_html / .to_dict / .to_plotly_json` を提供
  - `pycatdap.plot_target(df, target, explanatory, *, kind="auto", bins=None, backend=...)`
    — dtype 組合せで stacked / mosaic / violin / box / hist を自動選択（matplotlib/plotly 両対応）
  - 連続説明変数は `bins=None` で AIC 最適 binning、`bins=int` で等幅、`bins=list` で明示境界
- 連続目的変数サポート — Gaussian 回帰 AIC 拡張（H-0005、Issue #56）:
  - `pycatdap.RegressionTargetSummary` 新規 dataclass — 連続 target に対する
    per-X-bin `{count, target_mean, target_std}` + `delta_aic` + `r_squared` +
    `n_effective` + `intervals` + `criterion`、`.show / .to_html / .to_dict /
    .to_plotly_json` を提供
  - `target_summary` に `target_bins` / `criterion` パラメータ追加。連続 target
    かつ `target_bins=None` で `RegressionTargetSummary` を返し、`target_bins`
    指定で既存 `TargetSummary`(候補 (c) fallback)を返す
  - `criterion="bic"`(default、Yao 1988 推奨)/ `"aic"` / `"aicc"`(Hurvich-Tsai 系)
  - 欠損値ハンドリング戦略 **M2**: Y のみ dropna; X 欠損は明示的 `_missing_`
    pseudo-bin に集約。同一 Y 上の異なる X 候補で `AIC_null` が一致(R-1)
  - `plot_target` の `kind` に `"scatter"` / `"bin_means"` を追加、連続 target ×
    連続 X で散布図 + bin 平均線、連続 target × カテゴリ X で box / violin を自動選択
  - 参照実装: [`nbx-liz/AdvancedCATDAP`](https://github.com/nbx-liz/AdvancedCATDAP)
    `scoring.py:calc_score_reg_bincount_idx` から移植
  - 連続 target に対する従来の `ValueError` は廃止 — `RegressionTargetSummary`
    を返す挙動に変更
- チュートリアルノートブック 3 本を追加（Issue #27）:
  - `docs/tutorials/03-iris-pooling.ipynb` — iris での AIC 最適 binning
  - `docs/tutorials/04-hellogoodbye-multivariate.ipynb` — 56 binary 変数での `nvar` 利用例
  - `docs/tutorials/05-real-world-eda.ipynb` — seaborn Titanic（欠損あり）での実データ EDA
- `docs/tutorials/06-target-pair-titanic.ipynb` — `target_summary` / `plot_target`
  の全分岐デモ（cat × cat / multi-level / cat × continuous）、AIC 最適 binning
  と等幅 binning の比較、全 explanatory の ΔAIC ランキング、HTML / Plotly export。
  末尾に連続 target サポートの研究 Issue #56 へのリンク
- `pycatdap[tutorial]` extras（seaborn）— Notebook 05 用
- CI で nbmake によるノートブック実行検証（`notebooks` ジョブ）
- `[dependency-groups].notebooks` — Notebook 実行用開発依存（nbmake / seaborn / plotly / matplotlib / ipykernel）

### Changed

- `docs/tutorials/02-eda-titanic.ipynb` — 03/04/05 へのクロスリファレンスを追加、bundled clean 版と seaborn messy 版の関係を明示。さらに `target_summary` を使った single-pair drill-down teaser 節を追加し、06 へリンク
- `docs/tutorials/05-real-world-eda.ipynb` — クリーニング済み Titanic で `target_summary` を `sex` / `age`（連続）に適用する節を追加、AIC 最適 binning の効果を確認
- `docs/tutorials/06-target-pair-titanic.ipynb` — 末尾の「Coming soon: continuous targets」プレースホルダ節を H-0005 の動作デモ（連続 target = `fare`、`RegressionTargetSummary`、`plot_target` の box / scatter、`criterion="aic" / "aicc" / "bic"` 比較、`target_bins` fallback の対比）へ置換。Summary 表に regression-mode の 3 行を追加
- `docs/tutorials/01-basic-catdap.ipynb` — 解説文を英訳。v0.2 由来の日本語ナレーションを CONTRIBUTING.md の English-only ポリシーに揃える（PR #52）
- `BLUEPRINT.md` §3.1 / §5.7 — H-0004 / H-0005 / H-0006 で追加したモジュール（`_target_pair.py` / `_association.py`）と公開 API（4 関数 + 2 ペア API）を反映

## [0.3.0] — 2026-05-26

このリリースで pycatdap は「AIC ベース EDA + ML 誤差分析ライブラリ」として再定位された。詳細は HISTORY.md H-0001 / H-0002 / H-0003 を参照。

### Added

#### 公開 API
- `pycatdap.plot` — 描画バックエンドの選択機能（matplotlib / plotly 両対応）
- `pycatdap.plot.matplotlib.*`, `pycatdap.plot.plotly.*` — バックエンド別実装
- Plotly バックエンドの完全実装: `mosaic_plot`, `barplot_twoway`, `aic_comparison_plot`
- 結果オブジェクトの `.to_plotly_json()` メソッド（`Catdap1Result`, `Catdap2Result`）
- `pycatdap.describe(df) → DescribeResult` — 単変量サマリ
  - `.show()` / `.to_html()` / `.to_dict()` / `.to_plotly_json()` 各メソッド
  - 列分類: continuous / categorical / boolean / datetime / other（pandas 2.x の StringDtype に対応）
- `pycatdap.plot_variable(df, col, kind="auto"|"hist"|"bar", backend=...)` — 単変量プロット
- `pycatdap.plot_missing(df, backend=...)` — 欠損値パターンのバーチャート

#### サンプルデータセット
- `pycatdap.datasets.load_titanic()` — R `datasets::Titanic` 由来（2,201 × 4、全カテゴリカル）
- `pycatdap.datasets.load_iris()` — Fisher's iris（150 × 5、連続 4 列 + 種別）
- `pycatdap.datasets` を `__init__` から直接アクセス可能に

#### 任意依存
- `pycatdap[plotly]` extras（plotly + jinja2）
- `pycatdap[all]` extras（plot + plotly 一括）

#### ドキュメント・計画
- 戦略ドキュメント `HISTORY.md` — H-0001/H-0002/H-0003 accepted
- 全体開発計画 `PLAN.md` — v0.2.x〜v1.0 のロードマップ
- `BLUEPRINT.md` §3.2 — 5 つの Mermaid アーキテクチャ図
- ドキュメントサイト `mkdocs-material` + GitHub Pages
- mkdocstrings による API リファレンス自動生成
- mkdocs-jupyter による notebook 埋め込み
- 新規チュートリアル `02-eda-titanic.ipynb` — Phase A API の総覧
- README リフレッシュ（ポジショニング、比較表、quickstart、ロードマップ）
- CONTRIBUTING.md に R 参照 CSV 生成手順を追加

#### 品質・インフラ
- `tests/test_against_r.py` 2層化: property-based + 厳密数値比較（CSV reference があれば atol=1e-4）
- Makefile に `r-reference` / `test-slow` ターゲット追加
- `.github/workflows/docs.yml` — PR ビルド検証 + main push で Pages 自動デプロイ
- `pyproject.toml` の dependency-group: `docs` を追加

### Changed

- `pycatdap.plotting.*`(v0.2 互換)は `pycatdap.plot.matplotlib.*` への透過的な re-export shim に変更（既存ユーザー影響なし）
- `docs/tutorial.ipynb` を `docs/tutorials/01-basic-catdap.ipynb` に移動

### Migration

破壊的変更なし。`from pycatdap.plotting import mosaic_plot` は v1.0 まで動作し続ける。
新規ユーザーは canonical な `from pycatdap.plot import mosaic_plot`（`backend=...` で切替）を推奨。

## [0.2.0] — 2026-03-22

### Added
- コアAIC計算 (`_aic.py`): `compute_aic_twoway`, `compute_base_aic`, `compute_delta_aic`
- 分割表構築 (`_contingency.py`): `build_crosstab`, `build_multidim_crosstab`
- CATDAP-01 (`catdap1.py`): 全カテゴリカル変数ペアのΔAIC評価
- プーリング (`_pooling.py`): 等間隔・不等間隔の連続変数カテゴリ化
- CATDAP-02 (`catdap2.py`): 最適説明変数部分集合探索
- サンプルデータセット (`datasets.py`): HealthData (52例), HelloGoodbye (13,954例)
- 可視化 (`plotting.py`): `aic_comparison_plot`, `barplot_twoway`, `mosaic_plot`
- チュートリアルノートブック (`docs/tutorial.ipynb`) — 10項目の正当性検証付き
- R比較テスト (`tests/test_against_r.py`)
- Project scaffold with src layout
- CI/CD pipeline (GitHub Actions)
- PyPI trusted publishing via TestPyPI → PyPI
