# Architecture

This page presents pycatdap's architecture from five viewpoints, then drills into the file structure and design principles.

## A. Module dependency graph

Which module imports which? Yellow dashed boxes are planned for v0.3+; solid black are released in v0.2.

```mermaid
graph TD
    subgraph "Public API (v0.2 — released)"
        catdap1[catdap1.py]
        catdap2[catdap2.py]
        plotting[plotting.py]
        datasets[datasets.py]
    end

    subgraph "Public API (v0.3+ — planned)"
        profile[profile.py]
        error_pkg[error/]
        suite_pkg[suite/]
        measures_pkg[measures/]
        plot_pkg[plot/]
    end

    subgraph "Private core"
        aic[_aic.py]
        cont[_contingency.py]
        pool[_pooling.py]
        subset[_subset_search.py]
    end

    subgraph "Optional dependencies (extras)"
        scipy[scipy.special.xlogy]
        mpl[matplotlib]
        sm[statsmodels]
        plotly[plotly]
        jinja2[jinja2]
        anywidget[anywidget]
    end

    catdap1 --> aic
    catdap1 --> cont
    catdap2 --> aic
    catdap2 --> cont
    catdap2 --> pool
    catdap2 --> subset
    pool --> aic
    subset --> aic
    subset --> cont
    aic -.optional.-> scipy
    plotting -.-> mpl
    plotting -.-> sm

    profile --> catdap1
    profile --> catdap2
    profile --> plot_pkg
    profile --> datasets
    error_pkg --> catdap1
    error_pkg --> catdap2
    error_pkg --> measures_pkg
    suite_pkg --> aic
    suite_pkg --> cont
    measures_pkg --> aic
    plot_pkg -.-> mpl
    plot_pkg -.-> plotly
    plot_pkg -.-> jinja2
    profile -.-> jinja2

    classDef planned fill:#fff3cd,stroke:#856404,stroke-dasharray: 5 5
    class profile,error_pkg,suite_pkg,measures_pkg,plot_pkg planned
```

## B. EDA data flow — what `profile()` does

```mermaid
flowchart LR
    DF[pd.DataFrame] --> P["pycatdap.profile<br/>(df, response)"]
    P --> D[describe<br/>univariate stats]
    P --> Q[quality_report<br/>missing/cardinality]
    P --> C1[catdap1<br/>m×m ΔAIC]
    P --> C2[catdap2<br/>top-K subsets]
    P --> H[aic_heatmap]
    P --> A[association_matrix]

    D --> R[ProfileResult]
    Q --> R
    C1 --> R
    C2 --> R
    H --> R
    A --> R

    R --> HTML[".to_html(path)<br/>standalone HTML"]
    R --> Show[".show()<br/>Jupyter inline"]
    R --> JSON[".to_plotly_json()<br/>LizyStudio"]
    R --> Dict[".to_dict()<br/>serialization"]
```

A `DataFrame` enters, `ProfileResult` is composed from multiple analyses, and outputs branch out for different consumers.

## C. ML error analysis data flow — what `error_analysis()` does

```mermaid
flowchart LR
    Input["(df, y_true, y_pred)"] --> EA["pycatdap.error_analysis<br/>task=auto"]
    EA --> Detect[_detect_task]
    EA --> EL{Error labeling}
    EL --> EE[error_label<br/>correct/incorrect]
    EL --> CE[confusion_label<br/>TP/FP/FN/TN]
    EL --> RE[residual_label<br/>AIC pooling]

    EE --> Rank[catdap1<br/>variable ranking]
    CE --> Rank
    RE --> Rank
    Rank --> Discover[discover_error_slices<br/>CATDAP-02 search]

    Discover --> Result[ErrorAnalysisResult]
    Rank --> Result
    Result --> Slices[".top_slices<br/>(with .description)"]
    Result --> Conf[".confusion / .residual_pooling"]
    Result --> Out1[".to_html()"]
    Result --> Out2[".to_plotly_json()"]
    Result --> Out3[".to_divexplorer_format()"]
```

Predictions are detected as classification or regression, converted to categorical error labels, then fed to CATDAP-01/02 as targets.

## D. Layers and extension points

```mermaid
graph TB
    subgraph "Layer 1: Public API"
        L1["catdap1 / catdap2 / profile / error_analysis<br/>plot.* / suite.* / measures.* / datasets.*"]
    end

    subgraph "Layer 2: Private core"
        L2["_aic / _contingency / _pooling / _subset_search"]
    end

    subgraph "Layer 3: Required dependencies"
        L3["numpy / pandas"]
    end

    subgraph "Layer 4: Optional dependencies (extras)"
        L4a["[plot]: matplotlib / statsmodels"]
        L4b["[plotly]: plotly / jinja2"]
        L4c["[widget]: anywidget"]
        L4d["[data]: requests / scikit-learn"]
    end

    subgraph "Extension points (pluggable)"
        E1["Measures<br/>register('name', fn)<br/>aic / cramers_v / MI / custom"]
        E2["Plot backends<br/>matplotlib / plotly / custom"]
        E3["Suite checks<br/>independence / cardinality / pooling / custom"]
    end

    L1 --> L2
    L2 --> L3
    L1 -.optional.-> L4a
    L1 -.optional.-> L4b
    L1 -.optional.-> L4c
    L1 -.optional.-> L4d
    L1 -. plugin .-> E1
    L1 -. plugin .-> E2
    L1 -. plugin .-> E3
```

