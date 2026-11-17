#!/usr/bin/env python3
"""Exact contact-cover assignment and legal cooling schedule.

The bulk must be an independent set and every bulk vertex must have a contact
neighbor. Contact-contact edges do not affect this planner. A round is a
matching of SWAPs, iid depolarization, then independent perfect contact resets.

Python example::

    plan = plan_schedule(["s0", "s1"],
                         {"a": ["s0"], "b": ["s0", "s1"]}, "1/20")
    assert isinstance(plan.survival, Fraction)

CLI example (from the repository root)::

    python verification/contact_schedule.py --p 1/20 \
      --incidence '{"contacts":["s0","s1"],"neighbors":{"a":["s0"],"b":["s0","s1"]}}'

Use --input PATH instead of --incidence for a JSON file. --output PATH writes
the same JSON that would otherwise be printed. Rational numbers are serialized
as exact strings, never optimized through floating-point logarithms.

The algorithm is successive maximum-product augmenting paths in a bipartite
flow network with expanded unit-capacity contact slots. Marginal factors
h_p(j)=(1+(1-p)**j)/2 decrease with j, so occupied slots can be prefixes.
Bellman-Ford uses exact Fraction products and a secondary exact objective to
minimize the sum of terminal ages among equal primary optima. It does not
enumerate assignments. With b bulk vertices, s contacts, and e incidence
edges, the network has O(b+s) vertices and O(e+s*b+b) arcs; there are b
augmentations, each using O(V*E) rational comparisons. Stored path copies add
at most a factor V to this elementary implementation. Numerator/denominator
bit lengths grow polynomially in b, s and the input rational bit length.
This is a polynomial exact algorithm, not a strongly polynomial bit-cost or
large-instance performance claim. The optional integer-age optimum is solved
separately; it must not be confused with the finite-p primary objective.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Mapping, Sequence


Weight = tuple[Fraction, Fraction]
ONE: Weight = (Fraction(1), Fraction(1))


@dataclass
class _Arc:
    to: int
    reverse: int
    capacity: int
    weight: Weight


def _multiply(left: Weight, right: Weight) -> Weight:
    return left[0] * right[0], left[1] * right[1]


def _add_arc(graph: list[list[_Arc]], source: int, target: int,
             weight: Weight = ONE) -> _Arc:
    forward = _Arc(target, len(graph[target]), 1, weight)
    reverse = _Arc(source, len(graph[source]), 0,
                   (1 / weight[0], 1 / weight[1]))
    graph[source].append(forward)
    graph[target].append(reverse)
    return forward


def _maximum_product_path(graph: list[list[_Arc]], source: int, sink: int
                          ) -> tuple[list[tuple[int, int]], Weight, int]:
    """Bellman-Ford in the positive-rational multiplicative ordered group.

    Before each augmentation the current fixed-value flow is optimal, hence
    its residual graph has no cycle of product greater than one. The usual
    shortest-path induction therefore applies with products and reciprocals.
    Synchronous rounds retain paths explicitly, avoiding predecessor ambiguity
    at zero-cost cycles. Strict improvements give deterministic tie handling.
    """
    count = len(graph)
    distance: list[Weight | None] = [None] * count
    paths: list[list[tuple[int, int]] | None] = [None] * count
    distance[source], paths[source] = ONE, []
    relaxations = 0
    for _ in range(count - 1):
        next_distance, next_paths = distance.copy(), paths.copy()
        changed = False
        for u, arcs in enumerate(graph):
            if distance[u] is None:
                continue
            for index, arc in enumerate(arcs):
                if not arc.capacity:
                    continue
                candidate = _multiply(distance[u], arc.weight)
                relaxations += 1
                if (next_distance[arc.to] is None
                        or candidate > next_distance[arc.to]):
                    next_distance[arc.to] = candidate
                    next_paths[arc.to] = paths[u] + [(u, index)]  # type: ignore[operator]
                    changed = True
        distance, paths = next_distance, next_paths
        if not changed:
            break
    # An improving residual cycle would invalidate the fixed-value optimum.
    for u, arcs in enumerate(graph):
        if distance[u] is not None:
            for arc in arcs:
                if arc.capacity and (distance[arc.to] is None
                        or _multiply(distance[u], arc.weight) > distance[arc.to]):
                    raise RuntimeError("Improving residual cycle: solver invariant failed")
    if paths[sink] is None or distance[sink] is None:
        raise RuntimeError("No complete contact assignment exists")
    path = paths[sink]
    vertices = [source] + [graph[u][i].to for u, i in path]
    if len(set(vertices)) != len(vertices):
        raise RuntimeError("Non-simple optimal augmenting path")
    return path, distance[sink], relaxations


def _assignment(contacts: tuple[str, ...], bulk: tuple[str, ...],
                neighbors: dict[str, tuple[str, ...]], p: Fraction,
                age_only: bool = False) -> tuple[dict[str, str], dict]:
    b, s = len(bulk), len(contacts)
    source, bulk_start, contact_start = 0, 1, 1 + b
    sink = 1 + b + s
    graph: list[list[_Arc]] = [[] for _ in range(sink + 1)]
    contact_indices = {name: contact_start + i for i, name in enumerate(contacts)}
    assignment_arcs: dict[tuple[str, str], _Arc] = {}
    for index, vertex in enumerate(bulk):
        node = bulk_start + index
        _add_arc(graph, source, node)
        for contact in neighbors[vertex]:
            assignment_arcs[vertex, contact] = _add_arc(
                graph, node, contact_indices[contact])
    for contact in contacts:
        for age in range(1, b + 1):
            factor = Fraction(1, 1 << age)
            weight = ((factor, Fraction(1)) if age_only else
                      (h(p, age), factor))
            _add_arc(graph, contact_indices[contact], sink, weight)
    score, relaxations = ONE, 0
    for _ in bulk:
        path, gain, work = _maximum_product_path(graph, source, sink)
        relaxations += work
        for u, index in path:
            arc = graph[u][index]
            arc.capacity -= 1
            graph[arc.to][arc.reverse].capacity += 1
        score = _multiply(score, gain)
    chosen = {}
    for vertex in bulk:
        used = [contact for contact in neighbors[vertex]
                if assignment_arcs[vertex, contact].capacity == 0]
        if len(used) != 1:
            raise RuntimeError("A bulk vertex lacks a unique assigned contact")
        chosen[vertex] = used[0]
    loads = {contact: sum(chosen[v] == contact for v in bulk)
             for contact in contacts}
    age_sum = sum(load * (load + 1) // 2 for load in loads.values())
    prefix_product = Fraction(1)
    for load in loads.values():
        for age in range(1, load + 1):
            prefix_product *= h(p, age)
    expected = ((Fraction(1, 1 << age_sum), Fraction(1)) if age_only else
                (prefix_product, Fraction(1, 1 << age_sum)))
    if score != expected:
        raise RuntimeError("Flow score disagrees with compressed contact slots")
    return chosen, {"vertices": len(graph),
                    "forward_arcs": sum(len(x) for x in graph) // 2,
                    "augmentations": b,
                    "rational_path_relaxations": relaxations}


def h(p: Fraction, age: int) -> Fraction:
    """Zero-state population after `age` depolarizing layers from pure zero."""
    if age < 0:
        raise ValueError("A terminal age must be nonnegative")
    return (1 + (1 - p) ** age) / 2


def _probability(p: Fraction | str | int) -> Fraction:
    if isinstance(p, bool) or not isinstance(p, (Fraction, str, int)):
        raise TypeError("p must be an exact Fraction, integer, or rational string")
    value = Fraction(p)
    if not 0 <= value <= 1:
        raise ValueError("p must lie in [0,1]")
    return value


@dataclass
class ContactSchedule:
    contacts: tuple[str, ...]
    bulk: tuple[str, ...]
    p: Fraction
    assignment: dict[str, str]
    loads: dict[str, int]
    layers: tuple[tuple[tuple[str, str], ...], ...]
    terminal_ages: dict[str, int]
    survival: Fraction
    error: Fraction
    assignment_age_sum: int
    A_min: int | None
    A_min_assignment: dict[str, str] | None
    solver: dict

    @property
    def depth(self) -> int:
        return len(self.layers)

    def to_dict(self) -> dict:
        result = {
            "contacts": list(self.contacts), "bulk": list(self.bulk),
            "p": str(self.p), "assignment": self.assignment,
            "loads": self.loads, "depth": self.depth,
            "round_order": "SWAP matching; iid D_p on every site; reset every contact",
            "layers": [{"round": index + 1,
                        "swaps": [list(edge) for edge in layer],
                        "reset_contacts": list(self.contacts)}
                       for index, layer in enumerate(self.layers)],
            "terminal_ages": self.terminal_ages,
            "target_population": str(self.survival),
            "half_diamond_error": str(self.error),
            "assignment_age_sum": self.assignment_age_sum,
            "solver": self.solver,
        }
        if self.A_min is not None:
            result.update({"A_min": self.A_min,
                           "A_min_assignment": self.A_min_assignment,
                           "A_lower_error_bound": str((1 - (1 - self.p) ** self.A_min) / 2),
                           "A_upper_error_bound": str(min(Fraction(1), self.p * self.A_min / 2))})
        return result


def plan_schedule(contacts: Sequence[str], neighbors: Mapping[str, Iterable[str]],
                  p: Fraction | str | int, *, include_A: bool = True
                  ) -> ContactSchedule:
    """Return the optimal exact assignment and its attaining SWAP schedule.

    Vertex names must be distinct nonempty strings; contact and bulk names
    cannot overlap. Duplicate entries in a neighbor list are ignored. The
    returned error is a Fraction. An initial empty SWAP layer resets contacts;
    the total depth is 1+max(loads). Every bulk input visits a reset contact
    exactly once. This constructs the theorem's replacement channel, rather
    than numerically estimating a diamond norm.
    """
    contact_tuple = tuple(contacts)
    if (not contact_tuple or any(not isinstance(s, str) or not s for s in contact_tuple)
            or len(set(contact_tuple)) != len(contact_tuple)):
        raise ValueError("contacts must be a nonempty list of distinct nonempty strings")
    if not isinstance(neighbors, Mapping):
        raise TypeError("neighbors must map each bulk vertex to its contact neighbors")
    bulk = tuple(neighbors)
    if any(not isinstance(v, str) or not v for v in bulk):
        raise ValueError("bulk vertex names must be nonempty strings")
    if set(contact_tuple) & set(bulk):
        raise ValueError("bulk and contact names must be disjoint")
    allowed = set(contact_tuple)
    normalized = {}
    for vertex, entries in neighbors.items():
        if isinstance(entries, (str, bytes)):
            raise TypeError("each neighbor list must be an iterable of contact names")
        listed = tuple(entries)
        if any(not isinstance(s, str) or s not in allowed for s in listed):
            raise ValueError("every listed neighbor must be a named contact")
        # Canonical contact order makes input list duplication/order irrelevant.
        values = set(listed)
        normalized[vertex] = tuple(s for s in contact_tuple if s in values)
        if not normalized[vertex]:
            raise ValueError("every bulk vertex must have at least one contact neighbor")
    probability = _probability(p)
    chosen, statistics = _assignment(contact_tuple, bulk, normalized, probability)
    loads = {s: sum(chosen[v] == s for v in bulk) for s in contact_tuple}
    depth = 1 + max(loads.values(), default=0)
    layers: list[list[tuple[str, str]]] = [[] for _ in range(depth)]
    ages = {s: 0 for s in contact_tuple}
    survival = Fraction(1)
    for contact in contact_tuple:
        assigned = [v for v in bulk if chosen[v] == contact]
        for age, vertex in enumerate(assigned, start=1):
            layers[depth - age].append((contact, vertex))
            ages[vertex] = age
            survival *= h(probability, age)
    actual_A = sum(load * (load + 1) // 2 for load in loads.values())
    A_min, age_assignment = None, None
    if include_A:
        age_assignment, age_statistics = _assignment(
            contact_tuple, bulk, normalized, probability, age_only=True)
        age_loads = [sum(age_assignment[v] == s for v in bulk) for s in contact_tuple]
        A_min = sum(load * (load + 1) // 2 for load in age_loads)
        statistics = {"primary": statistics, "minimum_age": age_statistics}
    else:
        statistics = {"primary": statistics}
    return ContactSchedule(contact_tuple, bulk, probability, chosen, loads,
                           tuple(tuple(layer) for layer in layers), ages,
                           survival, 1 - survival, actual_A, A_min,
                           age_assignment, statistics)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--input", type=Path, help="JSON file with contacts and neighbors")
    source.add_argument("--incidence", help="inline JSON with contacts and neighbors")
    parser.add_argument("--p", required=True, help="exact rational, e.g. 1/20 or 0.05")
    parser.add_argument("--without-A", action="store_true", help="skip separate minimum-age solve")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = json.loads(args.input.read_text() if args.input else args.incidence)
    plan = plan_schedule(data["contacts"], data["neighbors"], args.p,
                         include_A=not args.without_A)
    serialized = json.dumps(plan.to_dict(), indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized)
    else:
        print(serialized, end="")


if __name__ == "__main__":
    main()
