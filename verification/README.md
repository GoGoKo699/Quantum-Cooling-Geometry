# Verification

This suite checks the finite identities and consequential failure modes in the boundary-reset argument. The general theorems rest on the written proofs; finite computations do not certify them or establish publication priority.

Run from the repository root with Python and NumPy:

```bash
python verification/verify.py
python verification/geometry_checks.py
python verification/make_figure.py
```

The main command writes `verification/results.json`. `geometry_checks.py` independently enumerates finite optimal placements, arbitrary interior ports and slabs, and writes `verification/geometry_checks_results.json`. `make_figure.py` regenerates the exact contact-layout SVG using only the standard library. An alternative destination can be supplied with `--output PATH`. The random seed is fixed at 1729; the result records the actual Python/NumPy versions and numerical tolerance.

## What is checked

| Check | Finite scope | Failure mode addressed |
|---|---|---|
| Carrier trajectories | Every path length from 1 through 128 | A SWAP circuit might leave one original input carrier at the end, or assign the wrong number of later noise exposures. Every original carrier is removed at round `2n−1`; the final noise-age multiset is `0,1,3,…,2n−3`. |
| Exact conveyor error | Six noise strengths, including zero and complete depolarization, at each path length | The output-error formula, finite-noise converse, union bound and weak-noise coefficient must use the same round convention. Stable logarithmic evaluation avoids cancellation near zero noise. |
| Reference-sensitive replacement channel | 2, 3 and 4 data qubits, each initially maximally entangled with a reference; eight endpoint/interior/multiple-port configurations and three noise strengths | Resetting a selected input population is weaker than replacing the complete channel. The normalized Choi output is compared with the predicted product replacement state tensored with the unchanged maximally mixed reference. |
| Interior-port conveyors | Every cell length 1–48, every actual port location, both starting parity phases and three late finishing times | A Voronoi cell's actual reset port need not be its endpoint. All input carriers must still be removed, and the final total noise age must be at most twice the sum of distances to that interior port. |
| Arbitrary entangling controls and boundary channels | 600 cases on 2–4 qubits | The converse must survive coherent compression and boundary maps other than ideal reset. Random pure, mixed and maximally mixed inputs, Haar nearest-neighbor gates and rank-four boundary CPTP maps are tested against the finite-noise largest-eigenvalue bound. |
| Selected-event factorization | 120 conditional trajectories on 2–4 qubits | The crucial claim is an exact channel push-through identity, rather than incorrect monotonicity of the largest eigenvalue under arbitrary resets. One full depolarizer is kept unconditioned; other noise occurrences are represented by fixed random Pauli unitaries. |
| Negative controls | Explicit two-qubit examples | A depolarization at the reset port is removed by its immediate reset, so the push-through assertion fails outside the terminal inaccessible region. Pure dephasing preserves the target, so “all unital noise” would be too broad without a positive complete-depolarization component. |
| Reset-port geometry | All 4,082 nonempty port placements on paths of length 2–11; slabs of dimension 1–3 and side 2–12 | For each fixed port set, contiguous nearest-port cells are constructed and their conveyors are checked at one common finishing time. The age sum is at most twice the actual distance sum. Dense-port limits must not be described by `n²/m` uniformly through `m=n`; all-site reset has zero terminal volume and zero residual ages. |

## Exact conventions

Sites are numbered from the left boundary. A round applies a layer of disjoint nearest-neighbor unitary gates, then independent local noise to **every** site, including idle sites, and then the boundary CPTP map. The constructive circuit uses ideal boundary replacement by the zero state. No mandatory extra noise follows the final reset.

For depth `T`, the terminal inaccessible region contains the noise positions `(j,s)` with `j−1>T−s`, where rounds are numbered from one. Its size is

```math
M_T=\sum_{j=1}^{n}\min\{T,j-1\}.
```

The random-control suite checks the bound

```math
\lambda_{\max}(\rho_{\rm out})
\leq\frac{1+(1-p)^{M_T}}{2}.
```

This bound holds for every input at a fixed circuit depth. A universal-reset protocol at very short depth also faces an independent information-removal obstruction. The tests do not silently impose noiseless exact reset on the converse controls.

The odd/even conveyor applies SWAPs on edges `(1,2),(3,4),…` in its first round and `(2,3),(4,5),…` in its second. The final channel is a product replacement with the checked noise ages. Its half-diamond error is exactly

```math
\epsilon_{\rm conv}
=1-\prod_{k=1}^{n-1}\frac{1+(1-p)^{2k-1}}2.
```

The Choi calculation checks full replacement and reference decoupling; the exact error identity then follows because the replacement output is diagonal and the target is pure. No numerical diamond-norm optimization is claimed.

For arbitrary fixed ports on a line, the construction partitions the line into contiguous nearest-port cells, breaking a distance tie toward the left port. Each cell runs the alternating SWAP pattern with its **actual** reset port, which can lie in its interior. All cells finish at the common time `2 max(cell length)−1`. The finite trajectory checks confirm

```math
\sum_v a_v\leq2\sum_v\operatorname{dist}(v,S),
\qquad
\epsilon_{\rm conv}\leq p\sum_v\operatorname{dist}(v,S),
```

where `a_v` counts the noise exposures of the final output carrier since its last reset. Neither an extra reset at a cell endpoint nor discarded output space is introduced.

## Source and interpretation limits

The nearest related internal models use different operations and objectives: `Boundary-Memory-Erasure` fixes an order-preserving qutrit hopping chain and targets a completely mixed replacement, while `Fermionic-Reset-Complexity` prices vacuum-loss action with global coherent controls and no bulk heating. Neither supplies this finite-noise spatial converse. Their source comparisons belong in the scientific related-work account, rather than being inferred from successful tests here.

All physical output qubits are retained in the present model. Fresh bulk pure ancillas, discarded syndrome registers, measurement/postselection, sequential output release and encoded-only recovery change that task. The suite does not test a heat/work cost, finite-rate reservoir, gate-synthesis cost, hardware performance or quantum advantage over classical transport.
