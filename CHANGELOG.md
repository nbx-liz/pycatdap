# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- 戦略ドキュメント `HISTORY.md` — 仕様変更提案・決定の履歴（H-0001/H-0002/H-0003 accepted）
- 全体開発計画 `PLAN.md` — v0.2.x〜v1.0 のロードマップとテーマ別 Issue マップ
- `BLUEPRINT.md` §3.2 — 5 つの Mermaid アーキテクチャ図（モジュール依存・EDA データフロー・ML 誤差分析データフロー・レイヤと拡張ポイント・統合境界）
- ドキュメントサイト `mkdocs-material` + GitHub Pages 構築（Diátaxis 構成: getting-started / tutorials / how-to / reference / explanation / project）
- `mkdocstrings` による API リファレンス自動生成
- `mkdocs-jupyter` による tutorial notebook の埋め込み
- `.github/workflows/docs.yml` — PR でのビルド検証 + main push で GitHub Pages 自動デプロイ
- `pyproject.toml` に `docs` dependency-group を追加

### Changed

- `docs/tutorial.ipynb` を `docs/tutorials/01-basic-catdap.ipynb` に移動
- `BLUEPRINT.md` 冒頭に関連ドキュメント（HISTORY/PLAN/CHANGELOG）へのクロスリンクを追加

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
