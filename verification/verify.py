#!/usr/bin/env python3
"""Finite checks for Quantum Cooling Geometry. Requires only NumPy.

These checks test conventions, exact finite identities and counterexamples.
They are not a substitute for the arbitrary-size written proof.
"""
from __future__ import annotations

import argparse
import itertools
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

SEED = 1729
TOL = 2e-10
PAULI = (
    np.eye(2, dtype=complex),
    np.array([[0, 1], [1, 0]], complex),
    np.array([[0, -1j], [1j, 0]], complex),
    np.diag([1, -1]).astype(complex),
)


def haar(d: int, rng: np.random.Generator) -> np.ndarray:
    a = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    q, r = np.linalg.qr(a)
    return q @ np.diag(np.diag(r) / np.abs(np.diag(r))).conj()


def density(d: int, rng: np.random.Generator, kind: int = 0) -> np.ndarray:
    if kind == 0:
        return np.eye(d, dtype=complex) / d
    a = rng.normal(size=(d, 1 if kind == 1 else d))
    a = a + 1j * rng.normal(size=a.shape)
    rho = a @ a.conj().T
    return rho / np.trace(rho)


def embed(a: np.ndarray, sites: tuple[int, ...], n: int) -> np.ndarray:
    """Embed an operator using most-significant-bit site numbering."""
    d = 1 << n
    k = len(sites)
    out = np.zeros((d, d), complex)
    masks = [1 << (n - 1 - j) for j in sites]
    clear = sum(masks)
    for col in range(d):
        small_col = sum(bool(col & mask) << (k - 1 - z)
                        for z, mask in enumerate(masks))
        base = col & ~clear
        for small_row in range(1 << k):
            row = base | sum(((small_row >> (k - 1 - z)) & 1) * mask
                             for z, mask in enumerate(masks))
            out[row, col] = a[small_row, small_col]
    return out


def site_blocks(n: int, j: int) -> tuple[np.ndarray, np.ndarray]:
    indices = np.arange(1 << n)
    mask = 1 << (n - 1 - j)
    return indices[(indices & mask) == 0], indices[(indices & mask) != 0]


def local_replacement(rho: np.ndarray, n: int, j: int,
                      maximally_mixed: bool = False) -> np.ndarray:
    zero, one = site_blocks(n, j)
    reduced = rho[np.ix_(zero, zero)] + rho[np.ix_(one, one)]
    out = np.zeros_like(rho)
    if maximally_mixed:
        out[np.ix_(zero, zero)] = reduced / 2
        out[np.ix_(one, one)] = reduced / 2
    else:
        out[np.ix_(zero, zero)] = reduced
    return out


def depolarize(rho: np.ndarray, n: int, j: int, p: float) -> np.ndarray:
    return (1 - p) * rho + p * local_replacement(rho, n, j, True)


def random_cptp(rng: np.random.Generator, rank: int = 4) -> list[np.ndarray]:
    a = rng.normal(size=(2 * rank, 2)) + 1j * rng.normal(size=(2 * rank, 2))
    v, _ = np.linalg.qr(a)
    ks = [v[2 * z:2 * z + 2] for z in range(rank)]
    assert np.linalg.norm(sum(k.conj().T @ k for k in ks) - np.eye(2)) < TOL
    return ks


def apply_cptp(rho: np.ndarray, ks: list[np.ndarray]) -> np.ndarray:
    return sum(k @ rho @ k.conj().T for k in ks)


def random_layer(n: int, step: int, rng: np.random.Generator) -> np.ndarray:
    out = np.eye(1 << n, dtype=complex)
    used = set()
    for j in range(step % 2, n - 1, 2):
        out = embed(haar(4, rng), (j, j + 1), n) @ out
        used.update((j, j + 1))
    for j in set(range(n)) - used:
        out = embed(haar(2, rng), (j,), n) @ out
    return out


def swap_density(rho: np.ndarray, n: int, a: int, b: int) -> np.ndarray:
    indices = np.arange(1 << n)
    shift_a, shift_b = n - 1 - a, n - 1 - b
    different = ((indices >> shift_a) ^ (indices >> shift_b)) & 1
    perm = indices ^ (different << shift_a) ^ (different << shift_b)
    return rho[np.ix_(perm, perm)]


