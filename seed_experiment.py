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

EXPERIMENT_ID = "auto_discount_vs_manual_coupon_v1"
CONTROL_CONVERSION = 0.20  # preliminary illustration only
TREATMENT_CONVERSION = 0.21  # illustrative +1 pp effect; not an empirical estimate

def assign_variant(customer_id: str, experiment_id: str = EXPERIMENT_ID) -> str:
    digest = hashlib.sha256(f"{experiment_id}:{customer_id}".encode("utf-8")).digest()
    return "treatment" if int.from_bytes(digest[:8], "big") % 2 else "control"

def generate(output: Path, customers: int, seed: int) -> None:
    if customers < 1:
        raise ValueError("customers must be at least 1")
    rng = random.Random(seed)
    output.parent.mkdir(parents=True, exist_ok=True)
    fields = ["experiment_id", "customer_id", "variant", "eligible", "assigned_at", "exposed", "exposure_count", "converted", "order_count", "revenue", "discount_cost", "contribution_margin", "refund", "payment_failed", "support_contact", "device", "country", "category", "data_status"]
    devices = ("mobile", "desktop", "tablet")
    countries = ("IN", "US", "GB", "CA")
    categories = ("apparel", "home", "beauty")
    with output.open("w", newline="", encoding="utf-8") as f:
        f.write("# SYNTHETIC illustrative data; not real customer data or experiment results\n")
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for i in range(customers):
            cid = f"synthetic_customer_{i+1:07d}"
            variant = assign_variant(cid)
            exposed = rng.random() < 0.96
            p = CONTROL_CONVERSION if variant == "control" else TREATMENT_CONVERSION
            converted = rng.random() < p
            revenue = round(rng.uniform(25, 180), 2) if converted else 0.0
            discount = round(min(revenue * 0.10, 20.0), 2) if converted else 0.0
            margin = round(revenue * 0.42 - discount, 2) if converted else 0.0
            writer.writerow({"experiment_id": EXPERIMENT_ID, "customer_id": cid, "variant": variant, "eligible": True, "assigned_at": "2026-10-21T00:00:00Z", "exposed": exposed, "exposure_count": 1 if exposed else 0, "converted": converted, "order_count": int(converted), "revenue": f"{revenue:.2f}", "discount_cost": f"{discount:.2f}", "contribution_margin": f"{margin:.2f}", "refund": bool(converted and rng.random() < 0.03), "payment_failed": bool(rng.random() < 0.02), "support_contact": bool(rng.random() < 0.04), "device": rng.choice(devices), "country": rng.choice(countries), "category": rng.choice(categories), "data_status": "SYNTHETIC"})
    print(f"Wrote {customers:,} synthetic rows to {output}")
    print("Reminder: generated outcomes are illustrative and must not be presented as real findings.")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--customers", type=int, default=20000)
    parser.add_argument("--seed", type=int, default=20261021)
    parser.add_argument("--output", type=Path, default=Path("data/synthetic_experiment.csv"))
    args = parser.parse_args()
    generate(args.output, args.customers, args.seed)
if __name__ == "__main__":
    main()

