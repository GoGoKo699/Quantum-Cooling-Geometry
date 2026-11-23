#!/usr/bin/env python3
"""Finite single-contact cooling checks, using only the Python standard library.

From the repository root: python verification/check_single_contact.py

The exhaustive cases check carrier ages under every tiny SWAP schedule, a
reversible sparse-lane circuit, and noise during the second contact transport.
The written proofs establish the uniform bounds and the full-channel claims.
"""

from fractions import Fraction
from itertools import combinations, product
from math import prod


def graph_matchings(vertices, gateway, contact):
    """Enumerate disjoint bulk-clique edges and the single contact edge."""
    if not vertices:
        yield ()
        return
    first, *rest = vertices
    yield from graph_matchings(rest, gateway, contact)
    for other in rest:
        if contact in (first, other) and gateway not in (first, other):
            continue
        remaining = [vertex for vertex in rest if vertex != other]
        for matching in graph_matchings(remaining, gateway, contact):
            yield ((first, other), *matching)


def age_step(ages, matching):
    moved = list(ages)
    for first, second in matching:
        moved[first], moved[second] = ages[second], ages[first]
    return tuple(age + 1 if age >= 0 else -1 for age in moved[:-1]) + (0,)


def refresh_layers(bulk):
    yield ()
    for leaf in range(1, bulk):
        yield ((bulk, 0),)
        yield ((0, leaf),)
    yield ((bulk, 0),)


def check_routing():
    states_checked = 0
    for bulk in range(1, 5):
        odd_ages = tuple(range(1, 2 * bulk, 2))
        reachable = {(-1,) * (bulk + 1)}
        seen_optimum = False
        matchings = tuple(graph_matchings(list(range(bulk + 1)), 0, bulk))
        horizon = 2 * bulk + 2
        for depth in range(horizon + 1):
            for ages in reachable:
                finite_ages = sorted(age for age in ages[:-1] if age >= 0)
                assert all(actual >= required
                           for actual, required in zip(finite_ages, odd_ages))
                assert ages[-1] == (0 if depth else -1)
                states_checked += 1
                if depth == 2 * bulk and tuple(finite_ages) == odd_ages:
                    seen_optimum = True
            reachable = {age_step(ages, layer)
                         for ages in reachable for layer in matchings}
        assert seen_optimum

    for bulk in range(1, 65):
        ages = (-1,) * (bulk + 1)
        layers = tuple(refresh_layers(bulk))
        assert len(layers) == 2 * bulk
        for layer in layers:
            ages = age_step(ages, layer)
        assert sorted(ages) == [0, *range(1, 2 * bulk, 2)]
        assert sum(ages) == bulk**2
        for p in (Fraction(0), Fraction(1, 17), Fraction(1)):
            actual = prod((1 + (1 - p)**age) / 2 for age in ages)
            expected = prod((1 + (1 - p)**(2 * j - 1)) / 2
                            for j in range(1, bulk + 1))
            assert actual == expected
    return states_checked


class Scratch:
    """Allocate wire addresses and retain a count when addresses are reused."""

    def __init__(self, first):
        self.next_wire = first
        self.peak = first

    def take(self, count=1):
        requested = tuple(range(self.next_wire, self.next_wire + count))
        self.next_wire += count
        self.peak = max(self.peak, self.next_wire)
        return requested


def add_layer(circuit, gates):
    layer = tuple(gates)
    if not layer:
        return
    active = [wire for gate in layer for wire in gate]
    assert len(active) == len(set(active)), "a matching layer reuses a wire"
    assert all(len(gate) in (2, 3) for gate in layer)
    circuit.append(layer)


def fanout_layered(circuit, groups):
    """All groups are disjoint, and each starts with one live output bit."""
    copies = 1
    while any(len(group) > copies for group in groups):
        add_layer(circuit, ((group[index - copies], group[index])
                            for group in groups
                            for index in range(copies, min(2 * copies, len(group)))))
        copies *= 2


def apply_circuit(circuit, bits):
    for layer in circuit:
        for *controls, target in layer:
            bits[target] ^= all(bits[wire] for wire in controls)


def encode_lanes(lanes, lane_size):
    """Checkable schedule for compute-copy-uncompute and lane erasure."""
    height = (lane_size - 1).bit_length()
    root_size = 2 * height + 1
    permanent = lanes * (lane_size + root_size)
    allocator = Scratch(permanent)
    circuit = []
    for lane in range(lanes):
        data = tuple(range(lane * lane_size, (lane + 1) * lane_size))
        root_start = lanes * lane_size + lane * root_size
        occupied = root_start
        first = tuple(range(root_start + 1, root_start + height + 1))
        last = tuple(range(root_start + height + 1, root_start + root_size))
        allocator.next_wire = permanent
        data = (*data, *allocator.take((1 << height) - lane_size))
        compute_and_erase_lane(circuit, allocator, data, occupied, first, last)
    return circuit, allocator.peak, permanent


