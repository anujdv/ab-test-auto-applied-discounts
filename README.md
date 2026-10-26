# Auto-applied discount vs manual coupon at checkout

> **Status: synthetic practice plan frozen; no real experiment has run and no findings are reported.** All data produced by `seed_experiment.py` is synthetic and exists only to demonstrate a reproducible workflow.

Experiment IDs for this practice simulation are 301 (Control variant 3011; Treatment variant 3012). The synthetic data and templates use these numeric IDs.\n\nOption 3 compares automatically applying an eligible discount at checkout with requiring customers to enter a coupon code. The project is designed as an end-to-end experimentation case study: pre-registration, assignment, data-quality checks, intent-to-treat analysis, and a decision memo.

## Executive summary (to complete after a real or clearly labeled simulated run)

| Item | Status |
|---|---|
| Verdict | **Pending** — Ship / Stage / Hold not yet selected |
| Primary metric | Checkout conversion per randomized eligible customer |
| Treatment | Eligible discount applied automatically |
| Control | Same offer available through manual coupon entry |
| Data | Synthetic generator available; no real customer data included |
| Scorecard | Pending experiment execution and validated analysis |

## Business hypothesis

**If** eligible customers receive the same discount automatically instead of having to enter a coupon, **then** checkout conversion will increase, **because** removing coupon-entry friction makes redemption easier. The experiment must also confirm that contribution margin per eligible customer and operational guardrails remain acceptable.

## Repository map

- `PRE_REGISTRATION.md` — planned contract and assumptions to lock before data collection.
- `DESIGN.md` — design, estimands, validity checks, and analysis plan.
- `decision_memo.md` — blank executive decision template; no recommendation has been made.
- `seed_experiment.py` — deterministic assignment and reproducible synthetic data generation.
- `sql/` — BigQuery Standard SQL templates; adapt table and field names to the actual warehouse.
- `analysis/stats.py` — dependency-free two-proportion z-test and confidence intervals.
- `analysis/analysis.ipynb` — starter notebook; it does not contain experiment results.
- `figures/` — location for charts generated from a validated readout.

## Quick start

Requires Python 3.10+ and DuckDB. Install the single external dependency, then generate the default 15,000-row synthetic CSV and local DuckDB database:

```bash
python -m pip install -r requirements.txt
python seed_experiment.py --seed 20261021
```

The generated CSV is at `data/synthetic_experiment.csv`; the DuckDB database is at `data/experiment.duckdb` with an `experiment_events` table. Pass `--csv-only` to write only the CSV. To use a different size, pass `--customers N`.

The default is sized for the illustrative 18.5% baseline and +1.85 pp MDE in `PRE_REGISTRATION.md`. A previous 20% baseline / +1.0 pp design requires about 52,800 total customers, so 55,000 is appropriate only if that smaller MDE is retained. Neither simulated sample size nor simulated outcomes are evidence about real customer behavior.

All generated data is synthetic and is not evidence about real customer behavior. Open `analysis/analysis.ipynb` in Jupyter to start a readout after loading data and explicitly confirming the analysis dataset.

## Before analyzing any experiment

1. Freeze the eligibility rules, primary metric, MDE, sample size, run window, and decision thresholds in `PRE_REGISTRATION.md`.
2. Confirm assignment is stable at the customer level and run `sql/01_srm_check.sql` before looking at outcomes.
3. Validate exposure and outcome logging; report the intent-to-treat effect as primary.
4. Use `DESIGN.md` and the notebook to analyze the primary metric and guardrails. Treat segments as exploratory unless multiplicity is handled.
5. Complete the decision memo only from validated results. Record actuals separately from assumptions.

## Data and credentials

The repository contains no live credentials or real customer records. `.env.example` lists placeholders only; `.env` is ignored. SQL snippets assume a BigQuery-style table named `project.dataset.experiment_events`, with columns documented in `DESIGN.md`.
