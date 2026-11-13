# Reset-contact geometry and matching constructions

This page builds matching upper bounds for the [model](model.md), using the [arbitrary-control graph converse](converse.md). It gives an exact SWAP-channel calculation, a tight order for every fixed path contact set, optimal path placement, and slabs cooled from one full face.

## A one-contact path conveyor

Consider a path of $`\ell\ge2`$ qubits with a cold contact at its left endpoint. Apply SWAPs on bonds $`(1,2),(3,4),\ldots`$ in odd rounds and on $`(2,3),(4,5),\ldots`$ in even rounds, with the stipulated noise and a reset at site 1 after every layer. Take $`T=2\ell-1`$. For $`\ell=1`$, take one reset round and the output is exactly pure.

**Lemma 3 — complete replacement and output ages.** Every original qubit carrier visits the contact by time $`2\ell-1`$ and is discarded there. The multiset of the final carriers' noise ages since their last contact reset is
```math
\{0,1,3,5,\ldots,2\ell-3\}.
\tag{4}
```

**Proof.** In the odd/even SWAP network a carrier moves one site per round until it reaches an endpoint. At that endpoint it waits for one round and reverses direction. An original carrier initially moving left reaches site 1 in at most $`\ell-1`$ rounds. One initially moving right first reaches site $`\ell`$, waits one round, and then reaches site 1, in at most $`2\ell-1`$ rounds. Reset discards the visiting carrier and inserts a fresh $`|0\rangle`$ carrier.

After the last round the contact itself has age zero. The other final carriers are exactly the fresh carriers inserted at the even-numbered rounds $`2,4,\ldots,2\ell-2`$: carriers inserted in odd rounds below $`2\ell-1`$ sit at site 1 during the following even round and are immediately reset again. Each even-round carrier moves right on its next round and, if it reaches the far endpoint, bounces without returning to site 1 before the final time. Its age is $`(2\ell-1)-2k`$, giving the odd numbers in (4). $`\square`$

Depolarization acts independently on these SWAP trajectories. All original carriers and their reference correlations have been discarded. The resulting channel is therefore exactly a replacement channel by a diagonal product state, independent of its input. A carrier of age $`a`$ has state
```math
\rho_a=\frac12\bigl[I+(1-p)^a Z\bigr].
```
Because the output is diagonal in the target basis, its half trace distance to the all-zero target equals one minus target population. Thus the conveyor's exact half-diamond error is
```math
\boxed{\displaystyle
\epsilon_{\rm conv}(\ell,p)
=1-\prod_{k=1}^{\ell-1}
\frac{1+(1-p)^{2k-1}}2.}
\tag{5}
```
The empty product for $`\ell=1`$ is one. In particular,
```math
\epsilon_{\rm conv}(\ell,p)
\le\frac p2\sum_{k=1}^{\ell-1}(2k-1)
=\frac p2(\ell-1)^2.
\tag{6}
```
For a fixed endpoint contact, $`M=\ell(\ell-1)/2`$. The [graph converse](converse.md) and (6) establish
```math
\inf_{T,\Phi_T}\epsilon(\Phi_T,0^{\otimes\ell})
=\Theta\!\left(\min\{1,p\ell(\ell-1)\}\right)
```
uniformly for $`\ell\ge2`$ and $`0\le p\le1`$, with universal constants. The known-gate depth of the upper is $`2\ell-1`$; its gates, reset count, and noise exposure are explicit. No compression oracle or ideal bulk correction is used.

## Every fixed contact placement on a path

The distance-sum converse also has a matching upper for every nonempty fixed contact set on a path; it is not limited to an optimized layout.

**Theorem 4 — fixed path placement.** For every $`\varnothing\ne S\subseteq V(P_n)`$, let $`M=M(P_n,S)`$. Then
```math
\frac{1-(1-p)^M}{2}
\le\inf_{T,\Phi_T}\epsilon(\Phi_T,0^{\otimes n})
\le\min\{1,pM\}.
\tag{7a}
```
For $`M\ge1`$ this is $`\Theta(\min\{1,pM\})`$ with universal constants. For $`M=0`$, every site is a contact and the exact optimum is zero after one reset round.

**Proof of the upper.** Partition the path into contiguous nearest-contact cells, breaking ties consistently. Each cell contains exactly one contact, at any position in that cell. Its contribution $`M_{\rm cell}`$ to $`M`$ is its sum of distances to that contact.

Within this cell apply the same odd/even full-cell SWAP brickwork as above, but reset its actual contact position. Run $`2a`$ rounds. Every original carrier visits every site during a period of $`2a`$ rounds, so it visits the contact and is discarded. This visitation property can be seen by unfolding the bouncing trajectory into a cycle of length $`2a`$: the position function on phases $`z=0,\ldots,2a-1`$ is
```math
f(z)=1+\min\{z,2a-1-z\}.
```
Each carrier advances one phase per round. At time zero an odd-positioned carrier $`j`$ has phase $`j-1`$, and an even-positioned one has phase $`2a-j`$. These phases reproduce the odd/even SWAP layers, including the one-round wait at each endpoint. The cycle visits every physical site.