def compute_and_erase_lane(circuit, allocator, data, occupied, first, last):
    height = len(first)
    scratch_start = allocator.next_wire
    if height == 0:
        add_layer(circuit, ((data[0], occupied),))
        add_layer(circuit, ((occupied, data[0]),))
        return

    build = []
    flags = [data]
    for _ in range(height):
        children = tuple(zip(flags[-1][::2], flags[-1][1::2]))
        parents = allocator.take(len(children))
        add_layer(build, ((left, out) for (left, _), out in zip(children, parents)))
        add_layer(build, ((right, out) for (_, right), out in zip(children, parents)))
        add_layer(build, ((left, right, out)
                          for (left, right), out in zip(children, parents)))
        flags.append(parents)

    flag_copies = [() for _ in range(height + 1)]
    for level in range(1, height + 1):
        flag_copies[level] = tuple((flag, *allocator.take(max(0, level - 2)))
                                   for flag in flags[level - 1])
    fanout_layered(build, tuple(group for level in flag_copies for group in level))

    low = [()] * len(data)
    high = [()] * len(data)
    for level in range(1, height + 1):
        pairs = tuple(zip(flag_copies[level][::2], flag_copies[level][1::2]))
        low, steps = index_layer(allocator, level, pairs, low, last_index=False)
        build.extend(steps)
        high, steps = index_layer(allocator, level, pairs, high, last_index=True)
        build.extend(steps)

    circuit.extend(build)
    add_layer(circuit, ((flags[-1][0], occupied), *zip(low[0], first), *zip(high[0], last)))
    circuit.extend(reversed(build))

    allocator.next_wire = scratch_start
    first_flag, last_flag = allocator.take(2)
    add_layer(circuit, ((occupied, first_flag),))
    add_layer(circuit, ((occupied, last_flag),))
    decode_first, first_mask = unary_decoder(allocator, first_flag, first)
    decode_last, last_mask = unary_decoder(allocator, last_flag, last)
    circuit.extend(decode_first)
    circuit.extend(decode_last)
    add_layer(circuit, zip(first_mask, data))
    add_layer(circuit, zip(last_mask, data))
    add_layer(circuit, zip(first_mask, last_mask, data))
    circuit.extend(reversed(decode_last))
    circuit.extend(reversed(decode_first))
    add_layer(circuit, ((occupied, last_flag),))
    add_layer(circuit, ((occupied, first_flag),))


def index_layer(allocator, level, flag_pairs, previous, last_index):
    current = [allocator.take(level) for _ in flag_pairs]
    steps = []
    add_layer(steps, ((right[0], output[-1])
                      for (_, right), output in zip(flag_pairs, current)))
    if not last_index:
        add_layer(steps, ((left[0], right[0], output[-1])
                          for (left, right), output in zip(flag_pairs, current)))

    # The chosen child already has index zero when its flag is zero.
    # A low output bit is chosen XOR (default AND NOT select).
    defaults = previous[::2] if last_index else previous[1::2]
    chosen = previous[1::2] if last_index else previous[::2]
    selectors = [pair[int(last_index)] for pair in flag_pairs]
    for child in (chosen, defaults):
        add_layer(steps, (operation for row, output in zip(child, current)
                          for operation in zip(row, output[:-1])))
    add_layer(steps, (operation for copies, row, output in zip(selectors, defaults, current)
                      for operation in zip(copies, row, output[:-1])))
    return current, steps


def unary_decoder(allocator, occupied, index):
    circuit = []
    copies = tuple((digit, *allocator.take((1 << level) - 1))
                   for level, digit in enumerate(reversed(index)))
    fanout_layered(circuit, copies)
    flags = (occupied,)
    for digits in copies:
        children = allocator.take(2 * len(flags))
        left, right = children[::2], children[1::2]
        add_layer(circuit, zip(flags, left))
        add_layer(circuit, zip(flags, digits, right))
        add_layer(circuit, zip(right, left))
        flags = children
    return circuit, flags


def read_integer(bits, wires):
    return sum(bits[wire] << index for index, wire in enumerate(wires))


