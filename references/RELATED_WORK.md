# Related work and attribution

The question here is synchronized initialization of **every physical output qubit** in hardware that continues to heat while entropy can leave only through prescribed reset contacts. The model uses exact, independent single-qubit depolarizing channels after local gate layers. Its accuracy is the half-diamond distance from a pure replacement channel. It does not identify heat, work, energy density, selected-qubit polarization, or logical recovery with this global accuracy.

The source comparisons below were checked on 13 November 2026. They identify the closest mechanisms and model differences; they are not an exhaustive priority certificate.

## What the present account adds

Local circuit causality, random-Pauli representations of depolarization, and SWAP-based transport to a dissipative port are established ingredients. The addition is a finite-noise, protocol-uniform implication of their combination. A depolarization occurring too late for its forward cone to reach any reset contact survives to the final output as a unitarily conjugated maximally mixed qubit factor. This statement is proved by moving the selected conditional-expectation channel through the subsequent circuit, including disjoint nonunitary reset operations. It does not assume that arbitrary reset maps preserve the largest eigenvalue of a global state.

Counting the terminal spacetime points gives the graph quantity

```math
M(G,S)=\sum_{v\in V}d(v,S).
```

Once the required cover-radius depth has been reached, every admissible controller has error at least $`[1-(1-p)^{M(G,S)}]/2`$ for the stated pure-register reset task. A parallel SWAP conveyor attains the corresponding order on a path and on the regular geometries explicitly constructed in the science pages. No matching theorem for every graph, optimal constant, or quantum-over-classical advantage is claimed.

## Noisy algorithmic cooling

