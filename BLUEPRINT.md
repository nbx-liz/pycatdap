# CATDAP Python実装計画

## 1. 概要

CATDAP（CATegorical Data Analysis Program）は、赤池弘次のAIC（赤池情報量規準）をカテゴリカルデータの分析に適用した手法であり、統計数理研究所の坂元慶行・桂光一により1980年に開発された。現在はRパッケージ（`catdap`）としてのみ公式実装が存在し、Python実装は存在しない。

本計画では、Pythonパッケージ `pycatdap` として以下の2つの主要機能を実装する。

- **CATDAP-01**: 全カテゴリカル変数ペア間の関連度をAICで評価
- **CATDAP-02**: 指定した目的変数に対する最適な説明変数の部分集合探索（連続変数の最適カテゴリ化を含む）

---

## 2. 数理的基礎

### 2.1 AIC統計量（分割表モデル）

目的変数 $E$、説明変数 $F$ に対し、分割表の度数を用いたAICは次式で定義される：

$$
AIC(E; F) = -2 \sum_{i,j} n_{EF}(i,j) \ln \frac{n_{EF}(i,j)}{n_F(j)} + 2(C_E - 1) C_F
$$

ここで：
- $n_{EF}(i,j)$: 目的変数のカテゴリ $i$、説明変数のカテゴリ $j$ のクロス度数
- $n_F(j)$: 説明変数のカテゴリ $j$ の周辺度数
- $C_E$: 目的変数のカテゴリ数
- $C_F$: 説明変数のカテゴリ数

### 2.2 ベースAIC（説明変数なしモデル）

$$
AIC(E; \phi) = -2 \sum_i n_E(i) \ln \frac{n_E(i)}{n} + 2(C_E - 1)
$$

### 2.3 出力AIC値

R版CATDAPに倣い、出力されるAIC値は差分形式とする：

$$
\Delta AIC = AIC(E; F) - AIC(E; \phi)
$$

- $\Delta AIC < 0$ → 説明変数 $F$ は目的変数の説明に有効
- $\Delta AIC \geq 0$ → 説明変数 $F$ は無用

ベースAICも別途出力し、ユーザーが絶対AICを復元できるようにする。

---

## 3. パッケージ構成

```
pycatdap/
├── __init__.py          # 公開API
├── catdap1.py           # CATDAP-01 実装
├── catdap2.py           # CATDAP-02 実装
├── _aic.py              # AIC計算コア（共通モジュール）
├── _pooling.py          # 連続変数のカテゴリ化（プーリング）
├── _subset_search.py    # 最適部分集合探索
├── _contingency.py      # 分割表構築ユーティリティ
├── plotting.py          # 可視化（モザイクプロット・帯グラフ等）
└── datasets.py          # サンプルデータセット
tests/
├── test_catdap1.py
├── test_catdap2.py
├── test_aic.py
├── test_pooling.py
└── test_against_r.py    # R版との結果比較テスト
```

---

## 4. 依存ライブラリ

| ライブラリ | 用途 | 必須/任意 |
|-----------|------|----------|
| numpy | 数値計算・配列操作 | 必須 |
| pandas | DataFrame入出力 | 必須 |
| scipy | 組み合わせ列挙 (`itertools` で代替可) | 任意 |
| matplotlib | モザイクプロット・帯グラフ | 任意 |
| statsmodels | モザイクプロット（`graphics.mosaicplot`） | 任意 |

---

## 5. モジュール別詳細設計

### 5.1 `_aic.py` — AIC計算コア

```python
def compute_aic_twoway(
    cross_freq: np.ndarray,   # shape (C_E, C_F)
    marginal_f: np.ndarray,   # shape (C_F,)
) -> float:
    """
    AIC(E; F) を計算する。
    ゼロ度数セルは 0*ln(0) = 0 として扱う。
    """

def compute_base_aic(
    marginal_e: np.ndarray,   # shape (C_E,)
    n: int,                   # 総度数
) -> float:
    """AIC(E; φ) を計算する。"""

def compute_delta_aic(
    cross_freq: np.ndarray,
    marginal_e: np.ndarray,
    marginal_f: np.ndarray,
    n: int,
) -> float:
    """ΔAIC = AIC(E;F) - AIC(E;φ) を計算する。"""
```

**実装上の注意点：**
- `n_EF(i,j) = 0` の場合、`0 * ln(0) = 0` として処理（`np.where` or `xlogy`）
- `scipy.special.xlogy` があれば利用、なければ自前実装
- 数値安定性のためlog計算にはガード条件を入れる

### 5.2 `_contingency.py` — 分割表構築

