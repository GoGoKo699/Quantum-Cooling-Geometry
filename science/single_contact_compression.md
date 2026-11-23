# Cooling a register through one gateway

A single contact can purge arbitrary input information from a register by exchanging whole qubits. Once the register is nearly cold, the remaining errors are sparse. Reversible compression can send their locations to the contact using far fewer exchanges. The distinction changes the achievable global error even when both controllers use the same hardware, noise, and output time convention.

## Model and result

Use the [round and channel conventions](model.md): each round applies a disjoint-edge layer of one- and two-qubit gates, independent depolarization of strength $`p`$ on every site, and a prescribed operation on the reset contact. All qubits remain in the output, immediately after the final contact operation. The error $`\epsilon`$ is the half-diamond distance to all-zero replacement.

The $`m`$ bulk qubits form a complete graph, for $`m\ge1`$. The lone contact $`s`$ is adjacent only to the bulk gateway $`g`$. The unrestricted class permits every operation in the model. The **SWAP class** permits only SWAPs as two-qubit gates, with arbitrary prescribed one-qubit unitaries and contact operations. Both classes allow input-independent randomization, with no access to the noise or bath record. Denote their optimal errors by $`\epsilon_*(m,p)`$ and $`\epsilon_{\rm SWAP}(m,p)`$.

For every $`0\le p\le1`$, set $`h_p(a)=[1+(1-p)^a]/2`$. The SWAP optimum is exactly

```math
\epsilon_{\rm SWAP}(m,p)=1-\prod_{j=1}^{m}h_p(2j-1).
```

For each fixed $`c>0`$ there are positive constants $`a_c,b_c`$ such that, for $`0\le p\le\min\{1,c/m^2\}`$,

```math
a_c\,p m\log_2(2m)\ \le\ \epsilon_*(m,p)\ \le\ b_c\,p m\log_2(2m).
```

The construction uses the same $`m+1`$ physical qubits and $`O(m)`$ prescribed gates and rounds. In particular, for a fixed $`c>0`$ and $`p=c/m^2`$ as $`m\to\infty`$,

```math
\epsilon_{\rm SWAP}(m,c/m^2)\longrightarrow 1-e^{-c/2},
\qquad
\epsilon_*(m,c/m^2)=\Theta_c\!\left(\frac{\log m}{m}\right).
```

The separation compares whole-qubit routing with reversible compression. The compressor implements a permutation of computational-basis strings and uses that classical reversible mechanism inside the quantum circuit.

## Exact SWAP benchmark

Fix a deterministic routing controller and apply it to the maximally mixed register. SWAPs track distinguishable carrier trajectories. One-qubit operations and contact maps preserve product structure on this input. For each final bulk carrier that has left the contact, record the round of its **last** departure $`t`$. Only the bridge SWAP can produce a departure. In the next round a bridge SWAP would send this same carrier back to the contact, since it is still at the gateway. Consequently the last departures of distinct final carriers are separated by at least two rounds.

A final carrier whose last departure was at time $`t`$ experiences $`a=T-t+1`$ subsequent noise layers, including the layer of its departure. Its maximal eigenvalue is at most $`h_p(a)`$, by covariance of depolarization under each local rotation. A carrier that has never left the contact remains maximally mixed on the chosen input. If there are $`q`$ departure times, their ages in increasing order satisfy $`a_j\ge2j-1`$. The probability of the all-zero outcome on the final register is at most

```math
2^{-(m-q)}\prod_{j=1}^q h_p(a_j)
\ \le\ \prod_{j=1}^m h_p(2j-1).
```

Here the factors appended for absent departures are all at least $`1/2`$, and the contact contributes a factor at most one. The all-zero test gives the stated lower bound on half-diamond error. The same input witnesses it for every randomized choice of routing controller, so averaging preserves it.

