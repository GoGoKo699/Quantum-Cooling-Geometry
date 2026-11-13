# What contact geometry changes

An ideal cold contact can erase the qubit that reaches it. Bulk noise continues to act while the controller moves entropy around the register. At a common output time, noise that occurred too far from a contact has had no opportunity to reach an entropy outlet. The [converse](converse.md) makes this causal picture exact even when the controller uses arbitrary local entangling gates or coherent compression.

On a path the right geometric quantity is the sum of distances to the nearest contact, not just the largest distance or the number of contacts:

```math
M(P_n,S)=\sum_{v=1}^n\operatorname{dist}(v,S),
\qquad
\epsilon_*\asymp\min\{1,pM(P_n,S)\}.
```

Here $`\asymp`$ denotes upper and lower bounds by absolute positive constants when $`M>0`$. The [construction](geometry.md) attains this order with ordinary SWAP gates and independent contact resets. No better quantum compression strategy changes the order in this model.

## One endpoint contact

For $`S=\{1\}`$,

```math
M=0+1+\cdots+(n-1)=\frac{n(n-1)}2.
```

The sum counts a triangular region of final noise opportunities. It yields $`\epsilon_*\asymp\min\{1,pn^2\}`$ for $`n\ge2`$. At small target error $`\epsilon`$, the supported chain length has order $`\sqrt{\epsilon/p}`$. Making the cooling schedule longer cannot remove this final-time floor.

For illustration, with $`n=100`$ and $`p=10^{-6}`$, the rigorous converse is approximately $`0.002469`$. The explicit endpoint conveyor has error approximately $`0.004888`$ and the simple analytic upper bound is $`0.0049005`$. These are dimensionless values in the stated round model, not hardware estimates; [verification](../verification/README.md) reproduces the finite formulas.

## The same contact count, different layouts

Take $`n=2m`$. Alternating contacts $`S=\{1,3,\ldots,2m-1\}`$ give $`M=m`$. Cluster the same $`m`$ contacts on the first half, $`S=\{1,\ldots,m\}`$, and instead

```math
M=1+2+\cdots+m=\frac{m(m+1)}2.
```

The optimal whole-register error therefore scales as $`\min\{1,pm\}`$ in the alternating layout and $`\min\{1,pm^2\}`$ in the clustered layout. Both conclusions permit arbitrary local quantum controls. Contact placement changes the asymptotic noise burden even when the number and quality of contacts are identical.

For arbitrary $`1\le m\le n`$, [optimal placement](geometry.md#optimally-placed-contacts-on-a-path) gives the exact minimum distance sum. Its uniform order is

```math
M_{n,m}^{\min}\asymp\frac{n(n-m)}m.
```

At sparse contact density this is $`n^2/m`$. Near full coverage the factor $`n-m`$ matters: when every site is a contact, one parallel final reset initializes the register exactly.

## Cooling from a full face

In a rectangular slab of thickness $`L`$ and cross-sectional size $`A`$, with the full face at one end cold, $`N=AL`$ and

```math
M=A\frac{L(L-1)}2=\frac{N(L-1)}2.
```

Independent longitudinal conveyors attain the same order as the converse, even though the converse permits transverse entangling controls. A cubic $`d`$-dimensional register therefore has small-error scale $`pN^{1+1/d}`$. For a two-dimensional square cooled from one edge it is $`pN^{3/2}`$; for a three-dimensional cube cooled from one face it is $`pN^{4/3}`$.

These statements concern all physical qubits at the same time. Mean energy density, a clean logical subsystem and partial-register cooling are weaker objectives with different attainable behavior. The graph lower bound remains valid beyond paths and slabs, but a matching upper on every graph is not claimed.
