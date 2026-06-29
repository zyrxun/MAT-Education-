# MAT Education — Michigan Traders

A hands-on, notebook-based curriculum that takes members from the Python scientific stack to **researching, building, and backtesting systematic trading strategies on [QuantConnect](https://www.quantconnect.com/)**.

> **Michigan Traders** is a student-led organization focused on algorithmic trading, quantitative market research, and competitive trading strategy development — combining mathematics, statistics, computer science, finance, machine learning, and high-performance computing. This curriculum is the on-ramp.

---

## How the notebooks work

Every notebook is an **interactive workbook**, not a lecture. Each topic follows the same loop:

1. **Worked example** — a short concept + one runnable example (output already shown).
2. **✏️ Your turn** — a `# TODO` cell you fill in yourself.
3. **Self-check** — a cell you run that prints **`✅ Correct!`** or tells you exactly what's off.

Every module ships as a **pair of files**:

| File | What it is |
|---|---|
| `NN_Title.ipynb` | **Exercise version** — blanks to fill in. Start here. |
| `NN_Title_SOLUTIONS.ipynb` | **Answer key** — every exercise filled in, all self-checks passing. Check yourself *after* trying. |

> Working through it yourself? Duplicate the exercise notebook and edit your copy — name it with `copy` in the title or drop it in a `my-work/` folder and it stays off GitHub automatically.

---

## Curriculum

| # | Module | Runs in | Status |
|---|--------|---------|--------|
| 01 | **NumPy for Quants** | Local Jupyter | ✅ Available |
| 02 | **Pandas for Financial Data** | Local Jupyter | ✅ Available |
| 03 | The 5 Pillars of a QuantConnect Algorithm | QuantConnect (LEAN) | 🔜 Planned |
| 04 | The Research Environment & Working with Financial Data | QuantConnect Research | 🔜 Planned |
| 05 | Indicators, Signals & Strategy Design Patterns | QuantConnect (LEAN) | 🔜 Planned |
| 06 | Backtesting Mechanics & Performance Analytics | QuantConnect (LEAN) | 🔜 Planned |
| 07 | Statistical Signal Research (mean reversion & pairs) | QuantConnect Research + LEAN | 🔜 Planned |
| 08 | Machine Learning for Alpha | QuantConnect Research + LEAN | 🔜 Planned |
| 09 | Algorithm Framework, Risk Management & Competition Readiness | QuantConnect (LEAN) | 🔜 Planned |

**Modules 01–02 (Foundations)** are pure Python — they run in any Jupyter kernel on your laptop. **Modules 03+** move to QuantConnect: the algorithm code runs inside the **LEAN engine** (the QuantConnect IDE or the LEAN CLI), and the research cells run in QuantConnect's **Research Environment** (`QuantBook`).

---

## Quick start

### Foundations (notebooks 01–02) — run locally

```bash
pip install numpy pandas matplotlib jupyter
jupyter notebook        # then open 01_NumPy_for_Quants.ipynb
```

That's it — no account, no keys. Run the cells top to bottom and do the exercises.

### QuantConnect modules (03+)

1. Create a free account at [quantconnect.com](https://www.quantconnect.com/).
2. In a notebook's code cell that defines a `class ...(QCAlgorithm)`, copy it into a new project's `main.py` and click **Backtest**.
3. Research-environment cells (`qb = QuantBook()`) run inside QuantConnect's own notebook.

> A QuantConnect algorithm will **not** run in a plain local kernel — the trading API only exists inside LEAN. Each notebook makes clear which cells go where.

---

## Conventions used throughout

- **QuantConnect Python API is `snake_case`** (`self.set_start_date(...)`, `def on_data(self, data):`, `self.set_holdings(...)`), matching QuantConnect's current PEP8 API. The old `PascalCase` still works but isn't used here.
- **US equities / ETFs only** (SPY, AAPL, TLT, …) — cleanest for learning. No crypto/futures/options.
- **Reproducible randomness** — every notebook seeds its RNG so your numbers match the comments.

---

## Repo layout

```
MAT Education/
├── 01_NumPy_for_Quants.ipynb              # exercise
├── 01_NumPy_for_Quants_SOLUTIONS.ipynb    # answer key
├── 02_Pandas_for_Financial_Data.ipynb
├── 02_Pandas_for_Financial_Data_SOLUTIONS.ipynb
└── README.md
```

---

*Questions or improvements? Bring them to the research channel.*
