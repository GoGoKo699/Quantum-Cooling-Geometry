# Physical initialization through reset contacts

Consider a register whose entropy can leave only through selected cold contacts. Local control must move entropy to those contacts, while bulk noise keeps injecting it. The task here is synchronized initialization: every physical qubit must be close to its prescribed pure state at the same final time, and no information may remain in correlations with an external reference.

The full-register requirement distinguishes this task from cooling a selected subsystem while discarding or retaining dirty workspace. The result is an accuracy law for a discrete local circuit model. It does not assign a thermodynamic work or heat cost to the cold contacts.

## Register, contacts, and round convention

Let $`G=(V,E)`$ be a finite connected graph, with $`n=|V|`$ qubits and a nonempty reset set $`S\subseteq V`$. Write

```math
d_v=\mathrm{dist}_G(v,S),\qquad
R=\max_{v\in V}d_v,\qquad
M(G,S)=\sum_{v\in V}d_v.
```

Distances count graph edges. A round $`t=1,\ldots,T`$ consists, in this exact order, of:

1. A depth-one layer $`U_t`$ of arbitrary one-qubit gates and two-qubit gates on disjoint graph edges.
2. Independent, unobserved depolarization on every qubit, including idle qubits.
3. A prescribed completely positive trace-preserving map supported on $`S`$.

For a site $`v`$, define the complete depolarizer and the actual noise by

```math
\mathcal E_v(X)=\frac{I_v}{2}\otimes\mathrm{Tr}_v X,
\qquad
\mathcal D_{p,v}=(1-p)\,\mathrm{id}+p\,\mathcal E_v,
\qquad 0\le p\le1.
```

Tensor factors are placed in their original order. Set $`\mathcal N_p=\bigotimes_{v\in V}\mathcal D_{p,v}`$ and $`\mathcal B_t=\mathcal C_{t,S}\otimes\mathrm{id}_{V\setminus S}`$, where $`\mathcal C_{t,S}`$ is CPTP. The final register channel is

```math
\Psi_T=(\mathcal B_T\circ\mathcal N_p\circ\mathrm{Ad}_{U_T})
\circ\cdots\circ
(\mathcal B_1\circ\mathcal N_p\circ\mathrm{Ad}_{U_1}),
\qquad \mathrm{Ad}_U(X)=UXU^\dagger.
```

Allowing an arbitrary joint map on $`S`$ strengthens the converse. The attaining constructions use only independent perfect resets at those sites. The cold contacts have no accuracy or entropy-removal penalty in this model, so the lower bound holds even for ideal contacts.

The output is taken immediately after the last contact operation. Thus noise on a reset site can be removed in the same round. A model with mandatory noise after the final reset has an additional error contribution.

## Controls and retained resources

The depth and controls may depend on the known graph, reset locations, noise strength, and desired error. They are predetermined and do not observe the noise realization. Input-independent classical randomization is allowed: the converse holds for each control realization and hence for their mixture.

All $`n`$ qubits are arbitrary inputs and remain physical outputs. They may initially be correlated with each other and with an inaccessible reference. No additional protected quantum register, fresh bulk qubits, bulk measurements, or discarded bulk workspace is supplied. The contact CPTP maps may discard entropy locally at $`S`$; no quantum memory outside the retained register is carried from one round to the next. Measurement-conditioned global feedback is outside the stated control class.

The elapsed circuit depth $`T`$, the number and positions of contacts, and the noise strength per round are explicit. The model assumes exact unitary gates followed by the stated noise. It is not a theorem for simultaneous continuous-time Hamiltonian dynamics with finite control strength.

## Error criterion

The target replacement channel is

```math
\mathcal R_0(X)=\mathrm{Tr}(X)\,|0^n\rangle\langle0^n|.
```

Measure the complete initialization error by half the diamond distance:

```math
\epsilon(\Psi_T)
=\frac12\Vert \Psi_T-\mathcal R_0\Vert _\diamond
=\sup_{\rho_{VA}}\frac12
\left\Vert (\Psi_T\otimes\mathrm{id}_A)(\rho_{VA})
-|0^n\rangle\langle0^n|\otimes\rho_A\right\Vert _1.
```

A reference of dimension $`2^n`$ suffices. This criterion requires both physical purity and decoupling from the input reference. Define $`\epsilon_*(G,S,p)`$ as the infimum over all finite depths and admissible controls, including the depth-zero identity if desired.

## Main statements

For every graph and reset set above,

```math
\boxed{\displaystyle
\epsilon_*(G,S,p)\ge
\frac{1-(1-p)^{M(G,S)}}2.}
```

The [converse](converse.md) is uniform in duration and in noise-dependent controls. The number $`M(G,S)`$ counts terminal noise locations from which no signal can reach a contact before the common output time.

On a path $`P_n`$, a matching constructive upper bound holds for every nonempty fixed reset set:

```math
\boxed{\displaystyle
\frac{1-(1-p)^{M(P_n,S)}}2
\le\epsilon_*(P_n,S,p)
\le\min\{1,pM(P_n,S)\}.}
```

Consequently, whenever $`M(P_n,S)>0`$,

```math
\epsilon_*(P_n,S,p)
=\Theta\!\left(\min\{1,pM(P_n,S)\}\right)
```

with absolute constants. If every site is a contact, $`M=0`$ and a final parallel reset initializes the register exactly. A single qubit with its own contact is included in this zero-error case. See [geometry and constructions](geometry.md) for the path theorem, optimal contact placement, and slabs with a fully cooled face. The graph converse does not by itself give a matching construction on every graph.

## Interpretation of the scale

For $`pM\ll1`$, the lower bound is $`pM/2+O((pM)^2)`$. It identifies the optimal order, not the exact finite-size optimum or its leading constant. For $`pM\gtrsim1`$, the converse supplies a constant error floor approaching $`1/2`$; it does not assert that every protocol's error approaches one.

At prescribed error $`0\lt \epsilon\lt 1/2`$ and $`0\lt p\lt 1`$, a necessary condition is

```math
M(G,S)\le
\frac{\ln(1-2\epsilon)}{\ln(1-p)}.
```

Both logarithms are negative. On paths, $`pM\le\epsilon`$ is sufficient by the construction. The [physical consequences](interpretation.md) turn this into register-size and contact-placement rules, while stating the limits for logical cooling and other noise models.