```python
def build_crosstab(
    data: pd.DataFrame,
    response: str,
    explanatory: str | list[str],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, int]:
    """
    DataFrameから分割表を構築する。
    
    Returns:
        cross_freq: クロス度数表
        marginal_e: 目的変数の周辺度数
        marginal_f: 説明変数の周辺度数
        n: 総度数
    """

def build_multidim_crosstab(
    data: pd.DataFrame,
    response: str,
    explanatory_set: list[str],
) -> tuple[np.ndarray, ...]:
    """多次元分割表を構築する（CATDAP-02用）。"""
```

### 5.3 `_pooling.py` — 連続変数のカテゴリ化

CATDAP-02の重要な機能。連続変数を離散化する2つの方式を実装する。

```python
def equal_pooling(
    values: np.ndarray,
    accuracy: float,
) -> np.ndarray:
    """
    等間隔プーリング（pool=0）。
    accuracy（観測精度）で指定した最小幅で等間隔に分割後、
    トップダウンで隣接区間をAICに基づき統合する。
    """

def unequal_pooling(
    values: np.ndarray,
    accuracy: float,
) -> np.ndarray:
    """
    不等間隔プーリング（pool=1、デフォルト）。
    accuracyで指定した最小幅の区間に分割後、
    ボトムアップで隣接区間をAICに基づき統合する。
    """

def optimal_binning(
    values: np.ndarray,
    response: np.ndarray,
    method: str = 'bottom_up',  # 'top_down' or 'bottom_up'
    accuracy: float = None,
) -> tuple[np.ndarray, list[float]]:
    """
    AIC最小化による最適カテゴリ化のメインルーチン。
    
    Returns:
        categorized: カテゴリ化された値
        boundaries: 区間境界値のリスト
    """
```

**アルゴリズム概要（ボトムアップ法）：**
1. 連続値を `accuracy` の幅で細かい区間に分割
2. 各隣接区間ペアについて、統合した場合のAIC変化量を計算
3. AICが最も減少するペアを統合
4. AICが減少しなくなるまで繰り返す

### 5.4 `_subset_search.py` — 最適部分集合探索

```python
def search_best_subset(
    data: pd.DataFrame,
    response: str,
    explanatory_candidates: list[str],
    max_vars: int = None,
) -> list[SubsetResult]:
    """
    説明変数の最適部分集合を探索する。
    
    手順：
    1. 各単一説明変数のAICを計算しランキング
    2. 上位変数からステップワイズに変数追加
    3. 各ステップで最小AICの組み合わせを記録
    
    Returns:
        AIC昇順にソートされた部分集合のリスト
    """

@dataclass
class SubsetResult:
    variables: list[str]    # 説明変数名
    n_vars: int             # 変数数
    n_categories: int       # 総カテゴリ数
    aic: float              # ΔAIC値
```

**探索アルゴリズム：**
- 単一変数 → 2変数 → ... → k変数と逐次的に探索
- 各段階で、前段階の上位変数を保持しつつ1変数追加
- 計算量を抑えるため `nvar` パラメータで探索対象変数数を制限可能
- R版と同様に、pa1/pa2/pa3 に相当するメモリ制御パラメータを提供

### 5.5 `catdap1.py` — CATDAP-01

```python
def catdap1(
    data: pd.DataFrame,
    response_names: list[str] | None = None,
) -> Catdap1Result:
    """
    全カテゴリカル変数ペア間の関連度をAICで評価する。
    
    Parameters:
        data: カテゴリカル変数のみからなるDataFrame
        response_names: 目的変数名リスト（Noneなら全変数を順に目的変数とする）
    
    Returns:
        Catdap1Result（二元表、AIC値、AIC順位を含む）
    """

@dataclass
class Catdap1Result:
    tway_tables: dict        # 各ペアの二元表
    aic: pd.DataFrame        # 各目的変数に対する説明変数のAIC
    aic_order: dict          # AIC昇順の説明変数リスト
    total: pd.Series         # 各変数の度数とコード
```

### 5.6 `catdap2.py` — CATDAP-02

```python
def catdap2(
    data: pd.DataFrame,
    pool: list[int] | None = None,
    response_name: str = None,
    accuracy: list[float] | None = None,
    nvar: int | None = None,
    additional_output: list[list[str]] | None = None,
) -> Catdap2Result:
    """
    目的変数に対する最適説明変数部分集合を探索する。
    
    Parameters:
        data: DataFrame（カテゴリカル・連続変数混在可）
        pool: 各変数のプーリング方式
              -m: m区間ヒストグラム（目的変数のみ）
               0: 等間隔プーリング（トップダウン）
               1: 不等間隔プーリング（ボトムアップ、デフォルト）
               2: プーリングなし（離散変数）
        response_name: 目的変数名
        accuracy: 各変数の離散化の最小幅
        nvar: 多次元分析に保持する変数数
        additional_output: 追加出力する変数組のリスト
    
    Returns:
        Catdap2Result
    """

@dataclass
class Catdap2Result:
    tway_tables: dict                  # 二元表
    intervals: dict                    # 連続変数の区間境界
    base_aic: float                    # ベースAIC
    aic: pd.DataFrame                  # 単一説明変数のAIC
    aic_order: list                    # AIC昇順の変数リスト
    subsets: list[SubsetResult]        # 部分集合のAICリスト
    contingency_tables: dict | None    # 最良・追加部分集合の分割表
```

