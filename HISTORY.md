# pycatdap 仕様変更履歴

> このファイルは仕様変更の Proposal / Decision / Migration を記録する。
> 詳細フォーマットは `.claude/skills/history-proposals/SKILL.md` を参照。
>
> 関連ドキュメント:
> - [BLUEPRINT.md](BLUEPRINT.md) — 仕様・モジュール構成
> - [PLAN.md](PLAN.md) — 全体開発計画・リリース計画・Issue マップ
> - [CHANGELOG.md](CHANGELOG.md) — リリース履歴

---

## 2026-05-26: pycatdap を EDA + ML 誤差分析ライブラリとして再定位

- ID: `H-0001`
- Status: `accepted`
- Scope: `API | scope | dependencies`
- Related: `BLUEPRINT.md §3 (パッケージ構成), §4 (依存ライブラリ), §5.7 (plotting)`

### Context

現状の `pycatdap` は CATDAP-01 / CATDAP-02 を Python に移植した「論文の手法そのもの」であり、可視化は `mosaic_plot` / `barplot_twoway` / `aic_comparison_plot` の3関数(matplotlib)のみ。

しかし実利用上の主要ユースケースは以下2つであり、現状の API ではカバー不足:

1. **EDA(探索的データ解析)** — `ydata-profiling` / `Sweetviz` / `DataPrep.eda` / R `DataExplorer` / R `vcd` 相当の「1コールでデータ属性を理解できる」体験
2. **ML 予測モデルの誤差分析** — `Microsoft Responsible AI / Error Analysis Tool` / `Manifold (Uber)` / `What-If Tool` / `Fairlearn` / `Evidently AI` 相当の「誤差を categorical target とみなし、AIC で説明変数を発見する」体験

これらのグローバルツールに対する **pycatdap の独自価値** は次の3点:

