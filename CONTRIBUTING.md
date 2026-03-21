# Contributing / 開発ガイド

## 開発環境セットアップ

```bash
git clone git@github.com:nbx-liz/pycatdap.git
cd pycatdap
uv venv && source .venv/bin/activate
uv pip install -e ".[all]"
```

## 開発フロー

### 1. ブランチ作成

```bash
git checkout -b feat/<feature-name>
```

### 2. TDD で実装

1. `tests/test_<module>.py` にテストを書く（RED）
2. テストが失敗することを確認: `.venv/bin/pytest tests/test_<module>.py`
3. 最小限のコードで実装（GREEN）
4. テストが通ることを確認
5. リファクタリング（IMPROVE）

### 3. 品質チェック

```bash
# lint + format
.venv/bin/ruff check src/ tests/
.venv/bin/ruff format src/ tests/

# 型チェック
.venv/bin/mypy src/

# テスト + カバレッジ
.venv/bin/pytest
```

### 4. コミット

```
<type>: <description>

例:
feat: implement AIC computation for two-way tables
fix: handle zero-frequency cells in cross tabulation
test: add R comparison tests for catdap1
refactor: extract common validation to _contingency
docs: update BLUEPRINT with pooling algorithm details
```

## コーディング規約

- すべてのファイルに `from __future__ import annotations` を記述
- 公開関数には NumPy スタイルの docstring を記述
- 入力データ（DataFrame, ndarray）は変更しない（イミュータブル）
- ゼロ度数セルは `0 * ln(0) = 0` として扱う
- `scipy` はオプショナル依存 — importできない場合のフォールバックを用意

## R版との照合

`tests/test_against_r.py` でR版catdapパッケージとの数値一致を検証する。

- 許容誤差: AIC値は小数第4位まで一致（`atol=1e-4`）
- テストデータ: HealthData, JNcharacter, Titanic, iris, HelloGoodbye

## 実装フェーズ

| Phase | 内容 | モジュール |
|-------|------|-----------|
| 1 | コアAIC計算 | `_aic.py`, `_contingency.py` |
| 2 | CATDAP-01 | `catdap1.py` |
| 3 | プーリング | `_pooling.py` |
| 4 | CATDAP-02 | `_subset_search.py`, `catdap2.py` |
| 5 | 可視化・パッケージ化 | `plotting.py`, `datasets.py` |
| 6 | テスト・ドキュメント | `test_against_r.py`, docs |
