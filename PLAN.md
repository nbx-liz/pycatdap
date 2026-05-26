# pycatdap 全体開発計画 (PLAN)

> このファイルは pycatdap の全体開発計画を時系列・テーマ別に整理する。
> 個別の仕様変更は [HISTORY.md](HISTORY.md)、機能設計は [BLUEPRINT.md](BLUEPRINT.md) を参照。
> 実績は [CHANGELOG.md](CHANGELOG.md) を参照。

最終更新: 2026-05-26

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

### マイルストーン一覧

| Version | テーマ | 主要 Issue | 状態 |
|---|---|---|---|
| v0.2.0 | CATDAP-01/02 コア実装(リリース済) | - | ✅ released |
| v0.2.x | R 数値クロスバリデーション | [#10](https://github.com/nbx-liz/pycatdap/issues/10), [#30](https://github.com/nbx-liz/pycatdap/issues/30) | 🟡 planned |
| v0.3.0 | Plotly backend + 単変量 EDA API | [#12](https://github.com/nbx-liz/pycatdap/issues/12), [#22](https://github.com/nbx-liz/pycatdap/issues/22) | 🟡 planned |
| v0.4.0 | 二変量 EDA API (heatmap, association) | [#13](https://github.com/nbx-liz/pycatdap/issues/13) | 🟡 planned |
| v0.5.0 | `profile()` + HTML レポート | [#14](https://github.com/nbx-liz/pycatdap/issues/14), [#23](https://github.com/nbx-liz/pycatdap/issues/23) | 🟡 planned |
| v0.6.0 | `target_analysis()` + Suite API | [#15](https://github.com/nbx-liz/pycatdap/issues/15) | 🟡 planned |
| v0.7.0 | Error labeling utilities | [#16](https://github.com/nbx-liz/pycatdap/issues/16) | 🟡 planned |
| v0.8.0 | `error_analysis()` one-call | [#17](https://github.com/nbx-liz/pycatdap/issues/17), [#24](https://github.com/nbx-liz/pycatdap/issues/24) | 🟡 planned |
| v0.9.0 | 分類・回帰の誤差可視化 | [#18](https://github.com/nbx-liz/pycatdap/issues/18) | 🟡 planned |
| v0.10.0 | キャリブレーション (AIC binning) | [#19](https://github.com/nbx-liz/pycatdap/issues/19) | 🟡 planned |
| v0.11.0 | スライス発見・コホート比較・ドリフト | [#20](https://github.com/nbx-liz/pycatdap/issues/20), [#25](https://github.com/nbx-liz/pycatdap/issues/25), [#31](https://github.com/nbx-liz/pycatdap/issues/31), [#32](https://github.com/nbx-liz/pycatdap/issues/32) | 🟡 planned |
| v0.12.0 | LizyStudio 統合の安定化 | [#21](https://github.com/nbx-liz/pycatdap/issues/21) | 🟡 planned |
| v1.0.0 | API 整理 (`plotting.*` → `plot.matplotlib.*`) | [#33](https://github.com/nbx-liz/pycatdap/issues/33) | 🟡 planned |

凡例: ✅ released / 🟢 in progress / 🟡 planned / ⏸️ blocked / ❌ cancelled

---

## 3. テーマ別 Issue マップ

### 3.1 EDA 機能(H-0001 Phase A〜D)

| Phase | Issue | バージョン | 主要 API |
|---|---|---|---|
| A | [#12](https://github.com/nbx-liz/pycatdap/issues/12) | v0.3.0 | Plotly backend, `describe`, `plot_variable`, `plot_missing` |
| B | [#13](https://github.com/nbx-liz/pycatdap/issues/13) | v0.4.0 | `plot_pair`, `aic_heatmap`, `association_matrix`, `association_plot` |
| C | [#14](https://github.com/nbx-liz/pycatdap/issues/14) | v0.5.0 | `profile()`, HTML レポート |
| D | [#15](https://github.com/nbx-liz/pycatdap/issues/15) | v0.6.0 | `target_analysis()`, `quality_report()`, `suite/` |

### 3.2 ML 誤差分析機能(H-0001 Phase G〜L, H-0002)

| Phase | Issue | バージョン | 主要 API |
|---|---|---|---|
| G | [#16](https://github.com/nbx-liz/pycatdap/issues/16) | v0.7.0 | `error.error_label`, `confusion_label`, `residual_label` |
| H | [#17](https://github.com/nbx-liz/pycatdap/issues/17) | v0.8.0 | `error_analysis()` one-call wrapper |
| I+J | [#18](https://github.com/nbx-liz/pycatdap/issues/18) | v0.9.0 | `plot_confusion`, `residual_plot`, `residual_by_category` |
| K | [#19](https://github.com/nbx-liz/pycatdap/issues/19) | v0.10.0 | `calibration_curve(n_bins="aic")`, Brier, ECE |
| L | [#20](https://github.com/nbx-liz/pycatdap/issues/20) | v0.11.0 | `discover_error_slices`, `compare_cohorts`, `detect_drift` |

### 3.3 データセット拡張(H-0003)

| 段階 | Issue | バージョン | データセット |
|---|---|---|---|
| D1 | [#10](https://github.com/nbx-liz/pycatdap/issues/10) | v0.2.x | R reference CSV + 既存データ厳密一致テスト |
| D2 | [#22](https://github.com/nbx-liz/pycatdap/issues/22) | v0.3.0 | Titanic, iris, JNcharacter |
| D3 | [#23](https://github.com/nbx-liz/pycatdap/issues/23) | v0.5.0 | German Credit, Heart Disease, Penguins |
| D4 | [#24](https://github.com/nbx-liz/pycatdap/issues/24) | v0.8.0 | Adult Income, COMPAS, California Housing |
| D5 | [#25](https://github.com/nbx-liz/pycatdap/issues/25) | v0.11.0 | Wine Quality, Bank Marketing, Mushroom |

### 3.4 ドキュメント

| Issue | テーマ |
|---|---|
| [#26](https://github.com/nbx-liz/pycatdap/issues/26) | mkdocs-material + GitHub Pages 構築、API リファレンス自動生成 |
| [#27](https://github.com/nbx-liz/pycatdap/issues/27) | Phase ごとの tutorial notebook(7本) |
| [#28](https://github.com/nbx-liz/pycatdap/issues/28) | README リフレッシュ(ポジショニング、比較表、quickstart) |

### 3.5 品質・インフラ

| Issue | テーマ |
|---|---|
| [#29](https://github.com/nbx-liz/pycatdap/issues/29) | パフォーマンスベンチマーク (pytest-benchmark) |
| [#30](https://github.com/nbx-liz/pycatdap/issues/30) | CI ワークフロー更新(slow tests を release CI に昇格) |
| [#34](https://github.com/nbx-liz/pycatdap/issues/34) | mypy strict + ruff の品質ゲート整備 |

### 3.6 互換性・相互運用

| Issue | テーマ |
|---|---|
| [#31](https://github.com/nbx-liz/pycatdap/issues/31) | pysubgroup 互換 (AIC measure 登録) |
| [#32](https://github.com/nbx-liz/pycatdap/issues/32) | DivExplorer 出力フォーマットアダプタ |

### 3.7 LizyStudio 統合

| Issue | テーマ |
|---|---|
| [#21](https://github.com/nbx-liz/pycatdap/issues/21) | LizyStudio に EDA / Error Analysis タブを追加(Plotly JSON 連携) |

### 3.8 v1.0 準備

| Issue | テーマ |
|---|---|
| [#33](https://github.com/nbx-liz/pycatdap/issues/33) | API 整理(`plotting.*` → `plot.matplotlib.*`、deprecation) |

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

### 4.2 並列開発の指針

| 並列可能 | 直列必須 |
|---|---|
| Phase A (#12) と D2 (#22) | Phase H (#17) は Phase G (#16) 完了が前提 |
| ドキュメント整備(#26, #27, #28) | Phase L (#20) は Phase G/H/I/J 完了が前提 |
| 互換性レイヤ(#31, #32) | LizyStudio 統合(#21) は Phase C/H/L 完了が前提 |
| パフォーマンスベンチ(#29) | v1.0 (#33) は全 Phase 完了が前提 |

### 4.3 主要な決定ゲート

各 Phase 開始時に下記の決定を確定する:

| ゲート | 確定すべき事項 |
|---|---|
| v0.3 開始時 | Plotly Figure JSON schema、`backend` パラメータの命名規約 |
| v0.5 開始時 | HTML レポートの jinja2 テンプレート構造、`ProfileResult` のフィールド確定 |
| v0.6 開始時 | `Suite` / `SuiteResult` のスキーマ(deepchecks 互換性検討) |
| v0.7 開始時 | Multiclass の `confusion_label` 仕様(`one-vs-rest`? 全 confusion 行列?) |
| v0.8 開始時 | `Slice.description` の文字列フォーマット標準化 |
| v0.10 開始時 | AIC binning vs Equal-width binning のキャリブレーションでの優位性の数値検証 |
| v0.11 開始時 | pysubgroup measure API のシグネチャ最終確定 |
| v0.12 開始時 | LizyStudio の API スキーマ(FastAPI 側との契約) |
| v1.0 開始時 | Deprecation 期間(v1.0 → v2.0?) |

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