For equality, first reset $`s`$. Start with a bridge SWAP, then alternate gateway-to-new-leaf SWAPs and bridge SWAPs, ending at the bridge. Reset $`s`$ after each noise layer. The $`m`$ departing carriers survive in the final bulk with ages $`1,3,\ldots,2m-1`$. This schedule discards every original carrier, including the initial contact and gateway inputs, and uses $`2m`$ rounds including the initial reset. The output channel is exact replacement by the diagonal tensor product of the states $`[I+(1-p)^{2j-1}Z]/2`$ and a pure contact. The half-diamond error of a replacement channel equals the trace distance of its output state to the target state. For this diagonal state the trace distance is one minus the all-zero probability. Finally at $`p=c/m^2`$ each factor equals $`1-(2j-1)p/2+O(p^2(2j-1)^2)`$, uniformly in $`j`$. The sum of the ages is $`m^2`$ and the sum of their squares is $`O(m^3)`$, so the log of the product tends to $`-c/2`$.

## Causal lower bound for arbitrary controls

Let $`n=m+1`$ and $`L=\max\{1,\lfloor\log_2 n\rfloor-1\}`$. Fix the controller's gate layer and contact map in every round. For a noise layer with $`k`$ future gate layers, take the union of the backward gate cones of the current and all subsequent contact operations. At the latest noise layer this set is $`\{s\}`$. Stepping backward through one disjoint gate layer keeps the existing sites and adds at most one partner per site. Adding the earlier contact contributes no new site, because $`s`$ is already included. Thus the union at age $`k`$ has at most $`2^k`$ sites.

