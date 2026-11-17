# Exact initialization accuracy with shared reset contacts

Short distance to a cold contact does not ensure accurate simultaneous initialization. A contact can participate in only one two-qubit gate per round, so data qubits sharing it must wait while noise continues to act. This page gives the exact finite-noise optimum when every noncontact qubit couples only to contacts. It also supplies the optimal contact assignment and a schedule that attains the complete-channel error, including arbitrary input-reference correlations.

The [distance converse](converse.md) remains valid on every graph, and the [path and slab results](geometry.md) retain their stated scope. The theorem here uses a different, explicitly restricted graph class to resolve contact contention. In particular, it shows why the distance sum alone cannot characterize general graphs.

## Architecture and assignment

Use the [same model and error convention](model.md): a round is a disjoint-edge unitary layer, independent single-qubit depolarization on all physical qubits, then a CPTP map on the contact set $`S`$. The output follows the final contact map. All physical qubits are retained outputs; no extra quantum memory or discarded bulk workspace is supplied.

Let $`B=V\setminus S`$ be the noncontact bulk, and assume that $`B`$ is an **independent set** in $`G`$: no two bulk vertices have a direct gate edge. Every bulk vertex has at least one neighbor in $`S`$. Edges within $`S`$ are allowed, and the contact maps may be arbitrary joint maps on $`S`$. Write

```math
m=|B|,\qquad s=|S|\ge1,
\qquad N_S(v)=\{u\in S:\{u,v\}\in E\}.
```

Thus a bulk qubit may have several possible contacts, but any two-qubit gate touching it must use one of them. This restriction concerns the available gates, rather than a protocol's voluntary decision to ignore bulk-bulk edges.

An allowed assignment chooses one adjacent contact for every bulk vertex:

```math
\mathfrak F
=\{f:B\longrightarrow S:f(v)\in N_S(v)\text{ for every }v\in B\},
\qquad
\ell_u(f)=|f^{-1}(u)|.
```

For a nonnegative integer age $`a`$, define

```math
h_p(a)=\frac{1+(1-p)^a}{2},\qquad h_p(0)=1.
```

Here an age counts noisy rounds since a fresh zero left its contact. In the stipulated gate-noise-reset order, a bulk qubit swapped out in the final gate layer has age one, because its final noise cannot be reset locally.

## Exact finite-noise theorem

**Theorem 7 — exact contact-throughput optimum.** Under the architecture above, for every $`0\le p\le1`$,

```math
\boxed{\displaystyle
\epsilon_*(G,S,p)
=1-F_*(G,S,p),
\qquad
F_*(G,S,p)
=\max_{f\in\mathfrak F}
\prod_{u\in S}\prod_{j=1}^{\ell_u(f)}h_p(j).}
```

The infimum in $`\epsilon_*`$ is over every finite depth and all the prescribed controls allowed by the model, including arbitrary one-qubit rotations, entangling edge gates, arbitrary joint contact CPTP maps, and input-independent classical randomization. Its half-diamond criterion includes arbitrary initial entanglement with an inaccessible reference. A finite SWAP/reset protocol attains the displayed value exactly.

If $`B`$ is empty, the product is empty, $`F_*=1`$, and one final parallel reset gives zero error. At $`p=0`$, the same exact zero error is attainable for every allowed graph. At $`p=1`$,

```math
F_*=2^{-m},\qquad \epsilon_*=1-2^{-m}.
```

The final bulk is then fully mixed and the contacts are pure. These endpoints do not require an asymptotic interpretation.

## Converse: the noise after the last contact gate

Fix any deterministic depth-$`T`$ circuit. First consider a bulk vertex $`v`$ that participates in a two-qubit gate. Let $`t_v`$ be its **last** such round, and let $`u_v\in S`$ be the other endpoint of that gate. Set

```math
a_v=T-t_v+1\ge1.
```

Because the bulk is independent, after round $`t_v`$ the qubit $`v`$ has no further nonlocal interaction. Its remaining operations are one-qubit unitaries and local depolarizing channels. The depolarizing channels in rounds $`t_v,t_v+1,\ldots,T`$ can therefore be moved to the output:

- They commute with every later operation disjoint from $`v`$, including joint contact maps.
- They commute through one-qubit rotations by unitary covariance of depolarization.
- Their composition has Bloch-vector retention $`(1-p)^{a_v}`$.

These moves can be performed simultaneously for all visited bulk vertices. Removing their terminal depolarizing channels leaves a CPTP circuit, so its output before the moved channels is some density matrix $`\sigma`$. No product-state assumption on $`\sigma`$ is needed. Let $`P_0=|0\rangle\langle0|`$ and write $`\mathcal D^{(a)}`$ for depolarization with retention $`(1-p)^a`$. Its adjoint effect is

