# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- チュートリアルノートブック 3 本を追加（Issue #27）:
  - `docs/tutorials/03-iris-pooling.ipynb` — iris での AIC 最適 binning
  - `docs/tutorials/04-hellogoodbye-multivariate.ipynb` — 56 binary 変数での `nvar` 利用例
  - `docs/tutorials/05-real-world-eda.ipynb` — seaborn Titanic（欠損あり）での実データ EDA
- `pycatdap[tutorial]` extras（seaborn）— Notebook 05 用
- CI で nbmake によるノートブック実行検証（`notebooks` ジョブ）
- `[dependency-groups].notebooks` — Notebook 実行用開発依存（nbmake / seaborn / plotly / matplotlib / ipykernel）

### Changed

- `docs/tutorials/02-eda-titanic.ipynb` — 03/04/05 へのクロスリファレンスを追加、bundled clean 版と seaborn messy 版の関係を明示

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
