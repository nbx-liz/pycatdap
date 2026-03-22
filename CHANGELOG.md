# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

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
