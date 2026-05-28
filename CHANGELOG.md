# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- ワンコール EDA レポート API（H-0007 Phase C、Issue #14）— 段階的に追加:
  - `pycatdap.profile(df, *, response=None, bins=None, criterion="bic", top_k_subsets=5, quality_thresholds=None) -> ProfileResult`
    — `describe` + `association_matrix` + `target_summary` + `catdap2` を 1 コールに統合
  - `ProfileResult` frozen dataclass — `overview` / `variables` / `association` /
    `top_subsets` / `quality_warnings` / `response` / `n_rows` / `n_cols` を保持。
    `.show / .to_dict / .to_plotly_json` を提供（`.to_html` は H-0007 PR-C2 で追加予定）
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
