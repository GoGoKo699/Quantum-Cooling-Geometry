# Thirty milestones in Quantum Cooling Geometry

This is a common understanding map for the scientific project. Its single educational anchor is John Watrous, *The Theory of Quantum Information* (2018), used through the [Watrous bridge](WATROUS_BRIDGE.md). The [scientific overview](../science/README.md) and the linked proof pages remain authoritative.

The allocation is **12 background/preliminary milestones and 18 narrative/innovation milestones**. The background builds from one qubit to the complete physical-register reset task. The narrative first develops the terminal-event converse and the path/slab transport constructions. It then explains why a contact can be a bottleneck even when every bulk site is only one edge away, and derives the exact contact-throughput optimum and its attaining assignment/SWAP schedule. The longer narrative connects complete-channel guarantees to both distance and contact capacity. The map covers the complete story, rather than every calculation or neighboring cooling problem.

## Background and preliminaries — M01 to M12

### M01 — The state of one physical qubit

**Central question.** What distinguishes a pure initialized qubit from a maximally mixed one?

**Understanding target.** Interpret density matrices, eigenvalues, the target $`|0\rangle\langle0|`$, and the tracial state $`I/2`$ as operationally different physical states.

**Dependencies and story role.** None; this supplies the local object that both heating and reset act on.

**Conceptual connection.** The eventual obstruction is a surviving maximally mixed qubit factor, so physical purity must have a precise meaning from the start.