```math
(\mathcal D^{(a)})^*(P_0)
=(1-p)^aP_0+\frac{1-(1-p)^a}{2}I,
\qquad
\left\Vert (\mathcal D^{(a)})^*(P_0)\right\Vert _\infty=h_p(a).
```

The pure all-zero target effect on the contacts has norm one. Positivity and the tensor-product operator norm consequently give

```math
\langle0^n|\Psi_T(\rho)|0^n\rangle
\le\prod_{v\in B}h_p(a_v)
```

when every bulk vertex was visited, for every input $`\rho`$. Earlier entanglement, coherent entropy compression, and correlations produced by the contact maps cannot increase this bound.

Assign each visited $`v`$ to $`u_v`$. At a fixed contact $`u`$, the last gates occur in distinct rounds because every gate layer is a matching. Their ages, sorted increasingly as $`a_{u,1},\ldots,a_{u,\ell_u}`$, therefore obey

```math
a_{u,j}\ge j.
```

Since $`h_p(a)`$ is nonincreasing in $`a`$,

```math
\prod_{v\in B}h_p(a_v)
\le\prod_{u\in S}\prod_{j=1}^{\ell_u}h_p(j)
\le F_*(G,S,p).
```

### Bulk vertices that were never visited

A shallow or deliberately incomplete circuit need not touch every bulk vertex. Let $`U\subseteq B`$ contain the $`q`$ untouched vertices. Use the maximally mixed full-register input. Each such vertex remains an independent tracial qubit throughout: there is no bulk-bulk gate and, by definition, no contact gate touching it. Local rotations and depolarization preserve its state. The preceding terminal-noise argument on the visited vertices gives

```math
\langle0^n|\Psi_T(I/2^n)|0^n\rangle
\le2^{-q}\prod_{v\in B\setminus U}h_p(a_v).
```

To compare this with a full assignment, assign each untouched vertex to any allowed neighbor and place it at a distinct older, unused age at that contact, leaving all existing ages unchanged. There are finitely many vertices, so finite older slots suffice. Every added factor is at least $`1/2`$. Compressing the occupied slots at each contact to $`1,\ldots,\ell_u`$ can only increase the product. Some full assignment therefore has value at least

```math
2^{-q}\prod_{v\in B\setminus U}h_p(a_v).
```

The upper bound by $`F_*`$ still follows. This includes depth zero. It avoids assuming that an accurate protocol must reset exactly when noise is removed.

For the input just used, the two-outcome test with effect $`|0^n\rangle\langle0^n|`$ now yields

```math
\frac12\left\Vert \Psi_T(\rho)-|0^n\rangle\langle0^n|\right\Vert _1
\ge1-\langle0^n|\Psi_T(\rho)|0^n\rangle
\ge1-F_*.
```

The half-diamond distance includes this input test. Hence every deterministic controller has error at least $`1-F_*`$. The same maximally mixed input works for every controller realization, so averaging input-independent classical randomization preserves the bound. Reference assistance is not needed for this converse; allowing a reference in the error criterion only strengthens it.

## Construction: assignment, slots, and SWAPs

Choose an assignment $`f`$ attaining $`F_*`$, and write $`L=\max_u\ell_u(f)`$. For nonempty bulk, run

```math
T=L+1
```

rounds. In round one, use the identity gate layer and reset every contact after its noise. At each contact, number its assigned bulk vertices by slots $`j=1,\ldots,\ell_u`$. Swap the vertex in slot $`j`$ with that contact at round

```math
t=T-j+1.
```

Reset all contacts after the noise in every round. Every bulk vertex is swapped exactly once. At each round each contact uses at most one edge, and different contacts have disjoint assigned bulk vertices; the proposed layer is therefore a legal matching. Contacts with smaller loads simply begin their SWAPs later.

Immediately before each SWAP its contact holds an independent fresh zero. The outgoing bulk qubit experiences exactly $`j`$ noise layers, including its SWAP round. Its final state is

```math
\rho_j=\frac12\bigl[I+(1-p)^jZ\bigr].
```

The initial contact inputs are discarded by the first resets. Every initial bulk input is moved into a contact by its SWAP and discarded by that round's reset. This also discards all its correlations with other inputs and with the reference. Thus the **entire channel** is exactly replacement:

```math
(\Psi_T\otimes\mathrm{id}_A)(\rho_{VA})
=\omega_f\otimes\rho_A,
\qquad
\omega_f
=|0^s\rangle\langle0^s|\otimes
\bigotimes_{u\in S}\bigotimes_{j=1}^{\ell_u}\rho_j,
```

with factors placed at their assigned physical vertices. This expression holds for every reference-entangled input. Since $`\omega_f`$ is diagonal in the target basis,

