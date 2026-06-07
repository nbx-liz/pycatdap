# pycatdap 全体開発計画 (PLAN)

> このファイルは pycatdap の全体開発計画を時系列・テーマ別に整理する。
> 個別の仕様変更は [HISTORY.md](HISTORY.md)、機能設計は [BLUEPRINT.md](BLUEPRINT.md) を参照。
> 実績は [CHANGELOG.md](CHANGELOG.md) を参照。

最終更新: 2026-05-31

---

## 1. ビジョン

pycatdap は CATDAP (Sakamoto & Katsura, 1980) の Python 実装を起点に、
**AIC ベースの EDA + ML 誤差分析ライブラリ** へと進化する。

差別化軸:

- **AIC ベースの変数関連度ランキング**(Cramér's V や mutual info とは異なる「情報量と複雑さのトレードオフ」)
- **連続変数の AIC 最適 binning**(他ツールは等幅/分位等分のみ)
- **サブセット最適探索 (CATDAP-02)**(feature importance とは異なる「変数組合せの探索」、Error Analysis Tree の AIC 版)
- **モデル非依存**(`y_true`, `y_pred` で動くため sklearn / LightGBM / XGBoost / PyTorch 等任意のモデルに対応)

参照: [H-0001](HISTORY.md) — 戦略的再定位、[H-0002](HISTORY.md) — 詳細要件・競合分析、[H-0003](HISTORY.md) — データセット拡張

---

## 2. リリース計画

### マイルストーン一覧(実績 — 2026-05-31 監査で実コードと突合済み)

EDA + ML 誤差分析アーク(Phase A→M)は **全て出荷済み**。最新リリースは
**v0.12.1**(2026-05-31 tag)。下表は実際の git tag / CHANGELOG と一致する。

| Version | テーマ | 主要 Issue | 状態 |
|---|---|---|---|
| v0.2.0 | CATDAP-01/02 コア実装 | - | ✅ released 2026-03-22 |
| v0.3.0 | Plotly backend + 単変量 EDA API (Phase A) | [#12](https://github.com/nbx-liz/pycatdap/issues/12), [#22](https://github.com/nbx-liz/pycatdap/issues/22) | ✅ released 2026-05-26 |
| v0.4.0 | 二変量 EDA API (heatmap, association — Phase B) | [#13](https://github.com/nbx-liz/pycatdap/issues/13) | ✅ released 2026-05-27 |
| v0.5.0 | `profile()` + HTML レポート (Phase C) | [#14](https://github.com/nbx-liz/pycatdap/issues/14) | ✅ released 2026-05-28 |
| v0.6.0 | `target_analysis()` + `quality_report()` + `suite/` + `measures/` (Phase D) | [#15](https://github.com/nbx-liz/pycatdap/issues/15) | ✅ released 2026-05-28 |
| v0.6.1 | API hardening: dataclass shallow-freeze 修正 (H-0009) | (H-0009) | ✅ released 2026-05-28 |
| v0.7.0 | Error labeling utilities + D3 datasets (Phase G) | [#16](https://github.com/nbx-liz/pycatdap/issues/16), [#23](https://github.com/nbx-liz/pycatdap/issues/23) | ✅ released 2026-05-28 |
| v0.8.0 | `error_analysis()` one-call + D4 datasets (Phase H) | [#17](https://github.com/nbx-liz/pycatdap/issues/17), [#24](https://github.com/nbx-liz/pycatdap/issues/24) | ✅ released 2026-05-29 |
| v0.9.0 | 分類・回帰の誤差可視化 (Phase I+J) | [#18](https://github.com/nbx-liz/pycatdap/issues/18) | ✅ released 2026-05-29 |
| v0.10.0 | キャリブレーション (AIC binning — Phase K) | [#19](https://github.com/nbx-liz/pycatdap/issues/19) | ✅ released 2026-05-29 |
| v0.11.0 | Slice discovery + cohort + drift + 回帰/多クラス calibration (Phase L) | [#20](https://github.com/nbx-liz/pycatdap/issues/20) | ✅ released 2026-05-29 |
| v0.12.0 | LizyStudio 統合イネーブルメント + 誤差分析積み残し (Phase M / H-0015) | [#21](https://github.com/nbx-liz/pycatdap/issues/21)(本体側) | ✅ released 2026-05-30 |
| v0.12.1 | `discover_error_slices` 候補数キャップ + numeric-category binning 修正 (H-0016) | [#20](https://github.com/nbx-liz/pycatdap/issues/20), [#29](https://github.com/nbx-liz/pycatdap/issues/29)(関連) | ✅ released 2026-05-31 |

### マイルストーン一覧(今後の計画 — 2026-05-31 監査で再策定)

監査の結論: 残 open issue の半数は「コードは既に出荷済みで PLAN が陳腐化していた
だけ」か「downstream(別リポジトリ)待ち」。ゼロ着手が必要なのは #25 / #29 /
#31 の具体物 / #47 の 4 件。これを **3 トラック**に整理する。

| Version | テーマ | 主要 Issue | Change Gate | 状態 |
|---|---|---|---|---|
| v0.12.2 | Housekeeping: 品質ゲート整備 + DivExplorer interop docs + PLAN/issue 整合 | [#34](https://github.com/nbx-liz/pycatdap/issues/34)✅, [#32](https://github.com/nbx-liz/pycatdap/issues/32)(docs)✅, 本 PLAN | 不要 | 🟢 in progress(develop, 未リリース): #34=PR #145, #32 docs=PR #146 マージ済、PLAN/issue 整合=本 PR |
| v0.13.0 | Datasets D5 + interop(pysubgroup AICMeasure / DivExplorer 真スキーマ) | [#25](https://github.com/nbx-liz/pycatdap/issues/25)✅, [#31](https://github.com/nbx-liz/pycatdap/issues/31)✅, [#32](https://github.com/nbx-liz/pycatdap/issues/32)✅ | 済(H-0017/18/19) | 🟢 develop(未リリース)。[#47](https://github.com/nbx-liz/pycatdap/issues/47) JNcharacter は won't-do(GPL、H-0020) |
| v0.14.0 | R cross-validation 実照合の有効化 + 性能ベンチ | [#10](https://github.com/nbx-liz/pycatdap/issues/10), [#30](https://github.com/nbx-liz/pycatdap/issues/30), [#29](https://github.com/nbx-liz/pycatdap/issues/29) | 一部(#29 dep+CI) | 🟡 planned(R環境依存) |
| v1.0.0 | API 整理(`plotting.*` → `plot.matplotlib.*` deprecation) | [#33](https://github.com/nbx-liz/pycatdap/issues/33) | 要(公開 API) | 🟡 planned |

注(改訂):
- v0.11.0 / v0.12.0 は 2026-05-28 レビューで分割予定だったが、最終的に **Phase L は
  v0.11.0 で一括出荷**(slice discovery + cohort + drift + calibration follow-up)、
  **v0.12.0 = Phase M (H-0015)** として LizyStudio 統合イネーブルメント(`.to_plotly_json()`
  契約テスト)+ 誤差分析積み残し(回帰スライス探索・回帰/多クラス calibration plot・
  多クラス confusion)に再定義された。
- D3 datasets (#23) は v0.7.0(Phase G の demo)、D4 (#24) は v0.8.0(Phase H)に
  同梱済み。**D5 (#25) は v0.13.0 で同梱済 (H-0017、develop 未リリース)。JNcharacter
  (#47) は GPL ライセンスのため won't-do (H-0020)** — catdap データは ISM 著作・GPL(>=2)
  で MIT package に再配布できない。既存同梱の HealthData/HelloGoodbye の GPL 整合は
  **#156 で解決済 (H-0025、develop 未リリース)**: HelloGoodbye は削除 (tutorial 04 を合成
  データ化)、HealthData は非配布の test fixture (`tests/fixtures/`、wheel/sdist 除外、NOTICE)
  に移し R bit-exact 照合を維持、デモは UCI heart_disease に差替。GPL 化は LizyStudio
  (GPL 非互換) を破壊するため不可、ISM 許諾も取得不可のため同梱解除を選択。
- **#21 の重い作業は LizyStudio 側(別リポジトリ #579)**。pycatdap 本体側の
  `.to_plotly_json()` 契約は v0.12.0 で出荷済み(全結果型実装 + 契約テスト)。
- **#32 の核メソッド `to_divexplorer_format` は v0.8.0 で実装済み**。残るは真の
  DivExplorer スキーマ整合 + docs + cross-test のみ(#32 本文 checklist は要更新)。
- **#10 の strict R 照合テストコードは出荷済み**(`tests/test_against_r.py`、atol=1e-4)。
  ただし参照 CSV が未コミットのため CI では `pytest.skip` され**実照合はゼロ**。
  R + catdap 1.3.5 環境での CSV 生成が唯一のブロッカー(維持者のオフライン作業)。
- v1.0 の R cross-validation は core AIC 計算のみを対象(Phase A-M surface は
  behavior + golden tests で代替、scope carve-out)。

凡例: ✅ released / 🟢 in progress / 🟡 planned / ⏸️ blocked / ❌ cancelled

---

## 3. テーマ別 Issue マップ

### 3.1 EDA 機能(H-0001 Phase A〜D — 全 phase 出荷済)

| Phase | Issue | バージョン | 主要 API | 状態 |
|---|---|---|---|---|
| A | [#12](https://github.com/nbx-liz/pycatdap/issues/12) | v0.3.0 | Plotly backend, `describe`, `plot_variable`, `plot_missing` | ✅ |
| B | [#13](https://github.com/nbx-liz/pycatdap/issues/13) | v0.4.0 | `plot_pair`, `aic_heatmap`, `association_matrix`, `association_plot` | ✅ |
| C | [#14](https://github.com/nbx-liz/pycatdap/issues/14) | v0.5.0 | `profile()`, HTML レポート | ✅ |
| D | [#15](https://github.com/nbx-liz/pycatdap/issues/15) | v0.6.0 | `target_analysis()`, `quality_report()`, `suite/`, `measures/` | ✅ |

### 3.2 ML 誤差分析機能(H-0001 Phase G〜M, H-0002 — 全 phase 出荷済)

| Phase | Issue | バージョン | 主要 API | 状態 |
|---|---|---|---|---|
| G | [#16](https://github.com/nbx-liz/pycatdap/issues/16) | v0.7.0 | `error.error_label`, `confusion_label`, `residual_label`, `abs_residual_pool` | ✅ |
| H | [#17](https://github.com/nbx-liz/pycatdap/issues/17) | v0.8.0 | `error_analysis()` one-call wrapper | ✅ |
| I+J | [#18](https://github.com/nbx-liz/pycatdap/issues/18) | v0.9.0 | `plot_confusion`, `residual_plot`, `residual_by_category` | ✅ |
| K | [#19](https://github.com/nbx-liz/pycatdap/issues/19) | v0.10.0 | `calibration_curve(n_bins="aic")`, Brier, ECE | ✅ |
| L | [#20](https://github.com/nbx-liz/pycatdap/issues/20) | v0.11.0 | `discover_error_slices`, `compare_cohorts`, `detect_drift` + 回帰/多クラス calibration | ✅ |
| M | [#21](https://github.com/nbx-liz/pycatdap/issues/21)(本体側), H-0015 | v0.12.0 | `.to_plotly_json()` 契約テスト + 回帰スライス探索 + 回帰/多クラス calibration plot + `multiclass_confusion_label` | ✅ |
| — | H-0016 | v0.12.1 | `discover_error_slices(max_candidates=)` + `SliceDiscoveryResult.truncated`(OOM ガード) | ✅ |

> 補足: pysubgroup interop (#31) / DivExplorer 真スキーマ整合 (#32) は Phase L/M とは
> 切り離し、interop トラック(v0.13.0)で扱う。詳細は §3.6 を参照。

### 3.3 データセット拡張(H-0003)

ポリシー(2026-05-28 レビュー): データセット issue は **独立リリースとして扱わず、それを使う Phase のリリースに同梱** する。Phase G/H/L には demo データセットが必要なので自然に対応する。

| 段階 | Issue | バージョン | データセット | 状態 |
|---|---|---|---|---|
| D1 | [#10](https://github.com/nbx-liz/pycatdap/issues/10), [#30](https://github.com/nbx-liz/pycatdap/issues/30) | v0.14.0 | R reference CSV + slow CI 昇格(scope carve-out: core AIC のみ) | 🟡 (テストコード・R生成script・Makefile・CONTRIBUTING 出荷済、**参照 CSV 同梱待ち**) |
| D2 | [#22](https://github.com/nbx-liz/pycatdap/issues/22) | v0.3.0 | Titanic, iris | ✅ released |
| D3 | [#23](https://github.com/nbx-liz/pycatdap/issues/23) | v0.7.0(Phase G に折込) | German Credit, Heart Disease, Penguins | ✅ released |
| D4 | [#24](https://github.com/nbx-liz/pycatdap/issues/24) | v0.8.0(Phase H に折込) | Adult Income, COMPAS, California Housing | ✅ released |
| D5 | [#25](https://github.com/nbx-liz/pycatdap/issues/25) | v0.13.0 | Wine Quality, Bank Marketing, Mushroom | ✅ develop(H-0017, 未リリース) |
| 追加 | [#47](https://github.com/nbx-liz/pycatdap/issues/47) | — | JNcharacter (CATDAP-01 復元) | ❌ won't-do(GPL ライセンス、H-0020) |

### 3.4 ドキュメント(全 issue CLOSED)

| Issue | テーマ | 状態 |
|---|---|---|
| [#26](https://github.com/nbx-liz/pycatdap/issues/26) | mkdocs-material + GitHub Pages 構築、API リファレンス自動生成 | ✅ closed |
| [#27](https://github.com/nbx-liz/pycatdap/issues/27) | Phase ごとの tutorial notebook(7本) | ✅ closed |
| [#28](https://github.com/nbx-liz/pycatdap/issues/28) | README リフレッシュ(ポジショニング、比較表、quickstart) | ✅ closed |

### 3.5 品質・インフラ

| Issue | テーマ | 監査時の実態(2026-05-31) |
|---|---|---|
| [#29](https://github.com/nbx-liz/pycatdap/issues/29) | パフォーマンスベンチマーク (pytest-benchmark) | 🟡 未着手(L)。H-0016 OOM の再発防止になるため価値↑。Adult Income ケースは `max_candidates` で要 cap |
| [#30](https://github.com/nbx-liz/pycatdap/issues/30) | CI ワークフロー更新(slow tests を release CI に昇格) | 🟢 ほぼ完了(S)。CI 配線・Makefile・CONTRIBUTING 済。残=#10 と同じ参照 CSV 同梱 |
| [#34](https://github.com/nbx-liz/pycatdap/issues/34) | mypy strict + ruff の品質ゲート整備 | ✅ DONE(PR #145, 2026-06-02 closed)。IPython `display` の no-untyped-call は `follow_imports="skip"` で環境差を解消(typed shim 不要)、ruff pydocstyle(`D`)導入 + docstring 17 件修正、pre-commit に mypy フック追加、`make ci` の D4 ネットワークハングを `-m "not slow"` で解消(フル実行は `make test-all`) |

### 3.6 互換性・相互運用

| Issue | テーマ | 監査時の実態(2026-05-31) |
|---|---|---|
| [#31](https://github.com/nbx-liz/pycatdap/issues/31) | pysubgroup 互換 (AIC measure 登録) | 🟡 基盤のみ(M)。measures registry 出荷済だが `AICMeasure` クラス・optional dep・cross-test・docs 未着手。外部 dep → Change Gate |
| [#32](https://github.com/nbx-liz/pycatdap/issues/32) | DivExplorer 出力フォーマットアダプタ | 🟢 コア出荷済 v0.8.0 + interop docs 出荷済(PR #146 `docs/interop/divexplorer.md`: 両世代スキーマをソース照合 + AIC↔divergence 対応 + 検証済み adapter)。残=`to_divexplorer_format()` 自体の真スキーマ列互換(データ契約 → Change Gate)+ cross-test(optional `divexplorer` dep)→ v0.13.0 |

### 3.7 LizyStudio 統合

| Issue | テーマ | 監査時の実態(2026-05-31) |
|---|---|---|
| [#21](https://github.com/nbx-liz/pycatdap/issues/21) | LizyStudio に EDA / Error Analysis タブを追加(Plotly JSON 連携) | 🟢 pycatdap 本体側完了 v0.12.0(全結果型 `.to_plotly_json()` + 契約テスト)。**重作業は downstream LizyStudio#579**。本体側は close 可能 |

### 3.8 v1.0 準備

| Issue | テーマ | 監査時の実態(2026-05-31) |
|---|---|---|
| [#33](https://github.com/nbx-liz/pycatdap/issues/33) | API 整理(`plotting.*` → `plot.matplotlib.*`、deprecation) | 🟡 構造は完了(M)。`plot/` パッケージ出荷済・内部移行済・`plotting.py` は既に再エクスポート shim。残=once-per-session `DeprecationWarning` 化 + docs/notebook 4 ファイル移行 + Proposal。v1.0 ゲート |

### 3.9 メタ

| Issue | テーマ |
|---|---|
| [#11](https://github.com/nbx-liz/pycatdap/issues/11) | 全体ロードマップのメタ Issue |

---

## 4. 開発フロー

### 4.1 標準フロー(各 Phase 共通)

1. **Proposal 確認**(必要に応じて HISTORY に追加)
2. **BLUEPRINT 改訂**(該当節を更新)
3. **TDD (RED → GREEN → REFACTOR)**:
   - テスト先行(`tests/test_<module>.py`)
   - 実装最小化
   - リファクタリング、80%+ coverage 維持
4. **code-reviewer agent でレビュー**
5. **PR を develop へ作成**(squash merge)
6. **slow tests を手動実行**(release 前の最終確認)
7. **release.py スクリプトでバージョンタグ → PyPI**

### 4.2 並列開発の指針(2026-05-31 改訂 — 前提 Phase は全て完了済み)

Phase A→M が出荷済みのため、旧来の Phase 間直列依存は解消。現在の制約は主に
**Change Gate・外部資源・downstream** に移っている。

| 並列可能 | 直列必須 / 外部依存 |
|---|---|
| #34 mypy shim と #32 docs(v0.12.2 内) | #25 / #31 / #32 は完了(H-0017/18/19、develop)。#47 は won't-do(H-0020) |
| (#25 D5 datasets 完了) | #10 / #30 の strict 照合有効化は **R + catdap 1.3.5 環境**(維持者作業)が前提 |
| #29 perf benchmark(独立、ただし dep+CI Gate) | #21 の E2E 受け入れ基準は **LizyStudio#579**(別リポジトリ)が前提 |
| PLAN/docs 整合(本作業、Gate 不要) | #33 rename は v1.0 リリース判断が前提 |

### 4.3 主要な決定ゲート

#### 解決済み(過去 Phase で確定)

| ゲート | 確定した事項 | 結果 |
|---|---|---|
| v0.3 | Plotly Figure JSON schema、`backend` 命名規約 | ✅ FLAT/SECTIONED 契約(BLUEPRINT §5.7.1) |
| v0.5 | HTML レポート jinja2 構造、`ProfileResult` フィールド | ✅ 確定 |
| v0.6 | `Suite` / `SuiteResult` スキーマ | ✅ 確定 |
| v0.7 | Multiclass `confusion_label` 仕様 | ✅ v0.12.0 で `multiclass_confusion_label`(one-vs-rest)として確定 |
| v0.8 | `Slice.description` 文字列フォーマット | ✅ 確定 |
| v0.10 | AIC binning vs equal-width の優位性検証 | ✅ `strategy="aic"` を既定に確定 |
| v0.11 | slice discovery の枝刈り方式 | ✅ **support(Apriori)に確定**、ΔAIC 枝刈りは健全な上界なしで却下(H-0014 §C) |
| v0.12 | `.to_plotly_json()` 契約(LizyStudio 連携) | ✅ FLAT/SECTIONED + 契約テストで確定(H-0015) |

#### 未確定(今後のトラックで確定が必要)

| ゲート | 確定すべき事項 | 関連 |
|---|---|---|
| v0.13 開始時 | D5 loader の取得元(UCI 直 DL vs OpenML pin)+ cache 方針 | #25 |
| v0.13 開始時 | pysubgroup measure API のシグネチャ + optional dep 配置(`[subgroup]` extra) | #31 |
| v0.13 開始時 | DivExplorer 真スキーマ整合の採否(option a 据置 vs b 破壊的) | #32 |
| ✅ 解決(2026-06-07) | JNcharacter: catdap は ISM 著作・GPL(>=2)(公式確認)→ MIT package に同梱しない won't-do | #47 → H-0020 |
| ✅ 解決(2026-06-07) | 既存同梱 catdap データの GPL 整合: HelloGoodbye 削除 + HealthData を非配布 test fixture 化(wheel/sdist 除外・NOTICE)、デモは heart_disease に差替。GPL 化は LizyStudio 非互換のため不可 | #156 → H-0025 |
| v0.14 開始時 | R 参照 CSV の生成・コミット(R + catdap 1.3.5)/ perf ベンチの runner・dep 選定 | #10, #30, #29 |
| v1.0 開始時 | Deprecation 期間(v1.0 → v2.0?)+ `load_hellogoodbye` rename の同梱可否 | #33 |

---

## 5. クロスカッティング関心事

### 5.1 コーディング規約

- Python 3.10+ (`from __future__ import annotations` 必須)
- 整形・lint: `ruff` (line-length 88)
- 型: `mypy --strict`、`npt.NDArray[T]` を bare `ndarray` の代わりに使用
- 公開関数には NumPy-style docstring 必須
- 不変データパターン(input DataFrame / numpy 配列を mutate しない)
- ゼロ頻度: `0 * ln(0) = 0` convention(`_safe_xlogy` 使用)

### 5.2 テスト戦略

| レイヤ | 内容 | カバレッジ目標 |
|---|---|---|
| Unit | `_aic.py`, `_pooling.py` 等の数学的検証(手計算と照合) | 95%+ |
| Integration | `catdap1`, `catdap2`, `error_analysis` 等のエンドツーエンド | 90%+ |
| R cross-validation | `tests/test_against_r.py`(atol=1e-4) | release CI で必須 |
| Performance | `benchmarks/`(pytest-benchmark) | 規制基準: 回帰 -20% で fail |
| Notebook | `pytest --nbmake` で tutorial が壊れていないか検証 | 全 notebook が CI で通過 |

### 5.3 CI/CD 戦略

- **Develop CI**(全 PR): fast unit + integration tests、ruff、mypy
- **Release CI**(tag push): + slow tests(R cross-validation)、+ benchmark、+ docs build
- **Documentation deploy**: main への push で GitHub Pages に自動デプロイ
- **PyPI release**: tag を契機に release.yml が TestPyPI → PyPI に publish

### 5.4 ドキュメント戦略(Diátaxis フレームワーク)

| 種別 | 対象 | 場所 |
|---|---|---|
| Tutorial | ステップバイステップ学習 | `docs/tutorial/*.ipynb` |
| How-to | 特定タスクの解決法 | `docs/how-to/*.md` |
| Reference | API 仕様 | `docs/reference/*`(mkdocstrings で自動生成) |
| Explanation | 設計思想・数理的基礎 | `docs/explanation/*.md`(BLUEPRINT.md から移行) |

### 5.5 互換性ポリシー

- v0.x: 新規 API は追加のみ。既存 API は維持
- v1.0: `plotting.*` を `plot.matplotlib.*` に正式 rename、旧名は `DeprecationWarning` 付きで v2.0 まで維持
- v2.0 以降: 旧名削除可能

### 5.6 依存管理ポリシー

- **必須依存**: `numpy`, `pandas`
- **任意依存(Extras)**:
  - `[plot]`: `matplotlib`, `statsmodels`
  - `[plotly]`: `plotly`, `jinja2`
  - `[widget]`: `anywidget`
  - `[data]`: `requests`, `scikit-learn`(fetch 用)
  - `[all]`: 上記全部
- `scipy` は任意。`scipy.special.xlogy` があれば使い、なければ自前実装にフォールバック

---

## 6. リスク管理

### 6.1 リスクレジスタ

| リスク | 影響 | 確率 | 緩和策 |
|---|---|---|---|
| Plotly 依存が重く採用率低下 | Mid | Mid | extras 分離。matplotlib をデフォルトに維持 |
| R catdap reference 生成が困難(R 環境不要構築) | High | Mid | R reference を CSV として同梱、再生成は維持者のみ |
| AIC monotonic 仮定が成り立たないケースが存在 | High | Low | プルーニング後の確率的サンプリング検証を導入 |
| DivExplorer / pysubgroup の API 変更で互換性破綻 | Mid | Mid | バージョン pin、互換性レイヤを optional に |
| LizyStudio 側の React Plotly 統合で予期せぬスキーマ要求 | Mid | Mid | LizyStudio 側に早期 Issue を立て同期開発 |
| ML 誤差分析の検証データ(COMPAS 等)が controversial | Low | Mid | bundled せず fetch、明示的同意 UI |
| パフォーマンスが期待値に届かず Adult Income が <30s で完了しない | High | Mid | プロファイリング先行、必要なら numba を `[fast]` extras に追加 |

### 6.2 ブロッカー予測

| Phase | 想定ブロッカー |
|---|---|
| Phase L | pysubgroup の measure API が pycatdap の計算契約と合わない可能性 |
| LizyStudio 統合 | LizyStudio 側の React 側で Plotly JSON のレンダリングに ad-hoc な前処理が必要になる可能性 |
| v1.0 | `plotting.*` の deprecation が既存外部ユーザに影響する可能性 |

---

## 7. 関連ドキュメント

- [BLUEPRINT.md](BLUEPRINT.md) — 仕様・数理的基礎・モジュール構成
- [HISTORY.md](HISTORY.md) — Proposal / Decision / Migration の履歴
- [CHANGELOG.md](CHANGELOG.md) — 実際のリリース内容
- [CLAUDE.md](CLAUDE.md) — 開発ルール
- [CONTRIBUTING.md](CONTRIBUTING.md) — 貢献ガイド
- GitHub Issues: <https://github.com/nbx-liz/pycatdap/issues>
- Meta Issue: [#11](https://github.com/nbx-liz/pycatdap/issues/11)

---

## 8. 更新方針

本 PLAN.md は次のタイミングで更新する:

- 新規 Issue 起票時(該当テーマに追加)
- リリース完了時(マイルストーン状態を `released` に更新)
- 大きな方針転換時(Proposal が HISTORY に追加されるタイミング)
- 月次レビュー(進捗確認、リスクレジスタの再評価)

実装が PLAN から逸脱した場合は、まず PLAN を更新するか、HISTORY に Proposal を追加して整合を取る(`doc-hierarchy.md` ルール)。

### 監査記録

- **2026-05-31**: 全 open issue(#10/#21/#25/#29/#30/#31/#32/#33/#34/#47)を
  出荷済みコードと突合し、各判定を独立エージェントで敵対的検証(全件 confirmed)。
  本 PLAN は最終更新 2026-05-26 時点で v0.6.1/v0.7.0 を "in progress" と誤記し、
  実態(v0.12.1 出荷済み・Phase A→M 完了・#12〜#28 closed)から 6 バージョン分
  乖離していたため §2〜§4 を全面改訂。実装が正・仕様(PLAN)が陳腐化していた
  ケースに該当するため `doc-hierarchy.md` に従い PLAN を実態へ更新(Change Gate
  不要、docs-only)。主要な発見:
  - #10/#30 は strict R 照合のテストコードは出荷済みだが参照 CSV 未コミットで
    CI は `pytest.skip` → **実照合ゼロ(緑だが無検証)**。R 環境での CSV 生成が
    唯一のブロッカー。
  - #21 本体側 / #32 コアメソッドは既に出荷済み。残作業は downstream / スキーマ
    整合 + docs のみ。
  - ゼロ着手が必要な真の未着手は #25 / #29 / #31 具体物 / #47 の 4 件。
- **2026-06-02**: v0.12.2 housekeeping トラックを実施(develop、未リリース)。
  - **#34 CLOSED**(PR #145): 品質ゲート整備。mypy を `IPython.*` の
    `follow_imports="skip"` で環境非依存化(typed shim 不要)、ruff pydocstyle(`D`)
    導入 + docstring 17 件修正、pre-commit に mypy フック追加、`make test`/`make ci`
    を `-m "not slow"` に変更し D4 ネットワークテストのローカルハングを解消
    (フル実行は新設 `make test-all`)。
  - **#32 scope A**(PR #146, issue は OPEN 継続): DivExplorer interop ガイド
    `docs/interop/divexplorer.md` を追加。両世代(0.1.x/0.2.x)の出力スキーマを
    upstream ソースと照合し、AIC↔divergence 対応と検証済み adapter を記載。真スキーマ
    列互換 + cross-test は v0.13.0(Change Gate)に残す。
  - **PLAN/issue 整合**(本更新): §2 マイルストーン・§3.5(#34)・§3.6(#32)を上記
    成果に合わせて更新。公開 Roadmap ページ `docs/project/roadmap.md` が v0.3.0〜
    v0.12.0 を依然「planned」と誤記していた(PLAN は #143 で修正済みだが公開ページ
    未修正)ため実態へ更新。issue 側の状態コメント(#10/#21/#30 の audit コメント、
    #32 進捗、#34 close)は既に反映済み。
