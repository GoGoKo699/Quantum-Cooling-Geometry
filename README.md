# Quantum Cooling Geometry

**How accurately can an entire noisy quantum register be initialized when entropy can leave only through selected reset contacts?** Distance sets a limit for every controller, and shared contacts introduce contention. When the bulk can interact, reversible compression can reduce how much information must pass through a contact to be erased.

For a path with reset set $`S`$, independent depolarization $`p`$ per round, and

```math
M=\sum_v\mathrm{dist}(v,S),
```

the optimal complete initialization error satisfies

```math
\boxed{\displaystyle
\frac{1-(1-p)^M}{2}
\le\epsilon_*\le\min\{1,pM\}.}
```

The lower bound permits arbitrary prescribed local entangling gates and contact CPTP maps. A periodic SWAP/reset conveyor attains the same order with no extra qubits. Error is half the diamond distance from pure-zero replacement, so the guarantee includes arbitrary reference-entangled inputs and every physical output qubit.

![Two paths with the same number of reset contacts: alternating contacts give distance sum 8, while clustering the contacts on one half gives distance sum 36.](figures/contact-layouts.svg)

The figure uses 16 qubits and 8 contacts. The [general comparison](science/interpretation.md#the-same-contact-count-different-layouts) gives a linear distance sum for alternating contacts and a quadratic one for clustered contacts.

## Results

| Geometry | Distance sum or optimal error scale | Scientific account |
|---|---|---|
| Any finite connected graph with nonempty contacts | Exact lower bound $`[1-(1-p)^M]/2`$ | [Causal converse](science/converse.md) |
| Any fixed contact placement on a chain | $`\epsilon_*=\Theta(\min\{1,pM\})`$ when $`M>0`$ | [Matching path construction](science/geometry.md#every-fixed-contact-placement-on-a-path) |
| One endpoint contact on an $`n`$-qubit chain, $`n\ge2`$ | $`\Theta(\min\{1,pn^2\})`$ | [Exact conveyor channel](science/geometry.md#a-one-contact-path-conveyor) |
| Best placement of $`m\lt n`$ contacts on a chain | $`\Theta(\min\{1,pn(n-m)/m\})`$; exact minimum distance sum also given | [Contact placement](science/geometry.md#optimally-placed-contacts-on-a-path) |
| Slab of thickness $`L\ge2`$ and $`N`$ qubits, one full cold face | $`\Theta(\min\{1,pN(L-1)\})`$ | [Slab construction](science/geometry.md#rectangular-slabs-with-one-full-cold-face) |
| Every site is a contact | Exact zero error after a final parallel reset | [Output convention](science/model.md#register-contacts-and-round-convention) |

The constants in the order statements are absolute. The [exact throughput theorem](science/contact_throughput.md) below covers a further architecture class; a matching routing theorem for arbitrary graphs is not supplied.

## Exact accuracy and an optimal reset schedule

Suppose the noncontact qubits $`B=V\setminus S`$ have no mutual graph edges. Assign each one to an adjacent reset contact, with $`\ell_s`$ qubits assigned to contact $`s`$. The optimum over **all allowed coherent controls, contact maps and durations** is

```math
\boxed{\displaystyle
\epsilon_*(G,S,p)=1-\max_f\prod_{s\in S}\prod_{j=1}^{\ell_s}\frac{1+(1-p)^j}{2}.}
```

A finite assignment calculation chooses the contact loads. Reset the contacts, then SWAP each data qubit once with its assigned contact and reset the contacts after every noisy layer. The schedule uses no extra qubits, has depth $`1+\max_s\ell_s`$, and replaces every input—including its reference correlations—by the stated diagonal product output. The [proof and resource account](science/contact_throughput.md) explain why entangling controls cannot improve the optimum in this model.

For one contact shared by $`m`$ leaves, every leaf is one edge from reset, yet

```math
\epsilon_* =1-\prod_{j=1}^{m}\frac{1+(1-p)^j}{2}
=\Theta\!\left(\min\{1,pm^2\}\right).
```

The quadratic cost comes from final waiting ages $`1,2,\ldots,m`$. Multiple contacts can reduce it by balancing their loads subject to the actual wiring. [Use the exact schedule planner](verification/README.md#exact-contact-assignment-and-schedule).

## Reversible compression through one reset contact

Connect a clique of $`m`$ bulk qubits to one reset contact through a single gateway. The best SWAP/reset schedule has final bulk ages $`1,3,\ldots,2m-1`$ and error of order $`\min\{1,pm^2\}`$. A two-pass reversible compressor uses the same contact and physical qubits to attain the optimal error

```math
\epsilon_*=\Theta_c(pm\log m),
\qquad 0\lt p\le c/m^2
```

for any fixed positive $`c`$ and sufficiently large bulk. At $`p=c/m^2`$, this error vanishes, while the exact SWAP/reset optimum tends to $`1-e^{-c/2}`$. The protocol refreshes the bulk, compresses sparse errors within blocks, and erases the resulting indices through the gateway. A final compression clears the errors accumulated during that transfer. The [proof and gate schedule](science/single_contact_compression.md) account for depolarization during every layer and show why even unrestricted control has a logarithmic terminal window of noise that cannot reach the contact.

## Why longer cooling does not remove the floor

At the common output time, some recent noise events are too far from a contact for their entropy to reach it. A selected complete-depolarization event in this terminal region leaves a tracial qubit factor, even after arbitrary allowed coherent processing. Its output has largest eigenvalue at most one half. Counting such locations gives the finite-noise lower bound. The [full proof](science/converse.md) does not assume independent output errors or noiseless exact reset by the controller.

## Read and reproduce

Start with the [scientific overview](science/README.md) and [exact model](science/model.md), then read the [converse](science/converse.md), [constructions](science/geometry.md), and [physical consequences](science/interpretation.md). [Noise and scope](science/noise_and_scope.md) gives the mixed-unitary extension and target-preserving counterexamples. The [LLM reading guide](llms.txt) maps questions to authoritative files.

For a guided conceptual route, use the [Watrous 2018 source bridge and worked three-qubit example](learning/WATROUS_BRIDGE.md), then the [30-milestone map](learning/MILESTONES.md). The [learning entrypoint](learning/README.md) connects the prerequisites to the scientific proofs.

From the repository root:

```bash
python -m pip install -r verification/requirements.txt
python verification/verify.py
python verification/geometry_checks.py
python verification/contact_throughput_checks.py
python verification/check_single_contact.py
python verification/make_figure.py
```

The [verification guide](verification/README.md) records numerical scopes, exact conventions and limits. Checks include arbitrary quantum controls and boundary channels, direct channel factorization, reference-sensitive replacement, interior-port trajectories and finite contact placements. Finite checks support the written analytical proofs.

## Scope and attribution

Each round applies disjoint nearest-neighbor unitary gates, independent depolarization on **all** sites including idle qubits, then CPTP operations at the contacts. The output follows the final contact operation. Contacts are ideal resources; bulk measurements, discarded workspace, protected side registers and observation-conditioned feedback are outside the model. All physical outputs must be pure together. Logical cooling, selected-subsystem polarization and thermodynamic heat or work costs are separate tasks.

One-port cooling, SWAP transport, and reversible entropy compression have prior precedents. The results here give explicit accuracy laws for synchronized full-register reset, including when SWAP schedules attain the optimum and when compression beats them. The [related-work comparison](references/RELATED_WORK.md) distinguishes these laws from prior cooling and reset models. The compression uses basis permutations, which also have a classical reversible interpretation.

## Purpose and contact

This repository serves as a record of the work and a guide for the author’s self-directed learning. For discussion or potential collaboration, please contact Ruge Lin at [gogoko699@gmail.com](mailto:gogoko699@gmail.com).