def check_sparse_lanes():
    patterns = 0
    for size in (1, 2, 3, 4, 5, 8, 9, 16, 17, 32, 33, 64, 65, 128):
        height = (size - 1).bit_length()
        padded_size = 1 << height
        circuit, peak, permanent = encode_lanes(17, size)
        assert peak <= 256 * size
        assert permanent == 17 * size + 17 * (2 * height + 1)
        assert peak - permanent < 16 * padded_size
        assert all(wire < peak for layer in circuit for gate in layer for wire in gate)
        # Disjoint two-qubit gates cost one layer, and a Toffoli uses five
        # serial two-qubit controlled-V/CNOT gates on its own three sites.
        physical_depth = sum(5 if any(len(gate) == 3 for gate in layer) else 1
                             for layer in circuit)
        assert physical_depth <= 17 * (145 * height + 5)

        single, peak, _ = encode_lanes(1, size)
        samples = [()]
        samples.extend((index,) for index in range(size))
        if size <= 32:
            samples.extend(combinations(range(size), 2))
        else:
            samples.extend((index, size - 1) for index in range(size - 1))
            samples.extend((index, index + 1) for index in range(size - 1))
        for sites in samples:
            bits = [0] * peak
            for site in sites:
                bits[site] = 1
            original = bits.copy()
            apply_circuit(single, bits)
            assert bits[size] == bool(sites)
            first = range(size + 1, size + 1 + height)
            last = range(first.stop, first.stop + height)
            assert read_integer(bits, first) == (min(sites) if sites else 0)
            assert read_integer(bits, last) == (max(sites) if sites else 0)
            assert not any(bits[:size]) and not any(bits[size + 1 + 2 * height:])
            apply_circuit(reversed(single), bits)
            assert bits == original
            patterns += 1
    return patterns


def microblock_permutation(size):
    """Complete the injector on 0-, 1- and 2-excitation inputs by paths."""
    pairs = combinations(range(size), 2)
    domain = [0, *(1 << i for i in range(size)),
              *((1 << i) | (1 << j) for i, j in pairs)]
    image = set(range(len(domain)))
    permutation = dict(zip(domain, range(len(domain))))
    for path_start in set(domain) - image:
        path_end = path_start
        while path_end in permutation:
            path_end = permutation[path_end]
        permutation[path_end] = path_start
    assert set(permutation) == set(permutation.values())
    assert all(permutation[word] == label for label, word in enumerate(domain))
    assert max(permutation[word] for word in domain).bit_length() <= 17
    return len(domain)


def drain_layers(bulk, code_sites):
    if 0 in code_sites:
        yield (bulk, 0)
    for leaf in sorted(code_sites - {0}):
        yield (0, leaf)
        yield (bulk, 0)


def drain_trajectories(bulk, code_sites, layers):
    carriers = [(site in code_sites, ()) for site in range(bulk + 1)]
    for time, (first, second) in enumerate(layers):
        carriers[first], carriers[second] = carriers[second], carriers[first]
        carriers = [(has_code, (*slots, (time, site)))
                    for site, (has_code, slots) in enumerate(carriers)]
        carriers[bulk] = (False, ())
    return carriers


def simulate_drain_bits(bulk, code_sites, layers, fault_flags):
    bits = [int(site in code_sites) for site in range(bulk + 1)]
    for time, (first, second) in enumerate(layers):
        bits[first], bits[second] = bits[second], bits[first]
        for site in range(bulk + 1):
            bits[site] ^= fault_flags.get((time, site), 0)
        bits[bulk] = 0
    return tuple(bits)


def check_contact_drain():
    cases = 0
    flip = Fraction(1, 7)
    for bulk in range(1, 9):
        for size in range(bulk + 1):
            for subset in combinations(range(bulk), size):
                code_sites = set(subset)
                layers = tuple(drain_layers(bulk, code_sites))
                assert len(layers) == 2 * size - (0 in code_sites)
                carriers = drain_trajectories(bulk, code_sites, layers)
                assert not any(has_code for has_code, _ in carriers)
                slots = [location for _, trajectory in carriers for location in trajectory]
                assert len(set(slots)) == len(slots)
                assert all(len(trajectory) <= len(layers) for _, trajectory in carriers)
                assert simulate_drain_bits(bulk, code_sites, layers, {}) == (0,) * (bulk + 1)
                if bulk <= 3:
                    for time, site in product(range(len(layers)), range(bulk + 1)):
                        one_fault = (time, site)
                        actual = simulate_drain_bits(bulk, code_sites, layers, {one_fault: 1})
                        expected = tuple(int(one_fault in path) for _, path in carriers)
                        assert actual == expected
                    distribution = {}
                    for outcomes in product((0, 1), repeat=len(slots)):
                        weight = sum(outcomes)
                        probability = flip**weight * (1 - flip)**(len(slots) - weight)
                        observed = simulate_drain_bits(bulk, code_sites, layers,
                                                      dict(zip(slots, outcomes)))
                        distribution[observed] = distribution.get(observed, 0) + probability
                    odd = tuple((1 - (1 - 2 * flip)**len(path)) / 2 for _, path in carriers)
                    for observed in product((0, 1), repeat=bulk + 1):
                        expected = prod(p if b else 1 - p for b, p in zip(observed, odd))
                        assert distribution.get(observed, 0) == expected
                cases += 1
    return cases


if __name__ == "__main__":
    print(f"Routing age states checked: {check_routing()}")
    microblock_cases = sum(microblock_permutation(size) for size in (256, 257, 383, 511))
    print(f"Microblock code inputs checked: {microblock_cases}")
    print(f"Reversible sparse-lane inputs checked: {check_sparse_lanes()}")
    print(f"Contact drain cases checked: {check_contact_drain()}")
