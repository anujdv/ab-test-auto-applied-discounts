#!/usr/bin/env python3
"""Generate a reproducible SYNTHETIC customer-level A/B test dataset.

Assignments are stable per experiment/customer via SHA-256. Outcomes use a local,
seeded PRNG and are illustrative only; they are not real customer findings.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import random
from pathlib import Path

EXPERIMENT_ID = 301
CONTROL_VARIANT_ID = 3011
TREATMENT_VARIANT_ID = 3012
CONTROL_CONVERSION = 0.185  # preliminary economic scenario; validate before registration
TREATMENT_CONVERSION = 0.2035  # illustrative +1.85 pp effect; not an empirical estimate
AOV_INR = 2500.0  # illustrative only
GROSS_MARGIN_RATE = 0.40  # before discount; illustrative only
DISCOUNT_INR = 150.0  # illustrative only
CONTROL_COUPON_REDEMPTION = 0.60  # manual entry scenario; illustrative only

def assign_variant(customer_id: str, experiment_id: int = EXPERIMENT_ID) -> str:
    digest = hashlib.sha256(f"{experiment_id}:{customer_id}".encode("utf-8")).digest()
    return "treatment" if int.from_bytes(digest[:8], "big") % 2 else "control"

def generate(output: Path, customers: int, seed: int, duckdb_output: Path | None = None) -> None:
    if customers < 1:
        raise ValueError("customers must be at least 1")
    rng = random.Random(seed)
    output.parent.mkdir(parents=True, exist_ok=True)
    fields = ["experiment_id", "variant_id", "customer_id", "variant", "eligible", "assigned_at", "exposed", "exposure_count", "converted", "order_count", "revenue", "discount_cost", "contribution_margin", "refund", "payment_failed", "support_contact", "device", "country", "category", "data_status"]
    devices = ("mobile", "desktop", "tablet")
    countries = ("IN", "US", "GB", "CA")
    categories = ("apparel", "home", "beauty")
    with output.open("w", newline="", encoding="utf-8") as f:
        f.write("# SYNTHETIC illustrative data; not real customer data or experiment results\r\n")
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for i in range(customers):
            cid = f"synthetic_customer_{i+1:07d}"
            variant = assign_variant(cid)
            variant_id = CONTROL_VARIANT_ID if variant == "control" else TREATMENT_VARIANT_ID
            exposed = rng.random() < 0.96
            p = CONTROL_CONVERSION if variant == "control" else TREATMENT_CONVERSION
            converted = rng.random() < p
            # Hold illustrative basket value and pre-discount margin constant by arm.
            revenue = AOV_INR if converted else 0.0
            redeemed = variant == "treatment" or rng.random() < CONTROL_COUPON_REDEMPTION
            discount = DISCOUNT_INR if converted and redeemed else 0.0
            refunded = bool(converted and rng.random() < 0.03)
            margin = (revenue * GROSS_MARGIN_RATE - discount) if converted and not refunded else 0.0
            writer.writerow({"experiment_id": EXPERIMENT_ID, "variant_id": variant_id, "customer_id": cid, "variant": variant, "eligible": True, "assigned_at": "2026-10-26T00:00:00Z", "exposed": exposed, "exposure_count": 1 if exposed else 0, "converted": converted, "order_count": int(converted), "revenue": f"{revenue:.2f}", "discount_cost": f"{discount:.2f}", "contribution_margin": f"{margin:.2f}", "refund": refunded, "payment_failed": bool(rng.random() < 0.02), "support_contact": bool(rng.random() < 0.04), "device": rng.choice(devices), "country": rng.choice(countries), "category": rng.choice(categories), "data_status": "SYNTHETIC"})
    print(f"Wrote {customers:,} synthetic rows to {output}")
    print("Reminder: generated outcomes are illustrative and must not be presented as real findings.")
    if duckdb_output is not None:
        try:
            import duckdb
        except ImportError as exc:
            raise RuntimeError("DuckDB output requested; install dependencies with 'python -m pip install -r requirements.txt'") from exc
        duckdb_output.parent.mkdir(parents=True, exist_ok=True)
        with duckdb.connect(str(duckdb_output)) as connection:
            connection.execute(
                "CREATE OR REPLACE TABLE experiment_events AS "
                "SELECT * FROM read_csv_auto(?, skip=1, header=true)",
                [str(output.resolve())],
            )
        print(f"Wrote synthetic experiment_events table to {duckdb_output}")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--customers", type=int, default=15000)
    parser.add_argument("--seed", type=int, default=20261021)
    parser.add_argument("--output", type=Path, default=Path("data/synthetic_experiment.csv"))
    parser.add_argument("--duckdb-output", type=Path, default=Path("data/experiment.duckdb"))
    parser.add_argument("--csv-only", action="store_true", help="skip the DuckDB database output")
    args = parser.parse_args()
    generate(args.output, args.customers, args.seed, None if args.csv_only else args.duckdb_output)

if __name__ == "__main__":
    main()