```math
\frac12\Vert \Psi_T-\mathcal R_0\Vert _\diamond
=\frac12\Vert \omega_f-|0^n\rangle\langle0^n|\Vert _1
=1-\prod_{u\in S}\prod_{j=1}^{\ell_u}h_p(j).
```

This equals the converse value and proves Theorem 7.

### Charged implementation resources

For the chosen assignment, the construction uses exactly $`m`$ edge SWAP gates, depth $`L+1`$ in the stated round convention, and $`s(L+1)`$ one-qubit resets if all contacts are reset in every round as specified. A standard CNOT decomposition uses $`3m`$ CNOTs, but replacing one model SWAP layer by three hardware gate layers changes the noise-per-round contract and requires recalculating the error. The exact theorem counts the permitted two-qubit gates and noise layers of [the model](model.md).

All $`m+s`$ physical qubits are counted and retained; the construction uses no additional quantum register. There are $`(m+s)(L+1)`$ physical single-site noise locations. Contact noise is removed by that round's reset. Only the displayed terminal ages remain on the final bulk carriers. Reset work, finite-duration gate synthesis, and a microscopic bath implementation are not assigned costs by this circuit model.

## Computing the optimal assignment

The assignment is an explicit classical optimization problem, rather than supplied oracle access. For $`j=1,\ldots,m`$, set

```math
c_p(j)=-\ln h_p(j),\qquad
C_p(\ell)=\sum_{j=1}^{\ell}c_p(j).
```

The exact maximization is equivalent to

```math
-\ln F_*=\min_{f\in\mathfrak F}\sum_{u\in S}C_p(\ell_u(f)).
```

The marginal costs $`c_p(j)`$ are nonnegative and nondecreasing, so $`C_p`$ is a discrete convex load cost. A min-cost flow formulation has a source, one node per bulk vertex, one node per contact, and a sink:

1. Send one unit from the source to each bulk vertex.
2. Allow a unit-capacity zero-cost arc from $`v`$ to every adjacent contact $`u\in N_S(v)`$.
3. From every contact to the sink, provide $`m`$ unit-capacity slot arcs with costs $`c_p(1),\ldots,c_p(m)`$.

An integral flow of value $`m`$ exists because every bulk vertex has a contact neighbor. Nondecreasing slot costs permit an optimal flow using a prefix of the slots at every contact. Its bulk-to-contact arcs give the required assignment. The formulation has $`m+s+2`$ nodes and $`m+|E(B,S)|+sm`$ arcs, with parallel contact-slot arcs; standard min-cost flow or an expanded-slot assignment solves it. At $`p=0`$ or $`p=1`$, tied costs may be compressed to prefixes without changing the value. Evaluation precision for real-valued costs is a classical numerical issue, separate from the exact physical statement.

For rational $`p`$, the [implemented planner](../verification/contact_schedule.py) uses exact rational products and reciprocals in successive maximum-product residual augmenting paths. It compares these products directly, without a floating-point logarithm or supplied optimization oracle. The number of augmentations, network size, and intermediate rational bit lengths are polynomial in the finite graph size and rational input length. This is not a strongly polynomial bit-cost or large-instance performance claim. The physical formula above remains exact for real $`p\in[0,1]`$; the implementation takes an exact rational description.

The scheduling and min-cost-flow ingredients are standard. The contribution is the proof that their product objective equals the optimum over **all** the allowed quantum controllers, rather than only over SWAP schedules. [Related work](../references/RELATED_WORK.md) distinguishes this statement from earlier one-port cooling and collective-ancilla purification.

## A simple uniform law from contact loads

Define the integer load functional

```math
A(G,S)=\min_{f\in\mathfrak F}\sum_{u\in S}\frac{\ell_u(f)(\ell_u(f)+1)}2.
```

The same flow formulation with marginal costs $`j`$ computes $`A`$. This is the minimum possible sum of compact terminal ages. For every graph covered by Theorem 7,

```math
\boxed{\displaystyle
\frac{1-(1-p)^{A(G,S)}}2
\le\epsilon_*(G,S,p)
\le\min\left\{1,\frac p2 A(G,S)\right\}.}
```

For the lower bound, for nonnegative integer ages $`a,b`$,

```math
h_p(a)h_p(b)\le h_p(a+b),
```

because $`(1-(1-p)^a)(1-(1-p)^b)\ge0`$. Iterating this inequality gives, for any assignment, a product at most $`h_p(\sum_u\ell_u(\ell_u+1)/2)\le h_p(A)`$. Apply the exact theorem.

For the upper, choose an $`A`$-minimizing assignment and use

```math
1-\prod_i x_i\le\sum_i(1-x_i),\qquad
1-h_p(j)=\frac{1-(1-p)^j}{2}\le\frac{pj}{2}
```

