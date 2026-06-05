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
- Status: `accepted`
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

**`bins=None` 時の `optimal_binning` メソッド**: デフォルト `method="bottom_up"`(catdap2 デフォルト `pool=1` と同等の unequal pooling)を採用。fine bins から始めて貪欲に merge する方式で、`top_down`(等幅初期 + merge)より AIC 最適に近い解を返す傾向がある。Proposal 当初稿では `pool=0 相当` と記載したが、`optimal_binning` 実装側のデフォルトと catdap2 のデフォルトに合わせて `pool=1 相当`(bottom_up)に統一する。

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
- [ ] 連続 explanatory の `bins=None` 時、`intervals` が `catdap2(pool=[2,1])`(unequal pooling、catdap2 デフォルト)の `intervals[explanatory]` と一致

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

- Date: `2026-05-27`
- Result: `accepted`
- Notes: プロジェクトオーナー承認(PR #53)。実装は PR kappa で `src/pycatdap/_target_pair.py` + `plot/{matplotlib,plotly}.py` に追加、tests/test_target_pair.py(31 テスト全 pass、coverage 87%)で検証済み。

### Migration

破壊的変更なし。新規 API のため移行不要。CHANGELOG `[Unreleased]` の `Added` に2関数 + 1 dataclass を記載する。

### Related References

- R `vcd` package(Friendly, M.): <https://cran.r-project.org/package=vcd>
- R `gmodels::CrossTable`: <https://cran.r-project.org/package=gmodels>
- sweetviz: <https://github.com/fbdesignpro/sweetviz>
- seaborn `catplot` / `histplot(hue=...)`: <https://seaborn.pydata.org/>
- plotly express: <https://plotly.com/python/plotly-express/>
- Pearson standardized residuals(Agresti, 2002, *Categorical Data Analysis*)

---

## 2026-05-27: 連続目的変数サポート — Gaussian 回帰 AIC 拡張(`target_summary` / `plot_target`)

- ID: `H-0005`
- Status: `proposed`
- Scope: `API | scope | likelihood-family`
- Related: `H-0001 Phase J`, `H-0002`, `H-0004`, `BLUEPRINT.md §3, §5.7`, Issue #56(研究フェーズ)、Issue #18(Phase J)

### Context

H-0004 で実装した `target_summary` / `plot_target` は **categorical / boolean target のみ対応**(連続 target で `ValueError`)。これは「ML 誤差分析(回帰残差・キャリブレーションスコア・連続リスクスコア)を扱う」という H-0001 / H-0002 の中心ユースケースを満たさない。

しかし元の CATDAP フレームワーク(Sakamoto & Katsura, 1980)は contingency table 上の多項分布 AIC で response を **離散カテゴリ前提**にしており、連続 response の AIC 化アルゴリズムを提供していない。Pooling(連続変数の AIC 最適 binning)も **explanatory 側のみ**で対称展開できない(`_bin_aic` のペナルティ `2·(C_E−1)·C_F` が response カテゴリ数 `C_E` を固定値前提)。

### Research summary

[Issue #56](https://github.com/nbx-liz/pycatdap/issues/56) の研究フェーズで、5 つの離散化候補(symmetric pooling / joint AIC / marginal binning / aggregate AIC / user-specified)を評価したが、いずれも cross-pair 比較性(R-1)・実装複雑度・理論基盤のいずれかで欠陥があり、**「Y を離散化する」という前提自体が誤り**と判明した。

`nbx-liz/AdvancedCATDAP`(sibling 私有ライブラリ)が **Y を bin せず、ガウス回帰 AIC を直接適用** することで連続 target をサポートしており、これが教科書的に正しいアプローチ(候補 (f))。研究ドキュメント [`docs/research/h0005-continuous-target.md`](docs/research/h0005-continuous-target.md) §10 で詳細導出 + 数値検証、§11 で cross-check-reviewer の独立検証を経ている。

### Proposal

#### コア式: ガウス回帰 AIC

連続 target `y` と binned explanatory `X`(`k_means` 個の非空 bin、bin 内平均 `ȳ_i`)に対し:

```
RSS    = Σ_i Σ_{j ∈ bin i} (y_j − ȳ_i)²    # within-bin 二乗和
AIC    = n · log(RSS / n)  +  penalty(k_means + 1, n, criterion)
AIC_0  = n · log(TSS / n)  +  penalty(2, n, criterion)   # null: y = global mean
ΔAIC   = AIC − AIC_0  =  n · log(1 − R²)  +  Δ_penalty
```

ペナルティ関数:

| `criterion` | penalty(k, n) | 用途 |
|---|---|---|
| `"bic"`(default) | `log(n) · k` | piecewise-constant の標準推奨(Yao 1988) |
| `"aic"` | `2 · k` | 古典 AIC、AdvancedCATDAP と互換 |
| `"aicc"` | `2k + 2k(k+1)/(n−k−1)` | 小標本補正(Hurvich & Tsai 1989 系列、注: K 規約は σ² を含む方を採用) |

派生: ΔAIC = `n · log(1 − R²) + Δ_penalty`(教科書 Gaussian-AIC for piecewise-constant regression、Yao 1988、Davis-Lee-RY 2006、MARS Friedman 1991 系列)。

#### 公開 API(変更点)

`target_summary` / `plot_target` のシグネチャは互換維持。連続 target を内部的に dispatch:

```python
pycatdap.target_summary(
    df: pd.DataFrame,
    target: str,
    explanatory: str,
    *,
    bins: int | Sequence[float] | None = None,         # 既存(explanatory binning)
    target_bins: int                                   # NEW(opt-in、(c) fallback)
              | Sequence[float]
              | Literal["quantile", "equal_width", "fd"]
              | None = None,
    criterion: Literal["aic", "aicc", "bic"] = "bic",  # NEW
) -> TargetSummary | RegressionTargetSummary
```

Dispatch ルール:

| target dtype | `target_bins` | 戻り値 | AIC 種別 |
|---|---|---|---|
| categorical / boolean | `None`(必須) | `TargetSummary`(既存 H-0004) | 多項分布 ΔAIC(既存) |
| categorical / boolean | `not None` | `ValueError`(target は既に離散) | — |
| **continuous** | **`None`(default)** | **`RegressionTargetSummary`(NEW)** | **Gaussian ΔAIC(本 Proposal)** |
| continuous | `not None` | `TargetSummary`(候補 (c) fallback) | 多項分布 ΔAIC(Y を bin した contingency) |

#### 新規 dataclass

```python
@dataclass(frozen=True)
class RegressionTargetSummary:
    target: str
    explanatory: str
    bin_stats: pd.DataFrame      # cols: count, target_mean, target_std, x_min, x_max
    delta_aic: float
    r_squared: float             # ΔAIC を解釈しやすく
    n_effective: int             # M2 戦略による有効 N(下記)
    intervals: list[float] | None  # X 側の binning(連続 explanatory のみ)
    criterion: Literal["aic", "aicc", "bic"]
```

メソッド: `.show()` / `.to_html(path=None)` / `.to_dict()` / `.to_plotly_json()`(既存 `TargetSummary` と揃える)。

#### 欠損値ハンドリング: 戦略 M2(Acceptance Criterion)

cross-check で発見された致命的欠陥(現行 `_target_pair.py:328` の per-pair `dropna()` が ペア間で `n` を変動させ R-1 を実質的に破る)を回避するため、**M2 戦略を採用**:

1. **Y のみ dropna**: 目的変数の欠損行のみ削除。これにより全 X 候補で `n` 共通。
2. **X の欠損は明示的 missing pseudo-bin**: X に欠損がある行は `_missing_` という特別 bin に集約。`bin_stats` の最終行に表示。
3. **`AIC_null` は全ペアで同一**: `n · log(TSS / n) + penalty(2, n)` は Y のみ依存 → 同一 Y 上の異なる X 候補で ΔAIC が直接比較可能。

参考実装: AdvancedCATDAP `scoring.py:calc_score_regression_partial` が `stats_missing` を含めた同等の処理を行っている。

#### `plot_target` の継続的拡張

`RegressionTargetSummary` に対して `plot_target` は次の自動 kind を選択:

| explanatory dtype | auto kind | 描画内容 |
|---|---|---|
| categorical (≤ 8 levels) | `box` | X カテゴリ別の Y 箱ひげ(seaborn 定石) |
| categorical (> 8 levels) | `box` + sort by `target_mean` | 多水準時の可読性 |
| continuous | `scatter` + `bin_means` overlay | X-Y 散布図に bin 平均線を重畳 |
| boolean | overlaid hist | Y 分布の two-class 重畳 |

明示 kind: `"scatter"`, `"box"`, `"violin"`, `"hist"`, `"bin_means"`(bin 平均のみ折れ線)。

### Impact

- **公開 API 追加**: `RegressionTargetSummary` 型 + `target_summary` / `plot_target` シグネチャに `target_bins` / `criterion` パラメータ追加(default 互換)
- **既存 API への破壊的変更なし**: `TargetSummary` の動作不変
- **新規モジュール**: `src/pycatdap/_aic_regression.py`(ガウス回帰 AIC 計算、AdvancedCATDAP から移植)
- **既存モジュール改修**: `_target_pair.py`(dispatch logic + M2 dropna)、`plot/matplotlib.py` / `plot/plotly.py`(RegressionTargetSummary 対応)、`__init__.py`(新規型 export)
- **BLUEPRINT.md §3 / §5.7**: モジュール構成・plotting 関数表に追記

### Compatibility

- **後方互換**: 完全
  - 既存 `target_summary(df, "Survived", "Sex")` は `target_bins=None`, `criterion="bic"` がデフォルトに変わるが、target が categorical なので criterion は使われず動作不変
  - `target_bins` パラメータは新規追加(default `None`)
  - 連続 target で `ValueError` を期待していたコードは `RegressionTargetSummary` を受け取る挙動に変わる(breaking?)

→ **連続 target の ValueError 期待は documentation 上の挙動であり、API 契約ではない**。H-0004 リリース時点で「連続 target はサポートされていない」と明記しているため、`RegressionTargetSummary` を返すように変わっても契約違反ではない。CHANGELOG に明示。

### Alternatives Considered

研究ドキュメント §6-§7 で 5 候補(a-e)を評価し棄却した経緯。要点:

| 候補 | 棄却理由 |
|---|---|
| (a) Symmetric pooling | C_X 依存 post-selection bias で R-1 失敗(研究 §2.5) |
| (b) Joint AIC binning | R-1 失敗 + 計算量 O(K²N²) で実用不能 |
| (c) Marginal Y binning | (f) 採用後は不要だが、`target_bins=...` 経由で **contingency-table view fallback** として温存 |
| (d) Aggregate AIC | (f) で動機消失 |
| (e) User-specified | (c) のエイリアスとして温存 |

#### IT-解釈ギャップ(明示的に許容)

- categorical mode: ΔAIC = `−2n·Î(E;F) + penalty` → 相互情報量解釈
- regression mode: ΔAIC = `n·log(1−R²) + penalty` → R² 解釈

同じ AIC 機械を異なる likelihood family で適用するため、**カテゴリと回帰の ΔAIC は直接比較不能**。ユーザーには same-mode 内での比較に限定するよう docs で明記。

### Acceptance Criteria

#### API
- [ ] 連続 target + `target_bins=None` で `RegressionTargetSummary` を返す
- [ ] 連続 target + `target_bins=int|list|"quantile"|"equal_width"|"fd"` で既存 `TargetSummary`(候補 (c) fallback)を返す
- [ ] `RegressionTargetSummary` に `.show / .to_html / .to_dict / .to_plotly_json` の4メソッド
- [ ] `plot_target` の auto kind が回帰モードで `scatter+bin_means` / `box` / `violin` / `hist` を正しく選択

#### 数値整合
- [ ] `gaussian_regression_aic` の結果が `AdvancedCATDAP.calc_score_reg_bincount_idx` と一致(同一データで 1e-10 以内)
- [ ] ΔAIC = `n · log(1−R²) + penalty_diff` が `sklearn.metrics.r2_score` から再構成可能(R² 整合性)
- [ ] M2 missing strategy で **同一 Y、異なる欠損パターンの X 候補に対し `AIC_null` が一致**(R-1 テスト)
- [ ] `criterion="bic" | "aic" | "aicc"` でペナルティ式が一致(`bic: log(n)·k` / `aic: 2k` / `aicc: 2k + 2k(k+1)/(n-k-1)`)

#### コード品質
- [ ] `tests/test_aic_regression.py` に unit テスト 15 個以上(各 criterion / edge case / M2 missing strategy / cross-pair comparability)
- [ ] `tests/test_target_pair.py` に regression dispatch テスト 8 個以上(dtype 判定、戻り値型、`.to_html` / `.to_plotly_json`)
- [ ] coverage 80%+ 維持
- [ ] `mypy --strict` pass
- [ ] docstring(NumPy style)に `Examples` セクション付き

#### ドキュメント
- [ ] `BLUEPRINT.md §3` モジュール構成図に `_aic_regression.py` を追記
- [ ] `BLUEPRINT.md §5.7` の signature 表に regression mode を追記
- [ ] `CHANGELOG.md [Unreleased]` の `Added` に `RegressionTargetSummary` + 2 パラメータを記載
- [ ] チュートリアル Notebook 06 の「Coming soon: continuous targets」節を `RegressionTargetSummary` を使うコード例に置換(別 PR)

### Decision

- Date: `2026-05-27`
- Result: `accepted`
- Notes: プロジェクトオーナー承認(PR #58 squash merge by `nbx`)。実装は本リポジトリの後続 PR で:
  - `src/pycatdap/_aic_regression.py`(新規)— `compute_rss` / `compute_gaussian_aic` / `compute_gaussian_null_aic` / `compute_delta_aic_regression` + `_penalty(criterion=aic|aicc|bic)`
  - `src/pycatdap/_target_pair.py`(拡張)— `RegressionTargetSummary` dataclass + `target_summary` の dispatch + M2 missing strategy + `_apply_target_discretization` (c) fallback
  - `src/pycatdap/plot/{matplotlib,plotly}.py`(拡張)— 回帰モードに対応(`box` / `violin` / `scatter` / `bin_means` / `hist`)
  - `__init__.py` に `RegressionTargetSummary` を export
  - `tests/test_aic_regression.py`(26 件)+ `tests/test_target_pair.py` 追加分(24 件)= 計 273 テスト pass、coverage 81.16%、ruff/mypy strict 通過(IPython display は既存と同じ pre-existing)

### Migration

破壊的変更なし。新規 API のため明示的な移行不要。CHANGELOG `[Unreleased]` の `Added` に `RegressionTargetSummary` 型と 2 つのパラメータを記載する。

ユーザー側の互換ポイント:
- 既存の `target_summary(df, "Survived", "Sex")` は完全に互換
- 連続 target で従来 `ValueError` を `try/except` していたコードは、引き続き例外なし(`RegressionTargetSummary` が返る)に置き換える
- `criterion` のデフォルトを `"aic"` 互換にしたい場合は `target_summary(..., criterion="aic")` で明示

### Related References

- Akaike, H. (1973). *Information theory and an extension of the maximum likelihood principle*. In Proc. 2nd Int. Symp. Information Theory, 267-281.
- Hurvich, C. M., & Tsai, C. L. (1989). *Regression and time series model selection in small samples*. Biometrika 76(2), 297-307.(AICc; 注:本実装は K 規約に σ² を含む AdvancedCATDAP 流儀)
- Yao, Y. C. (1988). *Estimating the Number of Change-Points via Schwarz Criterion*. Statistics & Probability Letters 6, 181-189.(BIC を changepoint 推奨)
- Davis, R. A., Lee, T. C. M., & Rodriguez-Yam, G. A. (2006). *Structural Break Estimation for Nonstationary Time Series Models*. JASA 101, 223-239.
- Friedman, J. H. (1991). *Multivariate Adaptive Regression Splines*. Annals of Statistics 19(1), 1-67.
- 参照実装: [`nbx-liz/AdvancedCATDAP/advanced_catdap/components/scoring.py`](https://github.com/nbx-liz/AdvancedCATDAP/blob/main/advanced_catdap/components/scoring.py)
- 研究フェーズ詳細: [`docs/research/h0005-continuous-target.md`](docs/research/h0005-continuous-target.md)

---

## 2026-05-27: Phase B 二変量 API(`plot_pair` / `aic_heatmap` / `association_matrix` / `association_plot`)

- ID: `H-0006`
- Status: `accepted`
- Scope: `API | scope`
- Related: `H-0001 Phase B`, `H-0002 FR-3`, `H-0004`, `BLUEPRINT.md §3, §5.7`, Issue #13

### Context

H-0004 / H-0005 で **目的変数指向**(asymmetric)の `target_summary` / `plot_target` は揃った。一方、`H-0001 Phase B`(Issue #13)が想定している残りの 4 つの公開 API は、いずれも **対称な二変量** または **多変数まとめ** の視点を提供するもので、未着手:

| API | 視点 | 必要性 |
|---|---|---|
| `plot_pair(df, x, y)` | 任意の 2 変数(対称) | EDA で `target` が定まっていない初手の探索 |
| `aic_heatmap(catdap1_result)` | m×m ΔAIC をヒートマップ化 | `Catdap1Result.aic` の DataFrame 表示は読みにくい |
| `association_matrix(df, measure=...)` | 全列ペアの関連度行列 | `catdap1` は **response 軸を指定する** ため対称行列を直接返さない |
| `association_plot(table)` | vcd 風 Pearson 残差ヒートマップ | `TargetSummary.pearson_residuals` の数値 DataFrame は解釈が重い |

H-0004 §A1 で「`plot_pair` は対称設計のため Phase B に分離」と明記済み。本 Proposal はその約束を回収する。

### 競合分析(対象パッケージ)

| Package | 該当機能 | 形式 | pycatdap での参考点 |
|---|---|---|---|
| **R `vcd::assoc(table, shade=TRUE)`** | 標準化残差ヒートマップ | mosaic + Pearson 残差で色付け | `association_plot` のリファレンス |
| **R `vcd::pairs(table)`** | 多変数 mosaic マトリクス | 全ペアの mosaic を grid 配置 | `plot_pair` の対称版に類似 |
| **seaborn `heatmap(corr_matrix)`** | 相関行列のヒートマップ | 連続変数の Pearson 相関を全ペアで | `association_matrix` + `aic_heatmap` の参考(連続のみ) |
| **ydata-profiling Correlations タブ** | 関連度行列 | `phi_k` / Cramér's V / Spearman 等を選択 | `association_matrix(measure=...)` の参考 |
| **plotly `imshow`** | ヒートマップ | matrix → interactive heatmap | plotly backend の実装方針 |
| **sweetviz Associations** | 関連度行列 | Cramér's V + 相関比、対角=NaN | `association_matrix` の出力契約 |

**学び**:
- 残差ヒートマップは **diverging colormap**(負=青、正=赤、ゼロ=白)+ 閾値線(±2σ)を引くのが業界標準(vcd)
- 関連度行列の対角は **NaN**(自己関連は意味なし)が pandas / seaborn / sweetviz の共通慣習
- 「**測度を選べる**」設計(`measure=` キーワード)が `phi_k` / Cramér's V / mutual_info の並立を可能にする
- `aic_heatmap` の色は **ΔAIC < 0 が informative**(Issue #13 では緑、≥ 0 で赤を指定)— これは vcd の「informative=高彩度」と方向は一致するが、AIC は **0 が baseline** という追加意味があるため diverging colormap の中心を 0 にする必要がある

### Proposal

#### 公開 API(新規 4 関数)

```python
# B1. 対称ラッパー: plot_pair
pycatdap.plot_pair(
    df: pd.DataFrame,
    x: str,
    y: str,
    *,
    kind: Literal["auto", "stacked", "mosaic", "violin", "box", "hist",
                   "scatter", "bin_means"] = "auto",
    bins: int | Sequence[float] | None = None,
    backend: Literal["matplotlib", "plotly"] = "matplotlib",
    **kwargs: Any,
) -> Any
```

**応答側の決定ルール**(`plot_pair` 専用、`plot_target` には影響しない):

| `x` dtype | `y` dtype | response として選ぶ側 | 根拠 |
|---|---|---|---|
| categorical / boolean | categorical / boolean | `y`(慣習: 縦軸=応答) | seaborn / vcd の formula 順序に一致 |
| categorical / boolean | continuous | `x`(離散側) | Pearson 残差の解釈は離散側を応答とする方が自然(H-0004 §A1) |
| continuous | categorical / boolean | `y`(離散側) | 同上 |
| continuous | continuous | `y`(慣習: 縦軸=応答) | H-0005 回帰モードでは `y` を target、`x` を explanatory |

ルール確定後は `plot_target(df, target=<response>, explanatory=<other>, kind=kind, bins=bins, backend=backend, **kwargs)` に **完全に委譲** する。`plot_pair` 単体ではロジックを持たない(対称→非対称の翻訳のみ)。

#### B2. `aic_heatmap`

```python
pycatdap.aic_heatmap(
    result: Catdap1Result | pd.DataFrame,
    *,
    threshold: float | None = 0.0,        # 強調する ΔAIC 閾値
    backend: Literal["matplotlib", "plotly"] = "matplotlib",
    **kwargs: Any,
) -> Any
```

- `Catdap1Result` を受け取った場合は `result.aic` を内部で使用
- `pd.DataFrame` を受け取った場合は **rows=response, cols=explanatory** と解釈(`association_matrix` の戻り値と互換)
- カラーマップ: **diverging**(`RdYlGn_r` 互換 — ΔAIC < 0=緑、> 0=赤、中心 0=白)
- `threshold` が指定された場合、各セルのテキストに `*` を付与(`< threshold` のセル)
- 対角(self)は NaN なので白(透明)表示

#### B3. `association_matrix`

```python
pycatdap.association_matrix(
    df: pd.DataFrame,
    *,
    measure: Literal["aic"] = "aic",     # v0.4.0 では "aic" のみ
    bins: int | None = None,             # 連続変数の binning
    criterion: Literal["aic", "aicc", "bic"] = "bic",   # 連続 target 時
) -> pd.DataFrame
```

- 戻り値: 正方 DataFrame, rows=`df.columns`, cols=`df.columns`, **対角=NaN**
- `measure="aic"`: 各セル `(i, j)` は **`target_summary(df, target=i, explanatory=j).delta_aic`** を格納
  - 連続 target × 連続 explanatory は H-0005 の `RegressionTargetSummary.delta_aic`
  - 連続 target × カテゴリ explanatory も H-0005 経由
  - カテゴリ target × * は H-0004 経由
- **非対称**(`M[i, j] != M[j, i]`):「i を target としたとき j がどれだけ説明するか」と「j を target としたとき i がどれだけ説明するか」は別物。これを行列で同時に提示することで、対称性の崩れ自体がユーザーへの情報になる
- `measure="cramers_v"` / `"mutual_info"` は **本 Proposal のスコープ外**(後続 H-0007 等で追加。H-0002 `measures/` プラグイン層が前提)

#### B4. `association_plot`

```python
pycatdap.association_plot(
    table: pd.DataFrame | TargetSummary,
    *,
    threshold: float = 2.0,              # |residual| > threshold を強調
    backend: Literal["matplotlib", "plotly"] = "matplotlib",
    **kwargs: Any,
) -> Any
```

- `TargetSummary` を受け取った場合は `table.pearson_residuals` を内部で使用
- `pd.DataFrame` を直接受け取る場合は **クロス頻度表** と解釈し、内部で Pearson 標準化残差を計算
- カラーマップ: **diverging**(青=負、赤=正、白=ゼロ)— vcd `assoc(shade=TRUE)` 互換
- `threshold` を超えるセルは **アスタリスク** をオーバーレイ(matplotlib)/ hover text(plotly)
- `RegressionTargetSummary` は対象外(連続 target には Pearson 残差概念がない)— 渡された場合 `TypeError` を上げ、`plot_target(kind="scatter")` を推奨するエラーメッセージを返す

#### dispatch / 配置

- `src/pycatdap/_association.py`(新規)— `association_matrix` のロジック(全ペア走査)を集約
- `src/pycatdap/plot/__init__.py` に 3 つの dispatcher(`plot_pair`, `aic_heatmap`, `association_plot`)を追加
- `src/pycatdap/plot/matplotlib.py` / `plotly.py` に各 backend 実装を追加
  - `plot_pair`: `plot_target` への委譲のみ(backend ごとの実装は不要)
  - `aic_heatmap` / `association_plot`: backend ごとに heatmap を実装
- `src/pycatdap/__init__.py` に再 export: `plot_pair`, `aic_heatmap`, `association_matrix`, `association_plot`

### Impact

- **公開 API の追加のみ**(4 関数)
- 既存 API への破壊的変更なし
- 新規モジュール: `src/pycatdap/_association.py`
- 既存モジュール変更: `src/pycatdap/plot/__init__.py` / `matplotlib.py` / `plotly.py` / `__init__.py`
- `BLUEPRINT.md §3`(モジュール構成)と `§5.7`(plotting テーブル)を改訂
- 任意依存の追加なし(matplotlib / plotly は既存 extras)

### Compatibility

- **後方互換**: 完全
- 既存の `target_summary` / `plot_target` / `Catdap1Result` への変更なし
- `plot_pair` は `plot_target` に委譲するため、`plot_target` の挙動変更がそのまま伝播する(`plot_pair` 単体の挙動を別 spec で固定はしない)

### Alternatives Considered

#### A1: `plot_pair` を `plot_target` とは独立のロジックで再実装
- **不採用理由**: 同じ dispatch を 2 つ保守するのは反 DRY。`plot_target` を改訂したときに `plot_pair` の auto 選択が乖離する事故を招く。委譲することで H-0004 / H-0005 の改善が自動的に `plot_pair` にも反映される。

#### A2: `association_matrix` を **対称化**(`(M + M.T) / 2` を返す)
- **不採用理由**: ΔAIC は **「i を target としたときの j の情報量」** という方向性のある量。対称化すると `cramers_v` や `phi_k` と区別がつかなくなり、AIC の優位性(モデル選択フレームワーク)を捨てる。非対称のまま提示する方が「**変数 i は j からよく説明されるが、逆は弱い**」というアサイメトリ自体を発見できる(因果探索の手がかり)。

#### A3: `association_matrix(measure="cramers_v" | "mutual_info")` を本 PR に同梱
- **不採用理由**: BLUEPRINT §5.11 で planned 状態の `measures/` プラグイン層(H-0002 で言及)が未実装。先に `measures/` 層を入れるか、本 PR では `aic` のみで出して別 Proposal(H-0007)で他測度を追加する方が、テストもレビューも軽い。

#### A4: `aic_heatmap` を **対角を 0 で埋める**(NaN は白だが意味不明)
- **不採用理由**: 自己 ΔAIC は数学的に未定義(`catdap1` も NaN を返す慣習)。0 で埋めると「自己関連が baseline と同等」というミスリードを生む。NaN を白(透明)表示し、tooltip / legend で「diagonal: undefined」と明記する方が誠実。

#### A5: `association_plot` を **`mosaic_plot` + shade=True フラグ** として既存に追加
- **不採用理由**: mosaic と heatmap は表現が根本的に異なる(mosaic は面積エンコード、heatmap は色エンコード)。`association_plot` は **heatmap 専用** で残差の数値解釈に特化する方が役割分担が明確。`mosaic_plot(table, shade=True)` を別途追加するのは将来の検討事項。

#### A6: `plot_pair` の応答決定ルールを **常に `y` を target** にする(seaborn 慣習に統一)
- **不採用理由**: カテゴリ × 連続のペアで連続側を target にすると、`plot_target` は H-0005 回帰モードに入る。連続変数を「目的」として扱うのは EDA 初手としては重い解釈になる。**離散側を優先** することで「カテゴリの違いによる連続変数の分布変化」という解釈しやすい view に揃える。

### Acceptance Criteria

#### API
- [ ] `pycatdap.plot_pair(df, x, y)` が matplotlib / plotly 両 backend で動作
- [ ] `plot_pair` の応答決定ルール 4 パターン(cat×cat / cat×cont / cont×cat / cont×cont)を unit テストで確認
- [ ] `pycatdap.aic_heatmap(catdap1_result)` が `Catdap1Result` と `pd.DataFrame` の両方を受け取れる
- [ ] `pycatdap.aic_heatmap` が両 backend で動作、diverging colormap で中心 0
- [ ] `pycatdap.association_matrix(df, measure="aic")` が正方 DataFrame を返し、対角 NaN、shape=(m, m)
- [ ] `association_matrix` の `M.loc[i, j]` が `target_summary(df, target=i, explanatory=j).delta_aic` と一致(全 (i,j) ペア)
- [ ] `pycatdap.association_plot(table)` が `TargetSummary` と `pd.DataFrame`(クロス頻度)の両方を受け取れる
- [ ] `association_plot` に `RegressionTargetSummary` を渡すと `TypeError` を `plot_target(kind="scatter")` を推奨するメッセージ付きで上げる
- [ ] 4 関数すべてに `**kwargs` フォワード機構あり

#### 数値整合
- [ ] `aic_heatmap` が表示する数値が `Catdap1Result.aic` の DataFrame の数値と一致
- [ ] `association_matrix(df, measure="aic")` の `M.loc[i, i]` が NaN
- [ ] `association_plot(target_summary(df, t, e))` のセル色が Pearson 残差の符号と一致(`> threshold` で強調)

#### コード品質
- [ ] `tests/test_plot_pair.py` に dispatch テスト 8 件以上(4 dtype 組合せ × 2 backend)
- [ ] `tests/test_aic_heatmap.py` に backend / 入力型 / colormap テスト 6 件以上
- [ ] `tests/test_association.py` に `association_matrix` + `association_plot` のテスト 10 件以上(計算正しさ・対角 NaN・対称性チェック・kwargs フォワード・回帰結果拒否)
- [ ] coverage 80%+ 維持
- [ ] `mypy --strict` pass
- [ ] 4 関数すべてに NumPy style docstring + `Examples` セクション

#### ドキュメント
- [ ] `BLUEPRINT.md §3` のモジュール構成図に `_association.py` を追記
- [ ] `BLUEPRINT.md §5.7` の plotting 関数一覧に 4 関数を追記
- [ ] 新規 tutorial `docs/tutorials/07-bivariate-phase-b.ipynb`(別 PR、PR-B4)
- [ ] `docs/tutorials/index.md` に Notebook 07 を追加

### PR 分割

実装は **4 PR** に分割する:

| PR | スコープ | 依存 |
|---|---|---|
| **PR-B0**(本 Proposal) | `docs(history): propose H-0006` | none |
| **PR-B1** | `plot_pair`(委譲ラッパー)+ tests | PR-B0 merge |
| **PR-B2** | `aic_heatmap` + `association_matrix(measure="aic")` + `_association.py` + tests | PR-B1 merge |
| **PR-B3** | `association_plot` + tests | PR-B2 merge |
| **PR-B4** | tutorial Notebook 07 + BLUEPRINT 反映 + Issue #13 close | PR-B3 merge |

各 PR は CI green を確認してから次に進む(`feedback_pr_dirty_blocks_ci` に従う)。

### Decision

- Date: `2026-05-27`
- Result: `accepted`
- Notes: PR-B0(#62)で Proposal 承認。実装は 4 PR に分けて develop へ:
  - PR-B1(#63): `plot_pair`(committed `f328c68`)
  - PR-B2(#64): `aic_heatmap` + `association_matrix` + `_association.py`(committed `490b5f1`、CI で `np.ma` untyped 問題 2 回踏んで `cmap.set_bad` に切替)
  - PR-B3(#65): `association_plot`(committed `c9be5b3`)
  - PR-B4: tutorial Notebook 07 + BLUEPRINT 反映 + Issue #13 close(本 PR)
  - 全 4 関数の合計 76 テスト(plot_pair 21 + association_matrix 15 + aic_heatmap 14 + association_plot 16 + 重複ラッパー除く)、最終 coverage 82.02%

### Migration

破壊的変更なし。新規 API のため移行不要。CHANGELOG `[Unreleased]` の `Added` に 4 関数を順次記載する(PR 毎)。

### Related References

- R `vcd::assoc` / `vcd::pairs`(Friendly, M.): <https://cran.r-project.org/package=vcd>
- ydata-profiling Correlations: <https://docs.profiling.ydata.ai/>
- sweetviz Associations: <https://github.com/fbdesignpro/sweetviz>
- seaborn heatmap: <https://seaborn.pydata.org/generated/seaborn.heatmap.html>
- Pearson standardized residuals(Agresti, 2002, *Categorical Data Analysis*, §3.2)
- 親仕様: H-0001 §Phase B、H-0004 §A1(plot_pair の Phase B 分離決定)

---

## 2026-05-27: Phase C ワンコール EDA — `profile()` + HTML レポート

- ID: `H-0007`
- Status: `accepted`
- Scope: `API | scope | dependencies`
- Related: `H-0001 Phase C`, `H-0002 FR-1`, `H-0004`, `H-0005`, `H-0006`, `BLUEPRINT.md §3, §5.9`, Issue #14

### Context

v0.4.0 で揃った EDA 基盤(`describe` / `target_summary` / `plot_target` / `association_matrix` / `aic_heatmap` / `catdap1` / `catdap2`)を **1 関数呼び出し** にまとめ、HTML レポートとして出力できる **フラッグシップ API** を提供する。pycatdap が「AIC ベース EDA + ML 誤差分析ライブラリ」として再定位された H-0001 において最も重要なユーザーフェイスとなる API。

競合は `ydata-profiling.ProfileReport` / `skrub.TableReport` だが、両者にはない pycatdap の差別化:

- **AIC 駆動の変数ランキング**(他は Cramér's V / phi_k / 相関係数のみ)
- **連続変数の AIC 最適 binning**(`_pooling.optimal_binning` を可視化に組み込む)
- **CATDAP-02 トップ K サブセット**(他は単一変数ランキングのみ)
- **target 指向と target-free モード両対応**(`response=None` でも動作)

### 競合分析(対象パッケージ)

| Package | ワンコール API | 出力形式 | pycatdap が学ぶ点 |
|---|---|---|---|
| **ydata-profiling** | `ProfileReport(df).to_file("report.html")` | self-contained HTML、Overview/Variables/Interactions/Correlations/Missing/Sample/Duplicates | セクション構成 / Plotly インライン |
| **skrub.TableReport** | `TableReport(df).open()` | HTML + JavaScript インタラクション、列ごとの type/cardinality/distribution カード | カード型レイアウト / カラム並び替え |
| **dataprep `create_report`** | `create_report(df).save("report.html")` | static HTML、相関ヒートマップ + 分布 | レポート構造の参考 |
| **pandas-profiling**(旧称) | `ProfileReport(df)` | ydata-profiling と同じ系列 | レガシー、参考度低 |
| **sweetviz** | `sv.analyze(df, target_feat=...).show_html()` | target 比較 | target awareness の参考(H-0004 で既に採用) |

**学び**:
- **「1 行 + `.to_html()`」が業界標準のシグネチャ** — `pycatdap.profile(df, response=...).to_html(path)`
- **single self-contained HTML** がデフォルト体験(メール / Slack で 1 ファイル送付できる)
- **target awareness は OPTIONAL**(`response=None` でも有用なレポート)
- **セクション分け**: Overview → Variables → Pairwise(AIC heatmap) → Top subsets → Quality warnings の順が解釈しやすい

### Proposal

#### 公開 API(新規 1 関数 + 1 dataclass)

```python
pycatdap.profile(
    df: pd.DataFrame,
    *,
    response: str | None = None,          # 指定で target-driven セクション追加
    bins: int | None = None,              # association_matrix に forward
    criterion: Literal["aic", "aicc", "bic"] = "bic",  # 連続 target 時
    top_k_subsets: int = 5,               # CATDAP-02 トップ K
    quality_thresholds: dict[str, float] | None = None,  # 品質警告閾値
) -> ProfileResult
```

返り値 `ProfileResult` は frozen dataclass:

| 属性 | 型 | 内容 |
|---|---|---|
| `overview` | `dict[str, Any]` | 行数 / 列数 / 欠損率 / 重複行 / メモリ / dtype カウント |
| `variables` | `list[VariableCard]` | 列ごとの型 / カーディナリティ / 欠損 / top カテゴリ / ΔAIC vs response(指定時) |
| `association` | `pd.DataFrame` | m × m ΔAIC 行列(`association_matrix` 結果) |
| `top_subsets` | `Catdap2Result \| None` | response 指定時のみ。`catdap2(df, response_name=..., nvar=top_k_subsets)` |
| `quality_warnings` | `list[QualityWarning]` | 高カーディナリティ / 定数列 / ID 候補 / 高欠損列 |
| `response` | `str \| None` | 入力 response 引数(レポートヘッダ表示用) |
| `n_rows` / `n_cols` | `int` | overview からも引けるが頻用するため top-level に露出 |

`VariableCard` は別 frozen dataclass:

```python
@dataclass(frozen=True)
class VariableCard:
    name: str
    kind: str                           # "categorical" / "continuous" / "boolean" / "datetime" / "other"
    n_obs: int
    n_missing: int
    n_unique: int
    top_value: Any                      # 最頻値
    top_freq: int                       # 最頻値の出現回数
    stats: dict[str, float] | None      # 連続変数: mean/std/min/q25/median/q75/max
    delta_aic_vs_response: float | None # response 指定時のみ
    intervals: list[float] | None       # 連続変数の AIC 最適 binning 境界(任意)
```

`QualityWarning` も frozen dataclass:

```python
@dataclass(frozen=True)
class QualityWarning:
    severity: Literal["info", "warning"]
    kind: Literal["high_cardinality", "constant", "id_candidate", "high_missing"]
    column: str
    message: str                        # 人間可読
    metric: float                       # threshold 比較に使った数値
```

#### 品質警告のデフォルト閾値

| Warning kind | デフォルト閾値 | 根拠 |
|---|---|---|
| `high_cardinality` | `nunique / n_obs > 0.5` かつ `nunique > 50` | カーディナリティが行数の半分以上で 50 超 → 識別子の可能性 |
| `constant` | `nunique <= 1`(欠損除外後) | 完全定数列は AIC 計算で無意味 |
| `id_candidate` | `nunique == n_obs` かつ `kind == "categorical"` | 全行一意のカテゴリ列は ID |
| `high_missing` | `missing_rate > 0.5` | 半分以上欠損は CATDAP で使い物にならない |

ユーザーは `quality_thresholds={"high_cardinality": 0.7, "high_missing": 0.3}` で上書き可能。

#### メソッド

```python
class ProfileResult:
    def show(self) -> None
        # Jupyter inline 表示: Overview を pandas table、aic_heatmap を inline figure
    def to_html(self, path: str | Path | None = None) -> str
        # jinja2 テンプレートで single self-contained HTML を生成
        # Plotly figure は include_plotlyjs=True で **インライン同梱**(オフライン可)
        # path=None なら HTML 文字列を返すのみ
        # path 指定時は atomic write(_io.atomic_write_text、H-0005 の慣習)
    def to_dict(self) -> dict[str, Any]
        # JSON シリアライズ可能な dict 化
    def to_plotly_json(self) -> dict[str, Any]
        # ProfileResult 全体を {section_name: plotly_spec} で返す(LizyStudio 連携、DP-4)
```

#### 実装配置

- `src/pycatdap/profile.py`(新規)— `profile()`, `ProfileResult`, `VariableCard`, `QualityWarning`
- `src/pycatdap/templates/profile.html.j2`(新規)— jinja2 テンプレート
- `src/pycatdap/templates/__init__.py`(新規)— `importlib.resources` 経由でテンプレート読み込み
- `pyproject.toml`: `jinja2>=3.1` を **`[plotly]` extra に追加**(BLUEPRINT 通り。`profile()` 自体は core 機能だが、`.to_html()` を呼ぶ場合のみ jinja2 必要)
- `src/pycatdap/__init__.py`: `profile`, `ProfileResult`, `VariableCard`, `QualityWarning` を再 export

HTML テンプレートの段組:

```
┌─────────────────────────────────────────┐
│ pycatdap profile: <dataset name>        │
│ Generated: 2026-05-27 by pycatdap v0.5  │
├─────────────────────────────────────────┤
│ ## Overview                             │
│ rows / cols / missing% / duplicates / mem │
├─────────────────────────────────────────┤
│ ## Quality warnings (collapsed if empty)│
├─────────────────────────────────────────┤
│ ## Variables (grid of cards)            │
│ [card1] [card2] [card3] [card4]         │
│ [card5] [card6] ...                     │
├─────────────────────────────────────────┤
│ ## Pairwise associations                │
│ <plotly heatmap of association_matrix>  │
├─────────────────────────────────────────┤
│ ## Top subsets (response=<r> only)      │
│ <plotly bar of CATDAP-02 top-K>         │
└─────────────────────────────────────────┘
```

### Impact

- **公開 API の追加のみ**(1 関数 + 3 dataclass + 1 サブパッケージ `templates/`)
- 既存 API への破壊的変更なし
- 任意依存: **jinja2 を `[plotly]` extra に追加**(既に BLUEPRINT に計画あり)
- 新規モジュール: `src/pycatdap/profile.py`, `src/pycatdap/templates/`
- 既存モジュール変更: `src/pycatdap/__init__.py`(再 export)、`pyproject.toml`(jinja2 追加 + package-data に templates 同梱)
- `BLUEPRINT.md §3.1`(モジュール構成)と `§5.9`(profile セクション)を改訂

### Compatibility

- **後方互換**: 完全
- `jinja2` は新規 optional dep。`.to_html()` を呼ばないなら追加インストール不要
- Plotly インラインは `pycatdap[plotly]` extras 必須(既存)

### Alternatives Considered

#### A1: CDN ロードを採用してファイルサイズを小さくする
- **不採用理由**: ユーザー希望(オフライン優先)。エンタープライズ環境では CDN access が制限されることが多い。+3MB 程度は許容できる(mkdocs build や Confluence 添付でも問題ない)。

#### A2: jinja2 を必須依存にする
- **不採用理由**: pycatdap の core は numpy/pandas のみで動く設計を維持したい。`.to_html()` 呼んだ時点で `ImportError` メッセージで `pycatdap[plotly]` インストールを促すパターンが既存(plotly 同様)。

#### A3: `ProfileResult` を mutable にしてユーザーがセクションを足せるようにする
- **不採用理由**: `DescribeResult` / `TargetSummary` 等の既存 dataclass はすべて `frozen=True`。ユーザー拡張は `to_dict()` 経由で取り出して別途構築する設計に揃える。

#### A4: HTML テンプレートを `src/pycatdap/profile.py` にハードコード
- **不採用理由**: 多段組 HTML を Python 文字列で書くと改行 / インデント / エスケープが地獄。jinja2 を入れた方が変更容易性が高い。

#### A5: `top_subsets` を `catdap2` 直接呼び出しではなく ユーザー側で渡す設計
- **不採用理由**: 「1 コール」エルゴノミクスが崩れる。`profile(df, response=...)` だけで catdap2 が走る必要がある。

#### A6: `Variables` セクションに連続変数の AIC 最適 binning ヒストグラムを **必ず** 含める
- **採用検討**: BLUEPRINT §5.9 にも書かれている要素。**初期 PR では VariableCard.intervals 属性として境界値のみ保持**、HTML テンプレート側でその境界を histogram に重ねて描く方式とする。これにより VariableCard データ構造は plot-backend non-dependent を保てる。

#### A7: `quality_warnings` を **HTML レポートの折り畳みアコーディオン** にする
- **採用**(マイナー設計): 警告 0 件のとき空セクションが残ると見栄え悪い。jinja2 `{% if quality_warnings %}` で条件付き表示。

### Acceptance Criteria

#### API
- [ ] `pycatdap.profile(df)` が `ProfileResult` を返す(response 省略可)
- [ ] `pycatdap.profile(df, response="col")` で `top_subsets` 付き ProfileResult を返す
- [ ] `ProfileResult` に `.show / .to_html / .to_dict / .to_plotly_json` の4メソッド
- [ ] `to_html(path)` で **単一の self-contained HTML** ファイルを生成
- [ ] Plotly figure はインライン同梱(オフライン閲覧可)、HTML は外部ファイル参照なし
- [ ] `to_html()` (path=None) で HTML 文字列を返す
- [ ] `to_html(path)` は `_io.atomic_write_text` 経由で原子的書き込み(H-0005 慣習)
- [ ] `VariableCard` / `QualityWarning` が frozen dataclass、JSON シリアライズ可能

#### 品質警告
- [ ] デフォルト閾値で 4 種類の警告(`high_cardinality` / `constant` / `id_candidate` / `high_missing`)を発出
- [ ] `quality_thresholds=` で各閾値を上書き可能

#### パフォーマンス
- [ ] 10k 行 × 20 列 のランダムデータで **`profile()` 実行が 5 秒以内** に完了(Issue #14 受入条件)
- [ ] `to_html()` 自体は ≤ 2 秒(jinja2 レンダリング + plotly インライン化)

#### コード品質
- [ ] `tests/test_profile.py` に unit テスト 20 件以上(各セクション / 各 dataclass / 各メソッド / response あり/なし / 品質警告 4 種 / atomic write 検証)
- [ ] `tests/test_profile_html.py` に HTML レポートテスト 8 件以上(自己完結性確認 / Plotly インライン確認 / 全セクション存在確認 / 警告 0 件時の表示確認)
- [ ] coverage 80%+ 維持
- [ ] `mypy --strict` pass(jinja2 stubs は `[[tool.mypy.overrides]]` で `ignore_missing_imports`)
- [ ] 全公開 API に NumPy style docstring + `Examples` セクション

#### ドキュメント
- [ ] `BLUEPRINT.md §3.1` のモジュール構成に `profile.py` / `templates/` を追記
- [ ] `BLUEPRINT.md §5.9` を実装後の確定 API に合わせて改訂
- [ ] 新規 tutorial `docs/tutorials/08-profile-titanic.ipynb`(PR-C3、`profile()` をフル活用)
- [ ] `docs/tutorials/index.md` + `mkdocs.yml` に Notebook 08 を追加
- [ ] `README.md` の Quickstart に `profile()` 例を追加(v0.5.0 の「目玉機能」として)

### PR 分割

実装は **4 PR** に分割する(Phase B と同じケイデンス):

| PR | スコープ | 依存 |
|---|---|---|
| **PR-C0**(本 Proposal) | `docs(history): propose H-0007` | none |
| **PR-C1** | `profile.py`(`profile()` + `ProfileResult` + `VariableCard` + `QualityWarning` + `show()` + `to_dict()` + `to_plotly_json()`)+ tests | PR-C0 merge |
| **PR-C2** | `templates/profile.html.j2` + `to_html()` + jinja2 dep 追加 + HTML テスト | PR-C1 merge |
| **PR-C3** | Tutorial Notebook 08 + BLUEPRINT 反映 + README 更新 + Issue #14 close | PR-C2 merge |

各 PR は CI green を確認してから次に進む。`feedback_release_pr_dirty_squash_trap` 通り、これらは全て develop に **squash** で merge して OK(release 時の sync PR だけが `--merge` 必須)。

### Decision

- Date: `2026-05-27`
- Result: `accepted`
- Notes: PR-C0(#71)で Proposal 承認。実装は 4 PR に分けて develop へ:
  - PR-C1(#72): `profile.py` core(`profile` + 3 dataclasses + `.show / .to_dict / .to_plotly_json`)
    — committed `0c9b316`。CI で 2 周踏んだ教訓: (a) `# type: ignore[assignment]` を `display = None` に
    付けると CI(IPython 未インストール)で unused-ignore → `feedback_mypy_ipython_display` 違反、
    (b) `to_plotly_json` から plotly backend を import すると `Quality (lowest-direct deps)` で
    ImportError、`Catdap1Result.to_plotly_json` と同じく dict 直接構築すべき
  - PR-C2(#73): jinja2 HTML テンプレート + `.to_html()` — committed `83e47a2`。
    `importlib_resources` fallback も CI で `[unused-ignore]` を踏んだ(Python 3.10+ は stdlib に
    `importlib.resources.files` あり、fallback 不要)
  - PR-C3: Tutorial Notebook 08 + BLUEPRINT / mkdocs / tutorials/index.md 反映 + Issue #14 close
    (本 PR)
  - 全テスト 392 + Notebook 08 1 件、coverage 83.32%

### Migration

破壊的変更なし。新規 API のため移行不要。CHANGELOG `[Unreleased]` の `Added` に `profile()`, `ProfileResult`, `VariableCard`, `QualityWarning` を順次記載する(PR 毎)。

`jinja2` を `pycatdap[plotly]` extras に追加 — 既存 `pycatdap[plotly]` ユーザーは `pip install -U "pycatdap[plotly]"` で自動取り込み。

### Related References

- ydata-profiling: <https://docs.profiling.ydata.ai/>
- skrub TableReport: <https://skrub-data.org/stable/auto_examples/01_encodings.html>
- dataprep `create_report`: <https://docs.dataprep.ai/>
- sweetviz: <https://github.com/fbdesignpro/sweetviz>
- jinja2: <https://jinja.palletsprojects.com/>
- Plotly HTML embed options: <https://plotly.com/python/interactive-html-export/>
- 親仕様: H-0001 §Phase C、H-0002 FR-1

---

## 2026-05-28: Phase D ターゲット分析 + 品質レポート + Pluggable measures + CI 統合 Suite

- ID: `H-0008`
- Status: `proposed`
- Scope: `API | scope | dependencies`
- Related: `H-0001 Phase D`, `H-0002 FR-10 / DP-6`, `H-0007`, `BLUEPRINT.md §5.10 / §5.11`, Issue #15

### Context

v0.5.0 で flagship `pycatdap.profile()` を出荷し、EDA 用途の「ワンコール」体験は揃った。
Phase D ではこの体験を **target 駆動分析** と **CI 統合可能な品質ゲート** に拡張する。

| 課題 | 既存 API | 不足している点 |
|---|---|---|
| 「response 列に対して全説明変数を ΔAIC でランキングしたい」 | `target_summary(df, target, expl)` を for ループで回す | 直接 API がなく、ユーザー側でループ + 整形が必要 |
| 「データ品質ウォーニングだけ手早く取り出したい」 | `profile(df).quality_warnings` | profile が catdap2 / association_matrix まで走るので過剰 |
| 「Cramér's V / 相互情報量で関連度を測りたい」 | `association_matrix(df, measure='aic')` のみ | `measure='cramers_v'` 等が `H-0007 / H-0006` で「H-0007 で予定」と書きながら未実装 |
| 「CI で『この CSV は使い物にならない』を pytest に統合したい」 | なし | 各 warning を例外/assert に変換する標準パターンがない |

これらを **Phase D の 4 つの追加 API** で解決する。

### 競合分析(対象パッケージ)

| Package | API | 学ぶ点 |
|---|---|---|
| **deepchecks** | `Suite([HasMissing(), MixedNulls()]).run(dataset)` → `SuiteResult.passed` / `.save_as_html()` | Check / Suite / SuiteResult 階層、CI 統合パターン |
| **great-expectations** | `expect_column_values_to_not_be_null(...)` の宣言的 expectation | Check の宣言的 API スタイル |
| **pandera** | `pa.DataFrameSchema({'col': pa.Column(int, checks=...)}).validate(df)` | Pythonic な schema-as-data |
| **ydata-profiling alerts** | `report.alerts` で missing / cardinality 警告を保持 | 警告 enum + threshold のレイアウト(quality_report と同方向) |
| **phik / phi_k** | `df.phik_matrix()` で混合型相関行列 | mixed-type 関連度の参考(measures/) |

**学び**:
- **`Suite([check1, check2]).run(dataset)` が業界標準シグネチャ** — Phase D の suite はこれに合わせる
- **Check は thresholds をコンストラクタで受ける小さなクラス** — `eval()` 不要のデータ宣言
- **`SuiteResult.passed: bool`** が CI assert の鍵 — 各 check の condition を boolean に集約
- **measures の register API** はユーザーが `pycatdap.measures.register("phi_k", fn)` する形式が pysubgroup 互換

### Proposal

#### 公開 API(新規 4 関数 + 4 dataclass + 2 サブパッケージ)

```python
# 1. target 駆動分析
result = pycatdap.target_analysis(
    df,
    response="symptoms",
    *,
    top_k=5,
    bins=None,
    criterion="bic",
    measure="aic",
) -> TargetAnalysisResult

# 2. 品質レポート
qr = pycatdap.quality_report(
    df,
    *,
    quality_thresholds=None,
) -> QualityReport

# 3. CI 統合可能な suite(deepchecks 互換 API per Issue #15)
suite = pycatdap.suite.AICIndependenceSuite(df, response="symptoms")
suite_result = suite.run() -> SuiteResult
assert suite_result.passed, suite_result.summary()

# 個別 check も独立利用可能
check_result = pycatdap.suite.HighCardinalityCheck(max_categories=50).run(df) -> CheckResult

# 4. measures pluggable interface
pycatdap.measures.aic(cross_freq) -> float
pycatdap.measures.cramers_v(cross_freq) -> float
pycatdap.measures.mutual_info(cross_freq) -> float
pycatdap.measures.register("my_measure", fn)
# association_matrix が measure 引数を受けるよう拡張
m = pycatdap.association_matrix(df, measure="cramers_v")
```

#### 1. `target_analysis()` 設計

```python
@dataclass(frozen=True)
class TargetAnalysisResult:
    response: str
    ranking: pd.DataFrame             # columns: variable, delta_aic, kind, n_obs
    top_summaries: dict[str, TargetSummary | RegressionTargetSummary]
                                      # 上位 top_k 列の TargetSummary
    response_card: VariableCard       # response 列自体の card(profile() 流用)
    n_rows: int
    n_cols: int

    def show(self) -> None: ...
    def to_html(self, path: str | Path | None = None) -> str: ...
    def to_dict(self) -> dict[str, Any]: ...
    def to_plotly_json(self) -> dict[str, Any]: ...
```

実装:
- `target_summary(df, target=response, explanatory=col)` を全列に対して実行(`profile()` と同じパターン)
- `delta_aic` で sort し top-K の TargetSummary をフル保持
- HTML テンプレートは `templates/target_analysis.html.j2` 新規(profile.html.j2 と段組共通化)

#### 2. `quality_report()` + `QualityReport` 設計

```python
@dataclass(frozen=True)
class QualityReport:
    warnings: list[QualityWarning]    # H-0007 で定義済みの dataclass を流用
    n_rows: int
    n_cols: int

    def by_severity(self) -> dict[str, list[QualityWarning]]: ...
    def by_kind(self) -> dict[str, list[QualityWarning]]: ...
    def show(self) -> None: ...
    def to_html(self, path: str | Path | None = None) -> str: ...
    def to_dict(self) -> dict[str, Any]: ...
    def to_plotly_json(self) -> dict[str, Any]: ...

    @property
    def passed(self) -> bool:
        """No "warning"-severity findings — convenient for CI assert."""
        return not any(w.severity == "warning" for w in self.warnings)
```

実装:
- **`_scan_quality` を `src/pycatdap/_quality.py` に切り出す**(profile.py / quality_report() の両方が同じ helper を呼ぶ)
- `profile.py` 側は `from pycatdap._quality import _scan_quality` に置き換え(behavior 不変、純粋 refactor)
- `quality_report()` は内部で `_build_variables(df, response=None)` + `_scan_quality()` のみ実行(catdap2 / association_matrix は走らない → profile() より大幅高速)

#### 3. `suite/` サブパッケージ設計

```
src/pycatdap/suite/
  __init__.py              # AICIndependenceSuite, SuiteResult, CheckResult を re-export
  _base.py                 # Check Protocol, CheckResult / SuiteResult dataclass
  _checks.py               # 4 個別 check クラス
  _suites.py               # AICIndependenceSuite(プリセット組合せ)
```

`_base.py`:
```python
from typing import Protocol

@dataclass(frozen=True)
class CheckResult:
    name: str                # "HighCardinalityCheck"
    passed: bool
    severity: Literal["info", "warning"]
    message: str
    metric: float | None
    affected_columns: list[str]

class Check(Protocol):
    name: str
    def run(self, df: pd.DataFrame, *, response: str | None = None) -> list[CheckResult]: ...

@dataclass(frozen=True)
class SuiteResult:
    suite_name: str
    checks: list[CheckResult]
    n_rows: int
    n_cols: int
    response: str | None

    @property
    def passed(self) -> bool:
        return all(c.passed for c in self.checks)

    @property
    def warnings(self) -> list[CheckResult]:
        return [c for c in self.checks if not c.passed]

    def summary(self) -> str: ...  # CI 失敗時の見やすい要約
    def show(self) -> None: ...
    def to_html(self, path: str | Path | None = None) -> str: ...
    def to_dict(self) -> dict[str, Any]: ...
    def to_plotly_json(self) -> dict[str, Any]: ...
```

`_checks.py`(個別 check):
```python
@dataclass(frozen=True)
class IndependenceCheck:
    """ΔAIC ≤ threshold の説明変数を独立として警告。response 必須。"""
    name: str = "IndependenceCheck"
    delta_aic_max: float = 0.0    # ΔAIC > 0 で「独立」(AIC で改善せず)

    def run(self, df: pd.DataFrame, *, response: str | None = None) -> list[CheckResult]: ...

@dataclass(frozen=True)
class HighCardinalityCheck:
    name: str = "HighCardinalityCheck"
    max_categories: int = 50
    max_ratio: float = 0.5
    def run(self, df: pd.DataFrame, *, response: str | None = None) -> list[CheckResult]: ...

@dataclass(frozen=True)
class ConstantColumnCheck:
    name: str = "ConstantColumnCheck"
    def run(self, df: pd.DataFrame, *, response: str | None = None) -> list[CheckResult]: ...

@dataclass(frozen=True)
class PoolingSuggestionCheck:
    """連続列で AIC 最適 binning と単純等分割の差が大きい列を提案。"""
    name: str = "PoolingSuggestionCheck"
    min_improvement: float = 5.0    # ΔAIC 改善量
    def run(self, df: pd.DataFrame, *, response: str | None = None) -> list[CheckResult]: ...
```

`_suites.py`(プリセット):
```python
class AICIndependenceSuite:
    """Issue #15 で例示された default プリセット。

    Equivalent to:
        Suite([
            HighCardinalityCheck(),
            ConstantColumnCheck(),
            IndependenceCheck(),
            PoolingSuggestionCheck(),
        ])
    """
    def __init__(self, df: pd.DataFrame, *, response: str | None = None,
                 checks: list[Check] | None = None) -> None: ...

    def run(self) -> SuiteResult: ...
```

**安全性原則**(memory `feedback_python_falsy_or_default_trap` + 設計判断):
- `Check` は **すべて frozen dataclass**。閾値はコンストラクタで受け、`eval()` / 文字列ベース DSL は一切使わない
- CI 設定ファイル化は将来検討(toml で `checks=[...]` を宣言的に書く)。Phase D では Python コードでの組立のみ

#### 4. `measures/` サブパッケージ設計

```
src/pycatdap/measures/
  __init__.py    # aic, cramers_v, mutual_info, register, get
  _aic.py        # 既存 _aic.aic_independence を thin wrap
  _cramers_v.py  # 新規実装(scipy.stats.contingency.association を fallback)
  _mutual_info.py # 新規実装(np 自前実装、scipy 不要)
  _registry.py   # register/get
```

API:
```python
# 標準提供 measure(分割表 → スカラー)
pycatdap.measures.aic(cross_freq: np.ndarray) -> float
pycatdap.measures.cramers_v(cross_freq: np.ndarray) -> float
pycatdap.measures.mutual_info(cross_freq: np.ndarray) -> float

# 登録
pycatdap.measures.register("phi_k", phi_k_fn)
pycatdap.measures.get("phi_k") -> Callable[[np.ndarray], float]

# 利用箇所 — association_matrix に measure 引数を追加
m = pycatdap.association_matrix(df, measure="cramers_v")
```

**association_matrix の互換性**:
- 既存 `measure="aic"` のみ受け付ける動作を維持(default `"aic"`)
- 新規に `"cramers_v"` / `"mutual_info"` / register された string を受け付ける
- ΔAIC は **負ほど良い**(独立性 H0 からのゲイン)、Cramér's V は **正で 0..1**(大きいほど関連強)
- → ヒートマップの colorscale は measure 毎に判定が必要。`aic_heatmap()` 側で対応(別 PR)
- Phase D PR-D5 では `association_matrix(measure=...)` だけ拡張し、`aic_heatmap` の colorscale 自動切替は v0.7 以降の TODO とする

### Impact

- **公開 API の追加のみ**(4 関数 + 4 dataclass + 2 サブパッケージ)
- 既存 API への破壊的変更なし。`association_matrix(measure='aic')` はデフォルト維持
- 新規モジュール:
  - `src/pycatdap/target_analysis.py`
  - `src/pycatdap/quality_report.py`
  - `src/pycatdap/_quality.py`(profile.py から `_scan_quality` を移設、共有 helper 化)
  - `src/pycatdap/measures/` 配下 5 ファイル
  - `src/pycatdap/suite/` 配下 4 ファイル
  - `src/pycatdap/templates/target_analysis.html.j2`
  - `src/pycatdap/templates/quality_report.html.j2`
  - `src/pycatdap/templates/suite_result.html.j2`
- 既存モジュール変更:
  - `src/pycatdap/profile.py` — `_scan_quality` を `_quality` から import するよう書き換え(動作不変)
  - `src/pycatdap/_association.py` — `measure` 引数の dispatch を追加
  - `src/pycatdap/__init__.py` — 4 関数 + 4 dataclass + `suite` / `measures` サブパッケージを re-export
- `BLUEPRINT.md §3.1 / §5.10 / §5.11` を実装後の確定 API に改訂
- 任意依存: なし(scipy は既に optional。Cramér's V / mutual_info は numpy 自前実装で動作)

### Compatibility

- **後方互換**: 完全
- 既存 `profile()` ユーザーは無影響(`_scan_quality` 移設は pure refactor)
- `association_matrix(measure='aic')` はデフォルト引数値を維持

### Alternatives Considered

#### A1: `quality_report` を `list[QualityWarning]` 直返し
- **不採用理由**: `.show / .to_html / .to_dict / .to_plotly_json` の 4 メソッドが付かず、`ProfileResult` との一貫性が崩れる。CI 用 `.passed` プロパティも持てない。

#### A2: suite を functional API(`pycatdap.suite.run(df, checks=[...])`)に
- **不採用理由**: Issue #15 で class-based API が明示。deepchecks のメンタルモデルに揃える方が学習コスト低い。**関数化が必要なら将来 `pycatdap.suite.run(df, checks=[...])` を追加で出せる**(class からの呼び出し優先順)。

#### A3: measures/ を Phase D に含めず後回し
- **不採用理由**: `association_matrix(measure='aic')` の `measure` 引数が H-0006 / H-0007 で「H-0007 で予定」と Proposal に明記されながら 2 リリース連続で未実装。技術的負債を解消する。

#### A4: measures/ を Phase D に含めるが register API は次回
- **不採用理由**: pluggable interface の **register** が pysubgroup / DivExplorer interop の入口(Issue #31 / #32)。標準 measure 3 個と register 1 個は同じ PR で出した方が API surface が一度で固まる。

#### A5: `target_analysis` を `profile(df, response=...)` の subset として実装
- **不採用理由**: profile は association_matrix と catdap2 を含む重い処理。target_analysis は「response 列に対して ΔAIC を全列ランキング」だけが欲しい用途で、profile を呼ぶと冗長。**`target_analysis(df, response=col).top_summaries` で個別 TargetSummary に到達できる体験**が target-driven ワークフローに合う。

#### A6: `Check` を ABC(abstract base class)で実装
- **不採用理由**: Protocol で十分。Python の static duck typing で抽象化、各 check を frozen dataclass のままにできる。継承禁止で `eval()` 経路を物理的に排除。

#### A7: `SuiteResult.to_html()` を `pycatdap[plotly]` 必須に
- **採用**: 既に `profile.to_html()` が jinja2 + plotly inline を必須としており同じパターン。`pycatdap[plotly]` extras 未インストール時は明確な ImportError を出す。

#### A8: `IndependenceCheck` のデフォルト閾値 `delta_aic_max = 0.0`
- **採用**: ΔAIC ≤ 0 は「説明変数を加えた方が AIC が悪化」= 独立に近い、を意味する CATDAP の標準解釈。ユーザーは `IndependenceCheck(delta_aic_max=-2.0)` で「最低でも 2 以上の改善が要る」と厳しくできる。

### Acceptance Criteria

#### API
- [ ] `pycatdap.target_analysis(df, response)` が `TargetAnalysisResult` を返す
- [ ] `TargetAnalysisResult` が 4 メソッド(`.show / .to_html / .to_dict / .to_plotly_json`)
- [ ] `pycatdap.quality_report(df)` が `QualityReport` を返す
- [ ] `QualityReport.passed` プロパティが CI assert に利用可能
- [ ] `QualityReport.by_severity()` / `.by_kind()` で grouping 可能
- [ ] `pycatdap.suite.AICIndependenceSuite(df, response).run()` が `SuiteResult` を返す
- [ ] `SuiteResult.passed` プロパティ + `assert suite_result.passed, suite_result.summary()` が機能
- [ ] 4 個別 check(`IndependenceCheck` / `HighCardinalityCheck` / `ConstantColumnCheck` / `PoolingSuggestionCheck`)が独立に `.run(df, response=...) -> list[CheckResult]`
- [ ] `pycatdap.measures.{aic, cramers_v, mutual_info}` が `(cross_freq: np.ndarray) -> float`
- [ ] `pycatdap.measures.register("name", fn)` + `pycatdap.measures.get("name")` 動作
- [ ] `pycatdap.association_matrix(df, measure='cramers_v')` が動作(`'mutual_info'` も)

#### 内部リファクタ
- [ ] `_scan_quality` が `src/pycatdap/_quality.py` に移設され、`profile.py` / `quality_report.py` の両方が同じ helper を呼ぶ(behavior 不変)
- [ ] PR-D1 で profile.py の全テスト(74 件)が無変更で pass

#### 安全性
- [ ] suite の check class はすべて frozen dataclass、`eval()` / `exec()` / 文字列 import を一切使わない
- [ ] CI で `pycatdap.suite.AICIndependenceSuite(load_titanic(), response='Survived').run().passed` が決定的に動作(乱数依存なし)

#### コード品質
- [ ] `tests/test_target_analysis.py`: 12+ tests(各メソッド / response 必須エラー / top_k=0 / measure 拡張)
- [ ] `tests/test_quality_report.py`: 12+ tests(4 warning kind / passed プロパティ / by_severity / by_kind / atomic write)
- [ ] `tests/test_quality_helper.py`: 6+ tests(`_scan_quality` 単体、profile 経由でない直接テスト)
- [ ] `tests/test_measures.py`: 10+ tests(3 measure × 2-3 入力 + register/get)
- [ ] `tests/test_suite.py`: 15+ tests(4 check × 2 ケース + AICIndependenceSuite + SuiteResult メソッド)
- [ ] `tests/test_association_measures.py`: 6+ tests(measure='cramers_v' / 'mutual_info' で association_matrix が動作)
- [ ] **各新規モジュール 100% line coverage**(H-0007 PR-#75 で確立したパターン)
- [ ] `mypy --strict` pass
- [ ] 全公開 API に NumPy style docstring + `Examples` セクション

#### パフォーマンス
- [ ] 10k 行 × 20 列で `quality_report()` ≤ 1 秒(profile() より大幅高速)
- [ ] 10k 行 × 20 列で `target_analysis(df, response=col, top_k=5)` ≤ 5 秒(profile() と同程度)

#### ドキュメント
- [ ] `BLUEPRINT.md §3.1` のモジュール構成に `target_analysis.py` / `quality_report.py` / `_quality.py` / `measures/` / `suite/` を追記
- [ ] `BLUEPRINT.md §5.10` を実装後の suite API に合わせて改訂
- [ ] `BLUEPRINT.md §5.11` を実装後の measures API に合わせて改訂
- [ ] 新規 tutorial `docs/tutorials/09-target-analysis-and-suite.ipynb`(`target_analysis` + `quality_report` + `suite.AICIndependenceSuite` をフル活用)
- [ ] `docs/tutorials/index.md` + `mkdocs.yml` に Notebook 09 を追加
- [ ] `README.md` Quickstart に suite 例(CI 統合の 3 行)を追加
- [ ] CHANGELOG `[Unreleased]` `Added` セクションに各 API を順次記載

### PR 分割

実装は **7 PR** に分割する:

| PR | スコープ | 依存 |
|---|---|---|
| **PR-D0**(本 Proposal) | `docs(history): propose H-0008` | none |
| **PR-D1** | `_quality.py` への `_scan_quality` 移設(pure refactor、profile.py の挙動不変) | PR-D0 merge |
| **PR-D2** | `quality_report()` + `QualityReport` dataclass + jinja2 テンプレート + テスト | PR-D1 merge |
| **PR-D3** | `target_analysis()` + `TargetAnalysisResult` dataclass + jinja2 テンプレート + テスト | PR-D1 merge(D2 と並行可) |
| **PR-D4** | `measures/` サブパッケージ(3 measure + register/get)+ テスト | PR-D0 merge(他 PR と並行可) |
| **PR-D5** | `suite/` サブパッケージ(4 check + AICIndependenceSuite + SuiteResult + jinja2 テンプレート)+ `association_matrix(measure=...)` 拡張 + テスト | PR-D2, D3, D4 merge |
| **PR-D6** | Tutorial Notebook 09 + BLUEPRINT 反映 + README 更新 + CHANGELOG 整理 + Issue #15 close | PR-D5 merge |

各 PR は CI green を確認してから次に進む。`feedback_release_pr_dirty_squash_trap` 通り、全 PR は develop に **squash** で merge。最終的な release PR(v0.6.0)のみ `--merge`。

**並行可能ペア**:
- PR-D2 / PR-D3 / PR-D4 は PR-D1 merge 後に並行可能(別ブランチで同時に開ける)
- PR-D5 は D2/D3/D4 の全 merge 待ち(suite が measures + quality を呼ぶため)

### Decision

- Date: `TBD`
- Result: `pending`
- Notes: PR-D0(本 PR)で Proposal 承認待ち。

### Migration

破壊的変更なし。新規 API のため移行不要。

`association_matrix(measure='aic')` のデフォルトを維持するため既存ユーザーは無影響。`measure='cramers_v'` / `'mutual_info'` 利用は opt-in。

### Related References

- deepchecks: <https://docs.deepchecks.com/stable/tabular/auto_tutorials/quickstarts/plot_quick_data_integrity.html>
- great-expectations: <https://docs.greatexpectations.io/docs/>
- pandera: <https://pandera.readthedocs.io/>
- phik / phi_k: <https://github.com/KaveIO/PhiK>
- pysubgroup interestingness measures: <https://github.com/flemmerich/pysubgroup>
- Cramér's V: <https://en.wikipedia.org/wiki/Cram%C3%A9r%27s_V>
- 親仕様: H-0001 Phase D、H-0002 FR-10 / DP-6、Issue #15


---

## 2026-05-28: v0.6.0 で導入した frozen dataclass の shallow-freeze 修正

- ID: `H-0009`
- Status: `proposed`
- Scope: `API contract | breaking-light`
- Related: `H-0008`, `CLAUDE.md「NEVER mutate」`, `BLUEPRINT.md §5.10 / §5.11`

### Context

H-0008(v0.6.0)で 4 つの `@dataclass(frozen=True)` を出荷した:

- `TargetAnalysisResult` (`src/pycatdap/target_analysis.py:32-59`)
- `CheckResult` (`src/pycatdap/suite/_base.py:33-61`)
- `SuiteResult` (`src/pycatdap/suite/_base.py:87-107`)

`frozen=True` は **field への再代入** は禁ずるが、**field の中身**(`pd.DataFrame` / `dict` / `list`)の mutation は防がない。CLAUDE.md は明示的に「NEVER mutate」を要求しており、現状の API は契約と矛盾する:

```python
result = pycatdap.target_analysis(df, response="symptoms")
result.ranking.drop(0, inplace=True)        # 静かに壊せる
result.top_summaries["new_key"] = ...       # 静かに壊せる
result.checks.pop(0)                        # SuiteResult: 静かに壊せる
```

問題のフィールド:

| Class | Field | 現状 | 漏れる mutation |
|---|---|---|---|
| `TargetAnalysisResult` | `ranking: pd.DataFrame` | mutable | `.drop`/`.assign(inplace=True)` |
| `TargetAnalysisResult` | `top_summaries: dict[str, ...]` | mutable | `result.top_summaries["k"] = v` |
| `CheckResult` | `affected_columns: list[str]` | mutable | `result.affected_columns.append(...)` |
| `SuiteResult` | `checks: list[CheckResult]` | mutable | `result.checks.pop()` |

v0.6.0 PyPI ship 直後の architect レビュー(2026-05-28)で「**Phase G(v0.7.0)で新たな result dataclass が増える前** にパターンを正す」と助言された。Phase G は `ErrorLabelResult` 相当の新規 dataclass を導入する予定で、ここで間違ったパターンを伝播させると将来 breaking change で修正する羽目になる。

### Scope 限定

本 Proposal は **v0.6.0 で導入された 4 フィールドのみ** を対象とする。pre-v0.6.0 の同種パターン(`QualityReport.warnings: list` / `ProfileResult.variables: list` 等)は **別 Issue を起票して v1.0 までに対応**(本 Proposal でまとめてやると差分が肥大化し、レビュー困難になる)。

### Proposal

#### 修正方針

| Field | 変更 | 理由 |
|---|---|---|
| `CheckResult.affected_columns: list[str]` | `tuple[str, ...]` | tuple は immutable、空集合は `()` |
| `SuiteResult.checks: list[CheckResult]` | `tuple[CheckResult, ...]` | 同上。`Sequence` interface は維持される |
| `TargetAnalysisResult.top_summaries: dict[str, ...]` | `Mapping[str, ...]`(`MappingProxyType` でラップ) | `dict` interface(`__getitem__` / `items()` 等)は維持、`__setitem__` は `TypeError` |
| `TargetAnalysisResult.ranking: pd.DataFrame` | docstring に "**read-only — call `.copy()` before mutating**" を明記し、`__post_init__` で `ranking.flags.writeable = False`(numpy buffer の値のみ freeze。column add/drop までは防げないが、最も一般的な要素書き換えはブロック) | DataFrame の完全 freeze は実現困難。要素書き換えのみブロックし契約を docstring で明示する pandas-API 互換アプローチ |

#### 互換性影響

- **Strict semver では breaking**(`list` → `tuple` で `result.checks.append(...)` が `AttributeError`)
- ただし `frozen=True` の宣言通り使っているコードには **無影響**
- 攻撃面: ユーザーが mutation で内部状態を corrupt させる API ホールを塞ぐ → **正方向の breaking**
- v0.6.0 は今日リリース(2026-05-28)で実運用ユーザーは事実上ゼロ。v0.6.1 patch として ship 可能

#### テスト戦略

- **新規 regression テスト** `tests/test_reg_h0009_shallow_freeze.py` 各 field について:
  - `TypeError` 期待: `.append()` / `__setitem__` / `inplace` mutation
  - golden: 既存 read-only consumer(`to_dict` / `to_html` / `to_plotly_json` / `show`)が動作継続
- 既存テストスイート(516 passed)が全て green を維持

### Alternatives Considered

#### A1: pre-v0.6.0 の同種パターンも一緒に修正
- **不採用理由**: 8 フィールド以上の breaking change を一度に出すと、レビュー困難で patch リリースの逸脱。v0.6.0 直後の今だからこそ v0.6.1 として narrow scope で出せる。pre-v0.6.0 は別 Issue で v1.0 までに段階対応。

#### A2: docstring 警告のみ(現状の `frozen=True` を維持)
- **不採用理由**: 「NEVER mutate」を docstring に書いても CLAUDE.md ルール違反のコードが静かに動く現状は変わらない。`assert` でも runtime 検出は実現可能だが、型システムレベルで保証する `tuple` / `MappingProxyType` の方が strict。

#### A3: pydantic.BaseModel に置き換え
- **不採用理由**: pydantic は必須依存に上がる。pandas DataFrame との相互作用に難あり。v0.6.1 patch の scope を超える。

#### A4: 全 field を完全 immutable に(DataFrame も)
- **不採用理由**: pandas は完全 freeze の標準 API を持たない。`flags.writeable = False` は要素書き換えのみブロックする部分対策。完全 immutable は別ライブラリ依存(`pyrsistent` 等)が必要で v0.6.1 patch の scope を超える。

### Acceptance Criteria

- [ ] `CheckResult.affected_columns` が `tuple[str, ...]`
- [ ] `SuiteResult.checks` が `tuple[CheckResult, ...]`
- [ ] `TargetAnalysisResult.top_summaries` が `Mapping[str, ...]`(`MappingProxyType` でラップ)
- [ ] `TargetAnalysisResult.ranking` の docstring に "read-only" 明記、`__post_init__` で `.flags.writeable = False`
- [ ] `tests/test_reg_h0009_shallow_freeze.py` 4+ 件の TypeError 期待テスト追加
- [ ] 既存 516 テスト全て green を維持
- [ ] CHANGELOG `## [0.6.1]` セクションに API hardening として明記
- [ ] BLUEPRINT §5.10 / §5.11 の型表記を更新
- [ ] pre-v0.6.0 の同種パターン(`QualityReport.warnings` / `ProfileResult.variables` 等)を v1.0 までに対応する **follow-up Issue を起票**

### PR 分割

| PR | スコープ | 依存 |
|---|---|---|
| **PR-E0**(本 Proposal) | `docs(history): propose H-0009` | none |
| **PR-E1** | 実装 + テスト + BLUEPRINT 更新 + CHANGELOG | PR-E0 merge |
| **PR-E2**(別 issue 起票のみ) | follow-up issue: 残り frozen dataclass の同種修正 | PR-E1 と並行可 |
| **PR-E3**(release) | `release: v0.6.1` | PR-E1 merge |

### Decision

- Date: `TBD`
- Result: `pending`
- Notes: PR-E0(本 PR)で Proposal 承認待ち。

### Migration

技術的には breaking。ただし v0.6.0 PyPI ship 直後で実運用ユーザーが事実上ゼロのため、`## [0.6.1]` patch で出荷可。

CHANGELOG に明記する文言案:

> ### Changed (API hardening — breaking for code that mutated result objects)
> - `SuiteResult.checks` is now `tuple[CheckResult, ...]` instead of `list`. Code calling `.append()` etc. on it must copy to a list first.
> - `CheckResult.affected_columns` is now `tuple[str, ...]`.
> - `TargetAnalysisResult.top_summaries` is now a read-only `Mapping` (`MappingProxyType`).
> - `TargetAnalysisResult.ranking` is documented as read-only and the underlying numpy buffer is frozen via `.flags.writeable = False`.

### Related References

- 親仕様: H-0008、CLAUDE.md「NEVER mutate」、BLUEPRINT.md §5.10 / §5.11
- architect 助言(2026-05-28): Phase G 開始前に v0.6.1 patch で先行修正(Phase G result dataclass が間違ったパターンを継承するのを避ける)
- Python types.MappingProxyType: <https://docs.python.org/3/library/types.html#types.MappingProxyType>
- pandas DataFrame.flags: <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.flags.html>

---

## 2026-05-28: Phase G 誤差ラベリング + D3 デモデータセット同梱

- ID: `H-0010`
- Status: `proposed`
- Scope: `API | datasets`
- Related: `H-0001 Phase G`, `H-0002 FR-4`, `BLUEPRINT.md §5.8`, Issue #16, Issue #23

### Context

H-0008(v0.6.0)で EDA arc(Phase A〜D)が完了し、v0.7.0 以降は **ML 誤差分析 arc(Phase G〜L)** を進める。Phase G は誤差ラベリングの基盤を提供し、後続の Phase H(`error_analysis()` ワンコール)/ I+J(誤差可視化)/ K(キャリブレーション)/ L(スライス発見)が直接依存する。

並行して、データセット拡張ロードマップ(H-0003)の D3(German Credit / Heart Disease / Penguins)は v0.5.0 → v0.6.0 と **2 回スリップ** している。原因は「独立リリースとして扱うとフィーチャー軸のリリースナラティブに勝てない」構造的問題で、2026-05-28 architect レビューで「Phase G にはラベル付き誤差例のデモデータが必要なので、D3 を Phase G に同梱する」方針が決まった(PLAN.md §3.3 反映済)。

### Proposal

#### A. Phase G 公開 API

BLUEPRINT.md §5.8 に既に定義済み。本 Proposal で確定する:

```python
# 二値・多値分類: 予測の正誤を「correct/incorrect」ラベルに
pycatdap.error.error_label(
    y_true: pd.Series | np.ndarray | list,
    y_pred: pd.Series | np.ndarray | list,
) -> pd.Series   # categorical("correct" | "incorrect")

# 二値分類: TP/FP/FN/TN ラベル
pycatdap.error.confusion_label(
    y_true: pd.Series | np.ndarray | list,
    y_pred: pd.Series | np.ndarray | list,
    *,
    positive: Any = None,    # None → 自動推定(2 ユニーク値の片方)
) -> pd.Series   # categorical("TP" | "FP" | "FN" | "TN")

# 回帰: 残差を AIC binning でカテゴリ化
pycatdap.error.residual_label(
    y_true: pd.Series | np.ndarray | list,
    y_pred: pd.Series | np.ndarray | list,
    *,
    method: Literal["aic_pool", "quantile", "equal_width"] = "aic_pool",
    n_bins: int = 4,
) -> pd.Series   # categorical(bin labels)

# 回帰: |residual| を AIC pooling
pycatdap.error.abs_residual_pool(
    y_true: pd.Series | np.ndarray | list,
    y_pred: pd.Series | np.ndarray | list,
    *,
    n_bins: int = 4,
) -> pd.Series   # categorical(bin labels)

# 内部 helper(公開)
pycatdap.error._detect_task(
    y_true: pd.Series | np.ndarray,
    y_pred: pd.Series | np.ndarray,
) -> Literal["classification", "regression"]
```

#### B. データクラス契約

Phase G は label を `pd.Series` で返すだけで result dataclass を導入しない(H-0009 shallow-freeze 問題の再発を避ける)。Phase H(`error_analysis()`)で `ErrorAnalysisResult` を導入する際は v0.6.1 で確立した immutable pattern(`tuple` / `MappingProxyType` / `__post_init__` freeze)に従う。

#### C. Multiclass 仕様

`confusion_label` の multiclass サポートは **v0.7.0 では `NotImplementedError`**(明示エラー)。one-vs-rest 実装は v0.8.0 以降の別 PR で対応。理由:
- v0.7.0 は binary をしっかり仕上げる focused release
- one-vs-rest は per-class 出力か aggregate 出力か設計判断が必要(PLAN.md §4.3 で「v0.7 開始時 multiclass 仕様」が未確定とフラグ済)
- error message に `"only binary classification supported in v0.7.0; see #16 follow-up for multiclass"` を含めて誘導

#### D. Task auto-detection ヒューリスティック

`_detect_task(y_true, y_pred)`:
- 両方が integer dtype かつ unique 値が 20 以下 → `classification`
- y_pred が float でレンジが [0, 1] かつ y_true が binary → `classification`(probability prediction)
- それ以外 → `regression`
- 明確化必要時は呼び出し側で `task=` を明示する API を後続 Phase H で導入する

#### E. D3 データセット同梱

3 データセットを `src/pycatdap/data/` に CSV(または gz)で同梱:

| Dataset | Rows × Cols | Task | License |
|---|---|---|---|
| German Credit | 1000 × 21 | Binary classification (creditworthy/bad) | UCI public domain |
| Heart Disease | 303 × 14 | Binary classification (heart disease presence) | UCI CC BY 4.0 |
| Penguins | 344 × 8 | 3-class multiclass (species) | CC0 (palmerpenguins) |

ローダー関数:

```python
pycatdap.datasets.load_german_credit() -> pd.DataFrame
pycatdap.datasets.load_heart_disease() -> pd.DataFrame
pycatdap.datasets.load_penguins() -> pd.DataFrame
```

Penguins は Phase G が **binary だけ** をサポートする v0.7.0 時点では `_detect_task` で classification と判定されるが `confusion_label` は `NotImplementedError`(項目 C 通り)。Tutorial では `error_label`(正誤 binary)で使用、multiclass 拡張は Phase H 以降。

### Alternatives Considered

#### A1: Phase G を multiclass フル対応で出荷
- **不採用理由**: PLAN.md §4.3 で「one-vs-rest? 全 confusion 行列?」が未確定とフラグされている。v0.7.0 を focused release にし、binary を完全な品質で出してから v0.8.0 で multiclass 設計を別途行う方が API 設計事故が少ない。

#### A2: D3 dataset を v0.8.0 (Phase H) に持ち越し
- **不採用理由**: 既に v0.5.0 → v0.6.0 と 2 回スリップ済。Phase G が demo データを必要とするため自然な fold-in タイミング。architect 推奨。

#### A3: Phase G に result dataclass を導入(`ErrorLabelResult` 等)
- **不採用理由**: 4 関数とも `pd.Series` を返す単純な計算ユーティリティで dataclass 化のメリットが小さい。むしろ shallow-freeze 問題(H-0009 で対処したばかり)の再発リスクが高い。dataclass 導入は Phase H(複数ラベル + ranking + slice を bundle する `ErrorAnalysisResult`)で行う。

#### A4: Phase G を `_pooling.py` の薄い wrapper にする
- **不採用理由**: `residual_label(method="aic_pool")` は `_pooling.py` を呼ぶが、`error_label` / `confusion_label` は別ロジック。Phase G を `error/` サブパッケージとして独立させることで H/I+J/K/L が import しやすい構造になる。

### Acceptance Criteria

- [ ] `pycatdap.error` サブパッケージが存在
- [ ] `error_label` / `confusion_label` / `residual_label` / `abs_residual_pool` / `_detect_task` が実装され公開
- [ ] `confusion_label` は multiclass 入力で `NotImplementedError` を raise(明示メッセージ付き)
- [ ] `residual_label` の 3 つの method(`aic_pool` / `quantile` / `equal_width`)全てテストされる
- [ ] `pycatdap.datasets.load_german_credit` / `load_heart_disease` / `load_penguins` が動作
- [ ] 各データセット CSV が `src/pycatdap/data/` に同梱され `pip install pycatdap` で使える
- [ ] 各データセット LICENSE 出典が docstring に明記
- [ ] 80% 以上の line coverage、TDD で test → impl
- [ ] BLUEPRINT.md §5.8 が公開状態(現在 planned → released へ)
- [ ] Tutorial Notebook 10 で `load_german_credit` + Phase G の流れを示す
- [ ] Issue #16 + Issue #23 が close される

### PR 分割

| PR | スコープ | 依存 |
|---|---|---|
| **PR-F0**(本 Proposal) | `docs(history): propose H-0010` | none |
| **PR-F1** | Phase G error labeling utilities(`error_label` / `confusion_label` / `residual_label` / `abs_residual_pool` / `_detect_task`)+ テスト | PR-F0 merge |
| **PR-F2** | D3 datasets(German Credit / Heart Disease / Penguins)CSV bundle + loader 関数 + 出典 docstring + テスト | PR-F0 merge(F1 と並行可) |
| **PR-F3** | Tutorial Notebook 10 + BLUEPRINT 反映 + README quickstart 更新 + CHANGELOG cut to v0.7.0 + Issue #15 + Issue #23 close | PR-F1 + PR-F2 merge |
| **PR-F4**(release) | `release: v0.7.0` | PR-F3 merge |

各 PR は CI green を確認してから次に進む。全 PR は develop に **squash** で merge。release PR(v0.7.0)のみ `--merge`(release line 維持)。

### Decision

- Date: `TBD`
- Result: `pending`
- Notes: PR-F0(本 PR)で Proposal 承認待ち。

### Migration

破壊的変更なし。新規 API + 新規データセットのため移行不要。既存 `pycatdap.datasets.load_*` は無影響。

### Related References

- 親仕様: H-0001 Phase G、H-0002 FR-4、Issue #16、Issue #23
- architect レビュー 2026-05-28: Phase G 直進 + D3 fold-in + multiclass deferred
- UCI ML Repository German Credit: <https://archive.ics.uci.edu/ml/datasets/Statlog+(German+Credit+Data)>
- UCI ML Repository Heart Disease: <https://archive.ics.uci.edu/ml/datasets/heart+disease>
- palmerpenguins: <https://allisonhorst.github.io/palmerpenguins/>
- H-0009 shallow-freeze pattern: Phase G は dataclass を導入せず `pd.Series` のみ返すことで再発を予防

## 2026-05-28: Phase H `error_analysis()` ワンコール + D4 fetch データセット

- ID: `H-0011`
- Status: `proposed`
- Scope: `API | datasets`
- Related: `H-0001 Phase H`, `H-0002 FR-2 / FR-8`, `H-0009 shallow-freeze pattern`, `H-0010 Phase G`, `BLUEPRINT.md §5.8`, Issue #17, Issue #24

### Context

H-0010(v0.7.0)で Phase G(`error_label` / `confusion_label` / `residual_label` / `abs_residual_pool` / `_detect_task`)が出荷され、誤差を `pd.Series` として返す基盤が整った。

Phase H(`error_analysis()` ワンコール)は次の合成を行う:

```
_detect_task → 適切な labeling 関数 → target_analysis(labeled_response) → ErrorAnalysisResult
```

これは `pycatdap.profile()`(H-0007)が EDA arc のワンコール入口だったのと同じ位置づけを ML 誤差分析 arc に持ち込むもので、後続 Phase I+J(可視化)/ K(キャリブレーション)/ L(スライス発見)の共通入口となる。

並行して、D4(Adult Income / COMPAS / California Housing)を Phase H デモ用に H-0010 の dataset-folding policy に従って同梱する。D3(German Credit)が binary classification を、Penguins が multiclass を提供したのに対し、D4 は **規模(Adult: 32K 行)** **fairness 文脈(COMPAS)** **回帰タスク(California Housing)** の 3 補完を担う。

### Proposal

#### A. `error_analysis()` 公開 API

```python
pycatdap.error_analysis(
    df: pd.DataFrame,
    y_true: str | pd.Series | npt.NDArray,
    y_pred: str | pd.Series | npt.NDArray,
    *,
    task: Literal["auto", "classification", "regression"] = "auto",
    top_k: int = 5,
    positive: Any = None,                # binary classification の positive class
    residual_method: Literal["aic_pool", "quantile", "equal_width"] = "aic_pool",
    n_bins: int = 4,
    bins: int | None = None,             # 説明変数の binning(target_analysis に forward)
    criterion: Literal["aic", "aicc", "bic"] = "bic",
) -> ErrorAnalysisResult
```

**`y_true` / `y_pred` の受け入れ形式**(2 通り):
- 列名(`str`): `df[y_true]` / `df[y_pred]` を引く
- 配列(`pd.Series` | `np.ndarray`): `len(df)` と一致必須、`df` に存在しない列を扱える

**Task dispatch**(`_detect_task` を流用):
- `task="auto"`: `_detect_task(y_true, y_pred)` で判定
- `task="classification"` + binary → `confusion_label` を主、補助で `error_label`
- `task="classification"` + multiclass(3+ unique 値) → `error_label` のみ(`confusion_label` は H-0010 §C に従い NotImplementedError なので使わない)
- `task="regression"` → `residual_label(method=residual_method, n_bins=n_bins)` を response として `target_analysis`

**説明変数 ranking**:
- 内部で `target_analysis(df_with_labels, response="<label_col>", top_k=top_k, bins=bins, criterion=criterion)` を呼び出し、その `ranking` / `top_summaries` をそのまま転載
- これにより既存の `target_analysis` 実装(H-0008)を再利用、Phase H 専用 ranking ロジックは持たない

#### B. `ErrorAnalysisResult` データクラス契約(v0.6.1 immutable pattern 準拠)

```python
@dataclass(frozen=True)
class Slice:
    """単一説明変数 × 単一エラーカテゴリの集中スライス。"""
    variable: str                     # 説明変数名
    category: str                     # その変数の値 / bin label(例 "young" / "[45, 60]")
    error_category: str               # 誤差ラベル("incorrect" / "FN" / "bin_3" 等)
    n_in_slice: int                   # スライス内サンプル数
    n_error_in_slice: int             # うち error_category のサンプル数
    error_rate: float                 # n_error_in_slice / n_in_slice
    pearson_residual: float           # 標準化残差(大きいほど集中)
    delta_aic: float                  # 親変数の ΔAIC(同変数の Slice 間で共通)

@dataclass(frozen=True)
class ErrorAnalysisResult:
    task: Literal["classification", "regression"]
    label_kind: Literal["error_label", "confusion_label", "residual_label"]
    response_name: str                # 内部で生成したラベル列名("__error_label__" 等)
    feature_ranking: pd.DataFrame     # variable / delta_aic / kind / n_obs(target_analysis 由来)
    top_summaries: Mapping[str, TargetSummary]   # MappingProxyType, top_k 件
    top_slices: tuple[Slice, ...]     # 全 top_k 変数を横断して |residual| 降順、最大 3×top_k 件
    confusion: pd.DataFrame | None    # binary classification のみ(`confusion_label` のクロス表)
    residual_pooling: Mapping[str, Any] | None    # regression のみ、bin 境界等
    n_rows: int
    n_correct: int | None             # classification のみ
    n_incorrect: int | None
    mae: float | None                 # regression のみ
    rmse: float | None

    def __post_init__(self) -> None:
        # numpy buffer freeze on feature_ranking + confusion (target_analysis と同じ)
        ...

    def show(self) -> None: ...
    def to_html(self, path: str | Path | None = None) -> str: ...
    def to_dict(self) -> dict[str, Any]: ...
    def to_plotly_json(self) -> dict[str, Any]: ...
    def to_divexplorer_format(self) -> pd.DataFrame: ...
```

**Immutable 規約**(v0.6.1 H-0009 教訓):
- `feature_ranking` / `confusion`: `__post_init__` で numpy buffer を `flags.writeable = False`
- `top_summaries`: `MappingProxyType` でラップ
- `top_slices`: `tuple` のみ(`list` 禁止)
- `residual_pooling`: 仮に `dict` を渡されても `MappingProxyType` でラップ

#### C. Slice 抽出ロジック

Phase H は **単変数スライス**のみ扱う(多変数スライスは Phase L で対応):

1. `feature_ranking` 上位 `top_k` 件の各変数について `TargetSummary` を取得済(`top_summaries`)
2. 各 `TargetSummary.pearson_residuals` から:
   - error_category(`"incorrect"` / `"FN"` / `"bin_3"` 等、コンテキスト依存で 1 つ選択)行の中で
   - `|residual|` が **2.0 以上** のセルを集中スライス候補とする(統計学慣習: standardized residual > 2 = 有意な集中)
3. 全変数横断で `|residual|` 降順にソート、最大 **3 × top_k** 件まで保持
4. 各セルから `Slice(variable, category, error_category, ...)` を構築

error_category の選択ルール:
- `error_label`: `"incorrect"`(モデルが間違えた行)
- `confusion_label`: `"FP"` と `"FN"` の 2 つを別 Slice として候補に
- `residual_label`: 最大値 bin と最小値 bin の 2 つ(over-prediction / under-prediction)

#### D. 出力 helper(`.show` / `.to_html` / `.to_plotly_json` / `.to_dict` / `.to_divexplorer_format`)

`TargetAnalysisResult` の 4-method 契約に **`to_divexplorer_format()` を追加した 5-method 契約**:

- `.show()`: header 行 → confusion(分類)or residual stats(回帰)→ feature_ranking → top_slices テーブル → top_summaries 順
- `.to_html(path)`: jinja2 テンプレート `src/pycatdap/templates/error_analysis.html.j2`、plotly inline、atomic_write_text(H-0009)
- `.to_dict()`: JSON-safe
- `.to_plotly_json()`: `confusion` / `feature_ranking` バー / 各 `top_summaries` を組み合わせた section dict
- `.to_divexplorer_format()`: DivExplorer subgroup API 互換 DataFrame(列: `description` / `size` / `error_rate` / `delta_aic` / `pearson_residual`)

#### E. D4 データセット — sklearn-backed fetch

実装は **`scikit-learn` の `fetch_openml` / `fetch_california_housing` を薄くラップ**:

| Loader | バックエンド | 規模 | タスク |
|---|---|---|---|
| `pycatdap.datasets.fetch_california_housing()` | `sklearn.datasets.fetch_california_housing(as_frame=True)` | 20,640 × 9 | regression |
| `pycatdap.datasets.fetch_adult_income()` | `sklearn.datasets.fetch_openml("adult", version=2, as_frame=True)` | 48,842 × 15 | binary classification |
| `pycatdap.datasets.fetch_compas()` | `sklearn.datasets.fetch_openml("compas-two-years", version=4, as_frame=True)` | 5,278 × 14 | binary classification(fairness 文脈) |

**設計判断**:
- HTTP / retry / checksum / cache は sklearn に委譲(`~/scikit_learn_data/` 配下、自前で再実装しない)
- `scikit-learn>=1.3` を `pycatdap[data]` extras として追加(`pip install pycatdap[data]`)
- ローダーは sklearn 未導入時に `ImportError` で明示誘導
- COMPAS の倫理的注意点は docstring に記載(ProPublica の disclaimer / bias 用デモ用途)
- ネットワーク要求テストは `@pytest.mark.slow` + `pytest.importorskip("sklearn")` で gate
- 既存 D1〜D3(`load_*`)は bundled CSV のまま変更なし、新規は `fetch_*` 接頭辞で区別

#### F. 実装 safeguards(cross-check 2026-05-28 で抽出)

第三者エージェントレビューで以下 3 つの実装トラップが洗い出された。実装フェーズで必須:

**F-1. 内部生成ラベル列の列名衝突ガード**

`error_analysis()` は `target_analysis(df_with_label_column, response="<internal_name>")` を呼ぶため、`df` に同名列が存在すると silent overwrite または KeyError が起きる。

実装方針:
- 候補名: `"__pycatdap_error_label__"` / `"__pycatdap_confusion_label__"` / `"__pycatdap_residual_label__"`(`__pycatdap_` プレフィックスで衝突確率を下げる)
- 呼び出し時に `if internal_name in df.columns: raise ValueError(...)` で明示エラー
- error message に「列名を変更するか `df.drop(columns=...)` で除去」誘導を含める
- Acceptance Criteria に「衝突時に明示エラー」テスト追加

**F-2. `confusion_label` クロス表での FP/FN 行欠落ガード**

`pd.crosstab(confusion_label, explanatory)` は **完璧なモデル(全 TP/TN)で `"FP"` / `"FN"` 行を省略する**。`pearson_residuals.loc["FP"]` を素直に書くと KeyError。

実装方針:
- `_extract_slices` で `if error_cat not in pearson_residuals.index: continue` でガード
- `confusion_label` 自体は `pd.Categorical(..., categories=["TP", "FP", "FN", "TN"])` で固定カテゴリを宣言済 (`_labels.py:183`) だが、`crosstab` の `dropna=False` を意識的に指定しない限り 0 行は捨てられる
- 代替案: `pearson_residuals.reindex(index=["TP","FP","FN","TN"]).fillna(0.0)` で固定行を担保(よりロバスト)

**F-3. `residual_label(method="aic_pool")` の bin 順序単調性は保証されている**

cross-check で確認済(`src/pycatdap/_pooling.py:220-221`):

```python
boundaries = sorted(float(e) for e in edges[1:-1])
codes = _codes_from_boundaries(values, boundaries)  # np.digitize against ascending
```

したがって `bin_0` = 最小残差(under-prediction)、最大番号 bin = 最大残差(over-prediction)は単調に保たれる。Slice 抽出で「`bin_0` / max bin の 2 つを別 Slice として候補に」前提は安全。実装では `n_categories = len(top_summary.counts.index)` から動的に bin_0 と bin_{n-1} を抽出。

#### G. Phase H が解決しないこと(明示スコープアウト)

- **Multivariable subgroup discovery**: 2+ 変数の組み合わせスライス。Phase L(`discover_error_slices`)で対応
- **可視化**: confusion matrix / residual scatter の Plotly Figure 構築。Phase I+J で対応(`.to_plotly_json()` の confusion セクションは bar chart 程度に留める)
- **Calibration**: `calibration_curve` / `brier_score` / `expected_calibration_error`。Phase K で対応
- **Multiclass confusion**: `confusion_label` の one-vs-rest 拡張。`error_label` で代替し本格対応は別 Issue
- **`PYCATDAP_DATA_DIR` env var**: Issue #24 で要求あるが sklearn の cache dir(`SCIKIT_LEARN_DATA`)を流用するため pycatdap 独自の env var は追加しない。docstring に sklearn 流儀を記載

### Alternatives Considered

#### A1: Phase H が独自に AIC ranking を再実装

- **不採用理由**: `target_analysis()` (H-0008) と完全に同じ動作。重複実装は H-0009 で得た「内部実装も DRY に」教訓に反する。`target_analysis` を内部呼び出しすることでロジック・テスト・ドキュメントを 1 か所に集約。

#### A2: `ErrorAnalysisResult` を `dataclass`(frozen なし) で導入

- **不採用理由**: H-0009 で `frozen=True` でも shallow-freeze 問題があると判明し、v0.6.1 で `tuple` / `MappingProxyType` / `__post_init__` パターンを確立した。Phase H は新規 dataclass の最初の機会で、ここで mutable に戻すと再び patch が必要になる。

#### A3: D4 を独自 HTTP 実装(`requests` + checksum 直書き)

- **不採用理由**: Issue #24 の原案はそうだったが、(1) `requests` を新規依存に加える(2) ETag/checksum 管理を自前で書く(3) 既存 D3 と loader 規約が分岐する、と複雑性が増す。sklearn は既に ML エコシステムの de-facto cache 機構を持ち、`fetch_openml` 一発で OpenML カタログ全体に到達できるためコスパが圧倒的に良い。

#### A4: D4 を全て v0.9.0 以降に持ち越し、Phase H は D1〜D3 のみで demo

- **不採用理由**: 回帰タスクの demo データが D1〜D3 に欠ける(全て分類)。Phase H は「分類 + 回帰の両刀」を売りにするため最低 1 つの回帰ベンチが必要。California Housing(sklearn 同梱でネットワーク不要)だけでも先行 fold-in する判断もあるが、せっかく sklearn extras を入れるなら 3 つまとめて出した方がユーザ体験が良い。

#### A5: Phase H の Slice 抽出を Phase L(subgroup discovery)に統合

- **不採用理由**: 単変数スライスは `pearson_residuals` から直接読めるためコストゼロ。一方 Phase L は多変数組み合わせ最適化を伴うため重い。Phase H で「目立つ単変数スライス」だけでもユーザに見せる方が ROI が高く、Phase L への動機付けにもなる。

#### A6: `error_analysis()` を `pycatdap.error.analysis` ではなく `pycatdap.error_analysis` でトップレベル公開

- **採用**: `pycatdap.profile` / `pycatdap.target_analysis` と同じワンコール入口の位置づけ。実装は `src/pycatdap/error/analysis.py` に置き、`pycatdap/__init__.py` から re-export。

### Acceptance Criteria

- [ ] `pycatdap.error_analysis(df, y_true, y_pred)` がトップレベルで呼べる
- [ ] `task="auto" | "classification" | "regression"` の 3 経路すべてに unit test
- [ ] `y_true` / `y_pred` を列名 / `pd.Series` / `np.ndarray` の 3 形式で受け入れ
- [ ] `ErrorAnalysisResult` が `frozen=True` + immutable 規約に準拠(`feature_ranking` 書き換え不可テスト追加)
- [ ] `Slice` dataclass 実装、`top_slices` が `|residual| >= 2.0` の集中セルのみ含む
- [ ] **F-1 ガード**: `df` に `__pycatdap_error_label__` 等が既存する場合は明示 `ValueError`(回帰テスト追加)
- [ ] **F-2 ガード**: 完璧なモデル(全 TP/TN、FP/FN 行が 0)で `error_analysis(task="classification")` が KeyError せず `confusion` フィールドが固定 4 行を保持
- [ ] **multiclass guard**: `task="classification"` + 3+ unique 値 で `confusion_label` を呼ばず `error_label` のみで動作することのテスト
- [ ] `.show` / `.to_html` / `.to_dict` / `.to_plotly_json` / `.to_divexplorer_format` 全て動作
- [ ] `to_html` は `jinja2` 未導入時に明示 `ImportError`(`pycatdap[plotly]` 誘導)
- [ ] `pycatdap.datasets.fetch_california_housing / fetch_adult_income / fetch_compas` が動作
- [ ] D4 ローダーは sklearn 未導入時に明示 `ImportError`(`pycatdap[data]` 誘導)
- [ ] D4 のネットワーク要求テストは `@pytest.mark.slow` で gate、デフォルト CI からは除外
- [ ] 80% 以上の line coverage、TDD で test → impl
- [ ] BLUEPRINT.md §5.8 を planned → released 更新(Phase H 部分)
- [ ] Tutorial Notebook 11 で `error_analysis()` の binary classification(German Credit) + regression(California Housing)demo
- [ ] Issue #17 + Issue #24 が close される
- [ ] CHANGELOG.md の v0.8.0 セクション、Phase G→H 連結と D4 fold-in を明記

### PR 分割

| PR | スコープ | 依存 |
|---|---|---|
| **PR-G0**(本 Proposal) | `docs(history): propose H-0011` | none |
| **PR-G1** | `Slice` + `ErrorAnalysisResult` データクラス + `_extract_slices` helper + tests(impl は最小、API 表面のみ) | PR-G0 merge |
| **PR-G2** | `error_analysis()` 本体 + `task` dispatch + `target_analysis` 合成 + classification / regression テスト | PR-G1 merge |
| **PR-G3** | `to_html` / `to_plotly_json` / `to_divexplorer_format` + jinja2 テンプレート | PR-G2 merge |
| **PR-G4** | D4 fetchers(`fetch_california_housing` / `fetch_adult_income` / `fetch_compas`)+ `[data]` extras + slow tests | PR-G0 merge(G1〜G3 と並行可) |
| **PR-G5** | Tutorial Notebook 11 + BLUEPRINT §5.8 更新 + README quickstart + CHANGELOG cut to v0.8.0 + Issue #17/#24 close | PR-G3 + PR-G4 merge |
| **PR-G6**(release) | `release: v0.8.0` | PR-G5 merge |

各 PR は CI green 確認後に次へ進む。develop に **squash** で merge、release PR のみ `--merge`(release line 維持)。

### Decision

- Date: `TBD`
- Result: `pending`
- Notes: PR-G0(本 PR)で Proposal 承認待ち。

### Migration

破壊的変更なし。Phase G の `pycatdap.error.*` 既存関数はそのまま、新規追加のみ:
- `pycatdap.error_analysis` (top-level)
- `pycatdap.error.ErrorAnalysisResult` / `pycatdap.error.Slice`
- `pycatdap.datasets.fetch_california_housing` / `fetch_adult_income` / `fetch_compas`
- `pycatdap[data]` 新規 extras

既存 user code への影響なし。

### Related References

- 親仕様: H-0001 Phase H、H-0002 FR-2 / FR-8、Issue #17、Issue #24
- 前段: H-0010 Phase G(`pycatdap.error.*` ラベリング、v0.7.0 で出荷済)
- Immutable pattern: H-0009(`TargetAnalysisResult` の `__post_init__` numpy freeze / `MappingProxyType` / `tuple`)
- 合成元: `pycatdap.target_analysis`(`src/pycatdap/target_analysis.py`)
- sklearn fetch_openml: <https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_openml.html>
- DivExplorer 互換性参考: <https://github.com/divexplorer/divexplorer>(Phase L で完全対応、Phase H はフォーマット互換のみ)

## 2026-05-29: Phase I+J 誤差可視化(confusion / residual プロット群)

- ID: `H-0012`
- Status: `proposed`
- Scope: `API | plot`
- Related: `H-0001 Phase I+J`, `H-0011 Phase H`, `BLUEPRINT.md §5.8 / §5.6 (plot)`, Issue #18

### Context

H-0011(v0.8.0)で `error_analysis()` ワンコール入口が出荷され、`ErrorAnalysisResult` に `confusion`(分類)/ `residual_pooling`(回帰)/ `feature_ranking` / `top_slices` が揃った。Phase I+J はこの結果オブジェクトの可視化を完成させる:

- **Phase I(分類)**: confusion matrix を「ヒートマップ」「スライス別 small-multiples」で可視化、加えて confusion 情報量を ΔAIC で定量化
- **Phase J(回帰)**: residual の散布図 / カテゴリ別 box / AIC pooling 結果のヒストグラム

既存 `pycatdap.plot.*` の backend dispatch(`matplotlib` / `plotly`)パターンと完全に揃え、`ax=` パラメータ(matplotlib)/ `plotly.Figure` 返却を一貫させる。

### Proposal

#### A. Phase I 公開 API(`pycatdap.error.*`)

```python
# 分類: confusion matrix のヒートマップ
pycatdap.error.plot_confusion(
    y_true, y_pred,
    *,
    labels: list | None = None,        # クラス順序の明示指定(None → np.unique 順)
    normalize: Literal["true", "pred", "all", None] = None,  # 行/列/全体正規化
    backend: Literal["matplotlib", "plotly"] = "matplotlib",
    ax=None,                           # matplotlib 用
    cmap: str = "Blues",
    show_values: bool = True,          # セルに数値を描画
) -> Axes | Figure

# 分類: 説明変数のカテゴリ別に confusion を small-multiples
pycatdap.error.plot_confusion_by_slice(
    df, y_true, y_pred, var,
    *,
    labels: list | None = None,
    n_cols: int = 3,                   # グリッド列数
    backend: Literal["matplotlib", "plotly"] = "matplotlib",
    normalize: Literal["true", "pred", "all", None] = "true",
    cmap: str = "Blues",
) -> Figure                            # 両 backend で Figure 返却(複数 axes 必要)

# 分類: confusion 情報量を ΔAIC で定量化(プロットではなく統計関数)
pycatdap.error.confusion_aic(
    y_true, y_pred,
) -> float
```

**`confusion_aic` の符号規約**: pycatdap 既存の `catdap1` / `target_analysis.ranking` と統一し、**ΔAIC = AIC(model) - AIC(null) で「負ほど情報量が大きい」**。null model = `y_pred` と `y_true` が独立(`y_pred` を捨てて baseline 多項分布で `y_true` を fit)。実装は `pycatdap._aic.compute_delta_aic` を流用(target_analysis と同じ経路)。

Issue #18 本文は「positive when informative」と書かれているが、これは執筆時のラフな期待値。pycatdap 全体で「ΔAIC は負が良い」を貫いてきたため、本 Proposal でこの方向を確定し、docstring と Notebook 12 で「負 = informative」と明示する。Issue にコメントで報告。

#### B. Phase J 公開 API(`pycatdap.error.*`)

```python
# 回帰: 残差散布図 (y_pred vs residual) または (y_true vs y_pred)
pycatdap.error.residual_plot(
    y_true, y_pred,
    *,
    kind: Literal["scatter_pred_resid", "scatter_true_pred", "histogram"] = "scatter_pred_resid",
    color_by: pd.Series | npt.NDArray | None = None,  # 第3変数で色分け
    backend: Literal["matplotlib", "plotly"] = "matplotlib",
    ax=None,
) -> Axes | Figure

# 回帰: 残差をカテゴリ別 box (説明変数のカテゴリで層別)
pycatdap.error.residual_by_category(
    df, y_true, y_pred, var,
    *,
    bins: int | None = None,           # var が連続なら AIC binning(target_summary と同じ規約)
    backend: Literal["matplotlib", "plotly"] = "matplotlib",
    ax=None,
) -> Axes | Figure

# 回帰: AIC pooling 結果を |residual| ヒストグラム + 境界線で可視化
pycatdap.error.residual_pool_plot(
    y_true, y_pred,
    *,
    n_bins: int = 4,                   # 初期分位ビン数(residual_label と同じ)
    backend: Literal["matplotlib", "plotly"] = "matplotlib",
    ax=None,
) -> Axes | Figure
```

#### C. `ErrorAnalysisResult` への delegation メソッド追加

ユーザーが `r = pycatdap.error_analysis(...)` の後で `r.plot_confusion()` を直接呼べるようにする(ergonomics):

```python
# src/pycatdap/error/_result.py に追加
class ErrorAnalysisResult:
    def plot_confusion(self, *, backend="matplotlib", **kwargs) -> Any:
        """Plot the confusion summary. classification + binary のみ動作。
        regression / multiclass 時は ValueError。"""
        ...

    def residual_plot(self, *, backend="matplotlib", **kwargs) -> Any:
        """Plot residuals. regression のみ動作。classification 時は ValueError。"""
        ...
```

これらは内部で `y_true` / `y_pred` を保持しないので、現在の `ErrorAnalysisResult` には十分なデータが**ない**(`confusion` は集計済 4 行 DataFrame、`residual_pooling` は bin layout のみ、生の y_true/y_pred を持たない)。

**選択肢**:

- **C-1**: `ErrorAnalysisResult` に `y_true: npt.NDArray | None` / `y_pred: npt.NDArray | None` フィールドを追加(immutable: `__post_init__` で `flags.writeable = False`)
- **C-2**: delegation メソッドを諦め、`pycatdap.error.plot_confusion(y_true, y_pred)` を直接呼ばせる
- **C-3**: delegation だが y_true/y_pred は外部から渡す(`r.plot_confusion(y_true, y_pred)`)

**採用: C-1**。理由:
- ユーザー体験が圧倒的に良い(ワンコールで完結)
- v0.6.1 immutable pattern で安全に追加可能
- メモリコスト: y_true/y_pred の numpy 配列、大規模(数百万行)でなければ問題なし
- LizyStudio が `result.to_dict()` 経由で配列もシリアライズできる(将来オプション)

ただし `to_dict()` / `to_plotly_json()` の出力サイズが膨らむため、`include_raw_predictions=False` デフォルトを追加するか、`to_dict()` は配列を含めない(別途 `result.y_true` / `result.y_pred` でアクセス)選択。後者を採用。

#### D. Backend 配置

既存パターン(`pycatdap.plot.matplotlib` / `pycatdap.plot.plotly` に backend impl、`pycatdap.plot.__init__` で dispatch)に揃える:

| ファイル | 追加内容 |
|---|---|
| `src/pycatdap/plot/matplotlib.py` | `plot_confusion_mpl` / `plot_confusion_by_slice_mpl` / `residual_plot_mpl` / `residual_by_category_mpl` / `residual_pool_plot_mpl` |
| `src/pycatdap/plot/plotly.py` | 同上(`_plotly` suffix) |
| `src/pycatdap/error/confusion.py`(NEW) | `plot_confusion` / `plot_confusion_by_slice` / `confusion_aic` dispatch + 型シグネチャ |
| `src/pycatdap/error/residual.py`(NEW) | `residual_plot` / `residual_by_category` / `residual_pool_plot` dispatch + 型シグネチャ |
| `src/pycatdap/error/__init__.py` | 上記を re-export |
| `src/pycatdap/error/_result.py` | `plot_confusion` / `residual_plot` メソッド追加、`y_true` / `y_pred` フィールド追加 |
| `src/pycatdap/error/analysis.py` | `ErrorAnalysisResult` 構築時に `y_true` / `y_pred` をセット |

#### E. Multiclass 対応

H-0010 §C で `confusion_label` は multiclass で `NotImplementedError`、Phase H wrapper は `error_label` に fallback する。だが **confusion matrix 自体は multiclass で意味があり可視化したい** ニーズが強い。

Phase I の `plot_confusion(y_true, y_pred)` は **3+ クラスを正しく扱う**:

- `labels=` 引数でクラス順序を制御
- `np.unique(np.concatenate([y_true, y_pred]))` でクラス検出
- N×N の行列をヒートマップとして描画(N=2 でも N=10 でも同じパス)

`plot_confusion_by_slice` も同様に multiclass 対応。これは `confusion_label` の二値前提とは別の話で、ヒートマップ可視化レイヤーは制限なし。

#### F. `confusion_aic` の数学的定義

`y_true`(観測) × `y_pred`(予測) の 2 元クロス表 `C[i,j]` に対して:

- **Saturated model**: 各セルが独立パラメータ(自由度 = N²−1、N = クラス数)
- **Null model**: `y_true` の周辺分布のみ(`y_pred` を捨てる、自由度 = N−1)
- **Model**: 「`y_pred = y_true` ならば correct、それ以外は incorrect」の 2 値出力 → 多項 model に変換し AIC 計算

実装方針(cross-check 2026-05-29 で確認、F-1 修正済):

既存 `pycatdap._aic.compute_delta_aic` の **正しいシグネチャは** `compute_delta_aic(cross_freq, marginal_e, marginal_f, n)`(全 numpy 配列 + スカラー)。`y_true` / `y_pred` を直接渡せないので、`confusion_aic` 実装は以下のフロー:

```python
def confusion_aic(y_true, y_pred) -> float:
    # 1. クラスの集合を確定(union)
    classes = np.unique(np.concatenate([y_true, y_pred]))
    # 2. C×C contingency table を構築(pd.crosstab で OK、欠損カテゴリは reindex で 0 補完)
    cross = pd.crosstab(y_true, y_pred, dropna=False).reindex(
        index=classes, columns=classes, fill_value=0
    ).to_numpy()
    # 3. marginals
    marginal_e = cross.sum(axis=1)  # y_true 周辺
    marginal_f = cross.sum(axis=0)  # y_pred 周辺
    n = int(cross.sum())
    # 4. compute_delta_aic を呼ぶ
    return compute_delta_aic(cross, marginal_e, marginal_f, n)
```

つまり `confusion_aic(y_true, y_pred) == catdap1(df, response="y_true", x="y_pred").delta_aic` と等価(値の上では)。Phase I 実装は **新規 AIC 計算をせず** 既存関数を呼ぶ薄いラッパー。`_aic.py:192-194` で確認済 — return は `AIC(model) - AIC(null)` で「負ほど informative」。

#### F-bis. `plot_confusion_by_slice` の戻り値型(cross-check Claim 6 修正)

既存 `pycatdap.plot.*` の matplotlib backend は **すべて `Axes` を返す**(`aic_heatmap` 含む)。`plot_confusion_by_slice` は multi-panel small-multiples のため `Axes` 1 つでは表現できない。`Figure` を返す:

- `backend="matplotlib"`: `matplotlib.figure.Figure`(他関数の `Axes` 規約からの**意図的な例外**)
- `backend="plotly"`: `plotly.graph_objects.Figure`(subplots を `make_subplots` で組み立てる)
- `ax=` 引数は **受け取らない**(複数 axes を内部生成)
- API docstring と Acceptance Criteria でこの例外を明記
- 将来 `plot_residual_by_category_grid` 等も追加する場合は同じ "grid 系は Figure" 規約を適用

これに伴い Acceptance Criteria の "matplotlib backend は Axes を返す" 行を「`plot_confusion_by_slice` を除き Axes、`plot_confusion_by_slice` のみ Figure」に修正。

#### F-ter. `ErrorAnalysisResult.plot_confusion()` の multiclass 仕様(cross-check Claim 4 修正)

cross-check で「C-1 を採用して `y_true`/`y_pred` を保持するなら、multiclass でも N×N ヒートマップは描画できる。`label_kind == "error_label"` (multiclass fallback) で ValueError は設計矛盾」と指摘された。

修正後の仕様:

- `result.plot_confusion(**kwargs)` は `self.task == "classification"` であれば **multiclass でも描画する**
- 内部実装: `pycatdap.error.plot_confusion(self.y_true, self.y_pred, **kwargs)` をそのまま呼ぶ(`y_true`/`y_pred` は v0.9.0 で追加するフィールドから取得)
- `self.task == "regression"` のときのみ `ValueError("plot_confusion is classification-only; got task='regression'")`
- 同様に `result.residual_plot()` は `self.task == "classification"` のとき `ValueError`

これにより `confusion`(集計 4 行 DataFrame、`label_kind == "confusion_label"` のみ有効)は **HTML レポート / `to_dict()` 用の表形式サマリ** として残し、**プロットは raw `y_true`/`y_pred` から再計算**する責務分離になる。

#### F-quater. `ErrorAnalysisResult` への `y_true` / `y_pred` 追加と `__post_init__` の None ガード(cross-check Claim 3 修正)

cross-check で「`tests/test_error_analysis_result.py` に 12 箇所の直接コンストラクタ呼び出しがあり、デフォルト値追加で技術的に壊れないが `__post_init__` の numpy freeze が `None` を受けるとエラー」と指摘された。

修正後の実装方針:

- `y_true: npt.NDArray[Any] | None = None`(デフォルト `None`)
- `y_pred: npt.NDArray[Any] | None = None`(同上)
- `__post_init__` で:
  ```python
  if self.y_true is not None and isinstance(self.y_true, np.ndarray):
      self.y_true.flags.writeable = False
  if self.y_pred is not None and isinstance(self.y_pred, np.ndarray):
      self.y_pred.flags.writeable = False
  ```
- 既存テスト 12 箇所は **修正不要**(デフォルト `None` で動作)。ただし PR-H3 で「delegation メソッドの test」を追加する際は `y_true`/`y_pred` を明示する fixture を新規追加
- `to_dict()` / `to_plotly_json()` は配列を含めない(既存出力サイズを変えない)
- `error_analysis()` ラッパーは構築時に必ず `y_true=y_true_arr.copy()` / `y_pred=y_pred_arr.copy()` をセット(`.copy()` で freeze が呼び出し側の元配列に波及しないようにする)

#### G. Phase I+J が解決しないこと(スコープアウト)

#### G. Phase I+J が解決しないこと(スコープアウト)

- **Multivariable subgroup viz**: 多変数組み合わせの confusion / residual サブグループ可視化 → Phase L
- **Calibration**: `calibration_curve` / `brier_score` / ECE → Phase K(v0.10.0)
- **Drift detection**: `compare_cohorts` / `detect_drift` → Phase L
- **アニメーション / インタラクティブ slider**: Phase I+J は静的可視化のみ。Plotly の hover は支援するが slider / animation はスコープ外
- **3D viz / surface plot**: Phase I+J はすべて 2D

### Alternatives Considered

#### A1: 既存 `pycatdap.plot.*` に直接追加(error/ サブパッケージを使わない)

- **不採用理由**: Phase G/H の「error 関連は `pycatdap.error.*` に集める」設計と乖離。tab completion で `pycatdap.error.<TAB>` を打つユーザは confusion / residual プロット関数を期待する。

#### A2: `ErrorAnalysisResult` に y_true / y_pred を持たせない(C-2 / C-3)

- **不採用理由**: ユーザー体験劣化。`r.plot_confusion()` の自然さを失う。メモリコストは現実的データサイズで無視できる。

#### A3: matplotlib backend を必須にする(plotly backend を後回し)

- **不採用理由**: pycatdap.plot の既存パターンは「両 backend 同時実装」。片方だけだと他関数との整合性が崩れる。Phase I+J はリリース時に両 backend サポート必須。

#### A4: confusion matrix を Plotly Table で描画

- **不採用理由**: ヒートマップ(`go.Heatmap`)の方が情報量を視覚的に伝える。sklearn `ConfusionMatrixDisplay` も heatmap。慣習に従う。

#### A5: `confusion_aic` を「positive = informative」符号にする(Issue 本文に従う)

- **不採用理由**: pycatdap 全体で `delta_aic` は「負ほど良い」(`target_analysis.ranking`、`catdap1`、`profile`)。confusion_aic だけ符号反転すると認知負荷が高い。Notebook 12 で「負 = informative」を明示し、Issue にコメントで報告。

### Acceptance Criteria

- [ ] `pycatdap.error.plot_confusion / plot_confusion_by_slice / confusion_aic` が動作(Phase I)
- [ ] `pycatdap.error.residual_plot / residual_by_category / residual_pool_plot` が動作(Phase J)
- [ ] 全プロット関数が `backend="matplotlib"` と `backend="plotly"` で動作
- [ ] matplotlib backend: `ax=` 引数受け入れ、`matplotlib.axes.Axes` を返す **(例外: `plot_confusion_by_slice` のみ `matplotlib.figure.Figure` を返す、`ax=` 受け取らず)**
- [ ] plotly backend: `plotly.graph_objects.Figure` を返す
- [ ] `plot_confusion(multiclass_y_true, multiclass_y_pred)` が正しく N×N ヒートマップを描画
- [ ] `confusion_aic` が `catdap1(df, response="y_true", x="y_pred").delta_aic` と数値一致(回帰テスト)
- [ ] `confusion_aic` が**負値**を返す(prediction informative の test fixture)
- [ ] `ErrorAnalysisResult.plot_confusion()` / `.residual_plot()` が delegation で動作
- [ ] `ErrorAnalysisResult.plot_confusion()` は **multiclass classification でも N×N ヒートマップを描画**(regression のみ `ValueError`)
- [ ] `ErrorAnalysisResult.residual_plot()` は **regression のみ動作**、classification で `ValueError`
- [ ] `ErrorAnalysisResult.y_true` / `.y_pred` が numpy buffer frozen(H-0009 pattern、`None` ガード付き `__post_init__`)
- [ ] 既存 `tests/test_error_analysis_result.py` 12 箇所の直接コンストラクタ呼び出しが **無修正で pass**(`y_true=None` / `y_pred=None` デフォルト動作)
- [ ] `error_analysis()` ラッパーは `y_true=arr.copy()` / `y_pred=arr.copy()` で defensive copy(呼び出し側元配列の freeze を防ぐ)
- [ ] `to_dict()` / `to_plotly_json()` は raw y_true / y_pred を含めない(出力サイズ抑制)
- [ ] Issue #18 に「confusion_aic の符号規約は ΔAIC 既存規約に従い負=informative」コメント済
- [ ] backend 未導入時は明示的 `ImportError`(matplotlib なら `pycatdap[plot]`、plotly なら `pycatdap[plotly]`)
- [ ] 80% 以上の line coverage、TDD で test → impl
- [ ] BLUEPRINT.md §5.8 を Phase I+J released に更新
- [ ] Tutorial Notebook 12 で 6 プロット関数 + `ErrorAnalysisResult` delegation のフルデモ
- [ ] Issue #18 が close される
- [ ] CHANGELOG.md v0.9.0 セクション、Phase H → I+J 連結明記

### PR 分割

| PR | スコープ | 依存 |
|---|---|---|
| **PR-H0**(本 Proposal) | `docs(history): propose H-0012` | none |
| **PR-H1** | Phase I 関数群: `confusion_aic` + `plot_confusion` + `plot_confusion_by_slice` + matplotlib/plotly backend 実装 + tests | PR-H0 merge |
| **PR-H2** | Phase J 関数群: `residual_plot` + `residual_by_category` + `residual_pool_plot` + matplotlib/plotly backend 実装 + tests | PR-H0 merge(H1 と並行可) |
| **PR-H3** | `ErrorAnalysisResult` に `y_true` / `y_pred` フィールド追加 + `plot_confusion` / `residual_plot` delegation メソッド + tests | PR-H1 + PR-H2 merge |
| **PR-H4** | Tutorial Notebook 12 + BLUEPRINT §5.8 更新 + README quickstart + CHANGELOG cut to v0.9.0 + Issue #18 close | PR-H3 merge |
| **PR-H5**(release) | `release: v0.9.0` | PR-H4 merge |

各 PR は CI green 確認後に次へ進む。develop に **squash** で merge、release PR のみ `--merge`(release line 維持)。

### Decision

- Date: `TBD`
- Result: `pending`
- Notes: PR-H0(本 PR)で Proposal 承認待ち。

### Migration

破壊的変更なし。新規追加のみ:

- `pycatdap.error.plot_confusion / plot_confusion_by_slice / confusion_aic`
- `pycatdap.error.residual_plot / residual_by_category / residual_pool_plot`
- `ErrorAnalysisResult.y_true` / `.y_pred` フィールド(新規追加。既存コンストラクタ呼び出しは引数追加で更新必要)
- `ErrorAnalysisResult.plot_confusion()` / `.residual_plot()` メソッド

**`ErrorAnalysisResult` のコンストラクタ署名変更は破壊的変更**:

`y_true: npt.NDArray | None = None` / `y_pred: npt.NDArray | None = None` をデフォルト引数で追加するので、既存呼び出しは無影響。`error_analysis()` ラッパー側で自動セットされるため、ユーザコードは変更不要。

### Related References

- 親仕様: H-0001 Phase I+J、Issue #18
- 前段: H-0011 Phase H(`error_analysis` + `ErrorAnalysisResult`、v0.8.0 で出荷済)
- backend dispatch パターン: `src/pycatdap/plot/__init__.py:43-54` の `_get_backend_module`
- 既存可視化リファレンス: `pycatdap.plot.aic_heatmap`(2D heatmap、Plotly 実装あり)、`pycatdap.plot_target` の binned-numeric mode(box per category)
- sklearn ConfusionMatrixDisplay: <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.ConfusionMatrixDisplay.html>(ヒートマップ慣習の参考)
- Immutable pattern: H-0009 / H-0011 PR-G1(`__post_init__` numpy freeze)

## 2026-05-29: Phase K calibration(AIC binning による信頼性診断)

- ID: `H-0013`
- Status: `accepted`
- Scope: `API | plot | data-contract`
- Related: `H-0001 Phase K`, `H-0012 Phase I+J`, `BLUEPRINT.md §5.8`, Issue #19 / #11

### Context

H-0012(v0.9.0)で Phase I+J(confusion / residual 可視化 + `ErrorAnalysisResult` delegation)が出荷され、誤差分析の「分類の当たり外れ」「回帰の残差」が可視化できるようになった。Phase K はその次の問い —— **「モデルが 70% と言ったとき、実際に 70% 起きるのか?」**(確率予測の calibration / 信頼性) —— に答える。

pycatdap 固有の価値は **確率軸の AIC-optimal binning**:sklearn / netcal の equal-width / quantile ビンと違い、観測陽性率が実際にシフトする位置に境界を置く。Issue #19 が指摘する **歪んだ(skewed)確率予測** に対して特に優位。既存 `_pooling.optimal_binning`(Phase J `residual_by_category` で連続変数 binning に使用済)を確率軸に流用する。

公開 API・data contract(`ErrorAnalysisResult` への新フィールド)に触れるため Change Gate 対象。本 Proposal を先行 merge(PR-K0)し、merge 前に cross-check で設計トラップを検証する(H-0011 / H-0012 と同じ運用 — 前回は 4 件の罠を事前に潰した)。

### Proposal

#### A. Phase K 公開 API(`pycatdap.error.*`)

```python
# 信頼性図(reliability diagram)+ Wilson 二項信頼区間。プロット関数。
pycatdap.error.calibration_curve(
    y_true, y_proba,
    *,
    strategy: Literal["aic", "equal_width", "quantile"] = "aic",
    n_bins: int = 10,                  # equal_width / quantile のビン数(strategy="aic" では無視)
    backend: Literal["matplotlib", "plotly"] = "matplotlib",
    ax=None,                           # matplotlib 用
) -> Axes | Figure

# 信頼性図の背後にある数値テーブル(metric の single source of truth)
pycatdap.error.calibration_table(
    y_true, y_proba,
    *,
    strategy="aic", n_bins=10,
) -> pd.DataFrame                       # cols: bin_low, bin_high, n, prob_pred, prob_true, ci_low, ci_high

# スカラーメトリクス(プロットではなく統計関数、confusion_aic と同じ位置づけ)
pycatdap.error.brier_score(y_true, y_proba) -> float
pycatdap.error.expected_calibration_error(y_true, y_proba, *, strategy="aic", n_bins=10) -> float
pycatdap.error.maximum_calibration_error(y_true, y_proba, *, strategy="aic", n_bins=10) -> float
```

**sklearn との命名差**:sklearn の `calibration_curve` は `(prob_true, prob_pred)` の配列を返すデータ関数だが、pycatdap の `calibration_curve` は Phase I/J の `plot_confusion` / `residual_plot` と一貫して **Figure を返すプロット関数**(Issue #19 の `backend=` 署名に従う)。数値が欲しい場合は `calibration_table` を使う。docstring でこの差を明記する。

#### B. binning 戦略(aic / equal_width / quantile)

| strategy | 実装 | 用途 |
|---|---|---|
| `"aic"`(default) | `optimal_binning(values=y_proba, response=y_true)` の `.boundaries` で確率軸を分割。`n_bins` は無視 | pycatdap 固有。陽性率がシフトする位置に境界。skewed 予測に強い |
| `"equal_width"` | `np.linspace(0, 1, n_bins+1)` | sklearn `strategy="uniform"` 相当 |
| `"quantile"` | `np.quantile(y_proba, ...)` で等頻度ビン | sklearn `strategy="quantile"` 相当 |

Issue #19 本文の `n_bins="aic"|int` という overload は、3 戦略を表現できないため **explicit な `strategy` + `n_bins`** に分解する(Alternatives A2)。AIC binning は `residual_by_category`(`plot/matplotlib.py`)の連続変数 binning と同じ消費パターン(`PoolingResult.codes` / `.boundaries`)だが、response は残差符号 proxy ではなく **y_true(二値)を直接** 使う。

#### B-bis. cross-check 由来の実装 safeguard(2026-05-29)

merge 前 cross-check で 2 件の実装トラップを検出。`_pooling.py` の挙動を読んで確認済:

- **(1) AIC の初期グリッドを有界化(必須)**: `optimal_binning(values, response, accuracy=None)` は `accuracy=None` のとき `_auto_accuracy`(`_pooling.py:49-58`)で「ソート済ユニーク値の最小正ギャップ」を accuracy にする。モデル確率は 0.6231, 0.6234… のように細かいため最小ギャップが `~1e-4` になり、`_initial_bins`(`_pooling.py:80`)の `n_bins = ceil((vmax-vmin)/accuracy)` が **数千本に爆発**して bottom-up merge が極端に遅くなる。

  → calibration では **明示的に `accuracy` を渡す**。確率は概念上 [0,1] 有界なので、固定の初期グリッド解像度 `_AIC_INIT_BINS`(モジュール定数、既定 50)から `accuracy = 1.0 / _AIC_INIT_BINS`(= 0.02)を算出して渡す。初期ビンは ≤ 50 本に有界化され、その後 AIC bottom-up merge が最適な粗いビンを発見する(AIC binning の本来の動作)。`residual_by_category` は粒度の粗い説明変数を対象とするため auto で問題が出ていなかったが、確率軸では明示指定が必須。

- **(2) ECE/MCE の空ビンスキップ(必須)**: `strategy="equal_width"` で [0,1] を等幅分割すると観測の無い空ビン(`n_b=0`)が生じうる。ECE は `n_b/N` 重みで自然に 0 寄与だが、**MCE と per-bin 平均(`prob_true_b` / `prob_pred_b`)は空ビンを除外**してゼロ除算 / 未定義平均を回避する。`_calibration_table` は空ビン行を出力しない(または `n=0` 行を metric 計算で skip)。

- **(3) response dtype(軽微)**: `_encode_response`(`_pooling.py:124-129`)は `np.unique(..., return_inverse=True)` ベースで int 0/1 をそのまま処理できる。`y_true` を object/str に astype する必要はなく、二値配列を直接渡す。

#### C. `ErrorAnalysisResult` への `y_proba` 追加 + `calibration_curve` delegation

calibration は y_pred(ラベル)ではなく **y_proba(確率)** を要するため、H-0012 の y_true/y_pred とは別に新フィールドが必要:

```python
# src/pycatdap/error/_result.py
class ErrorAnalysisResult:
    y_proba: npt.NDArray[Any] | None = field(default=None, repr=False)  # 新フィールド

    def calibration_curve(self, *, strategy="aic", n_bins=10,
                          backend="matplotlib", **kwargs) -> Any:
        """信頼性図。classification + y_proba 保持時のみ動作。
        regression / y_proba 未設定で ValueError。"""
        ...
```

- `default=None` で後方互換(H-0012 の y_true/y_pred 追加と同パターン。既存の直接コンストラクタ呼び出しは無修正)
- `__post_init__` で `None` ガード付き numpy freeze(`_result.py:187-190` の y_true/y_pred と同じ)
- `error_analysis(..., y_proba=None)` を optional param で追加。`_resolve_one` で正規化、defensive `.copy()`(`analysis.py:228-229` と同じ)
- `to_dict()` / `to_plotly_json()` は **y_proba を含めない**(出力サイズ抑制、y_true/y_pred と同様)

#### D. Backend 配置

H-0012 のパターン(error 層が dispatch、plot 層が impl)に揃える:

| ファイル | 追加内容 |
|---|---|
| `src/pycatdap/error/calibration.py`(NEW) | `calibration_curve` dispatch + `calibration_table` + `brier_score` + `expected_calibration_error` + `maximum_calibration_error` + 私的 `_calibration_table` / `_wilson_interval` / `_bin_edges`(aic/equal_width/quantile)+ モジュール定数 `_AIC_INIT_BINS = 50`(B-bis (1)) |
| `src/pycatdap/plot/matplotlib.py` | `calibration_curve`(reliability diagram、`Axes` 返却、`ax=` 受入) |
| `src/pycatdap/plot/plotly.py` | `calibration_curve`(`Figure` 返却、`error_y` で CI) |
| `src/pycatdap/error/__init__.py` | 上記 5 関数を re-export |
| `src/pycatdap/error/_result.py` | `y_proba` フィールド + `calibration_curve` メソッド |
| `src/pycatdap/error/analysis.py` | `y_proba` param + 構築時セット |

**循環 import 回避**:純 numpy の `_calibration_table`(binning + per-bin 統計 + CI)は `error/calibration.py` に置く。backend の `calibration_curve` は関数内で `from pycatdap.error.calibration import _calibration_table` を **lazy import**(`error/calibration.py` 側は backend を `_get_backend_module` で lazy dispatch)。これにより `import pycatdap.error` が matplotlib 非依存を維持する(lowest-deps CI 安全)。

#### E. Wilson 二項信頼区間

reliability diagram の各ビンの観測陽性率に二項信頼区間を表示する。既存ヘルパは無いため **pure-numpy で Wilson score interval** を新規実装:

```
center = (p̂ + z²/2n) / (1 + z²/n)
half   = (z / (1 + z²/n)) * sqrt(p̂(1-p̂)/n + z²/4n²)
ci = [center - half, center + half]   # z = 1.96 (95%)
```

normal approx は p→0/1 近傍で区間が [0,1] を外れるが、Wilson は内側に収まる —— skewed 予測の calibration(Issue #19 の主眼)で重要。**scipy 非依存**(`_aic.py` の `_safe_xlogy` のような optional-fallback すら不要)。

#### F. メトリクスの数学的定義

すべて `_calibration_table` の 1 回の呼び出しから導出 → diagram と metric が乖離しない(single source of truth):

- **Brier score** = `mean((y_proba - y_true)²)`(二値)。`sklearn.metrics.brier_score_loss` の二値と一致。table 非依存(全点)
- **ECE** = `Σ_b (n_b / N) · |prob_true_b − prob_pred_b|`(ビン重み付き絶対差の平均)
- **MCE** = `max_b |prob_true_b − prob_pred_b|`(最悪ビンの絶対差)

sklearn には ECE/MCE の直接関数が無い(netcal にある)。テストは **equal_width binning で inline reference 式と 1e-9 一致** を確認(netcal/sklearn 依存を避ける)。AIC binning は参照実装が無いため non-degenerate + 自値 pin。

#### G. Phase K が解決しないこと(スコープアウト)

- **回帰 calibration**(predicted vs actual quantiles、netcal の回帰モード)→ v0.11.0。二値分類 calibration とは別概念(quantile calibration)のため本リリースから分離(Alternatives A3)
- **multi-class calibration**(one-vs-rest)→ v0.11.0。Phase H が multiclass `confusion_label` を defer したのと同じ判断
- **確率の補正**(Platt scaling / isotonic recalibration)→ Phase K は **診断のみ**。再校正はスコープ外
- **top-level `pycatdap.*` 再エクスポート** → `pycatdap.error.*` のみ(Phase I/J と一貫)

### Compatibility

**破壊的変更なし。** すべて新規追加:

- 新規公開関数 5 個はすべて `pycatdap.error.*` 名前空間の追加のみ
- `ErrorAnalysisResult.y_proba` は `default=None` で追加(H-0012 の y_true/y_pred と同パターン)。既存の直接コンストラクタ呼び出し(テスト含む)は **無修正で動作**
- `error_analysis(y_proba=None)` は末尾 keyword-only optional param の追加。既存呼び出しは無影響
- `to_dict()` / `to_plotly_json()` の出力スキーマは不変(y_proba を含めない)

### Alternatives Considered

#### A1: `calibration_curve` を sklearn 同様にデータ(prob_true, prob_pred)を返す

- **不採用理由**: Phase I/J の `plot_*` が Figure を返す規約・Issue #19 の `backend=` 署名と矛盾。代わりに `calibration_table` で数値を提供し、命名差を docstring で明記。

#### A2: `n_bins="aic"|int` の overload(Issue #19 本文の署名)

- **不採用理由**: aic / equal_width / quantile の 3 戦略を 1 引数で表現できない。explicit な `strategy` + `n_bins` に分解。

#### A3: 回帰 calibration も v0.10.0 に含める

- **不採用理由**: 回帰の quantile calibration は二値分類 calibration とは別概念でスコープが肥大。Phase H の multiclass defer と同じ方針で v0.11.0 に分離。

#### A4: normal approximation の信頼区間(Wald)

- **不採用理由**: p→0/1 近傍で区間が [0,1] を外れる。skewed 予測の calibration で頻発するため Wilson を採用。

#### A5: scipy.stats で CI / メトリクスを計算

- **不採用理由**: scipy は optional dep。`Quality (lowest-direct deps)` CI で使えない。Wilson + Brier/ECE/MCE はすべて pure-numpy で十分。

#### A6: `ErrorAnalysisResult` に y_proba を持たせず delegation を諦める(C-2 相当)

- **不採用理由**: ユーザー判断で delegation 採用(2026-05-29)。`r.calibration_curve()` のワンコール体験を優先。メモリコストは現実的データサイズで無視可能。

#### A7: AIC binning で `optimal_binning(accuracy=None)` の auto-accuracy に委ねる

- **不採用理由**: cross-check で検出(B-bis (1))。連続確率の最小ギャップ `~1e-4` を accuracy に採ると初期ビンが数千本に爆発し bottom-up merge が極端に遅くなる。[0,1] 有界の固定初期グリッド(`_AIC_INIT_BINS`)から accuracy を明示算出する。

### Acceptance Criteria

- [ ] `calibration_curve / calibration_table / brier_score / expected_calibration_error / maximum_calibration_error` が動作
- [ ] `strategy="aic"` が `optimal_binning` で non-degenerate な bin を生成
- [ ] `strategy in {"equal_width", "quantile"}` が動作
- [ ] `calibration_curve` が両 backend で動作、matplotlib は `Axes`(`ax=` 受入)/ plotly は `Figure`
- [ ] reliability diagram に Wilson 二項 CI を表示
- [ ] `expected_calibration_error(strategy="equal_width")` が inline reference 式と `1e-9` 一致(netcal/sklearn 非依存)
- [ ] `brier_score` が手計算値と一致
- [ ] 二値以外の `y_true` → `ValueError`
- [ ] `y_proba ∉ [0, 1]` → `ValueError`
- [ ] 退化入力(全 proba 同値)→ 1 bin、クラッシュなし
- [ ] `strategy="aic"` の初期グリッドは [0,1] 上で有界(≤ `_AIC_INIT_BINS` 本)— 連続確率でも初期ビン爆発なし(明示 `accuracy` 渡し)
- [ ] ECE/MCE は空ビン(`n_b=0`)をスキップ(`equal_width` で発生しうる)、ゼロ除算なし
- [ ] `ErrorAnalysisResult.y_proba` が numpy buffer frozen(`None` ガード付き `__post_init__`)
- [ ] `error_analysis(y_proba=)` が `y_proba=arr.copy()` で defensive copy
- [ ] `r.calibration_curve()` delegation が動作、regression / y_proba 不在で `ValueError`
- [ ] 既存の直接コンストラクタ呼び出しが **無修正で pass**(`y_proba=None` default)
- [ ] `to_dict()` / `to_plotly_json()` は raw y_proba を含めない
- [ ] sklearn / scipy を src calibration path とテストで import しない(lowest-deps CI 安全)
- [ ] 80% 以上の line coverage、TDD で test → impl
- [ ] BLUEPRINT.md §5.8 を Phase K released に更新
- [ ] Tutorial Notebook 13 で全関数 + `ErrorAnalysisResult` delegation のフルデモ
- [ ] Issue #19 に scope note(回帰 / multi-class は v0.11.0 へ defer)コメント
- [ ] CHANGELOG.md v0.10.0 セクション

### PR 分割

| PR | スコープ | 依存 |
|---|---|---|
| **PR-K0**(本 Proposal) | `docs(history): propose H-0013` | none |
| **PR-K1** | `calibration.py`(curve dispatch + table + Brier/ECE/MCE + Wilson CI)+ matplotlib/plotly backend 実装 + `error/__init__` export + tests | PR-K0 merge |
| **PR-K2** | `ErrorAnalysisResult.y_proba` フィールド + `calibration_curve` delegation + `error_analysis(y_proba=)` + tests | PR-K1 merge |
| **PR-K3** | Tutorial Notebook 13 + BLUEPRINT §5.8 更新 + README + CHANGELOG cut to v0.10.0 + Issue #19 scope note | PR-K2 merge |
| **PR-K4**(release) | `release: v0.10.0` | PR-K3 merge |

各 PR は CI green 確認後に次へ進む。develop に **squash** で merge、release PR のみ `--merge`(release line 維持)。

### Decision

- Date: `2026-05-29`
- Result: `accepted`
- Notes: PR-K0 で Proposal 承認。merge 前 cross-check で §B-bis(AIC accuracy 有界化 / 空ビン skip)を反映。PR-K1〜K3 で実装・出荷(v0.10.0)。

### Migration

破壊的変更なし。新規追加のみ:

- `pycatdap.error.calibration_curve / calibration_table / brier_score / expected_calibration_error / maximum_calibration_error`
- `ErrorAnalysisResult.y_proba` フィールド(`default=None`、既存無影響)
- `ErrorAnalysisResult.calibration_curve()` メソッド
- `error_analysis(y_proba=)` optional param

ユーザコードの変更は不要。`error_analysis()` に `y_proba=` を渡せば `r.calibration_curve()` が使えるようになる(opt-in)。

### Related References

- 親仕様: H-0001 Phase K、Issue #19 / #11
- 前段: H-0012 Phase I+J(plot backend dispatch + `ErrorAnalysisResult` delegation pattern)
- AIC binning: `src/pycatdap/_pooling.py` `optimal_binning`、`residual_by_category`(`plot/matplotlib.py:1257-1272`)の連続変数 binning 消費パターン
- delegation pattern: `src/pycatdap/error/_result.py:439-526`(`plot_confusion` / `residual_plot`)
- defensive copy: `src/pycatdap/error/analysis.py:228-229`
- Wilson score interval: <https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval#Wilson_score_interval>
- sklearn calibration_curve(データ返却の対比): <https://scikit-learn.org/stable/modules/generated/sklearn.calibration.calibration_curve.html>
- netcal(ECE/MCE / 回帰 calibration の参考): <https://github.com/EFS-OpenSource/calibration-framework>

## 2026-05-29: Phase L slice discovery + cohort comparison + drift detection(誤差サブグループの自動発見)

- ID: `H-0014`
- Status: `accepted`
- Scope: `API | data-contract | types`
- Related: `H-0001 Phase L`, `H-0002 FR-5/FR-7/FR-9`, `H-0013 Phase K`, `BLUEPRINT.md §5.8`, Issue #20 / #11

### Context

H-0013(v0.10.0)で Phase K(binary calibration)が出荷され、確率予測の信頼性診断が可能になった。誤差分析アーク(Phase G→H→I+J→K)は「ラベル化 → ワンコール分析 → 可視化 → calibration」を揃えたが、最後に残るのが **「モデルはどの部分集団で失敗しているのか」** という問い。

Phase L は AIC ベースで以下を自動化する:
1. **slice discovery**(`discover_error_slices`)— 多変数サブグループの誤差集中を自動発見(DivExplorer / SliceLine analog)。Phase H の単変数 `Slice` を多変数に拡張する。
2. **cohort comparison**(`compare_cohorts`)— 2 コホート間の分布差・関係性シフトを ΔAIC で定量化(Sweetviz analog)。
3. **drift detection**(`detect_drift`)— train/prod 間のデータ・誤差ドリフト検出。

加えて、H-0013 §G でスコープアウトした **calibration follow-up**(回帰 calibration の quantile 版 + multi-class one-vs-rest)を本リリースに同梱する(v0.10.0 で「v0.11.0 へ」と明記した分の回収)。

公開 API・data contract(新コンテナ型)を追加するため Change Gate 対象。本 Proposal を先行 merge(PR-L0)し、merge 前に cross-check で設計トラップを検証する(H-0011 / H-0012 / H-0013 と同じ運用 — 3 期連続で実トラップを事前検出した)。

### Proposal

#### A. Phase L 公開 API(`pycatdap.error.*`)

```python
# スライス発見(多変数サブグループの誤差集中)
pycatdap.error.discover_error_slices(
    df, y_true, y_pred,
    *,
    max_vars: int = 3,
    measure: str | Callable = "aic",   # "aic" | "cramers_v" | "mutual_info" | callable
    top_k: int = 10,
    min_support: int | float = 30,     # 枝刈り床(int=行数、float=割合)。§C 参照
) -> SliceDiscoveryResult

# コホート比較(分布差 + ΔAIC delta、Sweetviz 風レポート)
pycatdap.error.compare_cohorts(
    df_a, df_b,
    *,
    response: str | None = None,
) -> CohortComparison           # .to_html(path=) / .to_dict()

# ドリフト検出(train→prod の ΔAIC 変化)
pycatdap.error.detect_drift(
    df_train, df_prod,
    *,
    y_true=None, y_pred=None,
) -> DriftReport                # .to_dict()
```

新コンテナ型(いずれも frozen、H-0009 immutability discipline 準拠):

```python
@dataclass(frozen=True)
class ErrorSlice:
    conditions: tuple[tuple[str, str], ...]   # (("age","[45, 60)"),("marital_status","Never-married"))
    description: str                          # "age ∈ [45, 60] × marital_status = Never-married"
    size: int
    error_metric: float                       # スライス内 error rate
    delta_aic: float
    measure_value: float
    n_error_in_slice: int

@dataclass(frozen=True)
class SliceDiscoveryResult:
    slices: tuple[ErrorSlice, ...]
    measure: str
    max_vars: int
    base_aic: float
    n_evaluated: int                          # 実際にスコアした組合せ数
    n_pruned: int                             # 枝刈りで省いた組合せ数(>50% 削減の測定可能化)
    label_kind: str
    def to_divexplorer_format(self) -> pd.DataFrame: ...
    def to_dict(self) -> dict[str, Any]: ...
```

**既存の単変数 `Slice`(`_result.py`)は破壊しない**。Issue #20 本文は `list[Slice]` を返すと書くが、現行 `Slice` の `variable`/`category` はスカラー(単変数)であり、多変数化は破壊的変更になる。新規 `ErrorSlice` を導入する(Alternatives A1)。

#### B. アルゴリズム(discover_error_slices)

1. `error_label(y_true, y_pred)`(Phase G、既存)で合成 response E を生成(再利用)。
2. `df` をコピー(入力非破壊)、連続列を `optimal_binning(..., accuracy=<有界グリッド>)` で離散化。`boundaries` を区間整形用に保持。
3. 候補変数部分集合(最大 `max_vars`)ごとに合成分割表を構築 → `(cross, marg_e, marg_f, n)`。
4. スコアリング:ΔAIC は `compute_delta_aic`(`build_multidim_crosstab` の 4-tuple を消費)、`cramers_v`/`mutual_info`/custom は **既存の `pycatdap.measures` レジストリ**(`Measure = Callable[[NDArray], float]`、2D 分割表を消費、`register`/`get`)を再利用。これが FR-9 plug-in API そのもの — 新レジストリは作らない。**この 2 経路(`measure="aic"` の直接 ΔAIC vs registry measure)は別 call path のため、`discovery.py` で dispatch を明示する**(cross-check 可読性メモ)。
5. セル単位で `ErrorSlice` を生成(具体的サブグループ)。
6. measure 降順で `top_k`。
7. 枝刈り:`min_support` 未満の枝を切る(§C)。

description ビルダ:categorical → `"col = value"`、連続 → `boundaries` 参照で `"col ∈ [low, high]"`(整数境界の `.0` 除去)、複数条件を `" × "` 連結。出力は機械パース可能(受入文字列を逐語生成)。

#### C. 枝刈りは ΔAIC ではなく support で行う(load-bearing 設計判断)

Issue #20 は「AIC 単調性を利用した SliceLine 風 upper-bound pruning」を要求するが、**ΔAIC は健全な上界を持たない**:

```
AIC(E;F) = −2·loglik + 2·(C_E − 1)·C_F      # ペナルティ項が合成カーディナリティ C_F に線形
```

変数を追加すると `C_F`(`build_multidim_crosstab` が数える**観測済み合成タプル数**。各変数カーディナリティの積で上界されるが、観測のない組合せは数えないので積より小さくなりうる)が増えてペナルティが膨らむ一方、loglik は改善しうる。よって親スライスの ΔAIC は子スライスの ΔAIC を上界も下界もしない → **ナイーブな ΔAIC 枝刈りは真の top-k を黙って取りこぼす(正当性バグ)**。`src/pycatdap/_aic.py:107`(`penalty = 2.0 * (c_e - 1) * c_f`)で確認済(cross-check で検証済み)。

→ **support(スライスサイズ)ベースの枝刈りを採用**。support は anti-monotone(Apriori):子スライスの size ≤ 親の size。`min_support` 床と併用すれば「親が `min_support` 未満なら全子孫も未満」で枝を健全に切れる。20 変数データで >50% 探索空間削減を満たし、`min_support` を満たす top-k は決して落とさない(床未満はそもそもスコープ外:小セルは統計的に不安定で ΔAIC ペナルティノイズに支配される)。

**正当性担保**:exhaustive 列挙(`enumerate_exhaustive`)を正解 oracle として先に実装し、pruned 列挙(`enumerate_pruned`)は「`size >= min_support` の exhaustive 結果と完全一致」を RED フェーズの invariant テストで保証する(等価テストの定式化は `pruned == exhaustive(size≥min_support 限定)`。ナイーブな `pruned == exhaustive` ではない)。

#### D. compare_cohorts / detect_drift

- `compare_cohorts(df_a, df_b, response=None)` → `CohortComparison`(frozen):
  - 列ごとの分布差(categorical 直接、連続は両コホート union 由来の同一 bin)
  - 「コホート所属(a/b)」を合成二値 response として `compute_delta_aic` → コホートを最も判別する変数
  - `response` 指定時:各特徴の対 response ΔAIC のコホート間差(関係性シフト)
  - `.to_html()` は既存 jinja2 + atomic write + `pycatdap.templates` を再利用(新 template `cohort_comparison.html.j2`)
- `detect_drift(df_train, df_prod, y_true=None, y_pred=None)` → `DriftReport`(frozen):`compare_cohorts` の特化。特徴ごとの train→prod ΔAIC 変化を magnitude 順。y_true/y_pred 指定時は error_label 分布のドリフト(モデル劣化シグナル)も report。

#### E. calibration follow-up(binary 非破壊)

`calibration.py` の binary 関数・`_validate_binary_proba` は **一切触らない**。並置で追加:

- `regression_calibration_table(y_true, y_pred, *, n_quantiles=10)`:予測を分位ビン化し、ビンごとの mean predicted vs mean actual(純 numpy `np.quantile`)。`regression_calibration_curve` は backend dispatch。
- `multiclass_calibration_table(y_true, y_proba_matrix, *, classes=None, strategy="aic", n_bins=10)`:クラス k ごとに OvR 二値化(`y_true==k`, `y_proba[:,k]`)し **既存 `_calibration_table` をそのまま呼ぶ** → `class → table` の MappingProxyType。binary コア再利用が非破壊の最強保証。
- 新 validator は別関数(`_validate_regression` / `_validate_multiclass_proba`)。

#### F. backend dispatch 抽出(負債解消)

`error/confusion.py` / `residual.py` / `calibration.py` に重複する `_get_backend_module` + `Backend` Literal を `src/pycatdap/error/_backend.py` に抽出(v0.10.0 レビュー合意済みの「次モジュール追加時に実施」)。`compare_cohorts.to_html` が 4 番目の消費者になる前に実施し、消費者追加(L4)前に refactor(L1)を入れて conflict storm を回避。

### Impact

| 対象 | 追加/変更 |
|---|---|
| `src/pycatdap/error/_backend.py`(新) | backend dispatch 抽出 |
| `src/pycatdap/error/_slice.py`(新) | `ErrorSlice` + `SliceDiscoveryResult` |
| `src/pycatdap/error/_describe.py`(新) | description ビルダ + 区間整形 |
| `src/pycatdap/error/_enumerate.py`(新) | exhaustive + support-pruned 列挙 |
| `src/pycatdap/error/discovery.py`(新) | `discover_error_slices` |
| `src/pycatdap/error/cohorts.py`(新) | `compare_cohorts` + `detect_drift` + 結果コンテナ |
| `src/pycatdap/error/calibration.py`(拡張) | regression + multiclass OvR(binary 無修正) |
| `src/pycatdap/error/__init__.py` / `pycatdap/__init__.py` | 新公開シンボル re-export |
| `src/pycatdap/templates/` | `cohort_comparison.html.j2` |
| `src/pycatdap/error/{confusion,residual,calibration}.py` | `_get_backend_module` を `_backend` import に置換 |

### Compatibility

**破壊的変更なし**。すべて純粋な追加。

- 新公開関数 3 + 新コンテナ型 3。既存シンボル(`Slice` / `ErrorAnalysisResult` / calibration binary 群)は無変更。
- `measures` レジストリ・`error_label`・`optimal_binning`・`compute_delta_aic` は既存のまま再利用。
- scipy / sklearn 非依存(純 numpy)。lowest-direct-deps CI matrix 安全。Adult Income 系テストは `@pytest.mark.slow` + `pytest.importorskip("sklearn")`。
- backend 抽出(§F)は内部 refactor で公開挙動不変。

### Alternatives Considered

- **A1: 既存 `Slice` を多変数化して再利用** — 却下。`variable`/`category` スカラーを tuple 化するのは v0.9.0+ 公開型の破壊的変更。新規 `ErrorSlice` で非破壊。
- **A2: ΔAIC の保守的上界で枝刈り** — 却下。乗算ペナルティ項のため、健全な上界は緩すぎて何も刈れず、刈れる上界は不健全。support(Apriori)が唯一の健全 surrogate(§C)。
- **A3: 枝刈りを heuristic と明記して ΔAIC で刈る** — 却下。「真の top-k を取りこぼしうる」診断ツールは誤差分析の信頼性を損なう。正当性を担保できる support を採用。
- **A4: calibration follow-up を v0.12.0 に分離** — 却下(ユーザー判断)。v0.10.0 で「v0.11.0 へ」と明記済み、OvR は binary コア再利用で低リスク。

### Acceptance Criteria

- [ ] `discover_error_slices` が Adult Income(32k×14)で既知の disparate cohort(gender / race)を surface。
- [ ] slice description が逐語パース可能:`"age ∈ [45, 60] × marital_status = Never-married"`。
- [ ] **exhaustive vs pruned 等価テスト**:`set(pruned_topk) == set(exhaustive_topk ∩ {size≥min_support})`(RED フェーズ)。
- [ ] 20 変数データで `n_pruned / (n_evaluated + n_pruned) > 0.5`(>50% 削減)。
- [ ] measure plug-in:`measures.register` で custom 登録 → `measure=<name>` / `measure=<callable>` 双方が経路。
- [ ] perf:Adult Income で <30s(`@pytest.mark.slow`)。
- [ ] 入力非破壊:全公開呼出後に入力 `df` 不変(`assert_frame_equal`)、frozen 再代入で raise。
- [ ] `compare_cohorts` / `detect_drift`:合成 shift で ΔAIC delta / drift ranking が期待順。`.to_html` が jinja2 欠如パスで適切に振る舞う。
- [ ] calibration:既存 `test_error_calibration.py` 無変更通過(回帰ガード)+ 2クラス OvR == binary。regression quantile calibration の数値検証(no-scipy)。
- [ ] R 比較:合成分割表 ΔAIC を R CATDAP-02 多変数結果と 1e-4 照合。
- [ ] `make ci` 全 green、coverage 80%+。

### Decision

- Date: `2026-05-29`
- Result: `accepted`
- Notes: PR-L0(#123)merge 前に cross-check 実施。6 件の load-bearing claim すべて TRUE/PARTIALLY-TRUE(FALSE なし)。§C(support 枝刈りの健全性)・等価テスト定式化・perf 予算(max_vars=3 × 14 列 = 469 評価で tractable)・OvR の binary 非破壊(`calibration.py:126` の bool 分岐)をコードで検証済み。実装は PR-L1〜L8 で段階的に進行。

### Migration

なし(純粋な追加、破壊的変更なし)。`Slice`(単変数)と `ErrorSlice`(多変数)は併存。既存ユーザーコードは無修正で動作。

### Related References

- 親仕様: H-0001 Phase L、H-0002 FR-5/FR-7/FR-9、Issue #20 / #11
- 前段: H-0013 Phase K §G(回帰 / multi-class calibration の defer 元)
- subset search エンジン: `src/pycatdap/catdap2.py`、`compute_delta_aic`(`src/pycatdap/_aic.py`)
- ペナルティ項(§C の根拠): `src/pycatdap/_aic.py` `compute_aic_twoway`
- measure レジストリ(FR-9): `src/pycatdap/measures/_registry.py`
- error_label: `src/pycatdap/error/_labels.py`
- immutability discipline: `src/pycatdap/error/_result.py`(H-0009 / `ErrorAnalysisResult`)
- 有界 accuracy binning の教訓: H-0013 §B-bis、`src/pycatdap/_pooling.py` `optimal_binning`
- SliceLine: <https://dl.acm.org/doi/10.1145/3448016.3457323>
- DivExplorer: <https://github.com/elianap/divexplorer>

## 2026-05-29: v0.12.0 — LizyStudio 統合イネーブルメント + 誤差分析の積み残し解消 (Phase M)

- ID: `H-0015`
- Status: `accepted`
- Scope: `API | data-contract | types`
- Related: `H-0001 v0.12.0`, `H-0002 FR-*`, `BLUEPRINT.md §5.7 / §5.8`, Issue #21 / #16 / #11

### Context

誤差分析アーク (Phase G→H→I+J→K→L) は v0.11.0 (H-0014) で完結した。README ロードマップ上 v0.12.0 = **「LizyStudio integration」(#21)** だが、cross-check の結果、**#21 の重い作業は LizyStudio 側 (別リポジトリ) にあり**、pycatdap 本体側は契約ハードニングのみで足りることが判明した:

- 全ての結果オブジェクトの `.to_plotly_json()` 実装と `[plotly]` extra は **既に存在** (#21 の pycatdap 側チェックボックスは充足可能)。
- 残るギャップは「機械検証可能な契約テストの不在」と「BLUEPRINT が契約をキー単位で明文化していない」点のみ。

そこでユーザー判断により、アークが defer した **3 つの積み残し (T2)** を v0.12.0 に同梱し、LizyStudio が消費する Error Analysis タブを「穴なし」で完成させてから統合する。公開 API・data contract・types を追加するため **Change Gate 対象**。本 Proposal を先行し、merge 前に cross-check で設計トラップを検証する (H-0011〜H-0014 と同じ運用 — 4 期連続で実トラップを事前検出)。

**本 Proposal は起票前に cross-check 済** (§Decision に結果)。D1 の「実装スコープ」見積もりに誤りが見つかり、修正済み。

### Proposal

#### A. T1 — `.to_plotly_json()` 契約の明文化 + 契約テスト

LizyStudio (FastAPI + react-plotly.js) が依存できる **バージョン付き契約**を確立する。新 API は追加しない (契約の明文化 + テスト)。

- **BLUEPRINT §5.7/DP-4 に契約を明記** (data-contract 追記):
  - 2 つの戻り形状を区別する: **FLAT** `{data: list, layout: dict}` (Catdap1Result / Catdap2Result / EDAResult) と **SECTIONED** `{<section_name>: <spec>}` (ProfileResult / ErrorAnalysisResult / TargetAnalysisResult / QualityReport / suite)。
  - 各 SECTIONED 結果の **安定キー集合**: always-present キーと conditional キー (発火条件つき) を列挙。例: `ErrorAnalysisResult` = `{feature_ranking, top_summaries}` 常時 + `confusion` (classification のみ); `ProfileResult` = `{association_heatmap}` 常時 + `top_subsets` (response 指定時)。
  - nested figure spec (`top_summaries[*]` / `top_subsets`) も FLAT 準拠であること。
  - **JSON-safety**: NaN/inf を含まない (heatmap z の None 置換等、既存挙動を契約化)。
- **`tests/contract/test_plotly_json_contract.py`** (新規):
  - 全結果型を parametrize し `json.dumps()` 成功を assert (現状 `ErrorAnalysisResult` のみが round-trip テスト保持)。
  - FLAT/SECTIONED を分類し、上記キー契約を assert。
  - `pytest.importorskip("plotly")` 下で `plotly.graph_objects.Figure(spec)` に通し react-plotly.js 互換を実証。
- **LizyStudio 側 Issue を別リポジトリに起票** (#21 へクロスリンク): `pycatdap[plotly]` 依存追加・EDA/Error Analysis タブ配線・pooling 調整 anywidget スライダ・FastAPI エンドポイント。

#### B. T2-① — 回帰スライス探索 (`discover_error_slices` 回帰経路)

現状 `discovery.py:214-220` で `NotImplementedError`。**採用案 D1**: 残差を categorical ラベル化して既存の分類スコアリング+Apriori support 枝刈りを再利用する。

- 既存 `abs_residual_pool(y_true, y_pred, n_bins)` (`_labels.py:290`) で |residual| を AIC プーリングし categorical ラベル化。**最上位ビンを動的特定** (`abs_residual_pool` は `bin_0..bin_{n-1}` を返すため `f"bin_{n_codes-1}"`、固定文字列ではない)。
- **cross-check 修正**: 分類セマンティクスがハードコードされた **計 4 + 1 箇所**を回帰対応する (guard 1 箇所だけではない):
  - `discovery.py:214` guard → 残差ラベル分岐へ
  - `discovery.py:230` `error_label(...)` → `abs_residual_pool` へ分岐
  - `discovery.py:234` `_ERROR_CATEGORY="incorrect"` 固定 → 最上位残差ビンへ
  - `discovery.py:259-261` `base_error_rate` 意味の再定義 (高残差ビン比率)
  - `discovery.py:293` `label_kind="error_label"` 固定 → 回帰用 kind へ
  - (+1) `discovery.py:133` 連続列 `optimal_binning(values, response)` は残差 response で bin を切る (= **設計上正しい**、INV-R9 で固定)
- measures レジストリ (response-agnostic)・enumerate・support 枝刈りは **無修正で再利用**。
- 新パラメータ: `n_bins=4`(回帰のみ)。残差マグニチュード binning は `abs_residual_pool`
  (AIC pooling)に固定し、`residual_method` の分岐は導入しない(magnitude=「高残差」
  の意味に最も忠実で、measure 契約を分岐させない最小実装)。signed-residual / quantile
  変種は後続の focused follow-up。

#### C. T2-② — 回帰/多クラス calibration reliability plot

現状 plot は binary `calibration_curve` のみ (表は regression/multiclass とも存在)。**採用案 A**: 既存 `_backend` dispatch + 既存テーブルを再利用する薄い dispatcher 2 本を追加。

- `regression_calibration_curve(y_true, y_pred, *, n_quantiles=10, backend="matplotlib", **kwargs)`: `regression_calibration_table` を `pred_mean × actual_mean` + y=x で描画。**軸は [0,1] にクランプせず**データ範囲オートスケール。
- `multiclass_calibration_curve(y_true, y_proba, *, classes=None, strategy="aic", n_bins=10, backend="matplotlib", **kwargs)`: OvR テーブル (二値[0,1]スキーマ) をクラスごとにオーバーレイ。
- `plot/matplotlib.py` / `plot/plotly.py` に実装追加。`ErrorAnalysisResult` デリゲーションは任意 (後続可)。

#### D. T2-③ — 多クラス `confusion_label` (one-vs-rest)

現状 `_labels.py:152` で >2 クラス `NotImplementedError`、`analysis.py:167` で error_label へ silent fallback。**採用案 A**: 新関数を追加し、二値 `confusion_label` は無修正。

- `multiclass_confusion_label(y_true, y_pred, *, classes=None) -> Mapping[class_label, pd.Series]`: クラス k ごとに `(y_true==k, y_pred==k)` へ縮約し既存二値 `confusion_label(positive=True)` を呼ぶ → `MappingProxyType`。`multiclass_calibration_table` の OvR 先例を踏襲。
- `error_analysis` wrapper への配線は本 Proposal scope 内では任意 (multiclass の confusion 露出は後続 PR でも可)。

#### E. Housekeeping

- **Issue #32 再スコープ** (v0.12.0 外/T3): 核メソッド `to_divexplorer_format` は `ErrorAnalysisResult` (`_result.py:405`) / `SliceDiscoveryResult` (`_slice.py:151`) に **v0.8.0 で実装済**。残るは DivExplorer 実スキーマ (`pattern/support/t_value_FPR`) 整合 + docs のみ。#32 のチェックリストを更新。
- **BLUEPRINT.md:127** ツリーコメント `H〜L は今後` を `H〜L 実装済 v0.11.0` に修正 (同ツリー 130-139 行と矛盾、docs-only / Change Gate 不要)。

### Impact

| 対象 | 追加/変更 |
|---|---|
| `tests/contract/test_plotly_json_contract.py` (新) | 全結果型の to_plotly_json 契約テスト |
| `BLUEPRINT.md §5.7/DP-4` | to_plotly_json 契約 (2 形状 + 安定キー) 明文化 |
| `src/pycatdap/error/discovery.py` (拡張) | 回帰スライス探索 (4+1 箇所の回帰対応) |
| `src/pycatdap/error/calibration.py` (拡張) | regression / multiclass calibration_curve dispatcher |
| `src/pycatdap/plot/{matplotlib,plotly}.py` (拡張) | 2 calibration plot 実装 |
| `src/pycatdap/error/_labels.py` (拡張) | `multiclass_confusion_label` |
| `src/pycatdap/error/__init__.py` | 新公開シンボル re-export |
| `BLUEPRINT.md:127` | 陳腐化コメント修正 |
| Issue #32 / LizyStudio repo | 再スコープ / 新規起票 |

### Compatibility

**破壊的変更なし**。すべて追加。

- 回帰スライス探索は新パス: 分類パスは byte-不変 (golden 回帰テストで固定)。
- calibration: 二値 `calibration_curve` / `_calibration_table` は無修正。
- `multiclass_confusion_label` は新関数: 二値 `confusion_label` は無修正、2クラス OvR == binary。
- scipy/sklearn 非依存 (純 numpy)。`[plotly]` extra は既存。lowest-direct-deps CI 安全。

### Alternatives Considered

- **回帰スライス D2 (連続 Gaussian response, `_aic_regression`)** — 却下。measure 契約 (2D 分割表) を分岐させ `cramers_v`/`mutual_info` が使えず、`ErrorSlice` に新フィールド (r_squared) が必要で公開 API 改変が大。
- **回帰スライス D3 (|residual| 閾値マスク)** — 却下。閾値という新パラメータ/判断が必要、残差符号を無視、AIC-native でない。
- **「guard だけ置換」(当初案)** — **cross-check で却下**。分類セマンティクスが 4+1 箇所ハードコードされ、guard だけでは例外なく誤結果を返す。
- **calibration plot B (単一多態 `calibration_curve`)** — 却下。安定 v0.10.0 二値契約を上書き、auto-detect は falsy-trap。one function one job 違反。
- **OvR confusion B (`confusion_label` を long-form 多態化)** — 却下。固定 4-category dtype 契約と下流消費者 (`_build_confusion`/`_extract_slices`) を破壊。

### Invariants (invariants-first)

**T2-① 回帰スライス探索:**
- INV-R1 (枝刈り健全性, MUST): `{c.conditions | enumerate(prune=True, min_support=m)} == {c.conditions | enumerate(prune=False) if size≥m}`。枝刈りは `size` のみ、残差/ΔAIC では刈らない。
- INV-R2: 入力 `df`/`y_true`/`y_pred` 非破壊、response は copy の予約列へのみ注入、予約列衝突で ValueError。
- INV-R3: 高残差比率 > baseline のスライスのみ surface。
- INV-R5: `measure_value` は higher=better、built-in "aic" のみ符号反転。
- INV-R6: 残差 NaN 行は tabulation から一貫除外、support を膨らませない。
- INV-R7: 長さ契約 `len == len(df) == len(y_true) == len(y_pred)`、不一致で ValueError。
- INV-R8: `SliceDiscoveryResult.label_kind` が実使用 labeller を反映 (回帰で `"error_label"` 固定にしない)。
- **INV-R9 (cross-check 追加)**: 回帰経路実行後、`_ERROR_CATEGORY="incorrect"` 等の分類セマンティクス定数が**一切結果に残らない** (最上位残差ビンが error pivot)。連続列 binning は残差 response を使う。

**T2-② calibration plot:** 二値 `calibration_curve`/`_calibration_table` byte-不変; plot 点 == テーブル値 (可視化と指標が乖離しない); backend は `_backend` のみ経由 (第4経路なし); 多クラスは [0,1]×y=x、回帰はオートスケール; 退化入力 (定数予測/欠如クラス) で raise しない; 戻り値型 Axes|Figure。

**T2-③ OvR confusion:** 二値経路 byte-不変; 2クラス OvR == binary; per-class TP/FP/FN/TN 排他 + カウント保存 (Σ_k TP_k == n_correct); classes=None は sorted(unique(y_true)); 戻り値 MappingProxyType・入力非破壊。

### Acceptance Criteria

- [ ] `tests/contract/test_plotly_json_contract.py`: 全結果型で `json.dumps` 成功 + FLAT/SECTIONED キー契約 + `Figure(spec)` 互換 (importorskip)。
- [ ] BLUEPRINT §5.7/DP-4 に契約 (2 形状 + per-result 安定キー) 明記。
- [ ] LizyStudio 側 Issue 起票 + #21 クロスリンク。
- [ ] **回帰スライス exhaustive vs pruned 等価テスト** (INV-R1, RED フェーズ): `set(pruned) == set(exhaustive ∩ {size≥min_support})`。
- [ ] 回帰スライス: 合成高残差サブグループを surface、分類パス byte-不変 (golden 回帰)、入力非破壊、INV-R9 (分類定数残存ゼロ)。
- [ ] regression/multiclass calibration plot: matplotlib (Axes) + plotly (Figure) 両 backend、plot 点 == テーブル値、二値 plot 無変更。
- [ ] `multiclass_confusion_label`: 2クラス OvR == 二値 `confusion_label`、per-class カウント保存、二値経路無変更。
- [ ] #32 チェックリスト更新 + BLUEPRINT:127 修正。
- [ ] `make ci` 全 green、coverage 80%+。

### Decision

- Date: `2026-05-30`
- Result: `accepted`
- Notes: 起票前 cross-check 実施。claim 2/3/4/6/7/10 TRUE、claim 1/5/8/9 PARTIALLY-TRUE、**FALSE なし**。最重要 claim #5「guard だけ置換」は誤りと判明 → 実装スコープを 4+1 箇所に修正、INV-R9 追加。D1 採用判断 (measures response-agnostic + abs_residual_pool 既存 + 枝刈り label 非依存) は有効。
  実装は PR-M1〜M5 で段階的に進行(単一ブランチ `feat/h0015-phase-m`):
  - PR-M1: `to_plotly_json` 契約スイート + BLUEPRINT §5.7.1。契約テストが `DescribeResult` の
    NaN セル(JSON 非準拠)を検出 → 共有 `_jsonsafe.scalar_to_json` を抽出し修正(`profile.py` も再利用)。
  - PR-M2: 回帰スライス探索(D1、`n_bins` のみ追加)。INV-R1〜R9 のテストスイート。
  - PR-M3: `regression_calibration_curve` / `multiclass_calibration_curve`(両 backend)。
  - PR-M4: `multiclass_confusion_label`(OvR、二値コア再利用)。
  - PR-M5: BLUEPRINT §5.8 / CHANGELOG / 本 Decision、§5.8 deferred 更新、BLUEPRINT:127 陳腐化修正、
    Adult Income slow テストの categorical `fillna` fixture 修正(pre-existing、release CI 専用)、
    Issue #32 再スコープ + #21 統合準備コメント。
  - 全 PR で non-slow suite green(934 passed)、ruff/mypy strict clean。`error_analysis` wrapper の
    multiclass confusion 露出への配線、専用 Notebook は後続フェーズへ。

### Migration

なし (純粋な追加)。回帰スライス探索は新パス、分類パス併存。既存ユーザーコード無修正。

### Related References

- 親仕様: H-0001 v0.12.0、Issue #21 / #11
- cross-check で確認したハードコード箇所: `discovery.py:214,230,234,259-261,293,133`
- 残差ラベル: `_labels.py:188` (`residual_label`) / `_labels.py:290` (`abs_residual_pool`)
- OvR 先例: `calibration.py:577-695` (`multiclass_calibration_table`)
- backend dispatch: `error/_backend.py`
- to_plotly_json 契約 (現状実装): `catdap1.py:49`, `catdap2.py:59`, `profile.py:265`, `error/_result.py:289`, ほか

## 2026-05-30: discover_error_slices 候補数キャップ（メモリ/時間ガード）

- ID: `H-0016`
- Status: `proposed`
- Scope: `API | data-contract | types`
- Related: `H-0014 §C`(support 枝刈り設計), incident 2026-05-30 (WSL OOM), Issue #20 / #29

### Context

2026-05-30 に、孤児化した `discover_error_slices(max_vars=3)` が Adult Income (32k×14、高カーディナリティ) で ~64GB を確保し WSL を OOM クラッシュさせた。根本原因: **support 枝刈り (`min_support`) は各セルの「サイズ」を下限保証するが、frequent cell の「個数」を一切制限しない**。個別に頻出する値が多い場合 (例: category dtype で binning をすり抜けた中カーディナリティ数値列 `age`〜73 値・`hours`〜94 値など、各値が >min_support)、frequent 2-cell が大量に残り、`_generate_candidates` の O(N²) join と level-3 評価が時間・メモリともに爆発する。暫定対策として Adult テストは `max_vars=2`+列限定で有界化済 (PR-M5) だが、**ライブラリ本体に普遍的なガードが無い**。

### Proposal

#### A. 公開 API

```python
pycatdap.error.discover_error_slices(
    df, y_true, y_pred,
    *, max_vars=3, measure="aic", top_k=10, min_support=30, columns=None, n_bins=4,
    max_candidates: int = 200_000,   # 新規: 評価する候補セル数の上限
) -> SliceDiscoveryResult
```

`SliceDiscoveryResult` に **`truncated: bool = False`** フィールドを追加。上限到達で探索を打ち切った場合 `True`。

#### B. アルゴリズム (`_enumerate.py`)

- `enumerate_cells(..., max_candidates: int)` を追加。`_enumerate_apriori` で `n_evaluated` が `max_candidates` に達したら、それ以降の候補生成・評価を停止し `truncated=True` を返す。
- `_generate_candidates(prev_level, frequent_set, *, limit)` に上限を渡し、候補リストが `limit` に達した時点で O(N²) join を early-break (生成段階での爆発も抑止)。
- 返り値を `(cells, n_evaluated, n_pruned, truncated)` の 4-tuple に拡張 (内部 API)。
- **exhaustive パス (`prune=False`) は無制限** — 正当性オラクル (等価テスト) を壊さないため。

#### C. 非サイレント (rule: no silent caps)

`discover_error_slices` は `truncated=True` のとき `warnings.warn(...)` で打ち切りを明示通知し、`SliceDiscoveryResult.truncated` で機械可読に公開。`to_dict()` にも含める。

### Impact

| 対象 | 追加/変更 |
|---|---|
| `src/pycatdap/error/_enumerate.py` | `max_candidates` + `truncated`、`_generate_candidates` の `limit` early-break |
| `src/pycatdap/error/discovery.py` | `max_candidates` パラメータ、`truncated` 受領 + `warnings.warn` |
| `src/pycatdap/error/_slice.py` | `SliceDiscoveryResult.truncated: bool`、`to_dict` 反映 |
| `BLUEPRINT.md §5.8` / `CHANGELOG` | API 追記 |

### Compatibility

**破壊的変更なし**。`max_candidates` はデフォルト付き追加パラメータ、`truncated` はデフォルト `False` の追加フィールド。デフォルト `200_000` は通常の探索 (Adult `max_vars=2` 等) では到達しないため、既存挙動は不変。

### Alternatives Considered

- **A1: `_is_continuous` を category-dtype 数値列対応に修正** — Adult の特定トリガー (binning すり抜け) は解消するが、一般の組合せ爆発は防げない。候補キャップが普遍的ガード。**併用可 (別 follow-up)**。
- **A2: 上限超過で例外 raise** — 却下。診断ツールは「打ち切った部分結果 + 警告」を返す方が有用 (sound な subset)。
- **A3: ΔAIC で枝刈り** — 却下済 (H-0014 §C、健全な上界なし)。

### Invariants

- **INV-C1**: `max_candidates` 未到達時、結果は無制限時と完全一致 (キャップは閾値未満で no-op)。
- **INV-C2**: 打ち切り時も返る slice はすべて sound (実在の frequent cell、support 正確)。完全性のみ失われ、`truncated=True` で明示。
- **INV-C3**: exhaustive パスは無制限 → 既存の `pruned == exhaustive ∩ {size≥min_support}` 等価テストは小データで不変。
- **INV-C4**: 分類・回帰いずれの経路でもキャップは label 非依存に作用 (enumerate は response 非依存)。

### Acceptance Criteria

- [ ] 高カーディナリティ合成データ + 小さい `max_candidates` → `truncated=True` かつ `warnings.warn` 発火、`n_evaluated <= max_candidates`。
- [ ] 大きい `max_candidates` (デフォルト) → `truncated=False`、結果が無制限時と一致 (INV-C1)。
- [ ] 打ち切り結果の全 slice が `size >= min_support` (INV-C2)。
- [ ] 既存 `test_error_enumerate.py` 等価テスト・全 discovery テストが pass (回帰なし)。
- [ ] メモリ安全に検証 (小規模合成データ・`max_vars<=2`、Adult は走らせない)。
- [ ] ruff / mypy strict clean、non-slow suite green。

### Decision

- Date: `(pending)`
- Result: `proposed`
- Notes: incident 2026-05-30 (memory `incident_discover_slices_oom`) の恒久対策。実装は memory-safe TDD で行う (キャップ検証は小規模合成データのみ)。

### Migration

なし (純粋な追加、デフォルトで既存挙動不変)。

### Related References

- incident: memory `incident_discover_slices_oom`(OOM の機序・kern.log 証跡)
- 枝刈り設計: H-0014 §C、`src/pycatdap/error/_enumerate.py`
- 暫定対策: PR-M5 `fix(test): bound Adult Income slow test for memory safety`
- 性能ベンチ (関連): Issue #29

## 2026-06-06: D5 データセット fetcher 追加（Wine Quality / Bank Marketing / Mushroom）

- ID: `H-0017`
- Status: `proposed`
- Scope: `API`
- Related: `H-0001 §E D5`, `H-0011 D4`(既存 fetch_openml 流儀), Issue #25 / #11

### Context

スライス発見・全カテゴリカル CATDAP のデモ/検証データが不足している。H-0001 §E D5 と
Issue #25 は UCI 3 データセット (Wine Quality / Bank Marketing / Mushroom) の
download-on-demand ローダを要求する。既存の D4 fetcher (`fetch_adult_income` /
`fetch_compas` / `fetch_california_housing`, v0.8.0) は `sklearn.datasets.fetch_openml`
の薄いラッパとして実装済みで、本追加はこの流儀を踏襲する。バンドル CSV を増やさず
OpenML キャッシュを利用するため配布サイズは不変。

### Proposal

#### A. 公開 API

`src/pycatdap/datasets.py` に 3 関数を追加 (いずれも既存 `[data]` extra の sklearn を
再利用、新規依存なし):

```python
pycatdap.datasets.fetch_wine_quality() -> pd.DataFrame    # 6,497 × 13
pycatdap.datasets.fetch_bank_marketing() -> pd.DataFrame  # 45,211 × 17
pycatdap.datasets.fetch_mushroom() -> pd.DataFrame        # 8,124 × 23
```

- **fetch_wine_quality**: OpenML `wine-quality-red`(1,599) + `wine-quality-white`(4,898)
  を pin して取得し、`color ∈ {red, white}` 列を付与して結合 → 6,497 行。11 連続特徴 +
  `quality`(target) + `color`。
- **fetch_bank_marketing**: OpenML `name="bank-marketing"` を pin して取得。OpenML 版は
  列名が generic (`V1..V16`) のため、loader 内で UCI 公式名 (`age, job, marital,
  education, default, balance, housing, loan, contact, day, month, duration, campaign,
  pdays, previous, poutcome` + target `y`) に rename する (受入基準「解釈可能な列名」を
  満たす)。初回取得時に実列数を検証し、既に名付き版なら rename は安全に no-op 化。
- **fetch_mushroom**: OpenML `name="mushroom"` を pin して取得。8,124 × 23、全列
  カテゴリカル、target `class ∈ {e, p}`。全カテゴリカル CATDAP デモに使用。

いずれも sklearn 未導入時は既存 fetcher と同一の `ImportError("pycatdap[data]")` を送出。

#### B. テスト

`tests/test_datasets_d5.py` を新規追加。D4 と同一方針:

- sklearn 不在時の ImportError fallback (mock で sklearn を None 化、network 不要、
  全環境で実行)。
- network smoke (`@pytest.mark.slow` + `pytest.importorskip("sklearn")`): 形状・列名・
  target 列の存在を検証。default CI (`-m "not slow"`) からは除外される。

### Impact

| 対象 | 追加/変更 |
|---|---|
| `src/pycatdap/datasets.py` | `fetch_wine_quality` / `fetch_bank_marketing` / `fetch_mushroom` 追加 |
| `tests/test_datasets_d5.py` | 新規 (ImportError fallback + slow smoke) |
| `docs/reference/datasets.md` | mkdocstrings 自動反映 (手動編集不要) |
| `CHANGELOG.md` | `[Unreleased]` に追記 |

### Compatibility

**完全に additive**。既存 API・data contract・型・バンドル CSV に変更なし。新規 optional
依存なし (sklearn は既存 `[data]` extra)。OpenML キャッシュ利用のため wheel/sdist サイズ
不変。

### Alternatives Considered

- **A1: CSV をバンドル同梱** — 配布サイズが肥大 (bank 45k 行) し、既存の「fetch_* は
  download-on-demand」方針と不統一。却下。
- **A2: UCI から直接 urllib で DL** — zip パース自前実装が重く、D4 の `fetch_openml`
  流儀と不統一。却下。
- **A3: OpenML wrapper (採用)** — 既存 D4 と一貫、pin で再現性確保。
- **bank 列名 (採用 = rename map)**: 名付き OpenML version を探す案も検討したが、live
  検証不可かつ version 依存で不安定。UCI 公式名への rename を一次手段とし、初回取得で
  名付き判明時は no-op。
- **wine 形状 (採用 = red+white 結合 + color 列)**: white 単体案より Issue #25 の
  「red+white 6,497 行」仕様に一致。

### Acceptance Criteria

- [ ] sklearn 不在で 3 ローダすべて `ImportError`(`pycatdap[data]` を指す)。
- [ ] `fetch_wine_quality` が 6,497 行、`quality`・`color` 列を含む。
- [ ] `fetch_bank_marketing` が 45,211 行、解釈可能な列名 (generic でない)、target `y`。
- [ ] `fetch_mushroom` が 8,124 行、全列カテゴリカル、target `class`。
- [ ] テストが slow+importorskip でガードされ default CI を汚さない。
- [ ] ruff / mypy strict clean、non-slow suite green。

### Decision

- Date: `(pending)`
- Result: `proposed`
- Notes: 純粋な API 追加。network smoke は個別実行で検証 (`make test-all` は D4 同様
  ハングするため使わない — memory `feedback_make_ci_d4_network_hang`)。

### Migration

なし (純粋な追加)。

### Related References

- 親仕様: H-0001 §E D5、Issue #25 / #11
- 既存流儀: H-0011 D4 (`fetch_adult_income` 等)、`src/pycatdap/datasets.py`
- network smoke の運用注意: memory `feedback_make_ci_d4_network_hang`

## 2026-06-06: pysubgroup interop — AICMeasure（AIC を interestingness measure として公開）

- ID: `H-0018`
- Status: `proposed`
- Scope: `API | optional-dependency`
- Related: `H-0002 DP-6 / FR-9`, `H-0008 PR-D4`(measures registry), `H-0014 §C`(ΔAIC に健全上界なし), Issue #31 / #20 / #11

### Context

H-0002 の設計原則 DP-6 は「pysubgroup 互換の pluggable interestingness measure」を要求する。
measures registry (`measures/_registry.py`, H-0008) は既に存在するが、それは
`Callable[[2D table], float]` の table 単位インターフェースであり、pysubgroup の
subgroup 単位 QualityFunction (`AbstractInterestingnessMeasure`) とは抽象度が異なる。
#31 は両者を橋渡しする互換レイヤ (`AICMeasure`) を求める。

調査 (実物 pysubgroup 0.9.0):

- binary target の QF 基底は `SimplePositivesQF` で、dataset 統計 `(N, P)`
  (全件数・全 positive 数) と subgroup 統計 `(n, p)` を提供する。
- `BeamSearch` / `SimpleDFS` は `evaluate(subgroup, target, data, statistics)` のみ
  使用し、`optimistic_estimate` を要求しない (Apriori / DFS は要求する)。

### Proposal

#### A. 公開 API

```python
pycatdap.measures.AICMeasure()  # pysubgroup 互換の QualityFunction
```

pysubgroup 0.9.0 の `SimplePositivesQF` を継承し `evaluate` のみ実装する:

- dataset 統計 `(N, P)` と subgroup 統計 `(n, p)` から 2×2 分割表を構築:

  ```
              target=pos   target=neg
  in-subgroup     p          n - p
  out-subgroup  P - p   (N - n) - (P - p)
  ```

- `pycatdap.measures.aic(table)` で ΔAIC を計算し、**quality = −ΔAIC** を返す
  (pysubgroup は quality を最大化する。ΔAIC は負 = informative なので符号反転で
  「高い = より informative」に揃える)。
- `n == 0` のとき `float("nan")` を返す (pysubgroup の `StandardQF` と同じ規約)。
- 退化分割表 (0 周辺度数) は `_aic.py` の `0·ln0=0` 規約で扱えるが numpy の
  eager division が `RuntimeWarning` を出すため、`evaluate` 内で
  `np.errstate(divide="ignore", invalid="ignore")` により局所抑制する。

`optimistic_estimate` は **意図的に実装しない** (`BoundedInterestingnessMeasure` を
継承しない)。ΔAIC には健全な上界が存在しない (H-0014 §C で確立) ため、提供すると
Apriori / DFS の枝刈りが不健全になる。`AICMeasure` は `BeamSearch` / `SimpleDFS`
専用とし、その旨を docstring と docs に明記する。

#### B. optional dependency

pysubgroup は **pycatdap の extra に含めない**。明示インストール (`pip install
pysubgroup`) とする。

- 理由 (実測): pysubgroup 0.9.0 は `numpy<2.0.0` を pin する。これを `[subgroup]`
  extra や `dev` group に入れると、**uv の universal lock がその cap を lock 全体に
  伝播**させ、`uv sync --frozen --dev`(CI Quality matrix) を含む全 install が
  numpy 1.26.4 に降格する。古い numpy スタブが Python 3.10 の `mypy --strict` で
  既存ファイル群に 13 件の型エラーを表面化させ CI が壊れる (PR #154 で実際に発生)。
  さらに pysubgroup は `scikit-learn` も要求し、dev 経由で sklearn が CI matrix と
  release-PR の slow テスト経路に混入する (D4 fetcher hang リスク再燃、
  `feedback_extra_all_pulls_sklearn_into_quality_ci` の轍)。
- `[tool.uv] conflicts` + `dev` への `numpy>=2` floor で resolution を fork すれば
  CI を numpy 2.x に保てることは確認したが、(a) cross-test は結局 dev fork に
  pysubgroup が無く CI で skip され「CI 検証」の利得が無い、(b) lock の numpy 3 分岐
  ・local-dev で dev↔subgroup 排他という機構コストが見合わない。よって最小・確実な
  「extra に含めない」を採用する。
- pysubgroup 未導入時、`pycatdap.measures.AICMeasure` は
  `ImportError("... pip install pysubgroup")` を送出する。`pycatdap.measures` 本体の
  import は pysubgroup を必須にしない (PEP 562 `__getattr__` で lazy 解決)。
- cross-test は `pytest.importorskip("pysubgroup")` でガードし、CI (pysubgroup 非導入)
  では skip、ローカル (`pip install pysubgroup`) で検証する (D5 slow と同じ割り切り)。

#### C. mypy

pysubgroup は型スタブを提供しないため:

- `[[tool.mypy.overrides]]` に `pysubgroup.*` を `ignore_missing_imports = true` で追加。
- bridge module `pycatdap.measures._pysubgroup` のみ `disallow_subclassing_any = false`
  (untyped 基底 `SimplePositivesQF` の継承を許可。strict は他所では維持)。

### Impact

| 対象 | 追加/変更 |
|---|---|
| `src/pycatdap/measures/_pysubgroup.py` | 新規 `AICMeasure` |
| `src/pycatdap/measures/__init__.py` | PEP 562 `__getattr__` で `AICMeasure` lazy export |
| `pyproject.toml` | mypy override のみ (`pysubgroup.*` ignore-missing + bridge module の subclassing 許可)。pysubgroup は extra/group に**含めない** |
| `tests/test_measures_pysubgroup.py` | 新規 (ImportError fallback + bridge 数理 + BeamSearch cross-test) |
| `docs/interop/pysubgroup.md` + `mkdocs.yml` | 新規 interop ガイド |
| `CHANGELOG.md` | `[Unreleased]` 追記 |

### Compatibility

**完全に additive**。既存 measures registry・`aic` 関数・API・型に変更なし。pysubgroup は
optional で、未導入環境の挙動は不変。`pycatdap.measures` の import は pysubgroup 非依存。

### Alternatives Considered

- **A1: `BoundedInterestingnessMeasure` を継承し optimistic_estimate も提供** — Apriori /
  DFS も使えるが、ΔAIC に健全上界がない (H-0014 §C) ため枝刈りが不健全。却下。
- **A2: registry の table 単位 measure をそのまま pysubgroup に渡す** — 抽象度
  (table vs subgroup) が合わず不可。bridge クラスが必要。
- **A3: quality = ΔAIC をそのまま返す** — pysubgroup は最大化するため informative
  (負 ΔAIC) が最下位になり順序が逆。符号反転 (−ΔAIC) が正しい。

### Acceptance Criteria

- [ ] `pysubgroup.BeamSearch().execute(task, qf=pycatdap.measures.AICMeasure())` が動作する。
- [ ] AICMeasure の出力が native `discover_error_slices` と数学的に整合 (同データで
      informative 変数が上位に来ることを cross-test で検証)。
- [ ] pysubgroup 未導入時 `pycatdap.measures.AICMeasure` が `ImportError`(`pip install pysubgroup`)。
- [ ] `pycatdap.measures` の import は pysubgroup なしで成功する。
- [ ] `docs/interop/pysubgroup.md` に side-by-side 例。
- [ ] ruff / mypy strict clean、non-slow suite green、CI 全 Python (3.10–3.13) green。

### Decision

- Date: `(pending)`
- Result: `proposed`
- Notes: DP-6 の具体化。BeamSearch 専用スコープ (Apriori 非対応) は H-0014 §C の帰結。
  **依存方針の修正 (PR #154 CI 失敗を受けて)**: 当初案は `[subgroup]` extra + `dev`
  group だったが、pysubgroup の `numpy<2.0.0` pin が uv universal lock 経由で numpy を
  全面降格させ Python 3.10 の strict mypy を壊した (§B 参照)。pysubgroup を extra/group
  から外し明示インストールに変更。cross-test は CI skip・ローカル検証。

### Migration

なし (純粋な追加)。

### Related References

- 設計原則: H-0002 DP-6 / FR-9、`BLUEPRINT.md §5.11`
- measures registry: H-0008 PR-D4、`src/pycatdap/measures/_registry.py`
- ΔAIC 非有界: H-0014 §C
- pysubgroup 0.9.0 `SimplePositivesQF`: `binary_target.py`