Run all cells from a common starting time to $`T=2\max_i a_i`$, using their local odd/even SWAP pattern and resetting every contact after every noise layer. Every original carrier has been discarded by that time. The cell channel is exactly a diagonal-product replacement channel. Its target error is bounded by $`(p/2)`$ times the sum of its final carrier ages, as in (6).

To bound that sum sharply, consider one arm of length $`b`$ from the contact to a cell endpoint. A fresh carrier travels outward one edge per round, waits one round at the outer endpoint, and returns inward until the contact discards it. At distance $`x\in\{1,\ldots,b\}`$, its age is $`x`$ in its outward phase and $`2b+1-x`$ in its inward phase. Count the endpoint's waiting phase as inward. At a fixed round the inward positions form one parity class of $`x`$, by the alternating SWAP checkerboard. Therefore
```math
\sum_{x=1}^b\mathrm{age}(x)
=\frac{b(b+1)}2
+\sum_{x\in P}(2b+1-2x)
\in\{b^2,b(b+1)\},
```
where $`P`$ is the odd or even positions. The total when the inward positions are odd equals $`b(b+1)`$, and the total when they are even equals $`b^2`$; these follow directly by summing the two arithmetic progressions and hold for either parity of $`b`$. The empty arm $`b=0`$ contributes zero.

Adding the two arms and the zero-age contact gives
```math
\sum_{\text{final carriers}}\mathrm{age}
\le2\sum_{v\in\mathrm{cell}}d(v,\mathrm{contact})
=2M_{\rm cell}.
```
The cell error is consequently at most $`pM_{\rm cell}`$. The tensor product of these replacement channels has error at most the sum of its cell errors, yielding (7a). No gate crosses a cell boundary. $`\square`$

The upper uses depth $`2\max_i a_i`$, with resets in every round and no extra qubits. Short cells continue their periodic conveyors until the common output time; the age bound holds in either steady phase, so there is no idle-output penalty. The accompanying finite verification checks token loss, the arm formulas, and both late phases for every contact position in cells of sizes $`1`$ through $`80`$. The cycle and arm arguments prove the arbitrary-size statements.

## Optimally placed contacts on a path

Let $`1\le m\le n`$, and minimize $`M(P_n,S)`$ over all $`m`$-vertex contact sets. Write
```math
n=qm+r,\qquad q=\lfloor n/m\rfloor,\qquad 0\le r<m.
```

**Proposition 5 — exact placement cost.** The minimum distance sum is
```math
\boxed{\displaystyle
M_{n,m}^{\min}
=(m-r)\left\lfloor\frac{q^2}{4}\right\rfloor
+r\left\lfloor\frac{(q+1)^2}{4}\right\rfloor.}
\tag{7}
```
It is attained by partitioning the path into $`m-r`$ contiguous cells of size $`q`$ and $`r`$ of size $`q+1`$, with a contact at a median vertex of each cell.

**Proof.** A contiguous cell of $`a`$ vertices has minimum distance sum to one contact
```math
g(a)=\left\lfloor\frac{a^2}{4}\right\rfloor,
```
attained at a median. For any contact set, assign each path vertex to a nearest contact, breaking ties consistently so the cells are contiguous. Its distance sum is at least $`\sum_i g(a_i)`$, where $`a_i\ge1`$ and $`\sum_i a_i=n`$. The discrete increments
```math
g(a+1)-g(a)=\left\lceil\frac a2\right\rceil
```
are nondecreasing. Balancing two cell sizes cannot increase their sum of costs, so the displayed balanced sizes minimize $`\sum_i g(a_i)`$, giving the lower bound (7). Place medians in such balanced cells. Assigning each cell to its own median costs exactly (7), while the actual nearest-contact cost can only be smaller. The lower bound already proved makes it equal. $`\square`$

This exact finite formula handles the dense-contact boundary. In particular,
```math
M_{n,m}^{\min}=n-m
\quad\text{when }m\ge\lceil n/2\rceil,
\qquad M_{n,n}^{\min}=0.
\tag{8}
```
More generally, setting $`C_{n,m}=n(n-m)/m`$,
```math
\frac14 C_{n,m}\le M_{n,m}^{\min}\le C_{n,m}.
\tag{9}
```
For the lower bound use $`g(a)\ge a(a-1)/4`$ and $`\sum_i a_i^2\ge n^2/m`$. For the upper, balanced cells satisfy $`a_i\le\lceil n/m\rceil\le2n/m`$, and $`g(a_i)\le a_i(a_i-1)/2\le(n/m)(a_i-1)`$. Sum over cells. All terms vanish when $`m=n`$.

Define the best error with $`m`$ freely placed contacts by
```math
\epsilon^*_{n,m}(p)
=\inf_{|S|=m}\inf_{T,\Phi_T}
\epsilon(\Phi_T,0^{\otimes n}).
```