- AIC ベースの変数関連度ランキング(Cramér's V / mutual info とは異なる「情報量と複雑さのトレードオフ」)
- 連続変数の **AIC 最適 binning**(他ツールは等幅/分位等分のみ)
- **サブセット最適探索(CATDAP-02)** = feature importance とは異なる「変数組合せの探索」≒ Error Analysis Tree の AIC 版

加えて、`LizyStudio` への統合(`react-plotly.js` フロントエンド + FastAPI バックエンド)が想定されており、Plotly Figure を返却できる API 設計が必要。

### Proposal

#### 用途の明示化

`pycatdap` を以下2用途に対応するライブラリとして再定位する:

1. **AIC ベース EDA**: 任意 DataFrame の属性把握、変数関連度の AIC ランキング、HTML レポート
2. **ML 誤差分析**: 予測結果 `(y_true, y_pred)` を入力とし、誤差を説明する変数・サブセットを AIC で発見

#### 描画バックエンドの追加

- `pycatdap.plot.matplotlib.*`(既存・後方互換、デフォルト)
- `pycatdap.plot.plotly.*`(新規・任意依存 `pycatdap[plotly]`)
- 全 plot 関数は `backend="matplotlib" | "plotly"` で切替可能
- `Catdap1Result` / `Catdap2Result` に `.to_plotly_json()` メソッドを追加(LizyStudio 等の Web フロントが直接消費可)

#### EDA API(Phase A〜D)

**Phase A: 単変量 API**
```python
pycatdap.describe(df)              # skim 風サマリ表(型推定/欠損/カーディナリティ/統計量)
pycatdap.plot_variable(df, col)    # 単変量プロット(型自動判定で hist or bar)
pycatdap.plot_missing(df)          # 欠損パターン
```

**Phase B: 二変量 API**
```python
pycatdap.plot_pair(df, x, y)              # 自動的にモザイク or 箱ひげ or 散布図
pycatdap.aic_heatmap(catdap1_result)      # m×m ΔAIC ヒートマップ
pycatdap.association_matrix(df)           # 全変数の関連度行列(ΔAIC / Cramér's V 選択可)
pycatdap.association_plot(table)          # vcd 風の標準化残差プロット
```

**Phase C: 1コール profile()**
```python
profile = pycatdap.profile(df, response="symptoms")
profile.to_html("report.html")
profile.show()        # Jupyter inline
```
含まれる要素:
- Overview セクション(行数 / 列数 / 欠損率 / 重複行 / メモリ)
- Variable cards(各列 1 カード、ΔAIC vs response を上位指標)
- ΔAIC ヒートマップ(全変数ペア)
- Top-K サブセット(CATDAP-02 結果)
- 連続変数の AIC 最適 binning 可視化
- データ品質警告(高カーディナリティ、定数列、ID 候補列)

**Phase D: target-driven + データ品質**
```python
pycatdap.target_analysis(df, response="symptoms")
# 全変数を ΔAIC 降順ソート、上位 K に対して:
#   - クロス表 / モザイク / 標準化残差 / pooling

pycatdap.quality_report(df)
# 欠損率 / 高カーディナリティ警告 / 定数列 / 重複行 / 推定 ID 列
```

#### ML 誤差分析 API(Phase G〜L)

**Phase G: 誤差ラベリングユーティリティ**
```python
pycatdap.error.error_label(y_true, y_pred)         # "correct" / "incorrect"
pycatdap.error.confusion_label(y_true, y_pred)     # "TP" / "FP" / "FN" / "TN"
pycatdap.error.residual_label(y_true, y_pred,
                              method="aic_pool")    # 回帰残差を AIC binning
pycatdap.error.abs_residual_pool(y_true, y_pred)   # |residual| の AIC binning
```

**Phase H: 1コール誤差分析**
```python
pycatdap.error_analysis(df, y_true, y_pred, task="classification")
# 内部処理:
#   1. error_label で誤差を categorical 化
#   2. CATDAP-01 で誤差を説明する変数をランキング
#   3. CATDAP-02 で worst-performing cohort を発見
#   4. 結果を ErrorAnalysisResult として返す(.show() / .to_html() 対応)
```

**Phase I: 分類誤差可視化**
```python
pycatdap.error.plot_confusion(y_true, y_pred)                     # confusion matrix heatmap
pycatdap.error.plot_confusion_by_slice(df, y_true, y_pred, var)   # スライス別 confusion
pycatdap.error.confusion_aic(y_true, y_pred)                      # 予測が情報量を持つか
```

**Phase J: 回帰誤差可視化**
```python
pycatdap.error.residual_plot(y_true, y_pred, color_by=None)
pycatdap.error.residual_by_category(df, y_true, y_pred, var)      # カテゴリ別箱ひげ
pycatdap.error.residual_pool_plot(y_true, y_pred)                 # 残差の AIC binning
```

**Phase K: キャリブレーション**
```python
pycatdap.error.calibration_curve(y_true, y_proba, n_bins="aic")
# 等幅 binning ではなく AIC 最適 binning でキャリブレーション診断
pycatdap.error.brier_score(y_true, y_proba)
pycatdap.error.expected_calibration_error(y_true, y_proba)
```

**Phase L: スライス発見・コホート比較・ドリフト**
```python
pycatdap.error.discover_error_slices(df, y_true, y_pred, max_vars=3)
# CATDAP-02 ベースの自動スライス発見(Microsoft Error Analysis Tree の AIC 版)

pycatdap.error.compare_cohorts(df_a, df_b, response=None)
# Sweetviz 風の比較(train vs test, segment A vs B)

pycatdap.error.detect_drift(df_train, df_prod, y_true, y_pred)
# 概念ドリフトを ΔAIC の変化で検出
```

#### LizyStudio 統合

- `pycatdap[plotly]` extras を LizyStudio が依存追加
- LizyStudio に **"Error Analysis" タブ** を新設
  - データセット + 予測結果アップロード → `pycatdap.error_analysis()` 実行 → 結果表示
  - 各 Plotly Figure を `react-plotly.js` で render
- **"EDA" タブ** を新設
  - データセットアップロード → `pycatdap.profile()` 実行 → HTML/Plotly で表示
- pooling 微調整は anywidget で実装(`accuracy` slider で再計算)

### Impact

- 公開 API の **追加のみ**(既存の `catdap1` / `catdap2` / `plotting.*` 3 関数は変更なし)
- 任意依存ライブラリの追加: `plotly`, `anywidget`, `jinja2`(HTML レポート), `missingno`(欠損パターン参考実装)
- `BLUEPRINT.md` の §3 / §4 / §5.7 を改訂(`error/` サブモジュールと `profile.py` / `quality.py` の追加)
- `README.md` のユースケース節を「CATDAP 実装」から「AIC ベース EDA + ML 誤差分析」に拡張

### Compatibility

- **後方互換性**: 既存 API は維持。`plotting.mosaic_plot` / `barplot_twoway` / `aic_comparison_plot` は matplotlib backend のまま動作
- **新規ユーザー**: `pycatdap.plot.plotly.*` または `result.to_plotly_json()` で Plotly 経路を利用可能
- **破壊的変更**: なし。ただし将来 v1.0 で `plotting.*` を `pycatdap.plot.matplotlib.*` にエイリアス整理する余地あり(別 Proposal にて議論)

### Alternatives Considered

#### A1: LizyStudio 側で React コンポーネントを自前実装、pycatdap は数値のみ返す
- 不採用理由: mosaic / association plot のロジックを React 側で再発明する負担が大きい。Notebook ユーザーが恩恵を受けない

#### A2: 可視化を別パッケージ `pycatdap-viz` に分離
- 不採用理由: ユースケースが「EDA + 誤差分析」と一体であり、`pycatdap` 単体でストーリーが完結する方が UX が良い。任意依存(`extras`)で十分

#### A3: 既存の `ydata-profiling` を fork する
- 不採用理由: pycatdap の独自価値(AIC ベース変数評価、AIC binning、CATDAP-02 サブセット探索)を組み込むには大幅改造が必要。一からの方が見通しが良い

#### A4: ML 誤差分析を完全に LizyML 側で実装
- 不採用理由: 誤差分析は CATDAP の自然な応用であり、`pycatdap` に置くと「予測モデル非依存」(任意の y_true, y_pred で動く)という利点が出る。LizyML 固有の機能にすると汎用性を失う

### Acceptance Criteria

#### 全体
- [ ] `BLUEPRINT.md` の §3 / §4 / §5.7 が改訂され、新規モジュール構成が記載される
- [ ] `README.md` のユースケース節が「EDA + ML 誤差分析」を含む
- [ ] 既存 API(`catdap1` / `catdap2` / `plotting.*`)の回帰テストが全て pass

#### Phase A〜L
- [ ] 各 Phase が独立した H-XXXX エントリとして起票され、それぞれに Acceptance Criteria を持つ
- [ ] 各 API に Plotly backend / matplotlib backend の両方に対するテストが存在
- [ ] HTML レポート(`profile.to_html`)はブラウザで開ける単一ファイルとして出力される
- [ ] `error_analysis()` は分類・回帰の両タスクで動作する(`task` パラメータで切替)

#### LizyStudio 統合
- [ ] LizyStudio 側に対応する Issue が立ち、pycatdap への依存が `pyproject.toml` に追加される
- [ ] LizyStudio の「EDA」「Error Analysis」タブが、サンプルデータで end-to-end に動作

#### 数値検証
- [ ] AIC 計算結果が既存テストと一致(`atol=1e-4`)
- [ ] 誤差分析の slice 発見が、手動で算出したスライス別 metric と一致

### Decision

- Date: `2026-05-26`
- Result: `accepted`
- Notes: プロジェクトオーナー承認。ML 誤差分析方面の詳細要件・競合分析・設計原則は H-0002 で確定する

### Migration

破壊的変更なしのため移行ガイドは不要。ただし以下を README / CHANGELOG に明記する:

- v0.3.0 以降: `pip install pycatdap[plotly]` で Plotly backend が利用可能
- v0.4.0 以降: `pycatdap.profile()` / `pycatdap.error_analysis()` 等の高レベル API を追加
- 既存ユーザー: 何もしなくても従来通り動作

### 実装ロードマップ(参考)

| Phase | バージョン | 内容 |
|---|---|---|
| A | v0.3.0 | Plotly backend + 単変量 API(`describe`, `plot_variable`, `plot_missing`) |
| B | v0.4.0 | 二変量 API(`plot_pair`, `aic_heatmap`, `association_matrix`, `association_plot`) |
| C | v0.5.0 | `profile()` + HTML レポート生成 |
| D | v0.6.0 | `target_analysis()` + `quality_report()` |
| G | v0.7.0 | 誤差ラベリングユーティリティ(`error.*_label`) |
| H | v0.8.0 | `error_analysis()` 1コールラッパー |
| I+J | v0.9.0 | 分類・回帰の誤差可視化 |
| K | v0.10.0 | キャリブレーション API(AIC binning) |
| L | v0.11.0 | スライス発見・コホート比較・ドリフト |
| - | v0.12.0 | LizyStudio 統合の安定化 |
| - | v1.0.0 | API 整理(`plotting.*` → `plot.matplotlib.*` エイリアス化、別 Proposal) |

---

## 2026-05-26: ML 誤差分析機能の詳細要件と競合分析

- ID: `H-0002`
- Status: `accepted`
- Scope: `API | scope | dependencies | design principles`
- Related: `H-0001`, `BLUEPRINT.md §3, §4, §5.7`

### Context

H-0001 で pycatdap の用途を「AIC ベース EDA + ML 誤差分析」に拡張する戦略が承認された。
本提案では、グローバルで高評価を得ているツール群(EDA・スライス発見・ドリフト検出・キャリブレーション・モデルデバッグ)を網羅的に調査した結果に基づき、特に **ML 誤差分析方面の詳細要件・設計原則・直接競合の特定** を確定する。

H-0001 の議論時点では `Microsoft Responsible AI`, `Manifold`, `What-If Tool`, `Fairlearn`, `Aequitas`, `TFMA`, `InterpretML`, `SHAP`, `yellowbrick`, `Evidently`, `deepchecks`, `DALEX` を参照していたが、その後の調査で **直接競合となる重要ツール** が複数判明した。

### Proposal

#### A. 競合分析(H-0001 以降に確認したツール群)

**EDA 系で重要視すべき追加ツール**:

| ツール | star | 称賛されている機能 |
|---|---|---|
| PyGWalker | ~14k | 1行で Tableau 風 UI + 自然言語クエリ(LLM 連携) |
| Skrub `TableReport` | 急成長 | sklearn パイプライン統合可能な軽量レポート、ydata-profiling のモダン版 |
| Buckaroo | - | Jupyter の DataFrame 表示を常時 summary+histograms 付きに置換 |
| itables | - | DataTables.js で DataFrame をソート・フィルタ可能 UI 化 |
| Renumics Spotlight | ~1.3k | 構造化+非構造データ+embedding の統合探索、Similarity Map |
| VisiData | ~8k | ターミナル vim-キーバインドで数百万行を高速探索 |
| whylogs | ~2.6k | 近似統計で大規模データを定メモリでプロファイル |
| popmon (ING Bank) | ~500 | 時系列の分布安定性監視 + トラフィックライト式アラート |

**ML 誤差分析・スライス発見系で重要視すべき追加ツール**:

| ツール | star/論文 | 称賛されている機能 |
|---|---|---|
| **DivExplorer** | (論文+OSS) | **pycatdap と最も近い直接競合**: FP-Growth + divergence でカテゴリ組合せ slice を発見 |
| **pysubgroup** | - | 20+ の interestingness measures を pluggable(WRAcc, Lift, χ² 等) |
| SliceLine (IBM) | - | monotonic scoring + 上界プルーニングで 1万特徴規模に scale |
| FreaAI (IBM) | 論文 | 人間が説明できる slice のみ返す + 統計的有意性保証 |
| Domino (Stanford) | - | embedding 上の GMM で slice 発見、自然言語ラベル自動生成 |
| HiBug2 / DebugAgent | 2025 論文 | LLM で task-specific attribute 生成、coherent な slice |
| NannyML | ~2k | ground truth なしで本番性能を推定(CBPE) |
| Cleanlab | ~10k | Confident Learning で label noise を任意分類器で検出 |
| Giskard | ~5.2k | tabular + LLM の自動脆弱性スキャン、OWASP LLM Top10 対応 |
| netcal | - | 分類 + 回帰両方の calibration を扱う数少ない pkg |
| Frouros | - | drift 検出 31 種類(同類最多) |
| OmniXAI (Salesforce) | - | tabular/image/text/time-series を統一 API + GUI dashboard |

#### B. 称賛されている機能パターン(横断分析)

調査から抽出した **9つの繰り返し称賛軸**:

| # | パターン | 代表ツール | pycatdap への含意 |
|---|---|---|---|
| 1 | 1コール → interactive HTML report | Skrub, Sliceguard, explainerdashboard, PyGWalker | `profile()` / `error_analysis()` を最優先実装 |
| 2 | Pluggable な scoring/measure API | pysubgroup, deepchecks | AIC を複数 measure の1つとして実装、Cramér's V 等も同居 |
| 3 | Monotonic scoring + 上界プルーニング | SliceLine | CATDAP-02 を AIC monotonic 性質で枝刈り |
| 4 | 多重検定補正・偽陽性制御 | Slice Finder, FreaAI | AIC は本質的に複雑さペナルティを持つため自然に充足(強み) |
| 5 | 可解釈な slice 出力(自然言語ラベル) | FreaAI, Domino, HiBug2 | `"age ∈ [45, 60] × region = East"` 形式を必須化 |
| 6 | CI 統合可能・テスト的 API | deepchecks, Evidently, Giskard | `Suite` パターン: `aic_suite.run(df) → pass/fail` |
| 7 | メモリ効率・スケール | whylogs, SliceLine, VisiData | numpy ベースで O(n) sweep、大規模は将来オプション |
| 8 | 分類 + 回帰両対応 | netcal | `error_analysis(task=...)` を最初から両対応 |
| 9 | ground truth 不要 / streaming | NannyML, River | 将来オプション(優先度低) |

#### C. 直接競合の特定

**DivExplorer** が機能・思想の両面で pycatdap と最も近接:
- FP-Growth でカテゴリ組合せ列挙 → divergence (FPR/FNR の偏差) でランキング
- pycatdap は **AIC を divergence の代替** として位置付けることで自然に差別化
- 出力形式の互換性を意識すれば、DivExplorer ユーザーの移行が容易

**pysubgroup** が API 設計のリファレンス:
- pluggable な interestingness measure(20+)
- pandas DataFrame ネイティブ
- pycatdap は **AIC を pysubgroup 互換の measure として登録できる** 設計を採る

#### D. 機能要件 (Functional Requirements)

**FR-1: ワンコール EDA**
```python
pycatdap.profile(df, response=None) → ProfileResult
profile.to_html(path)
profile.show()  # Jupyter inline
```
- AIC ヒートマップ・variable cards・CATDAP-02 上位サブセット・データ品質警告を統合
- Skrub `TableReport` / ydata-profiling 互換の UX

**FR-2: ワンコール誤差分析**
```python
pycatdap.error_analysis(
    df, y_true, y_pred,
    task="auto" | "classification" | "regression"
) → ErrorAnalysisResult
```
- 内部処理: `error_label` → CATDAP-01/02 → 上位 K cohort 抽出
- 自然言語形式の slice 説明文(`"age ∈ [45, 60] × cholesterol = high"`)を出力
- DivExplorer 互換の出力形式オプションを提供

**FR-3: 単/二変量プロット**(H-0001 Phase A/B を踏襲)
- `plot_variable`, `plot_pair`, `plot_missing`, `aic_heatmap`, `association_plot`
- matplotlib / plotly 両 backend

**FR-4: 誤差ラベリングユーティリティ**
```python
pycatdap.error.error_label(y_true, y_pred)         # "correct" / "incorrect"
pycatdap.error.confusion_label(y_true, y_pred)     # "TP" / "FP" / "FN" / "TN"
pycatdap.error.residual_label(y_true, y_pred,
                              method="aic_pool")    # 回帰残差を AIC binning
pycatdap.error.abs_residual_pool(y_true, y_pred)   # |residual| の AIC binning
```

**FR-5: 自動スライス発見**
```python
pycatdap.error.discover_error_slices(
    df, y_true, y_pred,
    max_vars=3,
    measure="aic" | "cramers_v" | "mutual_info" | callable,
) → list[Slice]
```
- AIC ベース monotonic scoring + 上界プルーニング(SliceLine 流)
- 各 `Slice` は `description: str`, `size: int`, `error_metric: float`, `delta_aic: float` を持つ

**FR-6: キャリブレーション**
```python
pycatdap.error.calibration_curve(y_true, y_proba, n_bins="aic"|int)
pycatdap.error.brier_score(y_true, y_proba)
pycatdap.error.expected_calibration_error(y_true, y_proba)
```
- AIC binning が他ツールに対する差別化
- 分類 + 回帰両対応(netcal の踏襲)

**FR-7: コホート比較・ドリフト**
```python
pycatdap.error.compare_cohorts(df_a, df_b, response=None)
pycatdap.error.detect_drift(df_train, df_prod, y_true=None, y_pred=None)
```
- Sweetviz 風の比較
- ΔAIC ベースのドリフト検出

**FR-8: タスク自動検出**
- `y_true` / `y_pred` の dtype と一意値数から classification / regression を自動推定
- 明示指定 (`task=...`) が優先

**FR-9: Pluggable measure API**
- pysubgroup 互換: AIC measure を他ライブラリから差し替え可能
- `interestingness_measure="aic" | "cramers_v" | "mutual_info" | callable`
- ユーザー定義 measure の登録 API: `pycatdap.measures.register("my_measure", fn)`

**FR-10: Suite / Test 統合**
```python
suite = pycatdap.suite.AICIndependenceSuite(df, response="symptoms")
result = suite.run()  # SuiteResult(passed: bool, warnings: list[Warning])
```
- deepchecks 風 — CI に統合可能
- 個別チェック: independence test、high cardinality warning、constant column、pooling suggestion

#### E. 非機能要件 (Non-Functional Requirements)

| # | 要件 |
|---|---|
| NFR-1 | 既存 `catdap1` / `catdap2` / `plotting.*` API は v1.0 まで後方互換維持 |
| NFR-2 | 任意依存(Extras): `[plot]` `[plotly]` `[widget]` `[all]` |
| NFR-3 | モデル非依存: `y_true`, `y_pred` を numpy/pandas で受け取れば任意のモデルで動作 |
| NFR-4 | DataFrame ネイティブ(pandas、将来 polars 検討) |
| NFR-5 | 全結果オブジェクトに `.show()` / `.to_html()` / `.to_dict()` / `.to_plotly_json()` |
| NFR-6 | 全 slice / cohort 出力に `description: str` フィールド必須(自然言語表現) |
| NFR-7 | R `catdap` との数値一致 atol=1e-4(Issue #10 が前提) + DivExplorer 出力との整合性検証 |

#### F. スコープ外 (Out of Scope)

| 領域 | 該当ツール | スコープ外とする理由 |
|---|---|---|
| 非構造データ(画像・音声・テキスト embedding) | Domino, Sliceguard | CATDAP の数理的基盤から外れる |
| streaming / online learning | River | 別ライブラリと組み合わせる方が自然 |
| 自然言語による slice 命名(LLM 連携) | HiBug2 | 将来検討、現状は規則ベース description で十分 |
| label error 検出 | Cleanlab | 直交する問題領域 |
| 大規模分散処理(Spark/Ray) | whylogs | numpy ベース single-node を優先 |

#### G. 設計原則 (Design Principles)

| # | 原則 | 由来 |
|---|---|---|
| DP-1 | 1コール体験を最優先 | Skrub, PyGWalker, explainerdashboard |
| DP-2 | 結果オブジェクトは探索可能(`.show` / `.to_html` / `.to_dict`) | pysubgroup, deepchecks |
| DP-3 | 自然言語 slice 表現を必須化(`description` field) | FreaAI, Domino |
| DP-4 | Plotly Figure を返せる(`.to_plotly_json()`) | LizyStudio 統合(H-0001) |
| DP-5 | 分類・回帰両対応をデフォルト | netcal |
| DP-6 | Pluggable measure 設計 | pysubgroup |
| DP-7 | AIC は monotonic とみなしプルーニング可能と仮定 | SliceLine |

### Impact

- H-0001 で定義した Phase G〜L(ML 誤差分析)の API シグネチャを確定
- 新規依存: `jinja2`(HTML レポート), `anywidget`(任意), `plotly`(任意)
- `BLUEPRINT.md` に「§5.8 error/ サブモジュール」「§5.9 profile.py」「§5.10 suite/」「§5.11 measures/」を追加
- `Slice` / `SuiteResult` / `ErrorAnalysisResult` / `ProfileResult` のデータクラス契約が公開 API に追加される

### Compatibility

- **後方互換性**: 既存 API は無影響
- **Phase 間の互換性**: FR-9 の Pluggable measure API は Phase H 以降で `error_analysis()` の `measure` パラメータとして公開、それより前の Phase では内部実装にとどめる
- **DivExplorer 互換性**: スライス出力に `.to_divexplorer_format()` メソッドを提供(オプション)

### Alternatives Considered

#### B1: DivExplorer をラップして AIC measure を注入する
- 不採用理由: DivExplorer は FP-Growth が前提だが、CATDAP は連続変数の AIC pooling を統合した独自探索が必要。fork/wrap より新規実装の方が見通しが良い

#### B2: pysubgroup の measure として AIC を貢献する(pycatdap は薄い wrapper のみ)
- 不採用理由: 連続変数の AIC pooling や CATDAP-02 のサブセット探索は pysubgroup の API に乗らない。pysubgroup 互換は維持しつつ、pycatdap は独立したライブラリとする

#### B3: ML 誤差分析を完全に LizyML 側で実装
- 不採用理由: H-0001 で議論済み。モデル非依存性を保つため pycatdap に置く

#### B4: 自然言語 slice 表現を LLM ベースで生成する(HiBug2 流)
- 不採用理由: 規則ベース description (`"var ∈ [a, b] × var2 = cat"`) で十分な情報を提供できる。LLM 連携は将来オプション

### Acceptance Criteria

#### 機能要件
- [ ] FR-1〜FR-10 の各 API がドキュメント化され、最小実装が存在
- [ ] 全結果オブジェクトが `.show()`, `.to_html()`, `.to_dict()`, `.to_plotly_json()` を実装
- [ ] 全 slice / cohort 出力に `description: str` フィールドが存在し、`"var ∈ [a, b] × var2 = cat"` 形式で生成される

#### 設計原則
- [ ] DP-1〜DP-7 が `BLUEPRINT.md` に明記される
- [ ] Pluggable measure API(FR-9)が pysubgroup スタイルで実装される
- [ ] `Suite` パターン(FR-10)が deepchecks 風に実装される

#### 競合との整合性
- [ ] DivExplorer 互換の出力形式(`.to_divexplorer_format()`)が機能する
- [ ] R `catdap` との数値一致 atol=1e-4(Issue #10 完了が前提)

#### LizyStudio 統合(H-0001 を継承)
- [ ] LizyStudio から `result.to_plotly_json()` 経由で全 Phase の結果が消費可能
- [ ] LizyStudio の「Error Analysis」タブで end-to-end に動作

### Decision

- Date: `2026-05-26`
- Result: `accepted`
- Notes: プロジェクトオーナー承認。`BLUEPRINT.md` への反映と GitHub Issue 起票を後続作業として実施

### Migration

破壊的変更なし。H-0001 のロードマップ(Phase A〜L)に変更を加える場合は本 H-0002 を参照する。

### Related Research Notes

調査の主要ソース:

**EDA 系**
- pygwalker, Renumics Spotlight, Buckaroo, itables, Mito, Skrub, Deepchecks, Evidently, whylogs, popmon, VisiData, Shapash, explainerdashboard
- SmartEDA (R), funModeling (R)

**ML 誤差分析・スライス発見系**
- SliceLine paper / SystemDS
- Slice Finder / AutoSlicer paper (Google)
- FreaAI arXiv 2108.05620 (IBM Haifa)
- DivExplorer (Politecnico di Torino) — `pip install DivExplorer`
- Domino arXiv 2203.14960 (Stanford HazyResearch)
- HiBug2 / DebugAgent arXiv 2501.16751 (2025)
- Sliceguard / Spotlight (Renumics)
- pysubgroup
- Frouros (drift, 31 methods)
- NannyML (CBPE)
- Cleanlab (Confident Learning)
- Giskard (5.2k stars)
- netcal (classification + regression calibration)
- OmniXAI (Salesforce)

---

## 2026-05-26: 検証用・チュートリアル用データセットの拡張

- ID: `H-0003`
- Status: `accepted`
- Scope: `API | data | dependencies`
- Related: `H-0001`, `H-0002`, `BLUEPRINT.md §3.1, §8`, Issue #10

### Context

H-0001 / H-0002 で pycatdap を「AIC ベース EDA + ML 誤差分析ライブラリ」として再定位した結果、検証用・チュートリアル用データセットの不足が新たな課題となった:

1. **検証用データの不足**:
   - 現状の `tests/test_against_r.py` は R `catdap` との数値一致テストが未実装(Issue #10)
   - 既存の `load_health_data` / `load_hello_goodbye` のみでは、Phase H〜L(ML 誤差分析)の検証ができない
   - 既知のバイアス/不均衡パターンを持つデータ(Adult, COMPAS, German Credit 等)が必要

2. **チュートリアル用データの不足**:
   - 現状の tutorial.ipynb は HealthData のみを使用
   - 回帰タスクや誤差分析機能をデモするデータがない
   - 学習者にとって直感的(Titanic, Penguins 等の世界共通の知名度を持つもの)が望ましい

### Proposal

#### A. 要件定義

**検証用データの要件 (V-1〜V-8)**:

| # | 要件 | 理由 |
|---|---|---|
| V-1 | R `catdap` で実行可能 | atol=1e-4 のクロスバリデーション(Issue #10) |
| V-2 | カテゴリカル + 連続変数の混在 | CATDAP-01/02 + pooling 両方の検証 |
| V-3 | 既知の関係性が文書化されている | テストで関係性を assert 可能 |
| V-4 | 小〜中規模(50〜5万行) | CI で繰り返し実行可能 |
| V-5 | 公開ライセンス + 再配布可能 | 同梱・配布上の問題なし |
| V-6 | ML タスク(分類/回帰)としても使える | error_analysis 機能の検証 |
| V-7 | 既知のバイアス/分布ずれパターン | スライス発見・ドリフト検出の検証 |
| V-8 | R 側の reference を CSV 化して同梱 | CI で外部依存なし |

**チュートリアル用データの要件 (T-1〜T-7)**:

| # | 要件 | 理由 |
|---|---|---|
| T-1 | ドメインが直感的 | 学習者が結果を解釈できる |
| T-2 | 小規模(数百〜数千行) | ノートブック実行が高速 |
| T-3 | 単一データセットで複数機能を実演可能 | 1ファイル完結 |
| T-4 | カテゴリカル + 連続変数の混在 | pooling 機能を見せられる |
| T-5 | 既知のデータセット | 学習者の事前知識を活用 |
| T-6 | 結果が「なるほど」となるストーリー性 | 普及効果 |
| T-7 | パッケージ同梱(`load_*` で即利用可) | 障壁ゼロ |

#### B. データセット候補

**Group A: R `catdap` 参照あり(検証最優先、V-1, V-8 充足)**

| Dataset | Source | Size | Type | R関数 | 用途 | License |
|---|---|---|---|---|---|---|
| HealthData | R catdap | 52 × 8 | Mixed | catdap1, catdap2 | 既存 | GPL-2 |
| JNcharacter | R catdap | 31 × 17 | Categorical | catdap1 | 文字データ | GPL-2 |
| HelloGoodbye | R catdap | 13,954 × 5 | Categorical | catdap1, catdap2 | 既存 | GPL-2 |
| Titanic | R `datasets` | 2,201 × 4 | Categorical | catdap1c | 知名度最高 | Public Domain |
| iris | R `datasets` | 150 × 5 | Mixed | catdap2 | 連続変数 pooling | Public Domain |

**Group B: ML 誤差分析ベンチマーク(Phase H〜L 検証用、V-6, V-7 充足)**

| Dataset | Source | Size | Task | 既知バイアス/特徴 | 配布方法 |
|---|---|---|---|---|---|
| Titanic | seaborn / openml | 891 × 12 | Classification | Sex, Pclass で生存率に明確な disparity | 同梱(`load_*`) |
| Adult Income | UCI / openml | 48,842 × 14 | Classification | Race, Gender で income に bias | `fetch_*` |
| COMPAS | ProPublica | 7,214 × 53 | Classification | Race による再犯予測 bias | `fetch_*` |
| German Credit | UCI | 1,000 × 20 | Classification | Age, Gender disparity | 同梱(`load_*`) |
| Bank Marketing | UCI | 45,211 × 16 | Classification | Job, Age で反応率に強い差 | `fetch_*` |
| Heart Disease | UCI | 303 × 14 | Classification | Sex, Age | 同梱(`load_*`) |
| California Housing | sklearn | 20,640 × 8 | Regression | 地理 stratification | sklearn 経由 |
| Diabetes | sklearn | 442 × 10 | Regression | Sex stratification | sklearn 経由 |
| Mushroom | UCI | 8,124 × 22 | Classification | 全カテゴリカル、決定論的 | `fetch_*` |

**Group C: チュートリアル / 教育用**

| Dataset | Why for tutorial |
|---|---|
| HealthData(既存) | 小規模・医療・既存テストカバー済 |
| Titanic | 世界共通知名度、分類 + error_analysis デモ |
| Palmer Penguins | Iris の倫理的代替、3 種 × 島 × 性別 × 連続体重 |
| Wine Quality | 11 個の連続化学指標 + 品質スコア(回帰/分類両用) |
| California Housing | 回帰の代表例、Phase J(residual_plot)のデモ |

#### C. 配布方式(sklearn パターン踏襲)

**同梱(< 500KB、git にコミット可)**:
```python
pycatdap.datasets.load_health_data()        # 既存
pycatdap.datasets.load_jncharacter()        # 新規
pycatdap.datasets.load_hello_goodbye()      # 既存(load_hellogoodbye を rename 検討)
pycatdap.datasets.load_titanic()            # 新規(R Titanic + seaborn Titanic 両対応)
pycatdap.datasets.load_iris()               # 新規
pycatdap.datasets.load_german_credit()      # 新規
pycatdap.datasets.load_heart_disease()      # 新規
pycatdap.datasets.load_penguins()           # 新規
```

**ダウンロード(初回のみ、`~/.pycatdap/data/` にキャッシュ)**:
```python
pycatdap.datasets.fetch_adult_income()       # OpenML 経由
pycatdap.datasets.fetch_compas()             # ProPublica raw
pycatdap.datasets.fetch_bank_marketing()     # UCI
pycatdap.datasets.fetch_california_housing() # sklearn ラッパ
pycatdap.datasets.fetch_diabetes()           # sklearn ラッパ
pycatdap.datasets.fetch_mushroom()           # UCI
pycatdap.datasets.fetch_wine_quality()       # UCI
```

**全データセットの共通契約**:
- 戻り値は `pd.DataFrame`(default)または `(X, y)` の tuple(`return_X_y=True` 時)
- `as_frame=False` で numpy 配列を返す(sklearn 互換)
- 各ローダーに data dictionary(列の意味・型・License・出典)の docstring を必須化

#### D. R 参照値の同梱戦略

```
docs/r_reference/
├── generate_reference.R              # 既存(全データセット対応に拡張)
├── healthdata_catdap1.csv            # 新規
├── healthdata_catdap2_aic.csv        # 新規
├── healthdata_catdap2_subsets.csv    # 新規
├── jncharacter_catdap1.csv           # 新規
├── hellogoodbye_catdap1.csv          # 新規
├── titanic_catdap1.csv               # 新規(R Titanic)
└── iris_catdap2.csv                  # 新規(連続変数 pooling)
```

`tests/test_against_r.py` で各 CSV を読み込み、`np.testing.assert_allclose(py_result, r_result, atol=1e-4)` を実施。これで Issue #10 の Acceptance Criteria が満たせる。

#### E. 段階的ロールアウト

| 段階 | 内容 | バージョン | 連動 Issue |
|---|---|---|---|
| **D1** | R reference CSV 生成 + 既存 HealthData/HelloGoodbye の数値検証実装 | v0.2.x patch | #10 |
| **D2** | Titanic / iris / JNcharacter を `load_*` に追加 | v0.3.0(Phase A) | (新規) |
| **D3** | German Credit / Heart Disease / Penguins を `load_*` に追加 | v0.5.0(Phase C) | (新規) |
| **D4** | Adult Income / COMPAS / California Housing を `fetch_*` に追加 | v0.8.0(Phase H) | (新規) |
| **D5** | Wine Quality / Bank Marketing / Mushroom を `fetch_*` に追加 | v0.11.0(Phase L) | (新規) |

### Impact

- 公開 API の **追加**: `load_*` 5件、`fetch_*` 7件(計 12 関数追加)
- 任意依存(オプショナル)の追加検討:
  - `scikit-learn`: California Housing / Diabetes / Adult Income (OpenML 経由)
  - `requests` または stdlib `urllib`: UCI / ProPublica からの fetch
- `tests/data/` に Group A の R reference CSV を同梱(計 5〜7 ファイル、合計 < 100KB)
- `BLUEPRINT.md §3.1` のパッケージ構成に `datasets.py` の拡張を明記
- `BLUEPRINT.md §8` の R照合 / Acceptance テスト節を更新

### Compatibility

- **後方互換性**: 既存の `load_health_data()` / `load_hellogoodbye()` は維持
  - ただし `load_hellogoodbye` は **将来 `load_hello_goodbye` に rename を検討**(sklearn 命名規約準拠)
  - rename する場合、旧名は v1.0 まで alias として残し、`DeprecationWarning` を出す
- **新規ユーザー**: `pip install pycatdap` で同梱データセットが即利用可、`pip install pycatdap[data]` で fetch 用依存を導入

### Alternatives Considered

#### C1: 全データセットを git に同梱する
- 不採用理由: Adult Income (5MB), Bank Marketing (5MB), Mushroom (370KB) 等は git リポジトリを肥大化させる。配布インストール時のサイズも増える

#### C2: sklearn のデータセット API を全面的に再利用する
- 不採用理由: sklearn には R catdap 互換の HealthData / HelloGoodbye がない。CATDAP の数値検証用には独自に持つ必要がある

#### C3: PyPI 経由の別パッケージ `pycatdap-datasets` に分離する
- 不採用理由: 同梱データセットは < 500KB と軽量で分離する意味が薄い。`fetch_*` で十分

#### C4: HuggingFace Datasets を利用する
- 不採用理由: 重い依存(`datasets` パッケージ自体が数十MB)。pycatdap の軽量性を損なう

#### C5: COMPAS を同梱せず fetch のみとする
- 採用: ProPublica の報道資料という性質上、同梱は controversy のリスクがある。fetch 経由で利用者の明示的アクションを伴うのが妥当

### Acceptance Criteria

#### 全体
- [ ] `BLUEPRINT.md §3.1` および `§8` が改訂され、新規データセット構成が記載される
- [ ] `README.md` のサンプルコードに新規データセットの使用例が追加される
- [ ] 全 `load_*` / `fetch_*` 関数に NumPy-style docstring(出典・License・列定義)を実装

#### D1(直近、Issue #10 解消)
- [ ] `docs/r_reference/` 配下に Group A の R reference CSV が同梱される
- [ ] `tests/test_against_r.py` で `np.testing.assert_allclose(atol=1e-4)` ベースの厳密一致テストが実装される
- [ ] 既存テストが `@pytest.mark.slow` から release-CI に昇格し、リリース前に実行される

#### D2〜D5
- [ ] 各段階で対応するローダーが実装され、サンプルコードがドキュメントに掲載される
- [ ] `fetch_*` のキャッシュディレクトリは `~/.pycatdap/data/` で、初回 download 後はオフラインで利用可能
- [ ] download 失敗時は明確なエラーメッセージ(URL、推奨アクション)を返す

#### 数値検証
- [ ] Group A のデータで R catdap との数値一致 atol=1e-4
- [ ] Group B のデータで `error_analysis` が既知バイアス(Adult の gender disparity 等)を検出する回帰テスト

### Decision

- Date: `2026-05-26`
- Result: `accepted`
- Notes: プロジェクトオーナー承認。D1 は Issue #10 で進行、D2-D5 は Issues #22-#25 で個別追跡

### Migration

破壊的変更なし。`load_hellogoodbye` → `load_hello_goodbye` の rename は別途 Proposal で議論。

### Related References

- R `catdap` package: <https://cran.r-project.org/package=catdap>
- UCI Machine Learning Repository: <https://archive.ics.uci.edu/>
- OpenML: <https://www.openml.org/>
- sklearn datasets API design: <https://scikit-learn.org/stable/datasets.html>
- Palmer Penguins (CC0): <https://allisonhorst.github.io/palmerpenguins/>
- ProPublica COMPAS analysis: <https://github.com/propublica/compas-analysis>
- Folktables (Adult replacement): <https://github.com/socialfoundations/folktables>

---

## 2026-05-27: 目的変数 × 説明変数 ペア分析 API(`target_summary` / `plot_target`)

- ID: `H-0004`
- Status: `proposed`
- Scope: `API | scope`
- Related: `H-0001 Phase B`, `BLUEPRINT.md §3, §5.7`, Issue #13

### Context

v0.3.0 で出荷した EDA API は **単変量**(`describe`, `plot_variable`, `plot_missing`)に閉じている。一方、チュートリアル(02/05)を実装した過程で次の欠落が判明した:

- **目的変数と各説明変数の関係を「1コール」で要約・可視化する手段がない**
- 既存の `plot.mosaic_plot(table)` / `plot.barplot_twoway(table)` は2変数を扱えるが、**呼び出し側で `pd.crosstab` 等を組み立てる必要があり、利用障壁が高い**
- `Catdap1Result.tway_tables` / `Catdap2Result.tway_tables` に2-way テーブル自体は格納されているが、**目的変数を軸にした「縦割り」の解釈ビューが提供されていない**

`H-0001 Phase B`(Issue #13)に `plot_pair(df, x, y)` 等の双方向 API が提案されているが、これは **対称**(x と y が交換可能)な設計であり、ユーザーが期待する「**目的変数を中心に各説明変数を見る**」エルゴノミクスとは噛み合わない。本 Proposal は Phase B を **目的変数指向に絞った最小 API** として段階的に細分化する。

### 競合分析(対象パッケージ)

| Package | 該当機能 | 提供されている形 | pycatdap での参考点 |
|---|---|---|---|
| **R `gmodels::CrossTable()`** | 集計表 | counts + row% + col% + total% + Chi² 寄与 セル毎 | 「**1関数で多視点の集計表**」 |
| **R `vcd::mosaic(formula, shade=TRUE)` / `vcd::assoc()`** | 図 | モザイク + Pearson 標準化残差で色付け | 「**残差ベースの色付けで関連の方向を可視化**」 |
| **R `descr::CrossTable()`** | 集計表 | gmodels 互換だが出力整形が異なる | 同上 |
| **sweetviz `sv.analyze(df, target_feat='Survived')`** | ターゲット指向の EDA | 列ごとに「数値列: 分布 + 相関」「カテゴリ列: ターゲット率 per level」のパネル | 「**target_feat という明示的キーワードでターゲット中心の API を構築**」 |
| **ydata-profiling** | 双方向 | Interactions(散布図)+ Correlations(phi_k 行列) | target awareness は弱い・参考度低 |
| **seaborn** | プリミティブ | `catplot(kind='bar'\|'violin'\|'box')`, `histplot(hue=target)` | 「**hue=target という1引数で target 軸を導入**」 |
| **plotly express** | プリミティブ | `px.histogram(df, x=feature, color=target)`, `px.box(df, x=target, y=feature)` | 同上 |

**学び**:
- 「**目的変数を明示するキーワード**」(`target_feat` / `hue` / `color` / `response`)で API を分岐させるのが業界標準
- 集計表は「counts + 行/列/全体 比率 + 統計量」を **同一オブジェクト** で持たせる(gmodels)
- 図はカテゴリ×カテゴリで **mosaic + Pearson 残差**(vcd)、カテゴリ×連続で **箱ひげ/バイオリン**(seaborn)が定石

### Proposal

#### 公開 API(新規 2 関数)

```python
# 1. 集計表(target × explanatory のクロス表 + 比率 + ΔAIC)
pycatdap.target_summary(
    df: pd.DataFrame,
    target: str,
    explanatory: str,
    *,
    bins: int | list[float] | None = None,   # 連続 explanatory の binning 制御
) -> TargetSummary
```

返り値 `TargetSummary` は frozen dataclass:

| 属性 | 型 | 内容 |
|---|---|---|
| `target` | `str` | 目的変数列名 |
| `explanatory` | `str` | 説明変数列名 |
| `counts` | `pd.DataFrame` | クロス頻度(rows=target, cols=explanatory) |
| `row_prop` | `pd.DataFrame` | 行方向比率(target カテゴリ内の説明変数分布) |
| `col_prop` | `pd.DataFrame` | 列方向比率(説明変数カテゴリ内の target 率) |
| `expected` | `pd.DataFrame` | 独立を仮定した期待頻度 |
| `pearson_residuals` | `pd.DataFrame` | `(observed - expected) / sqrt(expected)` |
| `delta_aic` | `float` | ΔAIC(`catdap1` と同一の計算) |
| `intervals` | `list[float] \| None` | 連続変数の binning 境界(該当時のみ) |

メソッド(既存 `DescribeResult` / `Catdap1Result` に揃える):
- `.show()` — Jupyter inline 表示
- `.to_html(path=None) -> str` — スタンドアロン HTML(複数視点の表を縦に積む)
- `.to_dict() -> dict` — JSON シリアライズ可能
- `.to_plotly_json() -> dict` — Plotly Table Figure spec

```python
# 2. 可視化(target × explanatory)
pycatdap.plot_target(
    df: pd.DataFrame,
    target: str,
    explanatory: str,
    *,
    kind: Literal["auto", "stacked", "mosaic", "grouped_bar", "box", "violin", "hist"] = "auto",
    bins: int | list[float] | None = None,
    backend: Literal["matplotlib", "plotly"] = "matplotlib",
    ax: Any = None,
    **kwargs: Any,
) -> Any
```

**`kind="auto"` の自動判定ルール**(`pycatdap.eda._detect_kind` を流用):

| target | explanatory | 自動選択 | 根拠 |
|---|---|---|---|
| categorical(任意) | categorical(≤ 8 levels) | `stacked`(target カテゴリ内の説明変数分布、Pearson 残差で色) | vcd `assoc()` 風、解釈容易 |
| categorical | categorical(> 8 levels) | `mosaic` | スペース効率 |
| categorical | continuous | `violin`(matplotlib)/ `box`(plotly fallback) | target 群間の分布比較、seaborn 定石 |
| boolean | continuous | `hist`(target 値で hue 分け) | 二値分類の標準ビュー |
| continuous | * | `auto` で `ValueError`、明示的 `kind` を要求 | v0.4.0 のスコープ外 |

`kind="stacked"` / `"mosaic"` は**Pearson 標準化残差で色付け**(vcd 風)— 残差 > +2 を強い正の関連、< -2 を強い負の関連として配色。これは `target_summary().pearson_residuals` を内部で使用。

#### 既存 API との関係

- 既存 `pycatdap.plot.mosaic_plot(table)` / `barplot_twoway(table)` は **低レベル API**(pd.DataFrame テーブルを直接受け取る)として残す。新規 `plot_target` は内部でこれらに委譲する。
- Issue #13 の `plot_pair(df, x, y)` はこの Proposal を受けて **`plot_target` の別名 / 対称ラッパー**として再定義する案を別 Proposal(将来)に回す。

#### 連続変数の binning

- `bins=None`(default): 連続 explanatory には `pycatdap._pooling.optimal_binning` を呼び、AIC 最適 binning を採用(`pool=0` 相当)
- `bins=int`: 等幅 K-bin(`pd.cut`)
- `bins=list[float]`: 明示的境界

`TargetSummary.intervals` で実際に使われた境界を返す。

### Impact

- **公開 API の追加のみ**(2 関数 + 1 dataclass)
- 既存 API への破壊的変更なし
- 新規モジュール: `src/pycatdap/_target_pair.py`(実装)+ `src/pycatdap/__init__.py` への再 export
- `BLUEPRINT.md §3`(モジュール構成)と `§5.7`(plotting テーブル)を改訂
- 任意依存の追加なし(matplotlib / plotly は既存 extras で十分)

### Compatibility

- **後方互換**: 完全
- 既存の `Catdap1Result.tway_tables` / `Catdap2Result.tway_tables` は **アクセサがそのまま動く**。`TargetSummary` は新規型なのでアクセサが衝突しない。

### Alternatives Considered

#### A1: 既存 `plot_pair(df, x, y)`(Issue #13)を対称 API として実装し、target 軸はユーザーが慣習で先頭に置く
- **不採用理由**: 「どちらが target か」が型シグネチャから読み取れない。Pearson 残差の正負解釈や `kind="auto"` の dtype 判定で曖昧性が残る。sweetviz / `vcd::mosaic(formula)` も target を明示する設計。

#### A2: target を Catdap1Result / Catdap2Result に紐づけ、`result.plot(var)` 形式とする
- **不採用理由**: catdap を実行せずに 2 変数の関係だけ見たいユースケース(EDA 初手)で使えない。`DescribeResult` のように分析実行に紐付かない独立 API である方が用途が広い。

#### A3: keyword 名を `response` に統一(`response` は既存 `catdap1` / `catdap2` の vocabulary)
- **採用検討**: 一貫性は高い。**ただし** sweetviz / sklearn / seaborn / plotly は全て `target`(または `hue` / `color`)を使っており、新規ユーザーの参照点としては `target` の方が広く認知される。**本 Proposal では `target` を採用するが、別途 v1.0 で `response` ↔ `target` の整理を行う**(別 Proposal)。

#### A4: 集計表と図を1つの関数 `pycatdap.target_pair(df, target, explanatory)` に統合し、戻り値で両方持つ
- **不採用理由**: pandas 1.x スタイル(計算と描画を分離する `DescribeResult.show()` 風)に揃える方が `.to_html()` / `.to_plotly_json()` のテストが書きやすい。

#### A5: 多目的変数を同時にサポート(`target=[c1, c2]`)
- **不採用理由**: スコープ拡大。`target_summary` を for ループで呼べば代替可能。将来 `target_summary_grid` を別 Proposal で検討。

### Acceptance Criteria

#### API
- [ ] `pycatdap.target_summary(df, target, explanatory)` が `TargetSummary` を返す
- [ ] `TargetSummary` に `.show / .to_html / .to_dict / .to_plotly_json` の4メソッド
- [ ] `pycatdap.plot_target(df, target, explanatory, kind="auto", backend=...)` が matplotlib / plotly 両 backend で動作
- [ ] `kind="auto"` が上記表の dtype 組合せで正しい kind を選択

#### 数値整合
- [ ] `TargetSummary.delta_aic` が `catdap1(df[[target, explanatory]], response_names=[target]).aic.loc[target, explanatory]` と一致
- [ ] `pearson_residuals` の絶対値が 2 を超える場合の符号と大きさが `scipy.stats.chi2_contingency` の結果と一致(参考実装比較)
- [ ] 連続 explanatory の `bins=None` 時、`intervals` が `catdap2(pool=[0])` の `intervals[explanatory]` と一致

#### コード品質
- [ ] `tests/test_target_pair.py` に unit テスト 12 個以上(各 kind / 各 dtype 組合せ + エラーパス)
- [ ] coverage 80%+ 維持
- [ ] `mypy --strict` pass(現存する `eda.py` の `display` 未型付き呼び出しは別 Issue で対応)
- [ ] docstring(NumPy style)に `Examples` セクション付き

#### ドキュメント
- [ ] `BLUEPRINT.md §3` のモジュール構成図に `_target_pair.py` を追記
- [ ] `BLUEPRINT.md §5.7` の plotting 関数一覧に `plot_target` / `target_summary` を追記
- [ ] `docs/reference/plotting.md` に新規関数を追加
- [ ] 既存の 02 / 05 チュートリアルに `target_summary` / `plot_target` を使う節を追加(別 PR)

### Decision

- Date: `pending`
- Result: `pending`
- Notes: プロジェクトオーナーレビュー待ち

### Migration

破壊的変更なし。新規 API のため移行不要。CHANGELOG `[Unreleased]` の `Added` に2関数 + 1 dataclass を記載する。

### Related References

- R `vcd` package(Friendly, M.): <https://cran.r-project.org/package=vcd>
- R `gmodels::CrossTable`: <https://cran.r-project.org/package=gmodels>
- sweetviz: <https://github.com/fbdesignpro/sweetviz>
- seaborn `catplot` / `histplot(hue=...)`: <https://seaborn.pydata.org/>
- plotly express: <https://plotly.com/python/plotly-express/>
- Pearson standardized residuals(Agresti, 2002, *Categorical Data Analysis*)