**Sources.** Watrous, Chapter 2, through the [bridge](WATROUS_BRIDGE.md); [local noise and target](../science/model.md#register-contacts-and-round-convention).

### M02 — Composite registers and inaccessible references

**Central question.** Why can a register look simple locally while still carrying information in correlations?

**Understanding target.** Distinguish a tensor-product state, correlations within the register, and entanglement with an inaccessible reference; explain what a partial trace discards.

**Dependencies and story role.** M01; this moves from an individual qubit to the physical register and its environment.

**Conceptual connection.** Initialization must remove input information held in correlations as well as improve individual qubit populations.

**Sources.** Watrous, Chapter 2, through the [bridge](WATROUS_BRIDGE.md); [retained resources](../science/model.md#controls-and-retained-resources).

### M03 — Operations that preserve or remove information

**Central question.** How does a unitary gate differ from a channel that resets a qubit?

**Understanding target.** Identify unitary conjugation and CPTP maps, and explain why a reset can discard entropy while a unitary alone cannot turn every input into one pure output.

**Dependencies and story role.** M01–M02; this introduces the two distinct control resources.

**Conceptual connection.** Coherent gates transport and rearrange information; contact channels supply the permitted entropy outlets.

**Sources.** Watrous, Chapter 2, through the [bridge](WATROUS_BRIDGE.md); [contact maps and circuit composition](../science/model.md#register-contacts-and-round-convention).

### M04 — Replacement as a complete reset task

**Central question.** What does it mean to erase an arbitrary input rather than prepare one favorable input?

**Understanding target.** Explain the replacement channel $`\mathcal R_0(X)=\mathrm{Tr}(X)|0^n\rangle\langle0^n|`$ and why its action must be independent of the supplied register state.

**Dependencies and story role.** M02–M03; this specifies the global operation the project seeks to approximate.

**Conceptual connection.** A cooling protocol for one known initial state need not initialize an unknown register or decouple its reference.

**Sources.** Watrous, Chapter 2, through the [bridge](WATROUS_BRIDGE.md); [error criterion](../science/model.md#error-criterion).

### M05 — Depolarization as a channel with two representations

**Central question.** How can the same unobserved noise be described by a depolarizing event or by random Pauli gates?

**Understanding target.** Relate $`\mathcal D_p=(1-p)\mathrm{id}+p\mathcal E`$ to the Pauli-twirl representation of $`\mathcal E`$, without treating either decomposition as an accessible noise record.

**Dependencies and story role.** M01 and M03; this supplies the exact local-noise mechanism used in the proof.

**Conceptual connection.** Keeping one full depolarizer while resolving the others into unitary trajectories will make a protocol-uniform argument possible.

**Sources.** Watrous, Chapters 2 and 4, through the [bridge](WATROUS_BRIDGE.md); [Pauli twirl](../science/converse.md#a-depolarizer-that-cannot-reach-a-contact).

### M06 — Independent noise across space and time

**Central question.** What does independence allow one to calculate, and what does it not imply about final errors?

**Understanding target.** Interpret the tensor product of local noise channels and independent event indicators across rounds; distinguish them from independence of the final output faults.

**Dependencies and story role.** M02 and M05; this connects one local channel to a noisy circuit history.

**Conceptual connection.** The converse computes the probability of a spacetime event, without assuming that different circuit faults remain independent after coherent processing.

**Sources.** Watrous, Chapter 2, through the [bridge](WATROUS_BRIDGE.md); [noise convention](../science/model.md#register-contacts-and-round-convention) and [terminal-event counting](../science/converse.md#count-terminal-noise-locations).

### M07 — Distinguishing a state from its pure target

**Central question.** How can target population give a lower bound on state-preparation error?

**Understanding target.** Explain half trace distance as distinguishability and use the target-projector measurement to relate it to $`1-\langle0^n|\rho|0^n\rangle`$.

**Dependencies and story role.** M01–M02; this turns a statement about output overlap into an observable error statement.

**Conceptual connection.** A bound on the output spectrum will later be converted into an operational reset obstruction.

**Sources.** Watrous, Chapter 3, through the [bridge](WATROUS_BRIDGE.md); [target test](../science/converse.md#count-terminal-noise-locations).

### M08 — Error of a channel, including reference correlations

**Central question.** Why is one tested state insufficient to establish a universal reset upper bound?

**Understanding target.** Interpret half diamond distance, the reference-assisted supremum, and the asymmetry between a fixed-input lower bound and a uniform channel upper bound.

**Dependencies and story role.** M02, M04, and M07; this completes the project's accuracy language.

**Conceptual connection.** The converse can use one input, whereas the conveyor must erase every input and all its reference correlations.

**Sources.** Watrous, Chapter 3, through the [bridge](WATROUS_BRIDGE.md); [complete initialization error](../science/model.md#error-criterion).

### M09 — A mixed factor survives unitary changes of coordinates

**Central question.** Why can coherent spreading fail to hide a maximally mixed qubit inside a globally pure output?

**Understanding target.** Explain why $`W[(I/2)\otimes\tau]W^\dagger`$ has largest eigenvalue at most $`1/2`$, even when its mixed qubit is no longer attached to one physical site.

**Dependencies and story role.** M01–M03 and M07; this prepares the spectral step of the converse.

**Conceptual connection.** Local purity loss becomes a global obstruction that entangling unitary gates cannot remove by changing its representation.

**Sources.** Watrous, Chapters 2 and 4, through the [bridge](WATROUS_BRIDGE.md); [surviving depolarizer factor](../science/converse.md#a-depolarizer-that-cannot-reach-a-contact).

### M10 — Graph distance and exact gate cones

**Central question.** How far can an operation spread in a prescribed number of local gate layers?

**Understanding target.** Define distance to a contact and the covering radius, and relate disjoint nearest-neighbor gate layers to exact forward and backward causal cones.

**Dependencies and story role.** M03; this introduces spatial structure into the channel framework.

**Conceptual connection.** Exact circuit cones connect a local noise occurrence to the question of whether any entropy outlet remains reachable.

**Sources.** The [project bridge](WATROUS_BRIDGE.md), which supplies this circuit-locality step beyond the textbook foundations; [graph model](../science/model.md#register-contacts-and-round-convention) and [terminal locations](../science/converse.md#count-terminal-noise-locations).

### M11 — Which resources define the cooling problem?

**Central question.** Why do output timing, discarded workspace, and the locations of resets change the claim?

**Understanding target.** State the gates–noise–contacts ordering, predetermined controls, ideal contact maps, and requirement that every physical qubit remain an output at one common time.

**Dependencies and story role.** M03–M06, M08, and M10; this assembles the load-bearing resource boundaries.

**Conceptual connection.** Logical recovery, bulk measurements, and selected-qubit cooling offer different entropy outlets or output objectives.

**Sources.** [Model resources](../science/model.md#controls-and-retained-resources), [physical-output scope](../science/noise_and_scope.md#every-physical-output-is-part-of-the-task), and the [bridge](WATROUS_BRIDGE.md).

### M12 — The complete physical-register question

**Central question.** What must a valid lower bound and a matching construction establish under the same model?

**Understanding target.** Connect the register, contacts, local noise, graph geometry, and complete-channel error into one operational question, while distinguishing accuracy from heat or work.

**Dependencies and story role.** M01–M11; this is the background synthesis before the contribution is assembled.

**Conceptual connection.** It fixes the common task against which the universal obstruction and explicit SWAP protocol must be compared.

**Sources.** [Scientific overview](../science/README.md), [main statements](../science/model.md#main-statements), and the [Watrous bridge](WATROUS_BRIDGE.md).

## Narrative and innovation — M13 to M30

### M13 — A terminal region of noise opportunities

**Central question.** Which noise locations have too little time left to reach a cold contact?

**Understanding target.** Derive the terminal condition $`T-t\lt d_v`$ and the count $`M_T=\sum_v\min\{T,d_v\}`$; distinguish a count of late noise opportunities from a count of independent final faults.

**Dependencies and story role.** M06, M10, and M12; this turns graph distances into the spacetime object needed by the general converse.

**Conceptual connection.** The nearest contact may be ideal, but a late local disturbance still cannot reach it before the common output time.

**Sources.** [Terminal-location count](../science/converse.md#count-terminal-noise-locations) and the [locality bridge](WATROUS_BRIDGE.md).

### M14 — Move one selected depolarizer past all remaining contacts

**Central question.** How can a noisy coherent circuit yield a simple surviving channel factor?

**Understanding target.** Keep one terminal event as a full depolarizer, resolve all other noise into Pauli-unitary trajectories, and conjugate the selected channel through later gates. Explain why disjoint causal support makes it commute through every later contact map.

**Dependencies and story role.** M05–M06, M09–M10, and M13; this supplies the load-bearing channel factorization.

**Conceptual connection.** Conditioning is a mathematical proof device; no noise flag or measurement-conditioned feedback is given to the controller.

**Sources.** [Selected-channel factorization](../science/converse.md#a-depolarizer-that-cannot-reach-a-contact) and the [worked proof bridge](WATROUS_BRIDGE.md).

### M15 — From a mixed factor to a finite-noise error bound

**Central question.** What operational obstruction follows from at least one surviving depolarizer?

**Understanding target.** Use the form $`W[(I/2)\otimes\tau]W^\dagger`$, its largest eigenvalue at most $`1/2`$, and the all-zero target test. Average occurrence patterns to obtain $`\epsilon\ge[1-(1-p)^{M_T}]/2`$.

**Dependencies and story role.** M07–M09 and M13–M14; this joins the local mechanism to an unconditional circuit bound.

**Conceptual connection.** Coherent compression may relocate the mixed degree of freedom, while the task retains every physical output.

**Sources.** [Spectral obstruction](../science/converse.md#a-depolarizer-that-cannot-reach-a-contact), [event probability](../science/converse.md#count-terminal-noise-locations), and the [bridge](WATROUS_BRIDGE.md).

### M16 — A graph bound that no choice of duration evades

**Central question.** Why do both short and long cooling schedules obey the distance-sum floor?

**Understanding target.** For $`T\ge R`$, identify $`M_T=M=\sum_vd_v`$. For $`T\lt R`$, use a maximally mixed input and an inserted unreachable depolarizer. Interpret $`[1-(1-p)^M]/2`$ at small noise and when every site is a contact.

**Dependencies and story role.** M10–M12 and M15; this completes the arbitrary-control, duration-independent graph converse.

**Conceptual connection.** The general lower bound is neither an exact finite-size optimum nor a matching construction on every graph.

**Sources.** [Remove the duration dependence](../science/converse.md#remove-the-duration-dependence) and [interpret the scale](../science/model.md#interpretation-of-the-scale).

### M17 — A path conveyor really erases the whole input

**Central question.** How does a local SWAP sequence become a reference-uniform replacement channel?

**Understanding target.** Follow the odd/even carrier routes until all original carriers reach the contact. Derive the final age multiset $`\{0,1,3,\ldots,2\ell-3\}`$ and the product of zero probabilities for the resulting diagonal replacement state.

**Dependencies and story role.** M02–M08, M10, and M16; this constructs an admissible controller rather than only testing one favorable input.

**Conceptual connection.** A carrier age counts noise layers after its final reset; earlier input information and reference correlations are discarded when that carrier reaches the contact.

**Sources.** [One-contact conveyor](../science/geometry.md#a-one-contact-path-conveyor) and the [complete three-qubit example](WATROUS_BRIDGE.md#a-complete-three-qubit-example).

### M18 — Fixed path layouts and optimal placement

**Central question.** How do contact cells convert a local conveyor into a path design rule?

**Understanding target.** Partition the path into contiguous nearest-contact cells, explain the two-arm age bound, and obtain $`\epsilon_*\le\min\{1,pM\}`$ for every fixed nonempty contact set. Use the cell cost $`g(a)=\lfloor a^2/4\rfloor`$ to understand balanced cells and median contacts.

**Dependencies and story role.** M16–M17; this matches the graph converse in order and then optimizes a supplied number of path contacts.

**Conceptual connection.** The exact placement formula concerns the distance sum; the path theorem gives matching error order, not an exact finite-noise optimum.

**Sources.** [Every fixed path placement](../science/geometry.md#every-fixed-contact-placement-on-a-path), [path placement formulas](../science/geometry.md), and the [bridge](WATROUS_BRIDGE.md#from-the-example-to-the-geometry-law).

### M19 — A full cold face cools parallel slab columns

**Central question.** When does a higher-dimensional register reduce to parallel path conveyors?

**Understanding target.** For a slab of thickness $`L`$ and cross-section containing $`A`$ sites, derive $`M=AL(L-1)/2`$ with one whole face reset. Explain why synchronized independent column conveyors provide a matching order construction.

**Dependencies and story role.** M10, M16, and M18; this identifies the proved higher-dimensional geometry.

**Conceptual connection.** A full cooled face supplies one contact per column; it does not establish an arbitrary-graph or sparse-boundary upper bound.

**Sources.** [Rectangular slabs](../science/geometry.md#rectangular-slabs-with-one-full-cold-face) and [full-face interpretation](../science/interpretation.md#cooling-from-a-full-face).

### M20 — A distance-one star exposes a contact bottleneck

**Central question.** Why can short routes still force a large initialization error?

**Understanding target.** For a star with $`m`$ bulk leaves and one contact, note that $`M=m`$ but the contact can touch only one leaf per gate layer. Reconstruct the three-leaf schedule and its final bulk ages $`3,2,1`$ before reading the exact general law.

**Dependencies and story role.** M11, M16–M19; this tests whether the old geometric quantity can describe a busy hub.

**Conceptual connection.** A graph distance counts route length, while a contact shared by many routes imposes additional waiting and terminal noise.

**Sources.** [Worked star and slot example](WATROUS_BRIDGE.md#when-short-routes-share-one-contact) and [contact throughput](../science/contact_throughput.md).

### M21 — Contact-cover architectures and feasible assignments

**Central question.** Which graph restriction lets one solve the contact bottleneck exactly?

**Understanding target.** Define the bulk $`B=V\setminus S`$ and require no bulk–bulk edges, with every bulk vertex adjacent to a contact. Define a feasible assignment $`f:B\to S`$ and contact loads $`\ell_s=|f^{-1}(s)|`$; explain why a bulk vertex with several neighbors must still be assigned to an actual allowed edge.

**Dependencies and story role.** M10–M12 and M20; this states the exact new theorem class before its proof.

**Conceptual connection.** Contact–contact edges and joint contact maps are allowed; independent bulk vertices are the crucial restriction.

**Sources.** [Exact contact-cover account](../science/contact_throughput.md) and the [scientific model](../science/model.md).

### M22 — Last-contact ages expose terminal local noise

**Central question.** Why is each bulk qubit’s final contact gate the useful event?

**Understanding target.** If the last contact gate on bulk vertex $`v`$ occurs at round $`t_v`$, count $`a_v=T-t_v+1`$ noise layers, including that round. Commute their composition to the output using depolarizing covariance and the absence of later nonlocal gates on $`v`$.

**Dependencies and story role.** M05, M11, M14, and M21; this replaces a single selected-fault argument by simultaneous terminal channels on the bulk.

**Conceptual connection.** The output state before these terminal maps can be arbitrarily entangled; the argument does not assume independently generated output faults.

**Sources.** [Terminal-channel proof](../science/contact_throughput.md) and the [throughput bridge](WATROUS_BRIDGE.md#why-this-schedule-is-globally-optimal).

### M23 — The target test turns contact ages into a product bound

**Central question.** How does one bound all coherent controllers without assuming a product state?

**Understanding target.** Set $`h_p(j)=[1+(1-p)^j]/2`$. Apply each terminal channel’s adjoint to its local zero projector and use the largest eigenvalue of the resulting tensor-product effect. At one contact, distinct last-gate rounds force sorted ages $`a_{s,j}\ge j`$. Include never-touched bulk vertices through a maximally mixed input and factors $`1/2`$.

**Dependencies and story role.** M07–M09 and M21–M22; this proves the optimal-assignment population ceiling for every finite depth.

**Conceptual connection.** A tensor product of effects bounds an arbitrary correlated pre-noise state; it is not a statement that that state factorizes.

**Sources.** [Complete lower-bound proof](../science/contact_throughput.md) and [why the star schedule is optimal](WATROUS_BRIDGE.md#why-this-schedule-is-globally-optimal).

### M24 — An assignment becomes a legal simultaneous SWAP schedule

**Central question.** How can every contact attain its best available ages at the common output time?

**Understanding target.** Reset all contacts in one initial round. For each contact, schedule its assigned leaves backwards from the final round, giving ages $`1,\ldots,\ell_s`$. Show that distinct assigned leaves and one gate per contact make every layer a matching, even for unequal loads.

**Dependencies and story role.** M03–M04, M11, M17, and M21–M23; this supplies the explicit attaining controller.

**Conceptual connection.** The initial reset purifies each contact before its first SWAP; the reset after every noisy round discards the bulk input that has just arrived.

**Sources.** [Attaining assignment/SWAP protocol](../science/contact_throughput.md) and [three-leaf schedule](WATROUS_BRIDGE.md#when-short-routes-share-one-contact).

### M25 — The exact optimum is a complete-channel statement

**Central question.** Why does attaining target population also attain the claimed half-diamond error?

**Understanding target.** Prove that every original input and its reference correlations are discarded. The final channel replaces the register by pure contacts and diagonal bulk states with target population $`\prod_s\prod_{j=1}^{\ell_s}h_p(j)`$. Combine both directions to obtain $`\epsilon_*=1-\max_f\prod_s\prod_{j=1}^{\ell_s}h_p(j)`$.

**Dependencies and story role.** M04, M07–M08, and M23–M24; this closes the exact finite-noise theorem.

**Conceptual connection.** Check empty bulk, $`p=0`$, and $`p=1`$ explicitly. Exact output-state calculations imply channel error here because the construction is replacement.

**Sources.** [Exact optimum and boundary cases](../science/contact_throughput.md) and the [Watrous channel-error translation](WATROUS_BRIDGE.md#translate-the-notation-and-the-task).

### M26 — Compile the optimal assignment by slot costs

**Central question.** How can the exact finite-noise optimum be turned into a concrete controller?

**Understanding target.** Convert the product objective into additive costs $`c_j=-\ln h_p(j)`$. Route one unit from each bulk vertex through an allowed contact and a unit-capacity contact-slot arc. Explain why nondecreasing costs permit occupied slot prefixes, and then translate the resulting assignment into M24’s schedule.

**Dependencies and story role.** M21 and M24–M25; this turns the optimum from an existence statement into a finite optimization procedure.

**Conceptual connection.** Min-cost flow is an inherited algorithmic tool. Its adjacency constraints enforce the physical graph; assigning by load alone can choose an impossible edge.

**Sources.** [Assignment compiler](../science/contact_throughput.md) and [slot interpretation](WATROUS_BRIDGE.md#from-a-layout-to-the-optimal-assignment).

### M27 — The throughput scale and balanced contact banks

**Central question.** What simple design law survives when the exact product is inconvenient?

**Understanding target.** Define $`A_*=A(G,S)=\min_f\sum_s\ell_s(\ell_s+1)/2`$ and derive error order $`\Theta(\min\{1,pA_*\})`$. For one-contact stars compute $`A_*=m(m+1)/2`$; for complete bipartite contact banks explain balanced loads and the quotient–remainder exact product.

**Dependencies and story role.** M18, M20, and M25–M26; this gives useful layout comparisons and noise/contact scaling.

**Conceptual connection.** The integer-slot optimizer for the order scale need not be asserted to optimize the exact finite-noise product on every restricted adjacency graph.

**Sources.** [Throughput law and examples](../science/contact_throughput.md) and the [worked assignment bridge](WATROUS_BRIDGE.md#from-a-layout-to-the-optimal-assignment).

### M28 — Which physical changes alter the result?

**Central question.** Why must the noise and entropy outlets remain part of the claimed law?

**Understanding target.** Explain the positive complete-depolarization plus mixed-unitary-residual condition for the general converse, and the target-preserving phase-noise exception. Retain the physical-output task, gates–noise–contacts order, unobserved noise and absence of extra protected memory. Identify why adding bulk–bulk edges removes the exact last-contact proof.

**Dependencies and story role.** M05, M11, M16, and M21–M27; this distinguishes proved extensions from changes of task.

**Conceptual connection.** The mixed-unitary extension supplies a converse parameter; it does not transfer the exact depolarizing contact-throughput formula or prove a continuous-time or heat/work theorem.

**Sources.** [Noise and scope](../science/noise_and_scope.md), [exact-throughput scope](../science/contact_throughput.md), and [physical interpretation](../science/interpretation.md).

### M29 — Attribution, analytical proof and finite evidence

**Central question.** What establishes the scientific advance, and what do the computations actually check?

**Understanding target.** Separate known channel facts, single-port/algorithmic cooling and standard min-cost flow from the protocol-uniform geometric converse and exact contact-cover optimum. Relate carrier tracking, assignment enumeration, channel checks and finite boundary cases to the specific identities they test.

**Dependencies and story role.** M14–M28; this connects the complete account to its prior work and reproducible evidence.

**Conceptual connection.** Finite calculations test conventions and examples. The arbitrary-size factorization, age-packing argument and complete-channel construction remain analytical claims with their stated assumptions.

**Sources.** [Related work](../references/RELATED_WORK.md), [verification guide](../verification/README.md), and [contact-throughput theorem](../science/contact_throughput.md).

### M30 — Assemble distance, contact throughput and complete initialization

**Central question.** How should a proposed register and reset layout be assessed from end to end?

**Understanding target.** State the physical task and noise timing; apply the general distance converse; select the proved path/slab construction or the exact contact-cover assignment method when its hypotheses hold. Report the resulting complete-channel accuracy and the contact/transport resources needed to attain it.

**Dependencies and story role.** M12 and M13–M29; this synthesizes the original geometry law and the exact throughput upgrade.

**Conceptual connection.** Distances control how far entropy must travel; contact throughput can add a queue even at distance one. Arbitrary-graph SWAP optimality, logical-only cooling, laboratory time, and thermodynamic reset costs remain separate questions.

**Sources.** [Scientific overview](../science/README.md), [model](../science/model.md), [geometry](../science/geometry.md), [exact contact throughput](../science/contact_throughput.md), and the [single-anchor bridge](WATROUS_BRIDGE.md).