**Li, Wang, Huber, Friis, and Bakhshinezhad (2026).** [Exploring Noisy Quantum Thermodynamical Processes via the Depolarizing-Channel Approximation](https://doi.org/10.1103/wg2x-z2vm), *Physical Review Letters* **137**, 190401. The [inspected manuscript](https://arxiv.org/html/2601.16317v1) derives a global depolarizing approximation under gate-noise and approximate-design assumptions. Its Proposition 1 solves the fixed noisy two-sort algorithmic-cooling steady state. The paper already establishes that noise can make a finite machine size optimal. The distinction here is an exact local-noise converse over arbitrary prescribed local coherent controls, with all physical outputs required pure. Neither the global approximation nor that particular steady-state solution supplies the terminal-event factorization or a reset-placement distance law. The published metadata were verified; theorem-level comparison used the named manuscript version.

**Raeisi and Mosca (2015).** [Asymptotic Bound for Heat-Bath Algorithmic Cooling](https://doi.org/10.1103/PhysRevLett.114.100404), *Physical Review Letters* **114**, 100404, establishes the ideal HBAC saturation bound and its dependence on reset-system spectra. This credits the general competition between reversible entropy compression and bath resets. Its finite-temperature reset resource and cooling objective differ from ideal pure contacts competing with unavoidable spatial bulk heating. The present result is not another derivation of the HBAC limit.

## One cold contact and coherent control

**Bergholm, Wilhelm, and Schulte-Herbrüggen (2017 manuscript).** [Arbitrary n-Qubit State Transfer Implemented by Coherent Control and Simplest Switchable Local Noise](https://arxiv.org/abs/1605.06473), arXiv:1605.06473v2, Theorem 1 gives full state reachability with one switchable amplitude-damping qubit and coherent controllability when no further decoherence is present. Example 1 already cools a chain by routing qubits through that contact; its sequential benchmark counts $`n(n-1)/2`$ nearest-neighbor swaps. Appendix E studies finite examples with additional dephasing. Accordingly, neither single-port cooling nor the occurrence of a sum of transport distances is claimed as new. The new converse counts unavoidable **late heating events** for every allowed controller; the constructive schedule matches its global-error order. Target-preserving dephasing cannot be substituted for the entropy-injecting noise of the present theorem.

**Žnidarič (2015).** [Geometry of Local Quantum Dissipation and Fundamental Limits to Local Cooling](https://doi.org/10.1103/PhysRevA.91.052107), *Physical Review A* **91**, 052107 ([manuscript](https://arxiv.org/abs/1501.03453)), bounds the steady singlet fraction obtainable using a two-qubit Hamiltonian and local Lindblad dissipation. It establishes a genuine local-cooling obstruction for sufficiently entangled targets. The present obstruction occurs already for a product target and grows with the physical distance to cold contacts under bulk heating. The steady-state entangled-target bound does not imply that geometry-dependent register law.

**Beer and Burgarth (2026).** [Global Zero-Excitation State Preparation through Subsystem Cooling](https://arxiv.org/abs/2609.23960), arXiv:2609.23960, gives a zero-forcing criterion under which localized dissipation makes the vacuum globally attractive in an excitation-conserving system. This is a relevant graph-theoretic sufficient condition for cooling through a subsystem. The present theorem instead bounds accuracy when bulk noise continually injects entropy. The primary abstract was verified; the full manuscript was unavailable during this comparison, so no detailed theorem or proof equivalence is asserted.

## Refrigeration without continual fresh ancillas

**Ben-Or, Gottesman, and Hassidim (2013).** [Quantum Refrigerator](https://arxiv.org/abs/1301.1995), arXiv:1301.1995, distinguishes computation under unital, dephasing, and nonunital noise without newly supplied pure ancillas. It builds on the entropy obstruction in [Aharonov, Ben-Or, Impagliazzo, and Nisan (1996)](https://arxiv.org/abs/quant-ph/9611028), *Limitations of Noisy Reversible Computation*. These works establish that the availability of entropy-removing resources matters fundamentally. Their computation-lifetime question does not include ideal resets on a specified sparse set and simultaneous physical purity of the entire register.

**Shtanko and Sharma (2025).** [Complexity of Local Quantum Circuits under Nonunital Noise](https://doi.org/10.1103/xwz2-wfr4), *PRX Quantum* **6**, 030347, Section III, builds local noise-enabled reset gadgets and measurement-free fault-tolerant computation. Its refrigerator uses many noisy ancillas, nonunital relaxation throughout those ancillas, and entropy compression to purify one target while allowing the other qubits to remain mixed. That is a constructive way to obtain a useful subsystem, and is fully compatible with the present all-output obstruction. The distinction is the location and extent of entropy removal and which physical outputs must be pure, rather than a general prohibition on coherent error correction.

## Thermal-state preparation with resettable baths

**Lloyd and Abanin (2026).** [Quantum Thermal State Preparation for Near-Term Quantum Processors](https://doi.org/10.1103/cbrd-ssnm), *Physical Review X* **16**, 031053, uses resettable bath qubits and modulated system-bath coupling to approximately impose quantum detailed balance. Its discussion identifies device noise as a limitation and gives a perturbative noise-to-cooling estimate. It does not establish a converse over all local controllers or a sparse-contact global-purity law. Its Gibbs-state preparation objective also differs from replacement of every physical qubit by a supplied pure product state.

**Molpeceres, Lu, Cirac, and Kraus (2025).** [Quantum Algorithms for Cooling: A Simple Case Study](https://doi.org/10.1103/4hx7-xnhw), *Physical Review Research* **7**, 033162, analyzes cooling cycles, steady-state energies and noise in a solvable fermionic model, including resettable bath modes and optimized couplings. Its noise analysis is an important fixed-protocol benchmark. The system-plus-bath architecture and energy objective do not yield the present universal accuracy floor; the bath supplies additional resettable modes and is excluded from the prepared-system output.

## Causality and related scientific accounts

Finite propagation speed is established background, including [Bravyi, Hastings, and Verstraete (2006)](https://doi.org/10.1103/PhysRevLett.97.050401), *Lieb-Robinson Bounds and the Generation of Correlations and Topological Quantum Order*. The circuit model here has exact gate cones, so no continuous-time Lieb-Robinson estimate is imported. A continuous-time bounded-Hamiltonian version would need an additional argument.

The following public accounts share ingredients but solve different tasks. Their scientific statements were compared at the linked revisions.

| Account | Shared ingredient | Why its theorem does not supply this result |
|---|---|---|
| [Boundary Memory Erasure](https://github.com/GoGoKo699/Boundary-Memory-Erasure/tree/7f9e4191fce6cdbec8119641caffadd6b5ad9553) | Endpoint dissipation and complete replacement-channel accuracy | A fixed order-preserving qutrit Hamiltonian, maximally mixed target, and a transport bottleneck. It neither permits arbitrary local coherent layers nor adds the bulk heating used here. |
| [Fermionic Reset Complexity](https://github.com/GoGoKo699/Fermionic-Reset-Complexity/tree/7cc91ccf5f1e7b503a95105b6d0b6885e1088349) | One loss port, whole-register vacuum target and coherent entropy compression | Optimizes total damping action with fast global controls and no bulk heating. Its action hierarchy leaves spatial synthesis and noisy transport outside the model. |
| [Noise-Assisted Fermionic Reset](https://github.com/GoGoKo699/Noise-Assisted-Fermionic-Reset/tree/25838345de4bb477f4ca2329d1825003bfeb3b15) | Local chain, one vacuum-loss contact and global reset accuracy | A fixed generator whose number dephasing preserves the vacuum. Its noise helps absorption rather than continuously reheating the target. |
| [Quantum Mixing Depth](https://github.com/GoGoKo699/Quantum-Mixing-Depth/tree/e059785fc822cb7701e12bffb97b60b95738aa3c) | Arbitrary local gates, iid depolarization, exact cones and complete-channel distance | Targets the maximally mixed state without reset contacts. Its inverse-observable spacetime-support bound describes information destruction. The selected late-event factorization here describes entropy that cannot reach a cold contact. |

The channel norm and reset conventions are standard; see [Watrous, *The Theory of Quantum Information* (2018)](https://jhwatrous.github.io/books-and-courses.html). The proof and construction in this repository are self-contained.
