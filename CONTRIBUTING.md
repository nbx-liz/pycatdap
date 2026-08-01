# Contributing / 開発ガイド

## 開発環境セットアップ

```bash
git clone git@github.com:nbx-liz/pycatdap.git
cd pycatdap
uv sync --frozen --dev
uv run pre-commit install
uv run bash .githooks/install.sh --preserve-pre-commit
```

## Git ブランチ戦略

- **main**: リリース済みの安定版
- **develop**: 開発統合ブランチ
- Feature ブランチは `develop` から作成: `feat/`, `fix/`, `docs/`, `refactor/`
- PRは `develop` へ squash merge
- リリース時に `develop` → `main` へPR（タイトル: `release: vX.Y.Z`）

```bash
git checkout develop
git checkout -b feat/<feature-name>
```

## 開発フロー

### 1. TDD で実装

1. `tests/test_<module>.py` にテストを書く（RED）
2. テストが失敗することを確認
3. 最小限のコードで実装（GREEN）
4. テストが通ることを確認
5. リファクタリング（IMPROVE）
6. カバレッジ 80%+ を確認

### 2. 品質チェック

```bash
make ci    # lint, format-check, typecheck, test を一括実行
```

| チェック | コマンド | 基準 |
|---------|---------|------|
| Lint | `uv run ruff check .` | エラーなし（`D` で public 関数の docstring 欠落も検出） |
| Format | `uv run ruff format --check .` | 差分なし |
| Type | `uv run mypy src/pycatdap/` | strict, エラーなし（型注釈欠落を検出） |
| Test | `uv run pytest --cov-fail-under=80` | カバレッジ 80%+ |

`pre-commit install` 済みなら、上記の `ruff`（lint + format）と `mypy --strict`
は push 前のフックで自動実行される。docstring 規約は NumPy convention
（`[tool.ruff.lint.pydocstyle]`）に従う。

### 3. コミット

Conventional Commits 形式:

```
<type>(<scope>): <description>

Types: feat, fix, refactor, docs, test, chore, perf, ci
```

### 4. PR

- `develop` ブランチへ squash merge
- PR テンプレートのチェックリストを完了させる

## コーディング規約

- すべてのファイルに `from __future__ import annotations` を記述
- 公開関数には NumPy スタイルの docstring を記述
- 入力データ（DataFrame, ndarray）は変更しない（イミュータブル）
- ゼロ度数セルは `0 * ln(0) = 0` として扱う
- `scipy` はオプショナル依存 — import できない場合のフォールバックを用意

## 言語規約

- **日本語**: BLUEPRINT.md, CHANGELOG.md, CONTRIBUTING.md
- **英語**: コード, docstring, コミットメッセージ, PR, Issue

## ドキュメント優先順位

1. BLUEPRINT.md（仕様・設計）
2. CHANGELOG.md（変更履歴）
3. CONTRIBUTING.md（開発フロー）
4. ソースコード

## R版との照合 (R version cross-check)

`tests/test_against_r.py` で R版 `catdap` パッケージとの数値一致を検証する。

- 許容誤差: AIC値は小数第4位まで一致（`atol=1e-4`）
- 対象データセット: HealthData（R catdap 由来・GPL のため `tests/fixtures/health_data.csv` に非同梱 fixture として配置、wheel/sdist には含めない — H-0025 / [#156](https://github.com/nbx-liz/pycatdap/issues/156)）。HelloGoodbye / JNcharacter は同梱しない（GPL のため、H-0025 / H-0020 / [#47](https://github.com/nbx-liz/pycatdap/issues/47)）
- 2層構成:
  - **Property-based tests** — R 参照 CSV がなくても実行可能(符号・順位など定性的検証)
  - **Strict numerical tests** — R 参照 CSV (`docs/r_reference/*.csv`) が必要、`atol=1e-4` で厳密照合

> **照合スコープ（重要）**: pycatdap の AIC エンジンは R catdap 1.3.5 と**任意の固定分割でビット一致**する。一方、連続変数の **binning 選択**（`pool=0`）は設計が異なる（pycatdap は細ビンからの AIC 貪欲マージ＝より AIC 最適、R は range 中点からの粗い split ヒューリスティック）。そのため strict 照合は (1) catdap1 のカテゴリ列、(2) catdap2 のカテゴリ（`pool=2`）単変数、(3) **連続変数を R の選んだカット点でビン化した場合の AIC 等価**、を検証する。連続変数の binning 選択そのものは意図的に照合対象外（[#10](https://github.com/nbx-liz/pycatdap/issues/10)）。

### R 参照 CSV の生成手順

参照 CSV は git にコミットされている前提だが、再生成手順は以下:

```bash
# 1. R と catdap パッケージをインストール
sudo apt install r-base                  # Ubuntu/Debian
# or: brew install r                     # macOS

R -e 'install.packages("catdap", repos="https://cloud.r-project.org")'

# 2. 参照 CSV を生成
make r-reference
# or directly:
Rscript docs/r_reference/generate_reference.R

# 3. 生成された CSV を commit
git add docs/r_reference/*.csv
```

生成される CSV:

| ファイル | 内容 |
|---|---|
| `health_catdap1.csv` | HealthData のカテゴリ列に対する catdap1 ΔAIC(response=symptoms) |
| `health_catdap2_aic.csv` | HealthData の catdap2 単一変数 AIC（カテゴリ `pool=2` 変数のみ） |
| `health_catdap2_fixed_partition.csv` | HealthData の連続変数について R が選んだカット点と ΔAIC（固定分割での engine 等価検証用） |

`make r-reference` ターゲットは R と catdap パッケージのインストール状態を確認したうえで生成スクリプトを実行する。R が未インストールの場合は明示的なエラーメッセージを表示する。

### CI 統合

- **Develop CI**: `pytest -m "not slow"` で slow テストを除外(高速フィードバック)
- **Release CI**: `pytest -m slow` を実行し、Strict numerical テストもすべてパスすることを必須とする([#30](https://github.com/nbx-liz/pycatdap/issues/30))

## リリース手順

1. `CHANGELOG.md` に `## [X.Y.Z]` セクションを追加
2. `develop` にコミット & push
3. `python scripts/release.py X.Y.Z` を実行
4. 作成されたPRをレビュー & squash merge
5. auto-release.yml がタグ作成 → release.yml が PyPI に公開

## 実装フェーズ

| Phase | 内容 | モジュール |
|-------|------|-----------|
| 1 | コアAIC計算 | `_aic.py`, `_contingency.py` |
| 2 | CATDAP-01 | `catdap1.py` |
| 3 | プーリング | `_pooling.py` |
| 4 | CATDAP-02 | `_subset_search.py`, `catdap2.py` |
| 5 | 可視化・パッケージ化 | `plotting.py`, `datasets.py` |
| 6 | テスト・ドキュメント | `test_against_r.py`, docs |
