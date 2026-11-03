# Auto-applied discount vs manual coupon at checkout

> **Completed synthetic case study. No live experiment has run and no real business findings are reported.** The data is generated solely to demonstrate an A/B testing workflow.

This project asks whether applying an eligible discount automatically at checkout could reduce coupon-entry friction. It demonstrates experiment planning, assignment checks, intent-to-treat (ITT) conversion analysis, contribution-margin and guardrail summaries, and clear communication of limitations.

**Important:** the generator sets the Control purchase probability to 18.5% and the Treatment probability to 20.35%. The positive Treatment lift in the readout is therefore built into the simulation. It is not evidence that automatic discounts cause higher purchases in a real business.

## Synthetic practice readout

| Measure | Control | Treatment | Treatment − Control |
|---|---:|---:|---:|
| Assigned customers | 7,561 | 7,439 | — |
| ITT conversion | 18.94% | 20.46% | +1.52 pp (95% CI +0.25 to +2.79; p=0.0192) |
| Contribution margin per assigned customer | ₹168.15 | ₹169.22 | +₹1.08 (approx. 95% interval −₹10.03 to +₹12.19) |

The planned +1.85 pp MDE is a sample-size planning assumption, not a guaranteed effect or a pass/fail cutoff. The simulation has no real guardrail thresholds and supports no Ship/Stage/Hold decision. See the [full synthetic readout](decision_memo.md) and [frozen practice plan](PRE_REGISTRATION.md).

## Repository map

- `PRE_REGISTRATION.md` — frozen assumptions and analysis rules for this synthetic exercise.
- `DESIGN.md` — design, estimands, validity checks, and analysis plan.
- `decision_memo.md` — completed simulated scorecard and limitations; no rollout decision.
- `seed_experiment.py` — deterministic customer assignment and synthetic-data generator.
- `data/synthetic_experiment.csv` — readable 15,000-row practice dataset.
- `data/experiment.duckdb` — the same synthetic rows in a local-queryable DuckDB database.
- `sql/` — BigQuery Standard SQL templates; they do not run unchanged in DuckDB.
- `analysis/stats.py` — dependency-free conversion-rate test and confidence intervals.
- `analysis/analysis.ipynb` — walkthrough of data checks, ITT conversion, economics, and guardrail summaries.

## Reproduce the simulation

Requires Python 3.10 or newer. Dependencies are listed in `requirements.txt`: DuckDB, pandas, IPython kernel, and JupyterLab.

Windows PowerShell (using Python 3.14):

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe seed_experiment.py --seed 20261021
.\.venv\Scripts\python.exe -m jupyterlab
```

Then open `analysis/analysis.ipynb` in JupyterLab or VS Code and select the `.venv` Python kernel. On another Python version, replace `3.14` with the installed version. The generator writes `data/synthetic_experiment.csv` and `data/experiment.duckdb`; use `--csv-only` to skip DuckDB or `--customers N` to choose a different row count.

The committed CSV and DuckDB file are synthetic examples. Re-running the generator recreates the outputs; the analysis must always be interpreted with the selected dataset and seed in mind.

## SQL and database notes

The generated local database is DuckDB and contains an `experiment_events` table. The SQL files under `sql/` are written for **BigQuery Standard SQL** and require adapting table and field names for a real warehouse; they are not DuckDB queries.

## Before any real experiment

A real test would require approved eligibility and identity rules, verified financial inputs and contribution-margin definition, an agreed outcome window, guardrail thresholds from Product and Finance, a fresh sample-size calculation, reliable assignment and exposure logging, and a new approved preregistration. Analyze validated live data before making a decision.
