# From quantum channels to cooling geometry

A cold contact can reset a qubit placed at that contact. Initializing a larger register requires local gates to carry information toward the contact while noise continues to act everywhere. The question is how accurately **all physical qubits can be initialized at one common output time**, including removal of their correlations with anything outside the register. Distance matters, and a contact shared by many nearby qubits can impose an additional bottleneck. The route below develops both effects.

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

The book does not provide the distance-sum cooling law, the exact contact-cover optimum, or their attaining SWAP schedules. Their authoritative accounts are the [general converse](../science/converse.md), [path/slab construction](../science/geometry.md), and [contact-throughput theorem](../science/contact_throughput.md). Standard min-cost flow supplies the finite assignment algorithm; the physical slot objective is derived here. The [related-work account](../references/RELATED_WORK.md) separately credits the research literature.

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

At $`pM\ll1`$, the converse is $`pM/2+O((pM)^2)`$. Increasing cooling time cannot remove this final-time error. The largest distance alone does not count all the noise opportunities; the **sum** of distances does. The distance-sum formula by itself is a converse beyond the proved path and full-face slab constructions. The contact-cover result below solves another graph class exactly and shows why the distance sum alone can underestimate its accuracy cost.

## When short routes share one contact

Take one contact $`s`$ joined to three bulk leaves $`b_1,b_2,b_3`$, with no leaf–leaf edges. Every bulk qubit is only one step from a contact, so $`M=3`$. Nevertheless, a depth-one matching layer allows $`s`$ to interact with only one leaf. To finish with all three leaves cooled, the contact must serve them at different times.

Use the same gates–noise–contacts ordering as before. First reset the contact in a round with no SWAP; then serve the leaves in three successive rounds, resetting the contact after each noisy layer.

| Round | Gate layer | Contact operation after noise | Served leaf’s age at the final output |
|---|---|---|---:|
| 1 | Idle | Reset $`s`$ before it supplies a pure carrier | — |
| 2 | SWAP $`(s,b_1)`$ | Reset the input arriving from $`b_1`$ | 3 |
| 3 | SWAP $`(s,b_2)`$ | Reset the input arriving from $`b_2`$ | 2 |
| 4 | SWAP $`(s,b_3)`$ | Reset the input arriving from $`b_3`$ | 1 |

Each leaf receives a zero carrier from a contact that was reset in the preceding round. Its age includes the noise layer in the SWAP round: the later reset acts on the **contact**, so it cannot remove that leaf’s noise. Every original input carrier and its correlations with a reference are discarded at a contact. The final channel is exactly replacement by

```math
|0\rangle\langle0|_s\otimes\rho_3\otimes\rho_2\otimes\rho_1,
\qquad
\rho_j=\frac12[I+(1-p)^j Z].
```

Define the zero probability of an age-$`j`$ carrier as

```math
h_p(j)=\frac{1+(1-p)^j}{2}.
```

The schedule’s exact half-diamond error is

```math
1-h_p(1)h_p(2)h_p(3).
```

At $`p=0.1`$, the three factors are $`0.95`$, $`0.905`$, and $`0.8645`$, giving error $`0.256746125`$. The distance-only lower bound is $`[1-0.9^3]/2=0.1355`$. Below we show that the larger value is the optimum over **all** allowed controllers on this star, rather than just the error of one SWAP protocol.

For comparison, three contacts serving one leaf each can prepare all three leaves in parallel, with all final ages equal to one. Contact–contact edges can connect that architecture without adding bulk–bulk edges. It has the same bulk distance sum $`M=3`$ but exact error $`1-h_p(1)^3=0.142625`$. The difference comes from contact throughput.

## Why this schedule is globally optimal

The exact extension applies when the bulk $`B=V\setminus S`$ has no internal edges and every bulk vertex has at least one adjacent contact. Every gate edge therefore has at least one endpoint in $`S`$; this is the graph-theoretic meaning of a **vertex cover**. Every remaining vertex can reach a contact in one step. Edges between contacts and arbitrary joint contact maps are allowed.

For a bulk vertex $`v`$ touched by a contact, let $`t_v`$ be its **last** contact-gate round in a depth-$`T`$ controller. After that gate there are

```math
a_v=T-t_v+1
```

noise layers on $`v`$, including the current round. There are no later nonlocal gates involving $`v`$: bulk–bulk edges are absent and its final contact gate has already occurred. Depolarization commutes with later one-qubit gates by unitary covariance, and with operations on other sites by disjoint support. All these terminal noise channels can therefore be moved to the output simultaneously.

This step makes no product-state assumption. A channel’s adjoint moves an operation from the state to the measurement effect: $`\mathrm{Tr}[P\Phi(\rho)]=\mathrm{Tr}[\Phi^\dagger(P)\rho]`$. This lets one bound a measurement probability by the largest eigenvalue of the transformed effect, without describing the unknown state. For retention $`q_v=(1-p)^{a_v}`$, the adjoint terminal channel maps the local target effect to

```math
\mathcal F_{a_v}^{\dagger}(|0\rangle\langle0|)
=q_v|0\rangle\langle0|+(1-q_v)\frac I2,
\qquad
\lambda_{\max}=h_p(a_v).
```

Here $`\mathcal F_{a_v}=(\mathcal D_p)^{a_v}`$ is the composition of those terminal one-site noise maps. The all-zero target population of an arbitrary pre-noise state is bounded by the norm of the tensor-product effect, hence by $`\prod_v h_p(a_v)`$. A correlated input cannot exceed that operator norm.

Assign each visited bulk vertex to the contact used in its last gate. One contact cannot have two last gates in the same round. If it serves $`\ell_s`$ vertices, its ages in increasing order therefore satisfy