Four layers of responsibility. Three extension points for third parties and users.

## E. Integration boundaries — connections to external systems

```mermaid
graph LR
    subgraph pycatdap_core[pycatdap]
        Core["Core analysis<br/>catdap1 / catdap2<br/>error_analysis / profile"]
    end

    subgraph Verification["Verification"]
        R["R catdap 1.3.5"] -->|generates| CSV["docs/r_reference/*.csv"]
        CSV --> Tests["tests/test_against_r.py<br/>atol=1e-4"]
        Tests -.checks.-> Core
    end

    subgraph Consumption["Consumption"]
        Core -->|".to_plotly_json"| Lizy["LizyStudio<br/>FastAPI + react-plotly.js"]
        Core -->|".show / .to_html"| Notebook["Jupyter / browser"]
    end

    subgraph Interop["Interop"]
        Core -->|".to_divexplorer_format"| DE["DivExplorer pipelines"]
        Core -->|"measures.AICMeasure"| PS["pysubgroup.BeamSearch"]
    end

    subgraph DataSources["Data sources"]
        UCI["UCI ML Repo"] -->|fetch_*| Core
        OpenML["OpenML"] -->|fetch_*| Core
        SK["sklearn datasets"] -->|fetch_*| Core
        Bundled["Bundled CSVs<br/>Titanic / Heart Disease / etc"] -->|load_*| Core
    end
```

pycatdap connects in four directions: (1) verified against R catdap, (2) consumed by LizyStudio / Notebooks, (3) interoperates with DivExplorer / pysubgroup, (4) sources data from UCI / OpenML / sklearn / bundled.

---

## Package structure (textual)

```
pycatdap/
├── __init__.py             # Public API
├── catdap1.py              # CATDAP-01 implementation
├── catdap2.py              # CATDAP-02 implementation
├── _aic.py                 # Core AIC computation
├── _pooling.py             # Continuous variable pooling
├── _subset_search.py       # Best subset search
├── _contingency.py         # Contingency table builder
├── datasets.py             # Sample datasets
├── plotting.py             # v0.2 plotting API (matplotlib)
├── plot/                   # v0.3+ dual-backend plotting (planned)
├── profile.py              # One-call EDA report (planned)
├── error/                  # ML error analysis (planned)
├── suite/                  # CI-integrable test suites (planned)
└── measures/               # Pluggable interestingness measures (planned)
```

## Design principles

From [HISTORY.md H-0002 §G](https://github.com/nbx-liz/pycatdap/blob/main/HISTORY.md):

1. **One-call experience prioritized** — `profile()`, `error_analysis()`
2. **Result objects are explorable** — `.show()`, `.to_html()`, `.to_dict()`, `.to_plotly_json()`
3. **Natural-language slice descriptions mandatory** — `"age ∈ [45, 60] × cholesterol = high"`
4. **Plotly Figure output enabled** — for LizyStudio and other web frontends
5. **Classification + regression both supported by default**
6. **Pluggable measure design** — pysubgroup-compatible
7. **AIC treated as monotonic for pruning** — SliceLine-inspired

## Module boundaries

- `_aic.py`, `_contingency.py`, `_pooling.py`, `_subset_search.py` are **private** numerical primitives — not part of the public API
- `catdap1.py`, `catdap2.py` are **public** classical CATDAP entry points (v0.2)
- `profile.py`, `error/`, `suite/`, `measures/` form the **modern** v0.3+ API surface

## Data classes

All result types follow the same contract:

```python
@dataclass
class SomeResult:
    # Domain-specific fields...

    def show(self) -> None: ...               # Jupyter inline
    def to_html(self, path: str) -> None: ... # Standalone HTML
    def to_plotly_json(self) -> dict: ...     # For web frontends
    def to_dict(self) -> dict: ...            # For serialization
```

This uniformity simplifies LizyStudio integration and downstream consumption.

## Backward compatibility

- v0.2 imports (`pycatdap.plotting.mosaic_plot`, etc.) remain stable through v1.0
- v0.3+ adds new modules; existing modules are not modified
- v1.0 introduces `plot.matplotlib.*` as the canonical path; old paths emit `DeprecationWarning`
- v2.0 may remove deprecated paths

## See also

- [Roadmap](../project/roadmap.md)
- [Tutorials](../tutorials/index.md)
- Canonical specification: [BLUEPRINT.md §3.2](https://github.com/nbx-liz/pycatdap/blob/main/BLUEPRINT.md#32-アーキテクチャ図視覚版) (Japanese)