### 5.7 `plotting.py` — 可視化

```python
def mosaic_plot(result, ax=None, **kwargs):
    """CATDAP結果のモザイクプロット。"""

def barplot_twoway(result, response, explanatory, ax=None, **kwargs):
    """二元表の帯グラフ（積み上げ棒グラフ）。"""

def aic_comparison_plot(result, ax=None, **kwargs):
    """説明変数のAIC比較棒グラフ。"""
```

---

## 6. 公開API設計

```python
import pycatdap

# CATDAP-01: カテゴリカル変数ペアの関連度分析
result1 = pycatdap.catdap1(data, response_names=["Survived"])
print(result1.aic)
print(result1.aic_order)

# CATDAP-02: 最適説明変数部分集合の探索
result2 = pycatdap.catdap2(
    data,
    pool=[2, 2, 2, 0, 0, 0, 0, 2],
    response_name="symptoms",
    accuracy=[0., 0., 0., 1., 1., 1., 0.1, 0.],
)
print(result2.base_aic)
print(result2.aic)
print(result2.subsets)

# 可視化
pycatdap.plot.mosaic(result2)
pycatdap.plot.barplot_twoway(result2, "symptoms", ["age", "ecg"])
pycatdap.plot.aic_comparison(result2)
```

---

## 7. 実装フェーズ計画

### Phase 1: コアAIC計算（推定工数：2日）

- `_aic.py`: AIC計算関数群
- `_contingency.py`: 分割表構築
- 単体テスト（手計算との照合）

### Phase 2: CATDAP-01（推定工数：2日）

- `catdap1.py`: 全変数ペアのAIC計算
- 出力フォーマット整備
- R版の `catdap1()` 結果との照合テスト

### Phase 3: プーリング機能（推定工数：3日）

- `_pooling.py`: 等間隔・不等間隔プーリング
- AIC最小化による最適区間統合
- 連続変数のカテゴリ化テスト

### Phase 4: CATDAP-02（推定工数：4日）

- `_subset_search.py`: 部分集合探索アルゴリズム
- `catdap2.py`: メイン関数統合
- 多次元分割表の構築と評価
- R版 `catdap2()` の HealthData, iris 等での結果照合

### Phase 5: 可視化・パッケージ化（推定工数：2日）

- `plotting.py`: モザイクプロット・帯グラフ・AIC比較
- `datasets.py`: サンプルデータ同梱
- PyPI公開用のパッケージ設定（pyproject.toml）

### Phase 6: テスト・ドキュメント（推定工数：2日）

- `test_against_r.py`: R版出力との体系的比較
- APIドキュメント（docstring + Sphinx）
- チュートリアルnotebook

**合計推定工数: 約15日**

---

## 8. 品質保証：R版との照合テスト戦略

R版CATDAPパッケージとの数値的一致を検証するため、以下のテストデータで結果を比較する。

| テストデータ | 検証内容 |
|-------------|---------|
| HealthData (catdap同梱) | catdap2のAIC値・最適部分集合 |
| JNcharacter (catdap同梱) | catdap1のペアワイズAIC |
| Titanic (R同梱) | catdap1/catdap1cの結果 |
| iris (R同梱) | 連続目的変数のプーリング結果 |
| HelloGoodbye (catdap同梱) | 多変数時の部分集合探索 |

照合手順：
1. R側で各テストデータに対しcatdap1/catdap2を実行し、結果をCSVに書き出す
2. Python側で同一データに対し実行し、数値差分を検証
3. 許容誤差: AIC値は小数第4位まで一致（浮動小数点丸め差を許容）

---

## 9. 技術的注意事項

### 9.1 ゼロ度数セルの処理
分割表内にゼロ度数のセルがある場合、$0 \times \ln 0 = 0$ として処理する。
`scipy.special.xlogy(x, y)` は $x=0$ のとき自動的に0を返すため安全に使用可能。

### 9.2 計算量の制御
- CATDAP-02の部分集合探索は変数数に対し組み合わせ爆発を起こすため、`nvar` パラメータで探索対象を制限する
- R版と同様の逐次的探索戦略（ステップワイズ）を採用し、全探索は避ける

### 9.3 欠測値の扱い
- R版の `missingmark` 方式に対応する機能を実装
- 加えて、pandas標準の `NaN` による欠測値ハンドリングも提供

### 9.4 大規模データへの対応
- numpy配列操作を中心に実装し、Pythonループを最小化
- 分割表構築には `pd.crosstab` を活用
- 必要に応じて、プーリングの内部ループをnumbaで高速化する余地を残す