**Theorem 6 — path contact-accuracy frontier.** For every $`n,m,p`$ in the stated domains,
```math
\frac{1-(1-p)^{M_{n,m}^{\min}}}{2}
\le\epsilon^*_{n,m}(p)
\le\min\{1,pM_{n,m}^{\min}\}.
\tag{10}
```
For $`m<n`$, consequently,
```math
\boxed{\displaystyle
\epsilon^*_{n,m}(p)
=\Theta\!\left(\min\left\{1,
p\,\frac{n(n-m)}m\right\}\right).}
\tag{11}
```
For $`m=n`$, its exact value is zero after one round of contact resets.

**Achievability and order.** Use the balanced median-contact placement from Proposition 5 and Theorem 4's fixed-placement conveyor. The construction has depth $`2\lceil n/m\rceil`$ and error at most $`pM_{n,m}^{\min}`$. Its full channel is exactly replacement by a diagonal product state. If $`a_v`$ denotes a final carrier's noise age, its exact target fidelity is
```math
F_{\rm cells}=\prod_{v\in V}\frac{1+(1-p)^{a_v}}2,
\qquad \sum_v a_v\le2M_{n,m}^{\min}.
\tag{12}
```
The lower follows from the [graph converse](converse.md) and Proposition 5. For $`pM\ge1`$, the lower is at least $`(1-e^{-1})/2`$; for $`pM\le1`$, it is at least $`(1-e^{-1})pM/2`$. These constants and (9) establish the uniform order (11).

When $`m\le n/2`$, (11) simplifies to $`\Theta(\min\{1,pn^2/m\})`$. Using that simplification at $`m=n`$ would be wrong; the factor $`n-m`$ in the uniform statement is essential.

## Rectangular slabs with one full cold face

Take the nearest-neighbor rectangular graph
```math
G=P_L\mathbin\square P_{L_2}\mathbin\square\cdots\mathbin\square P_{L_d},
\qquad
A=\prod_{j=2}^dL_j,\qquad N=AL,
```
where each side length is a positive integer. For $`d=1`$, use the empty product $`A=1`$. Let the entire face $`x_1=1`$ be cold, so $`|S|=A`$. A vertex at coordinate $`x_1`$ has contact distance $`x_1-1`$, even when transverse gates are allowed. Therefore
```math
\boxed{\displaystyle
M(G,S)=A\frac{L(L-1)}2
=\frac{N(L-1)}2.}
\tag{13}
```

For $`L\ge2`$, run independent endpoint conveyors along the $`A`$ longitudinal columns. They use no transverse gates and finish in $`2L-1`$ rounds. The exact error of this construction is
```math
\epsilon_{\rm slab,conv}
=1-\left[
\prod_{k=1}^{L-1}\frac{1+(1-p)^{2k-1}}2
\right]^A
\le\frac p2 A(L-1)^2.
\tag{14}
```
Combining with the arbitrary-local-circuit converse,
```math
\frac{1-(1-p)^{AL(L-1)/2}}2
\le\epsilon^*_{\rm slab}(p)
\le\min\left\{1,\frac p2 A(L-1)^2\right\}.
\tag{15}
```
Thus, uniformly over the positive side lengths and $`L\ge2`$,
```math
\boxed{\displaystyle
\epsilon^*_{\rm slab}(p)
=\Theta\!\left(\min\{1,pN(L-1)\}\right).}
\tag{16}
```
For $`L=1`$, every vertex lies on the cold face and one final reset gives exact error zero. Equation (16) is consistent with this degenerate limit when interpreted separately rather than invoking nonzero-order notation.

For a filled $`d`$-dimensional cube of side $`L\ge2`$, $`N=L^d`$, so the small-error noise scale is $`pN^{1+1/d}`$. At fixed small target error $`\varepsilon`$, the supported physical volume has order
```math
N=O_d\!\left((\varepsilon/p)^{d/(d+1)}\right),
```
and the explicit columns attain the same order. This concerns a whole pure physical register served by one cold face. It is not a threshold statement for an encoded logical subsystem, a bound on energy density, or an assertion about every graph with the same number of contacts.

## What geometry does and does not determine here

The quantity $`M(G,S)`$ is a universal obstruction: it counts unavoidable final noise opportunities whose entropy cannot reach any permitted sink before the required output. The path and full-face slab constructions show that this obstruction can be attained in order in those geometries. No matching upper is asserted for an arbitrary graph. Every fixed path placement is covered by Theorem 4. Routing congestion, local gate scheduling, and the locations of the contacts can create additional costs.

Every discarded syndrome register, bulk measurement, or supplied pure ancillary carrier creates an additional entropy outlet or changes the required output. Such resources require a new model. Likewise, local dephasing or amplitude damping that preserves a chosen pure state need not have the present depolarizing floor. The result prices unavoidable entropy-injecting noise and sparse reset access under the stated physical-output requirement.
