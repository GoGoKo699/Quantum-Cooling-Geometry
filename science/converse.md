# Late noise gives a geometry-dependent error floor

The [model](model.md) allows arbitrary prescribed local coherent control and even joint CPTP operations on the reset set. The proof identifies a part of the noise that cannot reach any contact before the output is required. It uses an exact channel factorization, rather than an assumption that different faults produce independent output errors.

## A depolarizer that cannot reach a contact

Complete depolarization on a qubit is a Pauli twirl:

```math
\mathcal E_v(X)
=\frac14\sum_{P\in\{I,X,Y,Z\}}P_vXP_v^\dagger.
```

Consider one occurrence of $`\mathcal E_v`$ at any point in a circuit. Suppose its entire future gate cone is disjoint from $`S`$ at every subsequent contact operation. Condition all other noise channels into unitary trajectories, leaving this occurrence as the full depolarizer.

Move this depolarizer forward through the circuit. Under a future unitary $`U`$, it becomes $`\mathrm{Ad}_U\circ\mathcal E\circ\mathrm{Ad}_{U^\dagger}`$. Its Kraus operators remain a conjugated copy of the qubit Pauli algebra, supported inside the evolving gate cone. At each contact operation their support is disjoint from $`S`$, so the corresponding channel commutes with that CPTP map. Continue until the depolarizer is the last map.

The resulting conditional output has the form

```math
\rho_{\mathrm{out}}
=W\left(\frac{I_v}{2}\otimes\tau_{V\setminus\{v\}}\right)W^\dagger
```

for some global unitary $`W`$ and density matrix $`\tau`$. In particular,

```math
\|\rho_{\mathrm{out}}\|_\infty\le\frac12.
```

This remains true when the earlier input is mixed or reference-entangled. The same factorization holds with the reference included in $`\tau`$; taking its partial trace gives the displayed register state. Averaging the other unitary trajectories preserves the largest-eigenvalue bound by convexity.

The conclusion does not rely on a general claim that reset maps preserve largest eigenvalues. They do not. It relies specifically on commuting the surviving depolarizer past every reset before bounding the final output spectrum.

## Count terminal noise locations

For a depth-$`T`$ protocol, label a noise layer by $`t\in\{1,\ldots,T\}`$. There are $`T-t`$ future gate layers after that noise. A disturbance at $`v`$ cannot reach a contact if

```math
T-t<d_v.
```

The terminal set and its size are therefore

```math
\mathcal L_T
=\{(v,t):1\le t\le T,\ T-t<d_v\},
\qquad
M_T=|\mathcal L_T|=\sum_v\min\{T,d_v\}.
```

This uses only the graph's unit propagation speed per disjoint gate layer. It includes locations where the chosen gates spread an operator more slowly, so it is a valid lower bound for every admissible circuit.

Represent each $`\mathcal D_{p,v}`$ by an independent Bernoulli choice between the identity and $`\mathcal E_v`$. Let $`A`$ be the event that at least one complete depolarizer occurs in $`\mathcal L_T`$. Then

```math
\Pr(A)=1-(1-p)^{M_T}.
```

For each occurrence pattern in $`A`$, choose one terminal depolarizer by a deterministic rule depending only on that pattern, such as the latest time followed by a fixed site order. Keep this selected occurrence as the full channel. Expand every other occurrence of $`\mathcal E`$ into its random Pauli representation and condition those Pauli choices.

The selected occurrence still satisfies the preceding lemma. Choosing it from the Bernoulli pattern does not reveal or condition its Pauli label. Thus, for every register input and every pure register vector $`|\psi\rangle`$,

```math
\langle\psi|\Psi_T(\rho)|\psi\rangle
\le (1-\Pr(A))+\frac12\Pr(A)
=\frac{1+(1-p)^{M_T}}2.
```

Averaging is essential: the Bernoulli labels are a mathematical decomposition of an unobserved channel, not an accessible detection record or a postselection resource.

For the target $`|0^n\rangle`$, the measurement with effect $`|0^n\rangle\langle0^n|`$ gives

```math
\frac12\|\Psi_T(\rho)-|0^n\rangle\langle0^n|\|_1
\ge1-\langle0^n|\Psi_T(\rho)|0^n\rangle
\ge\frac{1-(1-p)^{M_T}}2.
```

The diamond error includes this input test, so the same lower bound applies to complete initialization.

## Remove the duration dependence

If $`T\ge R`$, then $`M_T=M(G,S)`$ and the desired bound already follows.

For $`T<R`$, select a site $`v`$ with $`d_v>T`$ and use the maximally mixed register input $`I/2^n`$. Insert a complete depolarizer $`\mathcal E_v`$ at the input; it leaves this state unchanged. Expand all actual depolarizing noise into random Pauli unitaries. The inserted depolarizer's forward cone misses every contact through all $`T`$ rounds, so the same factorization lemma gives an output largest eigenvalue at most $`1/2`$. Its distance from a pure target is consequently at least $`1/2`$.

This covers the shallow case because $`[1-(1-p)^M]/2\le1/2`$. It also handles depth zero. Combining both cases gives, for every duration and all admissible controls,

```math
\boxed{\displaystyle
\epsilon(\Psi_T)\ge\frac{1-(1-p)^{M(G,S)}}2.}
```

Taking the infimum over finite depths proves the graph converse. The argument is uniform when the gates and depth depend on $`p`$; it does not assume a protocol that would reset exactly at zero noise.

## What the converse establishes

The proof counts noise events whose entropy cannot reach a contact by the final time, and then shows that arbitrary coherent compression cannot conceal even one selected event while returning a globally pure physical register. It does not count every circuit location as fatal, and it does not assume independent final errors.

For general graphs this is a lower bound only. Routing congestion and contact throughput can require additional time or increase attainable error. The [path and slab constructions](geometry.md) prove tight order in the geometries stated there. [Other noise models](noise_and_scope.md) identify precisely which part of the argument survives beyond depolarization.
