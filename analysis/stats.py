"""Dependency-free inference helpers for binary conversion metrics."""
from __future__ import annotations
from math import erf, erfc, sqrt
from typing import NamedTuple

class ZTestResult(NamedTuple):
    control_rate: float
    treatment_rate: float
    difference: float
    z_statistic: float
    p_value_two_sided: float

def _validate(successes: int, total: int) -> None:
    if total <= 0 or successes < 0 or successes > total:
        raise ValueError("require total > 0 and 0 <= successes <= total")

def proportion_ci(successes: int, total: int, confidence: float = 0.95) -> tuple[float, float]:
    """Wilson score interval for one Bernoulli proportion (normal critical value)."""
    _validate(successes, total)
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1")
    # Invert the normal CDF by bisection; no external statistics package required.
    target = (1 + confidence) / 2
    lo, hi = 0.0, 8.0
    for _ in range(80):
        mid = (lo + hi) / 2
        cdf = 0.5 * (1 + erf(mid / sqrt(2)))
        if cdf < target:
            lo = mid
        else:
            hi = mid
    z = (lo + hi) / 2
    p = successes / total
    denom = 1 + z*z/total
    center = (p + z*z/(2*total)) / denom
    half = z * sqrt(p*(1-p)/total + z*z/(4*total*total)) / denom
    return max(0.0, center-half), min(1.0, center+half)

def difference_ci(control_successes: int, control_n: int, treatment_successes: int, treatment_n: int, confidence: float = 0.95) -> tuple[float, float]:
    """Unpooled Wald CI for treatment minus control absolute risk difference."""
    _validate(control_successes, control_n)
    _validate(treatment_successes, treatment_n)
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1")
    lo, hi = 0.0, 8.0
    target = (1 + confidence) / 2
    for _ in range(80):
        mid = (lo + hi) / 2
        if 0.5 * (1 + erf(mid / sqrt(2))) < target: lo = mid
        else: hi = mid
    z = (lo + hi) / 2
    p0, p1 = control_successes/control_n, treatment_successes/treatment_n
    diff = p1-p0
    se = sqrt(p0*(1-p0)/control_n + p1*(1-p1)/treatment_n)
    return diff-z*se, diff+z*se

def two_proportion_z_test(control_successes: int, control_n: int, treatment_successes: int, treatment_n: int) -> ZTestResult:
    """Pooled two-sided z test for H0: treatment and control proportions equal."""
    _validate(control_successes, control_n)
    _validate(treatment_successes, treatment_n)
    p0, p1 = control_successes/control_n, treatment_successes/treatment_n
    pooled = (control_successes+treatment_successes)/(control_n+treatment_n)
    se = sqrt(pooled*(1-pooled)*(1/control_n+1/treatment_n))
    if se == 0:
        z, p = 0.0, 1.0
    else:
        z = (p1-p0)/se
        p = erfc(abs(z)/sqrt(2))
    return ZTestResult(p0, p1, p1-p0, z, p)