def token_conveyor(n: int, rounds: int | None = None, port: int = 0,
                   phase: int = 0) -> dict:
    rounds = 2 * n - 1 if rounds is None else rounds
    labels = [-(j + 1) for j in range(n)]
    ages = [0] * n
    removed = []
    first_clear = None
    for s in range(rounds):
        for j in range((s + phase) % 2, n - 1, 2):
            labels[j], labels[j + 1] = labels[j + 1], labels[j]
            ages[j], ages[j + 1] = ages[j + 1], ages[j]
        ages = [a + 1 for a in ages]
        if labels[port] < 0:
            removed.append(labels[port])
        labels[port] = s + 1
        ages[port] = 0
        if min(labels) > 0 and first_clear is None:
            first_clear = s + 1
    return {"labels": labels, "ages": ages, "removed": removed,
            "first_clear": first_clear, "rounds": rounds}


def voronoi_cells(n: int, ports: tuple[int, ...]) -> list[tuple[int, int, int]]:
    """Contiguous nearest-port cells; a distance tie goes to the left port."""
    assigned = [min(ports, key=lambda s: (abs(v - s), s)) for v in range(n)]
    cells = []
    for port in ports:
        members = [v for v, assigned_port in enumerate(assigned) if assigned_port == port]
        assert members == list(range(min(members), max(members) + 1))
        cells.append((min(members), max(members) + 1, port))
    return cells


def port_conveyor(n: int, ports: tuple[int, ...]) -> dict:
    cells = voronoi_cells(n, ports)
    rounds = 2 * max(end - start for start, end, _ in cells) - 1
    labels = [-(j + 1) for j in range(n)]
    ages = [0] * n
    for s in range(rounds):
        for start, end, _ in cells:
            for j in range(start + s % 2, end - 1, 2):
                labels[j], labels[j + 1] = labels[j + 1], labels[j]
                ages[j], ages[j + 1] = ages[j + 1], ages[j]
        ages = [age + 1 for age in ages]
        for port in ports:
            labels[port] = s + 1
            ages[port] = 0
    return {"cells": cells, "rounds": rounds, "labels": labels, "ages": ages}


def conveyor_error(ages: list[int], p: float) -> float:
    ages_array = np.array(ages)
    if p == 1:
        return float(-np.expm1(-np.count_nonzero(ages_array) * np.log(2)))
    # Stable both at p=0 and when p*n² is very small.
    log_factors = np.log1p(0.5 * np.expm1(ages_array * np.log1p(-p)))
    return float(-np.expm1(log_factors.sum()))