If $`T\ge L`$, the last $`L`$ noise layers each have at least $`\lfloor n/2\rfloor`$ sites outside this union. A complete depolarization on any of these sites can be commuted through all remaining gates and contact maps as in the [terminal-event factorization](converse.md#a-depolarizer-that-cannot-reach-a-contact). To apply that argument to the independent noise, use the decomposition of each noise channel as identity with weight $`1-p`$ or complete depolarization with weight $`p`$. Conditional on at least one selected site depolarizing, leave the first selected depolarizer as a full channel and expand all other depolarizers into random Pauli unitaries. The surviving depolarizer leaves a unitarily conjugated maximally mixed qubit factor, hence all-zero probability at most $`1/2`$. This holds for every input. The all-zero effect therefore detects error at least

```math
\frac{1-(1-p)^{L\lfloor n/2\rfloor}}{2}.
```

For $`T<L`$, take the maximally mixed input. The backward union of the contact operations at the initial time has at most $`2^T<n`$ sites. Inserting a full depolarizer on a site outside it leaves this input unchanged. The same factorization gives half trace distance at least $`1/2`$ for that input. The common maximally mixed witness works for both duration cases and for randomization. Since $`L\lfloor n/2\rfloor=\Theta(m\log_2(2m))`$, the displayed bound is $`\Omega(\min\{1,pm\log_2(2m)\})`$ for all $`p`$. It gives the claimed lower bound on the weak-noise interval.

## A reversible compressor with a paid workspace

The following circuit on a block of $`u`$ bulk sites takes a basis input of Hamming weight at most two to a string supported on a prescribed set of $`O(\log_2(2u))`$ code sites. It uses $`O(\log_2(2u))`$ disjoint-edge layers and $`O(u)`$ gates. All temporary wires are within the block and end at zero on the promised strings. The same circuit also works for inputs of weight at most one. The circuit always runs, independent of the input or the noise.

For $`u<256`$, use the whole block as the code and apply no gates. For $`u\ge256`$, write $`d=\lfloor u/256\rfloor`$. Partition into $`d`$ groups of 256 sites, adding the remainder to the last group so each size is between 256 and 511. In a group of size $`v`$, map its $`1+v+\binom v2`$ strings of weight at most two, in weight-then-lexicographic order, to consecutive binary code values on its first 17 wires. The other $`v-17`$ output wires are zero on these strings. The count is at most $`1+511+\binom{511}{2}=130817<2^{17}`$. Complete this partial injection on the union of its input and output sets. Each open path is closed by sending its end back to its start. Existing cycles are retained and every other basis string stays fixed. Decompose its cycles into basis transpositions, then decompose each transposition along a Gray-code path into controlled bit flips. The exact [one- and two-qubit gate decomposition](https://doi.org/10.1103/PhysRevA.52.3457) needs no additional wires. Group sizes are bounded, so this stage has uniformly bounded depth and $`O(u)`$ gates when the disjoint groups run in parallel. The constants from this compilation are only used for the asymptotic resource bound.

The 17 code positions define 17 lanes, each consisting of one bit from each group. At most two groups can have nonzero codes, so every lane has weight at most two. There are at least $`239d`$ clean wires on a promised block input. Compress the 17 lanes in a fixed sequence, reusing this workspace. Compressing one lane leaves all other lane inputs alone.

### Encode one lane

Pad a lane of $`d`$ bits with clean zeros to length $`N=2^{\lceil\log_2 d\rceil}`$ and put its wires at the leaves of a full binary tree. Dummy leaves are scratch wires from the same block. For a node at height $`k`$, store its occupancy $`f`$ and $`k`$-bit addresses of its first and last occupied leaves, measured within that node. An empty node has both addresses zero. Leaves have only an occupancy bit. The **retained code** is a copy of the root occupancy and the two root addresses. For $`d=1`$, the code can simply be the lane bit.

1. Compute all internal occupancies from bottom to top. To write $`f_L\lor f_R`$ into a zero target use two CNOTs from the children and a Toffoli from both. Each level uses constant depth since its node triples are disjoint.
2. For each parent of height $`k`$, copy each child's occupancy into $`k-1`$ distinct work bits. Copy trees for different child flags are disjoint and run in parallel, in depth $`O(\log_2(2\log_2 N))`$ for $`N\ge2`$. Use these copies solely as controls in the next step.
3. Compute the addresses from bottom to top. For a parent let $`y_L,y_R`$ be the first-leaf addresses and $`z_L,z_R`$ the last-leaf addresses of its children. The new low bits are

   ```math
   y=y_L\mathbin{\oplus}[(\neg f_L)y_R],
   \qquad
   z=z_R\mathbin{\oplus}[(\neg f_R)z_L],
   ```

   with bitwise multiplication by a Boolean scalar. The respective high bits are $`f_R\land\neg f_L`$ and $`f_R`$. These are the correct first and last addresses, including when one or both children are empty. Each low-bit sublayer consists of one CNOT per output bit into a distinct zero target, then one negatively controlled Toffoli per output bit with its own flag copy. First and last registers are disjoint. The two high bits are computed in separate sublayers using the original flags. All parents at one height use disjoint qubits, and an exact Toffoli over three sites of the clique requires a fixed number of one- and two-qubit layers. Thus each tree height uses a constant number of disjoint-edge layers.
4. Copy the root registers into zero code wires using disjoint CNOTs, then reverse steps 3, 2, and 1. This returns every temporary bit other than the code and leaves the original lane intact.

### Clear the lane and restore the workspace

For each of the two retained addresses run a decoder on a separate binary tree of scratch bits. Copy the root occupancy into both decoder root flags. For each address bit, copy it in parallel into one scratch control per node at its split level. Different bit-copy trees, including the two address registers, have disjoint wires. Run the decoders from top to bottom. A node with flag $`g`$ and the corresponding address bit $`b`$ writes child flags $`g\land\neg b`$ and $`g\land b`$ into distinct zero targets with two serial Toffolis. Distinct nodes and the two decoders run in parallel. The decoder flags indicate precisely the first and last occupied leaves when the lane is nonempty. If it has one occupied leaf the same index occurs in both decoders. If empty, all decoder flags are zero.

For each real leaf, XOR the OR of its two flags into its original lane bit. Use a CNOT from each flag then a Toffoli controlled by both, with disjoint triples across leaves. A string of weight at most two is the OR of exactly these two indicators, so this step zeros the lane. Dummy leaves do not need an update. Reverse the decoder computations and fanouts. Their controls and targets are unchanged by the lane update, so all decoder scratch is restored. The retained code remains.

The following counts include every temporary wire. The bound on each stage holds for $`N\ge2`$, and the single-bit case needs no scratch.

| Purpose | Wires |
|---|---:|
| Dummy lane leaves | $`N-d`$ |
| Encoder internal occupancies | $`N-1`$ |
| Encoder first and last addresses | $`2\sum_{k=1}^{\log_2N}(N/2^k)k\le4N`$ |
| Encoder occupancy copies | $`2\sum_{k=1}^{\log_2N}(N/2^k)(k-1)\le2N`$ |
| Decoder node flags, including roots | $`2(2N-1)`$ |
| Decoder address copies | $`2(N-1)`$ |

Even counting both encoder and decoder scratch simultaneously gives fewer than $`16N\le32d`$ wires. Across all 17 lanes, the retained codes occupy at most $`17(1+2\lceil\log_2 d\rceil)\le68d`$ wires. Both allocations fit within the $`239d`$ sites already cleared by the microblock permutations, and all allocations can be fixed before execution. A fresh lane uses the same encoder and decoder scratch, excluding the retained codes of preceding lanes. For each lane the ascending and descending traversals take $`O(\log_2(2d))`$ depth. The total gate count is $`O(d)`$, by the same sums as in the table. Processing 17 lanes serially therefore preserves the stated depth and gate counts. No ancillas are supplied from outside the physical block. Scratch is clean only under the input promise and the fault-free compressor branch, which are charged below.

## Two compression passes under continuous noise

Reset the contact after each round throughout the controller, including the compression layers.

Fix $`0\le p\le\min\{1,c/m^2\}`$. First run the exact SWAP schedule, including the initial reset. This makes the register and every reference a product, for arbitrary initial joint states: every original carrier has been discarded. The bulk is a diagonal product with error probabilities at most $`pm`$ at each site, since a carrier of age $`a\le2m-1`$ is in state one with probability $`(1-(1-p)^a)/2\le pa/2`$. Every operation afterward is independent of the original input and acts only on the register. Thus the resulting full channel remains replacement even on the failure branches considered below.

Choose $`b=\lceil\sqrt{m\ln(2m)}\rceil`$ capped at $`m`$. Partition the bulk into blocks of at most $`b`$ sites, using $`\lceil m/b\rceil\le2m/b`$ blocks. The probability that any block has at least three errors is bounded by summing over triples of sites, using the product seed output:

```math
\mathbb P(\text{some block has weight at least 3})\le O(p^3m^4b^2).
```

**First pass.** Run the compressors in parallel over the blocks. A union bound charges probability at most $`O(pm\ln(2b))`$ for any complete depolarization during their $`O(\log_2(2b))`$ layers, including idle wires. If the block strings satisfy their promises and the compressors have no such fault, all occupied bits at the end of compression are within the prescribed code positions. Their total number is bounded by $`K=O(m\ln(2b)/b)`$, including the code positions that contain zero in a given branch.

Discard these $`K`$ carriers through the single contact in a fixed order. If the gateway itself is in the code, discard it first by a bridge SWAP and reset. For each other coded site, swap its carrier into the gateway and then swap across the bridge, resetting the contact after every round. The process uses at most $`2K`$ rounds. Whether or not the gateway was initially in the code, in the ideal successful branch the gateway starts zero or becomes zero immediately after its own discard. Pure resets provide the subsequent clean gateway carriers. The empty code needs no routing.

Keep the full noise during this first discard stage. Conditional on success before the stage, the remaining final carriers all started from logical zero, either in an unencoded site before routing or upon preparation at the contact. All the initial code carriers are discarded. Each surviving carrier follows a separate space-time trajectory through the SWAP layers, so the local noise factors governing distinct final carriers are independent. The result on this branch is a new product with excitation probabilities at most $`O(pK)`$, regardless of the first pass's code values. The contact is pure after the last reset. Consequently,

```math
\mathbb P(\text{bulk weight after first routing is at least 2}\mid\text{first compression succeeds})
\ \le\ O(p^2m^2K^2)
\ =\ O\!\left(\frac{p^2m^4\ln^2(2b)}{b^2}\right).
```

**Second pass.** Run the same reversible compressor once on the entire bulk, then discard its $`O(\log_2(2m))`$ code positions through the gateway. This succeeds on bulk weight at most one if the second pass has no complete depolarization. Charge every noisy system site during the compression and routing in this pass, for a total fault probability at most $`O(pm\ln(2m))`$.

All the events used above are for analysis. The controller follows the same circuit on every branch. It neither queries noise flags nor conditions a reset on whether compression succeeded. The final state on the joint good event is exactly zero, so the probability of its complement is an upper bound on the output trace distance and hence on complete-channel error. Summing the four probabilities yields

```math
\epsilon_*\le O\!\left(pm\ln(2m)+p^3m^4b^2
+\frac{p^2m^4\ln^2(2b)}{b^2}\right).
```

Since $`b^2=\Theta(m\ln(2m))`$ and $`\ln(2b)\le\ln(2m)`$, the second and third terms are bounded by $`O(pm\ln(2m))`$ times $`(pm^2)^2`$ and $`pm^2`$, respectively. These ratios are bounded at the prescribed $`p`$. This proves the matching unrestricted upper bound. All prescribed gates, rounds, reset operations and physical sites are counted. In particular, $`K=O(m\ln(2b)/b)`$ is at most $`O(m)`$, and the two compressor passes use $`O(m)`$ gates each. The linear-length initial routing sets the total circuit depth. The construction needs only one ideal contact, with no measurement, protected workspace or discarded bulk output.

## Prior work and the scope of the comparison

The [verification guide](../verification/README.md#single-contact-compression) documents finite gate and routing checks.

Reversible entropy concentration followed by bath resets is the central mechanism of [Boykin et al.'s algorithmic cooling](https://doi.org/10.1073/pnas.241641898). The [one-port fermionic reset construction](https://github.com/GoGoKo699/Fermionic-Reset-Complexity/blob/7cc91ccf5f1e7b503a95105b6d0b6885e1088349/science/interacting_reset.md) also compresses low-weight errors and retains every system output. Its resource is integrated loss action under fast parity-preserving control. Here the bottleneck is a single discrete bridge and noise acts during every gate and idle layer. The exact routing comparator and the sharp simultaneous preparation law account for both restrictions.

[Chen et al.](https://arxiv.org/abs/2206.11166) and [Luo and Li, Lemma 13](https://arxiv.org/html/2406.16142v1#S3) supply prior one-hot to binary conversion circuits. The construction above uses the first and last positions for up to two excitations per lane, creates clean scratch inside the paid register on the sparse branch and erases that scratch before routing. The logarithmic-depth encoding alone gives no cooling guarantee without the two paid compression and discard passes.

[Li et al., Proposition 1](https://arxiv.org/html/2601.16317v1) solve the fixed two-sort cooling steady state under a global depolarizing approximation. [Sur et al., Sections II.1–II.2](https://arxiv.org/html/2603.03917v1) study whole-network purification through repeated ancillary reset with simultaneous summed exchange couplings. The present theorem uses exact local depolarization at every layer, disjoint two-qubit gates and a common output time for the contact and all data qubits. The existing [independent-bulk result](contact_throughput.md) gives exact SWAP optimality where there are no edges between data qubits. The gateway example demonstrates how bulk gates change that conclusion. Determining the unrestricted crossover when $`p`$ grows above $`O(m^{-2})`$ requires additional analysis.
