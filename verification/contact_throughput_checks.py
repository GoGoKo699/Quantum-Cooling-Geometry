#!/usr/bin/env python3
"""Finite checks for the exact contact-cover throughput law and planner.

Run from the repository root::

    python verification/contact_throughput_checks.py

The assignment checks use exact fractions and independently enumerate tiny
instances. The production planner does not enumerate assignments. NumPy is
used only for small full-reference channel and sampled-control checks, reusing
the existing verify.py channel conventions. These checks complement the
analytical all-circuit proof; they do not optimize over arbitrary controls or
numerically certify an arbitrary-channel diamond norm.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

import numpy as np

import verify
from contact_schedule import ContactSchedule, h, plan_schedule


SEED = 63017
TOL = 2e-10
PROBABILITIES = (Fraction(0), Fraction(1, 7), Fraction(2, 5),
                 Fraction(9, 10), Fraction(1))


def independent_score(assignment: tuple[str, ...], contacts: tuple[str, ...],
                       p: Fraction) -> tuple[Fraction, int]:
    """Reference objective, separate from the flow and schedule implementation."""
    loads = [assignment.count(contact) for contact in contacts]
    probability = Fraction(1)
    for load in loads:
        retention = Fraction(1)
        for _ in range(load):
            retention *= 1 - p
            probability *= (1 + retention) / 2
    return probability, sum(load * (load + 1) // 2 for load in loads)


def check_legal_schedule(plan: ContactSchedule,
                         neighbors: dict[str, tuple[str, ...]]) -> None:
    """Independent token/age simulation, including the initial reset round."""
    assert plan.depth == 1 + max(plan.loads.values())
    assert plan.layers[0] == ()
    sites = plan.contacts + plan.bulk
    tokens = {site: ("input", site) for site in sites}
    ages = {site: None for site in sites}
    touched = set()
    for time, layer in enumerate(plan.layers, start=1):
        used = set()
        for contact, vertex in layer:
            assert contact in neighbors[vertex]
            assert contact not in used and vertex not in used
            assert vertex not in touched
            used.update((contact, vertex))
            touched.add(vertex)
            tokens[contact], tokens[vertex] = tokens[vertex], tokens[contact]
            ages[contact], ages[vertex] = ages[vertex], ages[contact]
        ages = {site: None if age is None else age + 1
                for site, age in ages.items()}
        for contact in plan.contacts:
            tokens[contact] = ("reset", time)
            ages[contact] = 0
    assert touched == set(plan.bulk)
    assert all(token[0] == "reset" for token in tokens.values())
    assert ages == plan.terminal_ages
    assert sum(ages.values()) == plan.assignment_age_sum
    probability = Fraction(1)
    for vertex in plan.bulk:
        probability *= (1 + (1 - plan.p) ** ages[vertex]) / 2
    assert probability == plan.survival
    assert plan.error == 1 - probability


def check_exhaustive_assignments() -> dict:
    incidence_cases, probability_cases, assignments = 0, 0, 0
    for contact_count, maximum_bulk in ((1, 4), (2, 4), (3, 3)):
        contacts = tuple(f"s{i}" for i in range(contact_count))
        subsets = [tuple(contacts[j] for j in range(contact_count)
                         if mask & (1 << j))
                   for mask in range(1, 1 << contact_count)]
        for bulk_count in range(maximum_bulk + 1):
            for neighborhood_tuple in itertools.product(subsets, repeat=bulk_count):
                incidence_cases += 1
                neighbors = {f"b{i}": values
                             for i, values in enumerate(neighborhood_tuple)}
                for p in PROBABILITIES:
                    reference = [independent_score(candidate, contacts, p)
                                 for candidate in itertools.product(*neighborhood_tuple)]
                    assignments += len(reference)
                    optimum = max((population, -age_sum)
                                  for population, age_sum in reference)
                    minimum_age = min(age_sum for _, age_sum in reference)
                    plan = plan_schedule(contacts, neighbors, p)
                    assert (plan.survival, -plan.assignment_age_sum) == optimum
                    assert plan.A_min == minimum_age
                    assert plan.A_min_assignment is not None
                    age_assignment = tuple(plan.A_min_assignment[v] for v in plan.bulk)
                    assert independent_score(age_assignment, contacts, p)[1] == minimum_age
                    assert (1 - (1 - p) ** minimum_age) / 2 <= plan.error
                    assert plan.error <= min(Fraction(1), p * minimum_age / 2)
                    check_legal_schedule(plan, neighbors)
                    probability_cases += 1
    return {"scope": "Every ordered nonempty neighborhood tuple in the stated finite boxes",
            "contact_count_to_maximum_bulk": {"1": 4, "2": 4, "3": 3},
            "incidence_cases": incidence_cases,
            "probability_cases": probability_cases,
            "enumerated_reference_assignments": assignments,
            "p_values": [str(p) for p in PROBABILITIES],
            "status": "passed"}


def check_closed_families() -> dict:
    star_cases, dense_cases = 0, 0
    examples = []
    for bulk_count in range(25):
        contacts = ("s",)
        neighbors = {f"b{i}": ("s",) for i in range(bulk_count)}
        for p in PROBABILITIES:
            plan = plan_schedule(contacts, neighbors, p)
            expected = Fraction(1)
            for age in range(1, bulk_count + 1):
                expected *= (1 + (1 - p) ** age) / 2
            assert plan.survival == expected
            assert plan.A_min == bulk_count * (bulk_count + 1) // 2
            check_legal_schedule(plan, neighbors)
            star_cases += 1
        if bulk_count in (1, 3, 8):
            example = plan_schedule(contacts, neighbors, "1/100")
            examples.append({"family": "one-contact star", "bulk": bulk_count,
                             "M_distance_sum": bulk_count,
                             "A_min": example.A_min,
                             "p": "1/100", "exact_error": str(example.error),
                             "error_decimal": float(example.error)})
    for contact_count in range(1, 6):
        contacts = tuple(f"s{i}" for i in range(contact_count))
        for bulk_count in range(11):
            neighbors = {f"b{i}": contacts for i in range(bulk_count)}
            quotient, remainder = divmod(bulk_count, contact_count)
            for p in PROBABILITIES:
                expected = Fraction(1)
                for age in range(1, quotient + 1):
                    expected *= ((1 + (1 - p) ** age) / 2) ** contact_count
                expected *= ((1 + (1 - p) ** (quotient + 1)) / 2) ** remainder
                plan = plan_schedule(contacts, neighbors, p)
                assert plan.survival == expected
                assert plan.A_min == (contact_count * quotient * (quotient + 1) // 2
                                      + remainder * (quotient + 1))
                # Secondary age objective resolves p=0 and p=1 ties as well.
                assert sorted(plan.loads.values()) == sorted(
                    [quotient + 1] * remainder + [quotient] * (contact_count - remainder))
                check_legal_schedule(plan, neighbors)
                dense_cases += 1
    return {"star_bulk_range": [0, 24], "star_probability_cases": star_cases,
            "complete_bipartite_contact_range": [1, 5],
            "complete_bipartite_bulk_range": [0, 10],
            "complete_bipartite_probability_cases": dense_cases,
            "examples": examples, "status": "passed"}


def check_validation_and_rationals() -> dict:
    rejected = 0
    bad_inputs = [([], {}, "1/2"), (["s", "s"], {}, "1/2"),
                  (["s"], {"s": ["s"]}, "1/2"),
                  (["s"], {"b": []}, "1/2"),
                  (["s"], {"b": ["unknown"]}, "1/2"),
                  (["s"], {"b": "s"}, "1/2"),
                  (["s"], {}, "-1/2"), (["s"], {}, "3/2"),
                  (["s"], {}, 0.1), (["s"], {}, True)]
    for contacts, neighbors, p in bad_inputs:
        try:
            plan_schedule(contacts, neighbors, p)
        except (ValueError, TypeError):
            rejected += 1
        else:
            raise AssertionError((contacts, neighbors, p))
    rational_cases = 0
    contacts = ("s0", "s1", "s2")
    neighbors = {f"b{i}": contacts[:1 + i % 3] for i in range(10)}
    maximum_numerator_bits, maximum_denominator_bits = 0, 0
    for p in (Fraction(1, 10**30), 1 - Fraction(1, 10**30), Fraction("0.125")):
        plan = plan_schedule(contacts, neighbors, p)
        assert isinstance(plan.survival, Fraction) and isinstance(plan.error, Fraction)
        assert Fraction(plan.to_dict()["target_population"]) == plan.survival
        assert Fraction(plan.to_dict()["half_diamond_error"]) == plan.error
        check_legal_schedule(plan, neighbors)
        maximum_numerator_bits = max(maximum_numerator_bits, plan.survival.numerator.bit_length())
        maximum_denominator_bits = max(maximum_denominator_bits, plan.survival.denominator.bit_length())
        rational_cases += 1
    duplicate = plan_schedule(["s"], {"b": ["s", "s"]}, "1/3", include_A=False)
    assert duplicate.A_min is None and duplicate.survival == Fraction(5, 6)
    return {"invalid_inputs_rejected": rejected,
            "large_denominator_rational_cases": rational_cases,
            "maximum_result_numerator_bits": maximum_numerator_bits,
            "maximum_result_denominator_bits": maximum_denominator_bits,
            "duplicate_neighbor_normalization": "passed",
            "optional_A_omission": "passed", "status": "passed"}


def channel_configurations():
    for size in (2, 3, 4):
        yield f"star-{size}", size, (0,), {j: (0,) for j in range(1, size)}
    yield "two-contacts-shared-leaf", 3, (0, 1), {2: (0, 1)}
    yield "two-contacts-irregular", 4, (0, 1), {2: (0,), 3: (0, 1)}
    yield "two-contacts-complete", 4, (0, 1), {2: (0, 1), 3: (0, 1)}
    yield "all-contacts", 2, (0, 1), {}


def named_plan(contacts, neighbors, p):
    return plan_schedule(tuple(map(str, contacts)),
                         {str(v): tuple(map(str, ns)) for v, ns in neighbors.items()}, p)


def run_schedule(rho, plan, data_size):
    total = 2 * data_size
    for layer in plan.layers:
        for a, b in layer:
            rho = verify.swap_density(rho, total, int(a), int(b))
        for site in range(data_size):
            rho = verify.depolarize(rho, total, site, float(plan.p))
        for contact in plan.contacts:
            rho = verify.local_replacement(rho, total, int(contact))
    return rho


def replacement_state(plan, size):
    sigma = np.ones((1, 1), complex)
    for site in range(size):
        retention = (1 - float(plan.p)) ** plan.terminal_ages[str(site)]
        sigma = np.kron(sigma, np.diag([(1 + retention) / 2, (1 - retention) / 2]))
    return sigma


def check_reference_channels(rng) -> dict:
    cases, arbitrary_reference_cases = [], 0
    maximum_choi, maximum_arbitrary, maximum_error_residual = 0.0, 0.0, 0.0
    for name, size, contacts, neighbors in channel_configurations():
        dimension = 1 << size
        phi = np.eye(dimension, dtype=complex).reshape(-1) / np.sqrt(dimension)
        initial = np.outer(phi, phi.conj())
        for p in (Fraction(0), Fraction(1, 7), Fraction(1, 2), Fraction(1)):
            plan = named_plan(contacts, neighbors, p)
            actual = run_schedule(initial.copy(), plan, size)
            sigma = replacement_state(plan, size)
            expected = np.kron(sigma, np.eye(dimension) / dimension)
            discrepancy = float(np.linalg.norm(actual - expected))
            maximum_choi = max(maximum_choi, discrepancy)
            assert discrepancy < TOL
            target = np.zeros_like(sigma)
            target[0, 0] = 1
            delta = actual - np.kron(target, np.eye(dimension) / dimension)
            choi_trace_distance = float(np.abs(np.linalg.eigvalsh(delta)).sum() / 2)
            residual = abs(choi_trace_distance - float(plan.error))
            maximum_error_residual = max(maximum_error_residual, residual)
            assert residual < TOL
            cases.append({"configuration": name, "n": size, "p": str(p),
                          "depth": plan.depth, "exact_error": str(plan.error),
                          "choi_frobenius_error": discrepancy,
                          "choi_trace_error_residual": residual})
            # One arbitrary pure, entangled input supplements the complete Choi test.
            if p == Fraction(1, 7):
                vector = rng.normal(size=dimension**2) + 1j * rng.normal(size=dimension**2)
                vector /= np.linalg.norm(vector)
                rho = np.outer(vector, vector.conj())
                reference = np.trace(rho.reshape(dimension, dimension, dimension, dimension),
                                     axis1=0, axis2=2)
                actual_random = run_schedule(rho, plan, size)
                discrepancy_random = float(np.linalg.norm(actual_random - np.kron(sigma, reference)))
                maximum_arbitrary = max(maximum_arbitrary, discrepancy_random)
                assert discrepancy_random < TOL
                arbitrary_reference_cases += 1
    return {"scope": "Complete normalized Choi states plus arbitrary entangled pure inputs; all physical data outputs retained",
            "cases": cases, "choi_cases": len(cases),
            "arbitrary_entangled_input_cases": arbitrary_reference_cases,
            "maximum_choi_frobenius_error": maximum_choi,
            "maximum_arbitrary_input_frobenius_error": maximum_arbitrary,
            "maximum_choi_trace_error_residual": maximum_error_residual,
            "diamond_statement": "Exact replacement-channel diamond formula is analytical; these finite identities support it",
            "status": "passed"}


def random_joint_contact_map(rng, contacts, size, rank=3):
    dimension = 1 << len(contacts)
    matrix = (rng.normal(size=(rank * dimension, dimension))
              + 1j * rng.normal(size=(rank * dimension, dimension)))
    isometry, _ = np.linalg.qr(matrix)
    return [verify.embed(isometry[k * dimension:(k + 1) * dimension], tuple(contacts), size)
            for k in range(rank)]


def check_sampled_controls(rng) -> dict:
    count, max_population_violation, max_terminal_violation = 0, -1.0, -1.0
    max_trace_residual, minimum_eigenvalue = 0.0, 1.0
    configurations = list(channel_configurations())[:-1]
    for name, size, contacts, neighbors in configurations:
        edges = [(s, v) for v, ns in neighbors.items() for s in ns]
        edges += list(itertools.combinations(contacts, 2))
        for rounds in range(6):
            for p in (Fraction(0), Fraction(1, 7), Fraction(1, 2), Fraction(1)):
                plan = named_plan(contacts, neighbors, p)
                for sample in range(4):
                    rho = np.eye(1 << size, dtype=complex) / (1 << size)
                    last_touch = {}
                    for step in range(1, rounds + 1):
                        unitary = np.eye(1 << size, dtype=complex)
                        used = set()
                        for index in rng.permutation(len(edges)):
                            a, b = edges[index]
                            if a in used or b in used or rng.random() < 0.3:
                                continue
                            used.update((a, b))
                            unitary = verify.embed(verify.haar(4, rng), (a, b), size) @ unitary
                            for site in (a, b):
                                if site in neighbors:
                                    last_touch[site] = step
                        for site in set(range(size)) - used:
                            unitary = verify.embed(verify.haar(2, rng), (site,), size) @ unitary
                        rho = unitary @ rho @ unitary.conj().T
                        for site in range(size):
                            rho = verify.depolarize(rho, size, site, float(p))
                        if sample % 2 == 0:
                            for contact in contacts:
                                rho = verify.local_replacement(rho, size, contact)
                        else:
                            rho = verify.apply_cptp(rho, random_joint_contact_map(
                                rng, contacts, size))
                    population = float(rho[0, 0].real)
                    terminal_bound = Fraction(1, 1 << (len(neighbors) - len(last_touch)))
                    for site, last in last_touch.items():
                        terminal_bound *= (1 + (1 - p) ** (rounds - last + 1)) / 2
                    assert terminal_bound <= plan.survival
                    max_population_violation = max(max_population_violation,
                                                    population - float(plan.survival))
                    max_terminal_violation = max(max_terminal_violation,
                                                  population - float(terminal_bound))
                    assert population <= float(terminal_bound) + TOL
                    eigenvalues = np.linalg.eigvalsh((rho + rho.conj().T) / 2)
                    minimum_eigenvalue = min(minimum_eigenvalue, float(eigenvalues[0]))
                    max_trace_residual = max(max_trace_residual, float(abs(np.trace(rho) - 1)))
                    assert eigenvalues[0] > -TOL and abs(np.trace(rho) - 1) < TOL
                    count += 1
    return {"scope": "Maximally mixed input; sampled legal Haar layers, one-qubit gates, resets and arbitrary joint contact CPTP maps; depths include zero",
            "cases": count, "depth_range": [0, 5],
            "maximum_population_minus_optimal_bound": max_population_violation,
            "maximum_population_minus_last_touch_bound": max_terminal_violation,
            "maximum_trace_residual": max_trace_residual,
            "minimum_output_eigenvalue": minimum_eigenvalue,
            "status": "passed"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("contact_throughput_results.json"))
    args = parser.parse_args()
    rng = np.random.default_rng(SEED)
    result = {"status": "passed",
              "generated_at_utc": datetime.now(timezone.utc).isoformat(),
              "python_version": platform.python_version(),
              "numpy_version": np.__version__, "seed": SEED,
              "absolute_tolerance": TOL,
              "model": "Independent bulk; nonempty contact neighbors; SWAP matching then iid D_p then contact resets",
              "exhaustive_assignments": check_exhaustive_assignments(),
              "closed_families": check_closed_families(),
              "input_and_exact_arithmetic": check_validation_and_rationals(),
              "reference_channels": check_reference_channels(rng),
              "sampled_quantum_controls": check_sampled_controls(rng),
              "limits": ["Finite enumeration is a test oracle, not the production solver.",
                         "Random controls are sampled; the all-circuit converse is analytical.",
                         "The exact diamond error is justified by the proved replacement-channel form.",
                         "No bulk-bulk gates, protected workspace, observed-noise feedback, heat, or hardware time model is tested."]}
    folder = Path(__file__).resolve().parent
    result["source_sha256"] = {name: hashlib.sha256((folder / name).read_bytes()).hexdigest()
                               for name in ("contact_schedule.py", "contact_throughput_checks.py", "verify.py")}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": "passed", "output": str(args.output),
                      "exact_probability_cases": result["exhaustive_assignments"]["probability_cases"],
                      "reference_choi_cases": result["reference_channels"]["choi_cases"],
                      "sampled_control_cases": result["sampled_quantum_controls"]["cases"],
                      "maximum_choi_error": result["reference_channels"]["maximum_choi_frobenius_error"]}, indent=2))


if __name__ == "__main__":
    main()