def check_conveyor() -> dict:
    count = 0
    max_weak_relative_error = 0.0
    examples = []
    for n in range(1, 129):
        tr = token_conveyor(n)
        expected = [0] + list(range(1, 2 * n - 2, 2))
        assert sorted(tr["ages"]) == expected
        assert sorted(tr["removed"]) == list(range(-n, 0))
        assert tr["first_clear"] == 2 * n - 1
        # Continuing after the first clear time cannot secretly reintroduce input.
        for extra in (2, 6):
            continued = token_conveyor(n, 2 * n - 1 + extra)
            assert sorted(continued["ages"]) == expected
            assert min(continued["labels"]) > 0
        for p in (0.0, 1e-5, 0.01, 0.2, 0.8, 1.0):
            error = conveyor_error(tr["ages"], p)
            lower = (1 - (1 - p) ** (n * (n - 1) // 2)) / 2
            assert error + TOL >= lower
            assert error <= min(1.0, p * (n - 1) ** 2 / 2) + TOL
            count += 1
        if n > 1:
            # Numerical derivative taken where p*n² is uniformly small.
            p = 1e-7 / (n * n)
            coefficient = conveyor_error(tr["ages"], p) / p
            expected_coefficient = (n - 1) ** 2 / 2
            relative = abs(coefficient / expected_coefficient - 1)
            max_weak_relative_error = max(max_weak_relative_error, relative)
            assert relative < 3e-5
        if n in (1, 2, 3, 8, 32):
            examples.append({"n": n, "rounds": tr["rounds"],
                             "age_multiset": sorted(tr["ages"]),
                             "error_at_p_0.001": conveyor_error(tr["ages"], 0.001)})
    return {"n_range": [1, 128], "probability_cases": count,
            "max_weak_noise_coefficient_relative_error": max_weak_relative_error,
            "examples": examples}


def check_dense_conveyor_reference() -> dict:
    maximum = 0.0
    cases = []
    configurations = [(2, (0,)), (3, (0,)), (4, (0,)),
                      (3, (1,)), (4, (1,)), (4, (1, 3)),
                      (4, (0, 2)), (4, (0, 1, 2, 3))]
    for n, ports in configurations:
        d = 1 << n
        phi = np.eye(d, dtype=complex).reshape(-1) / np.sqrt(d)
        initial = np.outer(phi, phi.conj())
        for p in (0.0, 0.07, 0.45):
            rho = initial.copy()
            total = 2 * n
            tr = port_conveyor(n, ports)
            for s in range(tr["rounds"]):
                for start, end, _ in tr["cells"]:
                    for j in range(start + s % 2, end - 1, 2):
                        rho = swap_density(rho, total, j, j + 1)
                for j in range(n):
                    rho = depolarize(rho, total, j, p)
                for port in ports:
                    rho = local_replacement(rho, total, port)
            ages = tr["ages"]
            sigma = np.array([[1.0]], complex)
            for age in ages:
                q = (1 - p) ** age
                sigma = np.kron(sigma, np.diag([(1 + q) / 2, (1 - q) / 2]))
            expected = np.kron(sigma, np.eye(d) / d)
            discrepancy = float(np.linalg.norm(rho - expected))
            maximum = max(maximum, discrepancy)
            assert discrepancy < TOL
            # The data replacement is diagonal, so pure-target trace error = 1-F.
            diagonal_error = 1 - float(np.real(sigma[0, 0]))
            assert abs(diagonal_error - conveyor_error(ages, p)) < TOL
            cases.append({"n": n, "ports": list(ports), "p": p,
                          "choi_frobenius_error": discrepancy})
    return {"scope": "Normalized Choi state: all data qubits initially maximally entangled with reference",
            "cases": cases, "max_frobenius_error": maximum}


def check_interior_ports() -> dict:
    cases = 0
    largest_ratio = 0.0
    latest_first_clear_fraction = 0.0
    for n in range(1, 49):
        for port in range(n):
            distance_sum = sum(abs(j - port) for j in range(n))
            for phase in (0, 1):
                # Both parity phases and both late finishing parities matter.
                for extra in (0, 1, 2):
                    tr = token_conveyor(n, 2 * n - 1 + extra, port, phase)
                    assert min(tr["labels"]) > 0
                    assert tr["first_clear"] <= 2 * n - 1
                    assert sum(tr["ages"]) <= 2 * distance_sum
                    latest_first_clear_fraction = max(latest_first_clear_fraction,
                                                       tr["first_clear"] / (2 * n - 1))
                    if distance_sum:
                        largest_ratio = max(largest_ratio,
                                            sum(tr["ages"]) / (2 * distance_sum))
                    for p in (0.003, 0.4):
                        assert conveyor_error(tr["ages"], p) <= min(1.0, p * distance_sum) + TOL
                    cases += 1
    return {"n_range": [1, 48], "all_ports_and_two_starting_phases": True,
            "finishing_times": "2n-1,2n,2n+1", "cases": cases,
            "largest_sum_age_over_twice_distance_sum": largest_ratio,
            "largest_first_clear_over_2n_minus_1": latest_first_clear_fraction}


def check_dense_control_bound(rng: np.random.Generator) -> dict:
    cases = 0
    max_violation = -1.0
    max_trace_error = 0.0
    min_eigenvalue = 1.0
    for n in (2, 3, 4):
        for rounds in range(1, n + 3):
            m = sum(min(rounds, j) for j in range(n))
            for p in (0.001, 0.04, 0.3, 0.9, 1.0):
                bound = (1 + (1 - p) ** m) / 2
                for sample in range(8):
                    rho = density(1 << n, rng, sample % 3)
                    for s in range(rounds):
                        u = random_layer(n, s, rng)
                        rho = u @ rho @ u.conj().T
                        for j in range(n):
                            rho = depolarize(rho, n, j, p)
                        # Cover ideal reset as well as genuinely arbitrary CPTP maps.
                        if sample % 4 == 0:
                            rho = local_replacement(rho, n, 0)
                        else:
                            ks = [embed(k, (0,), n) for k in random_cptp(rng)]
                            rho = apply_cptp(rho, ks)
                    eigenvalues = np.linalg.eigvalsh((rho + rho.conj().T) / 2)
                    violation = float(eigenvalues[-1] - bound)
                    max_violation = max(max_violation, violation)
                    max_trace_error = max(max_trace_error, float(abs(np.trace(rho) - 1)))
                    min_eigenvalue = min(min_eigenvalue, float(eigenvalues[0]))
                    assert violation < TOL
                    assert eigenvalues[0] > -TOL
                    assert abs(np.trace(rho) - 1) < TOL
                    cases += 1
    return {"n_values": [2, 3, 4], "cases": cases,
            "p_values": [0.001, 0.04, 0.3, 0.9, 1.0],
            "max_lambda_max_minus_bound": max_violation,
            "max_trace_error": max_trace_error,
            "minimum_output_eigenvalue": min_eigenvalue,
            "scope": "Random pure, mixed and maximally mixed inputs; Haar entangling layers; ideal or random rank-four boundary CPTP maps"}


def apply_operations(rho: np.ndarray, operations: list, n: int,
                     omit_selected: bool = False) -> np.ndarray:
    for kind, value in operations:
        if kind == "u":
            rho = value @ rho @ value.conj().T
        elif kind == "cptp":
            rho = apply_cptp(rho, value)
        elif kind == "selected" and not omit_selected:
            rho = local_replacement(rho, n, value, True)
    return rho


def check_push_through(rng: np.random.Generator) -> dict:
    maximum = 0.0
    maximum_lambda = 0.0
    cases = 0
    for n in (2, 3, 4):
        for rounds in (n - 1, n + 1):
            late = [(j, s) for s in range(rounds) for j in range(n)
                    if j > rounds - 1 - s]
            for _ in range(20):
                selected_j, selected_s = late[int(rng.integers(len(late)))]
                operations = []
                selected_index = None
                for s in range(rounds):
                    operations.append(("u", random_layer(n, s, rng)))
                    for j in range(n):
                        if (j, s) == (selected_j, selected_s):
                            selected_index = len(operations)
                            operations.append(("selected", j))
                        else:
                            operations.append(("u", embed(PAULI[int(rng.integers(4))], (j,), n)))
                    ks = [embed(k, (0,), n) for k in random_cptp(rng, rank=3)]
                    operations.append(("cptp", ks))
                rho0 = density(1 << n, rng, 2)
                actual = apply_operations(rho0.copy(), operations, n)
                remaining = apply_operations(rho0.copy(), operations, n, True)
                v = np.eye(1 << n, dtype=complex)
                for kind, value in operations[selected_index + 1:]:
                    if kind == "u":
                        v = value @ v
                predicted = v @ local_replacement(v.conj().T @ remaining @ v,
                                                  n, selected_j, True) @ v.conj().T
                discrepancy = float(np.linalg.norm(actual - predicted))
                lam = float(np.linalg.eigvalsh((actual + actual.conj().T) / 2)[-1])
                maximum = max(maximum, discrepancy)
                maximum_lambda = max(maximum_lambda, lam)
                assert discrepancy < TOL
                assert lam <= 0.5 + TOL
                cases += 1
    # Negative control: an event at the reset port is erased immediately.
    zero = np.zeros((4, 4), complex)
    zero[0, 0] = 1
    after = local_replacement(local_replacement(zero, 2, 0, True), 2, 0)
    false_push = local_replacement(local_replacement(zero, 2, 0), 2, 0, True)
    negative_gap = float(np.linalg.norm(after - false_push))
    assert np.linalg.eigvalsh(after)[-1] == 1
    assert negative_gap > 0.5
    # Pure dephasing is unital but preserves |0...0>; a heating component matters.
    z = embed(PAULI[3], (1,), 2)
    dephased = (zero + z @ zero @ z.conj().T) / 2
    assert np.linalg.norm(dephased - zero) < TOL
    return {"cases": cases, "max_push_through_frobenius_error": maximum,
            "max_conditional_lambda_max": maximum_lambda,
            "outside_late_cone_negative_control_gap": negative_gap,
            "dephasing_preserves_target_negative_control": True,
            "scope": "Selected full depolarizer kept unconditioned; all other depolarizers conditioned only as random Pauli unitaries"}


def check_geometry() -> dict:
    examples = []
    maximum_comparison_ratio = 0.0
    minimum_comparison_ratio = 1.0
    placements = 0
    for n in range(2, 12):
        for m in range(1, n + 1):
            scores = []
            for ports in itertools.combinations(range(n), m):
                score = sum(min(abs(v - s) for s in ports) for v in range(n))
                scores.append(score)
                tr = port_conveyor(n, ports)
                assert min(tr["labels"]) > 0
                assert sum(tr["ages"]) <= 2 * score
                for p in (0.003, 0.4):
                    assert conveyor_error(tr["ages"], p) <= min(1.0, p * score) + TOL
                placements += 1
            best = min(scores)
            if m < n:
                scale = n * (n - m) / m
                ratio = best / scale
                minimum_comparison_ratio = min(minimum_comparison_ratio, ratio)
                maximum_comparison_ratio = max(maximum_comparison_ratio, ratio)
                assert 0.25 - TOL <= ratio <= 1 + TOL
            else:
                assert best == 0
            sizes = [n // m + (j < n % m) for j in range(m)]
            t = 2 * max(sizes) - 1
            total_ages = 0
            for size in sizes:
                tr = token_conveyor(size, t)
                assert min(tr["labels"]) > 0
                total_ages += sum(tr["ages"])
            assert total_ages == sum((size - 1) ** 2 for size in sizes)
            if n in (5, 10) and m in (1, 2, n - 1, n):
                examples.append({"n": n, "m": m, "optimal_distance_sum": best,
                                 "balanced_endpoint_interval_sizes": sizes,
                                 "conveyor_noise_age_sum": total_ages})
    slabs = []
    for dimension in (1, 2, 3):
        for length in range(2, 13):
            points = list(itertools.product(range(length), repeat=dimension))
            distance_sum = sum(point[0] for point in points)
            formula = length ** (dimension - 1) * length * (length - 1) // 2
            assert distance_sum == formula
            assert len(points) == length ** dimension
            slabs.append({"dimension": dimension, "length": length,
                          "n": len(points), "distance_sum": distance_sum})
    return {"exhaustive_line_n_range": [2, 11], "port_placements": placements,
            "observed_min_optimal_distance_sum_over_n_n_minus_m_over_m": minimum_comparison_ratio,
            "observed_max_optimal_distance_sum_over_n_n_minus_m_over_m": maximum_comparison_ratio,
            "examples": examples, "slabs": slabs,
            "scope": "Exact finite enumeration; asymptotic graph claims require the written proof"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).resolve().with_name("results.json"))
    args = parser.parse_args()
    rng = np.random.default_rng(SEED)
    result = {
        "status": "passed",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "seed": SEED,
        "python_version": platform.python_version(),
        "numpy_version": np.__version__,
        "absolute_tolerance": TOL,
        "model": "Disjoint nearest-neighbor unitary layer; iid D_p on all sites including idle; boundary CPTP/reset last; all qubits retained",
        "conveyor": check_conveyor(),
        "reference_channel": check_dense_conveyor_reference(),
        "interior_port_conveyors": check_interior_ports(),
        "arbitrary_quantum_controls": check_dense_control_bound(rng),
        "selected_event_factorization": check_push_through(rng),
        "geometry": check_geometry(),
        "limits": [
            "Finite checks do not prove arbitrary-size theorems or certify novelty.",
            "Random controls are sampled, not an exhaustive optimization.",
            "No heat, work, gate-synthesis cost, finite-rate reservoir or hardware crossover is tested.",
            "The full physical register is retained; hidden fresh ancillas, discarded syndrome registers and encoded-only recovery are outside the model.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "output": str(args.output),
                      "random_control_cases": result["arbitrary_quantum_controls"]["cases"],
                      "push_through_cases": result["selected_event_factorization"]["cases"],
                      "max_choi_discrepancy": result["reference_channel"]["max_frobenius_error"],
                      "max_push_through_discrepancy": result["selected_event_factorization"]["max_push_through_frobenius_error"]}, indent=2))


if __name__ == "__main__":
    main()
