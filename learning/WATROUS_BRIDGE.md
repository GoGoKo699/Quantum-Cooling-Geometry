# From quantum channels to cooling geometry

A cold contact can reset a qubit placed at that contact. Initializing a larger register requires local gates to carry information toward the contact while noise continues to act everywhere. The question is how accurately **all physical qubits can be initialized at one common output time**, including removal of their correlations with anything outside the register.

The selected educational anchor is **John Watrous, *The Theory of Quantum Information*, Cambridge University Press (2018)**, DOI [10.1017/9781316848142](https://doi.org/10.1017/9781316848142). The [author's book page](https://jhwatrous.github.io/books-and-courses.html) provides the source and individual chapters. Use the 2018 book, rather than its older course-note precursor. This guide supplies the spatial and constructive steps specific to this project; the book supplies the channel-theoretic foundations.

[Learning route](README.md) · [30-milestone map](MILESTONES.md) · [Exact scientific model](../science/model.md)

## Focused source pointers

There is no need to read the whole book before beginning the worked example below. Return to these portions when their concepts become useful.

| Watrous source | Foundation used here | Project-specific step supplied here |
|---|---|---|
| [Chapter 2](https://jhwatrous.github.io/TQI.2.pdf), Sections 2.1 and 2.1.3 | Registers, states, partial traces and reference systems | Identify every retained physical qubit and the inaccessible input reference. |
| Chapter 2, Sections 2.2.1–2.2.2 | CPTP channels, preparation, discarding, and channel representations | Compose gates, local noise, and contact operations in the specified order. |
| [Chapter 3](https://jhwatrous.github.io/TQI.3.pdf), Section 3.1 | Trace distance and distinguishability by measurements | Use the all-zero measurement to turn a target-population ceiling into an error lower bound. |
| Chapter 3, Section 3.3, especially 3.3.2–3.3.3 | Completely bounded trace norm and channel discrimination with a reference | Formulate universal reset and establish the conveyor's reference-uniform error. Definition 3.43 fixes the norm; Theorem 3.46 explains reference-size stabilization. |
| [Chapter 4](https://jhwatrous.github.io/TQI.4.pdf), Section 4.1.1 and Definition 4.2 | Mixed-unitary channels | Keep one complete depolarizer intact while resolving other noise into unitary trajectories. |
| Chapter 4, Section 4.3 | Majorization and changes of spectra under unital processing | Understand why a surviving maximally mixed factor limits overlap with every pure target. The causal factorization is still needed because contact resets are nonunital. |

The book does not provide the distance-sum cooling law or the SWAP schedule proved in this repository. Their authoritative accounts are the [converse](../science/converse.md) and [construction](../science/geometry.md). The [related-work account](../references/RELATED_WORK.md) separately credits the research literature.

## Translate the notation and the task

A state $`\rho`$ is a positive operator with trace one. A channel is a linear, completely positive, trace-preserving map: it describes a valid operation even when the register is entangled with a reference. A unitary gate acts by $`\mathrm{Ad}_U(X)=UXU^\dagger`$. Discarding one qubit means taking its partial trace; resetting it then prepares a fresh $`|0\rangle`$ at that same contact.

For a register $`V`$ of $`n`$ qubits, ideal initialization is the replacement channel

```math
\mathcal R_0(X)=\mathrm{Tr}(X)|0^n\rangle\langle0^n|.
```

This discards the input information and prepares the specified state. A circuit that happens to leave $`|0^n\rangle`$ unchanged has not thereby implemented replacement on an unknown input.

The project uses half trace distance for states and half diamond distance for channels:

```math
D(\rho,\sigma)=\frac12\Vert \rho-\sigma\Vert _1,
\qquad
\epsilon(\Psi)=\frac12\Vert \Psi-\mathcal R_0\Vert _\diamond.
```

Watrous calls the latter norm the **completely bounded trace norm**, writing it with triple bars and subscript 1. It is the same norm denoted by $`\Vert \cdot\Vert _\diamond`$ here; our error includes the additional factor $`1/2`$.

Operationally, the initialization guarantee is

```math
\frac12\left\Vert 
(\Psi\otimes\mathrm{id}_A)(\rho_{VA})
-|0^n\rangle\langle0^n|\otimes\rho_A
\right\Vert _1\le\epsilon
```

for every register–reference input $`\rho_{VA}`$. The reference marginal is $`\rho_A=\mathrm{Tr}_V\rho_{VA}`$. Taking no reference gives an ordinary state test. Such a test can disprove a universal guarantee, while success on one input does not establish it. A replacement-channel construction, as below, establishes the reference guarantee directly.

Use **target population** for $`f_0=\langle0^n|\rho|0^n\rangle`$. This is a measurement probability; it avoids confusing that probability with a square-root fidelity convention. The measurement “all zeros or otherwise” implies

```math
D(\rho,|0^n\rangle\langle0^n|)\ge1-f_0.
```

Equality holds for the diagonal output states of the conveyor, but is not assumed for arbitrary coherent outputs.

## A complete three-qubit example

Take a path of three qubits with its only cold contact at site 1. Every round consists of a disjoint nearest-neighbor gate layer, then independent noise on **all three sites**, then a reset at site 1. The output follows that final reset.

The one-site noise is

```math
\mathcal D_p=(1-p)\,\mathrm{id}+p\,\mathcal E,
\qquad
\mathcal E(X)=\mathrm{Tr}(X)\frac I2.
```

Thus $`p`$ is the weight of complete depolarization in this decomposition. Equivalently, the Pauli probabilities are $`1-3p/4`$ for the identity and $`p/4`$ for each of $`X,Y,Z`$. The decomposition labels are not observed by the controller. Idle qubits experience the same noise.

### Why every controller has a nonzero floor

The distances to the contact are $`d_1=0`$, $`d_2=1`$, and $`d_3=2`$. For a depth $`T\ge2`$, consider these final noise opportunities:

| Site | Noise layers too late to reach the contact | Number |
|---|---|---:|
| 1 | None: its reset follows the noise | 0 |
| 2 | Layer $`T`$ | 1 |
| 3 | Layers $`T-1`$ and $`T`$ | 2 |

A gate layer can move an operator's support at most one edge. Consequently none of these three locations can influence a subsequent contact operation before output. The number of locations is

```math
M=d_1+d_2+d_3=3.
```

At least one complete depolarizer occurs in this set with probability $`1-(1-p)^3`$. The following channel argument makes that count useful even for entangling gates and coherent entropy compression.

Select one such occurrence from its occurrence pattern. Write every other noise occurrence as a random Pauli unitary and condition on those other Pauli choices. The selected occurrence stays a **full** complete-depolarization channel; its own Pauli label is not conditioned upon. Conjugating it through later gates enlarges its support only inside its forward cone. That support avoids the contact, so the channel commutes through every subsequent contact map. At output the register state therefore has the form

```math
W\left(\frac I2\otimes\tau\right)W^\dagger
```

for a unitary $`W`$ and a density matrix $`\tau`$. Its largest eigenvalue is at most $`1/2`$, so its overlap with any pure target is at most $`1/2`$. Averaging the conditioned trajectories preserves this ceiling.

Contact resets can increase global largest eigenvalues. The proof works because the selected depolarizer is first moved past every contact operation; it does not apply an eigenvalue monotonicity claim to those resets.

Even granting target population one when the selected event does not occur, every controller obeys

```math
f_0\le\frac{1+(1-p)^3}{2},
\qquad
\epsilon\ge\frac{1-(1-p)^3}{2}.
```

For $`T\lt 2`$, inserting a complete depolarizer on site 3 at the maximally mixed input changes nothing. Its cone still cannot meet the contact, so the same mixed-factor argument gives error at least $`1/2`$. Thus shortening the protocol cannot evade the displayed floor. The [full converse](../science/converse.md) makes the argument duration-uniform on every graph.

### A concrete controller and its exact error

Alternate SWAP on $`(1,2)`$ in odd rounds and on $`(2,3)`$ in even rounds, resetting site 1 after each noisy layer. Run five rounds. To see that the protocol discards all unknown input information, label the original carriers $`a,b,c`$ and the fresh carrier introduced by the round-$`t`$ reset $`z_t`$.

| After the contact reset | Gate in that round | Carriers at sites 1, 2, 3 |
|---|---|---|
| Initial input | — | $`(a,b,c)`$ |
| Round 1 | SWAP $`(1,2)`$ | $`(z_1,a,c)`$ |
| Round 2 | SWAP $`(2,3)`$ | $`(z_2,c,a)`$ |
| Round 3 | SWAP $`(1,2)`$ | $`(z_3,z_2,a)`$ |
| Round 4 | SWAP $`(2,3)`$ | $`(z_4,a,z_2)`$ |
| Round 5 | SWAP $`(1,2)`$ | $`(z_5,z_4,z_2)`$ |

These labels track routing, not the noisy quantum states. Every original carrier has been discarded at the contact, including its correlations with a reference. The final carriers have experienced respectively 0, 1, and 3 noise layers since their last resets. Write the state of a reset carrier after $`a`$ further noise layers as

```math
\rho_a=\frac12\left[I+(1-p)^aZ\right].
```

The full final channel is exactly replacement by $`\rho_0\otimes\rho_1\otimes\rho_3`$. Its all-zero probability and its error are

```math
f_{0,\mathrm{conv}}
=\frac{1+(1-p)}2\frac{1+(1-p)^3}2,
\qquad
\epsilon_{\mathrm{conv}}=1-f_{0,\mathrm{conv}}.
```

Because both channels are replacements, adjoining any reference merely tensors their output difference with $`\rho_A`$. The trace norm is unchanged by that density-matrix factor, so the ordinary output half trace distance is exactly the half diamond error here.

For $`p=0.1`$, the two nontrivial zero probabilities are $`0.95`$ and $`0.8645`$. Therefore

```math
0.1355
\le\epsilon_*(P_3,\{1\},0.1)
\le\epsilon_{\mathrm{conv}}
=1-(0.95)(0.8645)
=0.178725.
```

The lower bound applies to every admissible controller; the upper value is the error of this particular five-round schedule. Their difference is not a determined optimal constant. For $`p=0`$, this schedule is exact pure replacement.

## From the example to the geometry law

On a graph with reset set $`S`$, define $`d_v=\mathrm{dist}(v,S)`$. At noise layer $`t`$ there are $`T-t`$ future gate layers. The layers satisfying $`T-t\lt d_v`$ contribute

```math
M_T=\sum_v\min\{T,d_v\}.
```

For depth at least the cover radius $`\max_v d_v`$, this is $`M(G,S)=\sum_vd_v`$. A maximally mixed input and an inserted unreachable depolarizer handle smaller depths. The resulting bound is

```math
\epsilon_*(G,S,p)\ge\frac{1-(1-p)^{M(G,S)}}2.
```

On a path, conveyors in nearest-contact cells establish the matching upper $`\epsilon_*\le\min\{1,pM\}`$. Thus, for $`M>0`$, the optimum has order $`\min\{1,pM\}`$. For one endpoint contact $`M=n(n-1)/2`$. For a slab of thickness $`L`$ and cross-sectional size $`A`$, cooled from one full face, $`M=AL(L-1)/2`$ and parallel column conveyors also match the order. See [geometry](../science/geometry.md) for the exact formulas and schedules.

At $`pM\ll1`$, the converse is $`pM/2+O((pM)^2)`$. Increasing cooling time cannot remove this final-time error. The largest distance alone does not count all the noise opportunities; the **sum** of distances does. Beyond paths and the stated full-face slabs, the graph formula is a converse and does not by itself prove an attainable upper bound.

## Conditions that remain part of the explanation

All physical outputs are retained and must be initialized simultaneously. Gates are prescribed in advance; the noise is unobserved. No clean bulk ancillas, bulk measurement/reset, discarded bulk workspace, protected side memory, or measurement-conditioned global feedback is included. The contacts may be ideal CPTP maps, and even joint maps on the contact set are allowed in the converse. This strengthens the bound; the constructions require only independent resets.

The final contact reset follows the final noise. If every site is a contact, $`M=0`$ and one final reset gives zero error. Moving a mandatory noise layer after the final reset changes that boundary condition.

The entropy-injecting noise assumption also matters. Phase flips preserve $`|0\rangle`$ and allow an exact conveyor flush. Mixed-unitary structure alone therefore does not imply a positive floor; the extension in [noise and scope](../science/noise_and_scope.md) requires a positive complete-depolarization component with a mixed-unitary residual. Nothing here identifies a fault-tolerant logical-memory ceiling, a quantum-over-classical advantage, or a continuous-time heating theorem.

Continue through the [30-milestone map](MILESTONES.md), or go directly to the [connected scientific account](../science/README.md) and [finite checks](../verification/README.md).