```math
a_{s,j}\ge j,\qquad j=1,\ldots,\ell_s.
```

Because $`h_p(j)`$ decreases with age, the best possible population for that assignment is at most $`\prod_s\prod_{j=1}^{\ell_s}h_p(j)`$. A never-touched bulk vertex remains an independent maximally mixed factor for the maximally mixed full-register input. Its zero probability is $`1/2`$; assigning it an older unused slot at any allowed contact can only increase that ceiling, since every finite-age $`h_p(j)\ge1/2`$. This covers shallow controllers and controllers that leave some vertices untouched.

On the three-leaf star the only possible contact loads are $`\ell_s=3`$, so every controller has target population at most $`h_p(1)h_p(2)h_p(3)`$. The target test gives an error at least one minus that product. The displayed SWAP schedule attains it as a replacement channel, including arbitrary input-reference correlations. Thus its exact error is the global optimum under this model.

## From a layout to the optimal assignment

For a general contact-cover graph, choose a feasible assignment $`f:B\to S`$, with $`f(v)`$ adjacent to $`v`$, and let $`\ell_s=|f^{-1}(s)|`$. For this assignment, reset all contacts in an initial round and serve each contact’s assigned leaves backwards from a common final round. Its most recently served leaf has age one; its next has age two; and so on. Different contacts act in parallel, and no bulk vertex is assigned twice, so every gate layer is a legal matching. Unequal loads merely leave some contacts idle in early rounds. With $`m=|B|`$ and $`L=\max_s\ell_s`$, this construction uses exactly $`m`$ allowed two-qubit SWAPs, $`L+1`$ noisy rounds, and $`|S|(L+1)`$ one-qubit resets as specified. It retains all register qubits and uses no additional quantum register. Replacing a model SWAP layer by several hardware gate layers changes the noise exposure; the same error formula cannot be retained without recalculation.

Combining the universal population ceiling with that construction gives the exact finite-noise optimum

```math
\boxed{\epsilon_*(G,S,p)
=1-\max_f\prod_{s\in S}\prod_{j=1}^{\ell_s}h_p(j).}
```

Empty products equal one. In particular, empty bulk has zero error, $`p=0`$ permits exact pure replacement, and $`p=1`$ gives $`1-2^{-|B|}`$.

A feasible assignment can be compiled by **min-cost flow**, a standard classical optimization method. Send one unit from every bulk vertex to an adjacent contact, then through one of that contact’s unit-capacity slot arcs. Give slot $`j`$ the cost

```math
c_j=-\ln h_p(j).
```

The costs are nonnegative and nondecreasing, so slots can be taken in prefixes $`1,\ldots,\ell_s`$. Minimizing their sum maximizes the product above. The chosen assignment determines the optimal SWAP schedule; it is not necessary to search all quantum control circuits. Adjacency still matters: a balanced load vector that requires a missing edge is infeasible.

For a simpler order law define

```math
A_* = A(G,S) = \min_f\sum_{s\in S}\frac{\ell_s(\ell_s+1)}2.
```

This is the minimum total slot age, found by the same flow construction with integer slot costs $`j`$. For nonempty bulk,

```math
\frac{1-(1-p)^{A_*}}2
\le\epsilon_*(G,S,p)
\le\min\{1,pA_*/2\},
\qquad
\epsilon_*=\Theta(\min\{1,pA_*\}).
```

The exact finite-noise costs $`c_j`$ and the integer costs $`j`$ are different objectives. No general claim that their minimizing assignments coincide is needed. A one-contact $`m`$-leaf star has $`A_*=m(m+1)/2`$, explaining the quadratic weak-noise exposure despite distance sum $`M=m`$.

When every one of $`m`$ bulk vertices can use every one of $`s`$ contacts, balanced loads optimize both objectives. Write $`m=sq+r`$, $`0\le r\lt s`$. Then

```math
f_{0,*}=\left[\prod_{j=1}^{q}h_p(j)\right]^s h_p(q+1)^r,
\qquad
A_*=\frac{s q(q+1)}2+r(q+1).
```

This gives a direct design calculation: distribute traffic where physical edges permit, compile the assignment, and read off its exact complete-register accuracy. The proof relies on independent bulk vertices; it does not establish SWAP optimality after adding bulk–bulk couplings. See the [complete throughput proof](../science/contact_throughput.md#exact-finite-noise-theorem) and [assignment compiler](../science/contact_throughput.md#computing-the-optimal-assignment) for the authoritative statement.

## Conditions that remain part of the explanation

All physical outputs are retained and must be initialized simultaneously. Gates are prescribed in advance; the noise is unobserved. No clean bulk ancillas, bulk measurement/reset, discarded bulk workspace, protected side memory, or measurement-conditioned global feedback is included. The contacts may be ideal CPTP maps, and even joint maps on the contact set are allowed in the converse. This strengthens the bound; the constructions require only independent resets.

The final contact reset follows the final noise. If every site is a contact, $`M=0`$ and one final reset gives zero error. Moving a mandatory noise layer after the final reset changes that boundary condition.

The entropy-injecting noise assumption also matters. Phase flips preserve $`|0\rangle`$ and allow an exact conveyor flush. Mixed-unitary structure alone therefore does not imply a positive floor; the extension in [noise and scope](../science/noise_and_scope.md) requires a positive complete-depolarization component with a mixed-unitary residual. Nothing here identifies a fault-tolerant logical-memory ceiling, a quantum-over-classical advantage, or a continuous-time heating theorem.

Continue through the [30-milestone map](MILESTONES.md), or go directly to the [connected scientific account](../science/README.md) and [finite checks](../verification/README.md).