for $`0\le x_i\le1`$. This establishes the displayed bounds without assuming that an $`A`$-minimizing assignment is the exact finite-$`p`$ optimizer. When $`m>0`$,

```math
\epsilon_* =\Theta\!\left(\min\{1,pA(G,S)\}\right)
```

with absolute constants. More precisely, as $`pA\to0`$ the two bounds imply

```math
\epsilon_* =\frac{pA}{2}\,[1+O(pA)].
```

Every bulk vertex in this architecture has graph distance one from $`S`$, so the original distance sum is always $`M(G,S)=m`$. The functional $`A`$ measures the additional contention that this distance sum cannot see.

## Worked geometries

### One reset contact serving a star

For a star with $`m\ge1`$ bulk leaves and one contact at its center, every assignment has load $`m`$. Therefore

```math
\boxed{\displaystyle
\epsilon_*\bigl(K_{1,m},S,p\bigr)
=1-\prod_{j=1}^{m}\frac{1+(1-p)^j}{2},
\qquad
A=\frac{m(m+1)}2,\qquad M=m.}
```

Although the diameter is two and every leaf is adjacent to reset, the low-error scale is $`pm^2`$, rather than the distance bound's $`pm`$. The center's disjoint-gate throughput forces the final leaves to have distinct ages. Arbitrary coherent compression does not remove the terminal local noise after those last interactions.

For four leaves, the attaining protocol first resets the center and then swaps one leaf per round, producing final leaf ages $`4,3,2,1`$. It uses five noisy rounds, four SWAPs, and five center resets. At $`p=0.01`$ its exact optimal half-diamond error is approximately $`0.048649679291`$. The simple upper is $`pA/2=0.05`$.

### A bank of shared contacts

For the complete bipartite graph $`K_{s,m}`$, take all $`s`$ vertices on one side as contacts and all $`m`$ vertices on the other as bulk. Every bulk vertex can use every contact. Balancing loads minimizes the convex cost: if one load exceeds another by at least two, moving one vertex from the larger to the smaller cannot increase the sum, because $`c_p(j)`$ is nondecreasing.

Write $`m=sq+r`$ with $`0\le r\lt s`$. There are $`s-r`$ loads $`q`$ and $`r`$ loads $`q+1`$, and

```math
\boxed{\displaystyle
F_*=\left[\prod_{j=1}^{q}h_p(j)\right]^s h_p(q+1)^r,
\qquad
A=\frac{s q(q+1)}2+r(q+1).}
```

For nonempty bulk this gives $`A=\Theta(m+m^2/s)`$. If $`s\ge m`$, every bulk qubit can be served in the same final gate layer and $`A=m`$. If $`m\gg s`$, contention contributes the quadratic-over-contact term $`m^2/s`$. Restricted adjacency can force a larger value than this fully connected bank; the assignment problem accounts for that restriction.

With four bulk qubits, the following values all have the same distance sum $`M=4`$:

| Available contacts in $`K_{s,4}`$ | Balanced loads | $`A`$ | Attaining rounds | Exact optimal error at $`p=0.01`$ |
|---|---|---|---|---|
| $`s=1`$ | $`4`$ | $`10`$ | $`5`$ | $`0.048649679291`$ |
| $`s=2`$ | $`2,2`$ | $`6`$ | $`3`$ | $`0.029578482550`$ |
| $`s=4`$ | $`1,1,1,1`$ | $`4`$ | $`2`$ | $`0.019850499375`$ |

The contact qubits are physical resources as well: these rows use respectively five, six, and eight total qubits. The comparison isolates what additional reset access buys for a fixed four-qubit bulk.

## Boundary of the conclusion

The exact law relies on the independent bulk. With bulk-bulk gate edges, a qubit can transfer entropy through another noncontact qubit after its last direct contact gate, so its terminal noise need not remain a separately movable local channel. The general [distance converse](converse.md) continues to apply there; Theorem 7 does not supply an arbitrary-graph optimum or prove universal optimality of SWAP routing.

The disjoint-edge layer is also essential. A simultaneous many-body or summed Hamiltonian interaction between one ancilla and many data spins changes its contact throughput. A microscopic reset duration, heating during a reset pulse, protected workspace, bulk measurements, or observation-conditioned feedback changes the model. These distinctions are made explicitly in the [literature comparison](../references/RELATED_WORK.md#one-cold-contact-and-coherent-control).

The result concerns common-time purity and input-reference decoupling of every physical output. It does not prohibit cooling a selected subsystem while leaving other outputs dirty, give a thermodynamic heat/work law, or establish an advantage over classical reset scheduling. Its physical consequence is an exact design rule for a shared ideal reset interface under continuing local heating.
