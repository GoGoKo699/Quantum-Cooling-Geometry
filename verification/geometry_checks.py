#!/usr/bin/env python3
"""Finite diagnostics for Quantum Cooling Geometry's analytical path results.

These checks address discrete placement, carrier loss and noise-age conventions.
They do not establish the arbitrary-circuit graph converse.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path


def median_cost(n: int, m: int) -> int:
    q, r = divmod(n, m)
    return (m - r) * (q * q // 4) + r * ((q + 1) ** 2 // 4)


def conveyor(length: int, port: int, rounds: int):
    # Original carrier labels are nonnegative; -1 labels reset-produced carriers.
    carriers = list(range(length))
    ages = [None] * length
    for t in range(rounds):
        for j in range(t % 2, length - 1, 2):
            carriers[j], carriers[j + 1] = carriers[j + 1], carriers[j]
            ages[j], ages[j + 1] = ages[j + 1], ages[j]
        ages = [None if x is None else x + 1 for x in ages]
        carriers[port] = -1
        ages[port] = 0
    return carriers, ages


def check_placement(max_n=12):
    tested = 0
    for n in range(1, max_n + 1):
        by_m = {}
        for m in range(1, n + 1):
            optimum = min(
                sum(min(abs(v - s) for s in contacts) for v in range(n))
                for contacts in itertools.combinations(range(n), m)
            )
            assert optimum == median_cost(n, m), (n, m, optimum)
            assert 4 * m * optimum >= n * (n - m), (n, m, optimum)
            assert m * optimum <= n * (n - m), (n, m, optimum)
            if 2 * m >= n:
                assert optimum == n - m, (n, m, optimum)
            by_m[m] = optimum
            tested += 1
    return {"n_max": max_n, "parameter_pairs": tested, "status": "passed"}


def check_conveyors(max_length=80):
    tested = 0
    for length in range(1, max_length + 1):
        for port in range(length):
            distance_sum = sum(abs(j - port) for j in range(length))
            # After flushing, both parity phases suffice for the age formula.
            for rounds in (2 * length, 2 * length + 1):
                carriers, ages = conveyor(length, port, rounds)
                assert all(x == -1 for x in carriers), (length, port, rounds)
                assert ages[port] == 0
                assert all(a is not None for a in ages)
                assert sum(ages) <= 2 * distance_sum, (length, port, rounds, ages)
                for arm in (list(reversed(ages[:port])), ages[port + 1 :]):
                    b = len(arm)
                    assert sum(arm) in (b * b, b * (b + 1)), (
                        length, port, rounds, arm
                    )
                    outbound = [x for x in range(1, b + 1) if arm[x - 1] == x]
                    inbound = [x for x in range(1, b + 1) if arm[x - 1] != x]
                    assert all(arm[x - 1] == 2 * b + 1 - x for x in inbound)
                    if inbound:
                        parity = inbound[0] % 2
                        assert inbound == [x for x in range(1, b + 1) if x % 2 == parity]
                tested += 1
        if length >= 2:
            carriers, ages = conveyor(length, 0, 2 * length - 1)
            assert all(x == -1 for x in carriers)
            assert sorted(ages) == [0] + list(range(1, 2 * length - 2, 2)), (
                length, ages
            )
            assert sum(ages) == (length - 1) ** 2
    return {
        "length_max": max_length,
        "arbitrary_port_phase_cases": tested,
        "endpoint_age_multisets": max_length - 1,
        "status": "passed",
    }


def check_slab_sums():
    tested = 0
    for dimension in (1, 2, 3):
        for sides in itertools.product(range(1, 6), repeat=dimension):
            longitudinal, *transverse = sides
            area = 1
            for x in transverse:
                area *= x
            direct = sum(point[0] for point in itertools.product(*(range(x) for x in sides)))
            closed = area * longitudinal * (longitudinal - 1) // 2
            assert direct == closed, (sides, direct, closed)
            tested += 1
    return {"dimensions": [1, 2, 3], "side_max": 5, "boxes": tested, "status": "passed"}


def main():
    result = {
        "scope": "Finite exact-integer geometry and carrier-age diagnostics; no proof certification.",
        "placement": check_placement(),
        "conveyors": check_conveyors(),
        "slabs": check_slab_sums(),
    }
    destination = Path(__file__).with_name("geometry_checks_results.json")
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
