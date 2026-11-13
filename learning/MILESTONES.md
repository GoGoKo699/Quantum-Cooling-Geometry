# Thirty milestones in Quantum Cooling Geometry

This is a common understanding map for the scientific project. Its single educational anchor is John Watrous, *The Theory of Quantum Information* (2018), used through the [Watrous bridge](WATROUS_BRIDGE.md). The [scientific overview](../science/README.md) and the linked proof pages remain authoritative.

The allocation is **12 background/preliminary milestones and 18 narrative/innovation milestones**. The background builds from one qubit to the complete physical-register reset task. The narrative assembles the terminal-event converse, the attaining transport construction, and their consequences for contact geometry. The longer narrative reflects the project's connection between a channel argument and a spatial construction. The map covers the complete story, rather than every calculation or neighboring cooling problem.

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

**Understanding target.** Derive the terminal condition $`T-t\lt d_v`$ and explain the count $`M_T=\sum_v\min\{T,d_v\}`$ from one site's last vulnerable rounds to the whole graph.

**Dependencies and story role.** M06, M10, and M12; this identifies the geometric object that the proof will use.

**Conceptual connection.** Distances become a spacetime count, rather than only a minimum transport duration.

**Sources.** [Terminal-location count](../science/converse.md#count-terminal-noise-locations) and the [locality bridge](WATROUS_BRIDGE.md).

### M14 — Keep one depolarizer and resolve the other noise

**Central question.** How can one analyze a selected late fault without making the noise visible to the controller?

**Understanding target.** Separate Bernoulli occurrence patterns from Pauli labels, keep one selected terminal event as the full channel, and resolve every other noise occurrence into unitary trajectories.

**Dependencies and story role.** M05–M06 and M13; this converts a complicated noisy history into the useful proof representation.

**Conceptual connection.** The representation is mathematical conditioning for an unconditional bound, not heralding, observed flags, or feedback.

**Sources.** [Selection and averaging](../science/converse.md#count-terminal-noise-locations); Watrous, Chapters 2 and 4, through the [bridge](WATROUS_BRIDGE.md).

### M15 — Push the selected channel through the circuit

**Central question.** Why can a late depolarizer be moved to the output even though reset maps occur in between?

**Understanding target.** Explain unitary conjugation of its Pauli algebra and commutation with a contact map whose support is disjoint from its evolving gate cone.

**Dependencies and story role.** M03, M09–M10, and M14; this is the load-bearing channel factorization.

**Conceptual connection.** Causal disjointness supplies the exact algebraic step that a general claim about reset and eigenvalues would not justify.

**Sources.** [Depolarizer factorization](../science/converse.md#a-depolarizer-that-cannot-reach-a-contact) and the [project proof bridge](WATROUS_BRIDGE.md).

### M16 — From the surviving factor to a purity obstruction

**Central question.** What does one terminal complete depolarizer force at the required output?

**Understanding target.** Obtain the conjugated tracial-factor form, its largest-eigenvalue bound, and the resulting overlap limit with any pure register target, including mixed or correlated earlier inputs.

**Dependencies and story role.** M07–M09 and M15; this extracts the operational consequence of the factorization.

**Conceptual connection.** Coherent compression may move the mixed degree of freedom but cannot leave every retained physical output pure.

**Sources.** [Surviving factor and spectrum](../science/converse.md#a-depolarizer-that-cannot-reach-a-contact); Watrous, Chapters 2–4, through the [bridge](WATROUS_BRIDGE.md).

### M17 — A finite-noise lower bound

**Central question.** How does the chance of at least one terminal event become an unconditional reset-error bound?

**Understanding target.** Combine independence, the probability $`1-(1-p)^{M_T}`$, and the conditional overlap bound to establish the finite-depth lower bound with its factor $`1/2`$.

**Dependencies and story role.** M06–M08 and M13–M16; this joins the local mechanism to a whole-circuit statement.

**Conceptual connection.** The proof is nonperturbative and does not count every circuit fault as fatal or assume independent output errors.

**Sources.** [Event probability and target test](../science/converse.md#count-terminal-noise-locations) and the [bridge](WATROUS_BRIDGE.md).

### M18 — Eliminate the cooling-duration loophole

**Central question.** Why can neither a shallow circuit nor a longer schedule escape the graph floor?

**Understanding target.** Distinguish $`T\ge R`$, where $`M_T=M(G,S)`$, from $`T\lt R`$, where an inserted input depolarizer on the maximally mixed state yields a half-error obstruction.

**Dependencies and story role.** M09–M10 and M17; this completes the duration-independent arbitrary-control converse.

**Conceptual connection.** The short-depth proof uses a surviving global mixed factor, rather than inferring global impurity merely from one mixed marginal.

**Sources.** [Duration-independent converse](../science/converse.md#remove-the-duration-dependence) and the [bridge](WATROUS_BRIDGE.md).

### M19 — Read the distance-sum law accurately

**Central question.** What does the graph bound establish in weak noise, large exposure, and full contact coverage?

**Understanding target.** Interpret $`M=\sum_v d_v`$, the small-exposure scale $`pM`$, the constant lower floor at large exposure, and exact zero geometry cost when $`M=0`$.

**Dependencies and story role.** M11–M12 and M18; this turns the converse into a physical accuracy constraint without overstating it.

**Conceptual connection.** The lower bound gives neither an exact optimal constant nor error tending to one, and it supplies no arbitrary-graph attaining protocol.

**Sources.** [Scale and necessary condition](../science/model.md#interpretation-of-the-scale) and [converse limits](../science/converse.md#what-the-converse-establishes).

### M20 — Reset by a local SWAP conveyor

**Central question.** How can a simple local circuit erase every original carrier through one endpoint?

**Understanding target.** Follow the odd/even SWAP trajectories, their endpoint wait and reversal, and the finite flush that discards all original carriers, including their reference correlations.

**Dependencies and story role.** M02–M04, M08, and M10; this starts the constructive side from explicit local operations.

**Conceptual connection.** The reference-uniform guarantee follows from complete carrier removal, not from checking one favorable population profile.

**Sources.** [One-contact conveyor](../science/geometry.md#a-one-contact-path-conveyor) and the [worked bridge](WATROUS_BRIDGE.md).

### M21 — Count output ages and calculate the actual channel

**Central question.** Why is the noise remaining after a conveyor flush determined by final carrier ages?

**Understanding target.** Explain the age multiset $`\{0,1,3,\ldots,2\ell-3\}`$, the single-carrier state, and the product formula for the endpoint conveyor's exact half-diamond reset error.

**Dependencies and story role.** M05–M08 and M20; this derives the finite-error certificate for the construction.

**Conceptual connection.** Noise before a carrier's last reset is erased; noise since that reset sets its output state. A diagonal replacement channel makes target population sufficient here.

**Sources.** [Exact conveyor channel and error](../science/geometry.md#a-one-contact-path-conveyor); Watrous, Chapters 2–3, through the [bridge](WATROUS_BRIDGE.md).

### M22 — An interior contact and two bouncing arms

**Central question.** How is a contact at an arbitrary position controlled by the sum of distances on its two sides?

**Understanding target.** Follow the unfolded carrier cycle and the outward/inward arm ages to establish that total final age is at most twice the cell's distance sum.

**Dependencies and story role.** M10 and M20–M21; this extends the attaining mechanism beyond an endpoint contact.

**Conceptual connection.** The arm estimate links an exact transport schedule to the same geometric quantity that appears in the converse.

**Sources.** [Fixed-placement proof and arm calculation](../science/geometry.md#every-fixed-contact-placement-on-a-path) and the [conveyor bridge](WATROUS_BRIDGE.md).

### M23 — Match the converse for every fixed path layout

**Central question.** How do nearest-contact cells turn the local conveyors into a complete path theorem?

**Understanding target.** Partition a path into contiguous contact cells, run synchronized periodic conveyors, and combine replacement-channel errors to obtain the upper bound $`\epsilon_*\le\min\{1,pM\}`$.

**Dependencies and story role.** M08, M18–M19, and M22; this integrates lower and upper arguments under the same model.

**Conceptual connection.** The tight order covers every nonempty fixed path contact set, while the arbitrary-graph result remains a converse alone.

**Sources.** [Fixed path placement theorem](../science/geometry.md#every-fixed-contact-placement-on-a-path) and [main statements](../science/model.md#main-statements).

### M24 — Place a fixed number of contacts optimally

**Central question.** Why do balanced cells with median contacts minimize the path distance sum?

**Understanding target.** Connect the cell cost $`g(a)=\lfloor a^2/4\rfloor`$, its nondecreasing discrete increments, and the exact quotient–remainder formula for $`M_{n,m}^{\min}`$.

**Dependencies and story role.** M10 and M23; this moves from analyzing a supplied layout to designing the layout.

**Conceptual connection.** A discrete placement problem becomes an initialization-accuracy rule because the same distance sum governs the path frontier.

**Sources.** [Optimal path placement and proof](../science/geometry.md#optimally-placed-contacts-on-a-path) and the [project bridge](WATROUS_BRIDGE.md).

### M25 — Sparse, clustered, and nearly complete contact layouts

**Central question.** When does contact placement matter more than contact count?

**Understanding target.** Compare alternating and clustered layouts, interpret the uniform order $`n(n-m)/m`$, and retain the dense-contact boundary where $`M_{n,n}^{\min}=0`$.

**Dependencies and story role.** M19 and M23–M24; this develops the practical meaning of the one-dimensional result.

**Conceptual connection.** The sparse simplification $`n^2/m`$ is useful in its regime but cannot describe a register whose every site can reset.

**Sources.** [Layout comparison](../science/interpretation.md#the-same-contact-count-different-layouts) and [finite placement formula](../science/geometry.md#optimally-placed-contacts-on-a-path).

### M26 — Cool a slab from one full face

**Central question.** How do the lower bound and construction extend when many longitudinal columns share a cold face?

**Understanding target.** Derive $`M=AL(L-1)/2`$, combine independent column conveyors, and interpret the cubic-register scale $`pN^{1+1/d}`$ with its stated geometry and $`L=1`$ limit.

**Dependencies and story role.** M18–M19 and M21–M23; this joins the channel mechanism to a higher-dimensional architecture.

**Conceptual connection.** The lower permits transverse entangling gates; the upper attains the order without them. This does not establish matching performance on every graph.

**Sources.** [Rectangular slab theorem](../science/geometry.md#rectangular-slabs-with-one-full-cold-face) and [full-face interpretation](../science/interpretation.md#cooling-from-a-full-face).

### M27 — Which changes of noise preserve the obstruction?

**Central question.** Why does entropy-injecting depolarization behave differently from noise that preserves the target?

**Understanding target.** State the complete-depolarization plus mixed-unitary-residual sufficient condition, interpret its Pauli-channel example, and explain the phase-noise and amplitude-damping exceptions.

**Dependencies and story role.** M05, M09, and M14–M19; this tests the mechanism at its noise-model boundary.

**Conceptual connection.** The extension supplies a converse parameter, while the depolarizing conveyor upper cannot be transferred using that parameter alone.

**Sources.** [Noise decomposition](../science/noise_and_scope.md#a-mixed-unitary-residual-is-sufficient-for-the-converse) and [target-preserving exceptions](../science/noise_and_scope.md#target-preserving-noise-can-evade-the-floor); Watrous, Chapter 4, through the [bridge](WATROUS_BRIDGE.md).

### M28 — Identify the consequential difference from earlier cooling results

**Central question.** Which ingredients are inherited, and what operational conclusion does this account add?

**Understanding target.** Distinguish known single-port cooling, noisy algorithmic-cooling limits, and local refrigeration from the protocol-uniform late-event factorization and spatial whole-register accuracy law.

**Dependencies and story role.** M11–M12, M18, M23, and M27; this locates the supported contribution in its scientific setting.

**Conceptual connection.** The quantum claim concerns arbitrary coherent controls and complete-channel accuracy; no quantum-over-classical speedup or new thermodynamic work law is asserted.

**Sources.** [Attribution and comparisons](../references/RELATED_WORK.md), [physical scope](../science/noise_and_scope.md#every-physical-output-is-part-of-the-task), and the [bridge](WATROUS_BRIDGE.md).

### M29 — Understand the evidence and its limits

**Central question.** Which parts of the account are proved analytically, and what can the finite computations verify?

**Understanding target.** Relate small-channel calculations, carrier-age checks, placement enumeration, and regenerated figures to their precise claims without treating a finite screen as the universal proof.

**Dependencies and story role.** M17–M18 and M21–M28; this integrates the result with its reproducible evidence.

**Conceptual connection.** Numerical and exact-integer diagnostics check conventions and finite identities, while the factorization, counting, and transport proofs establish the arbitrary-size statements.

**Sources.** [Verification guide](../verification/README.md), [recorded checks](../verification/results.json), and [geometry diagnostics](../verification/geometry_checks_results.json).

### M30 — Assemble the complete geometry–accuracy account

**Central question.** What can be concluded about a proposed register and contact layout, and what remains outside the result?

**Understanding target.** Connect the physical task, graph floor, fixed-path and slab constructions, contact-placement choices, noise assumptions, and reference-stable output guarantee into one qualified explanation.

**Dependencies and story role.** M12 and M13–M29; this is the narrative synthesis and the end of the project map.

**Conceptual connection.** The field can use distance sum as a tight path/slab accuracy scale while keeping logical cooling, extra entropy outlets, arbitrary-graph achievability, continuous-time dynamics, and heat/work costs distinct.

**Sources.** [Scientific overview](../science/README.md), [model and theorem](../science/model.md), [geometry](../science/geometry.md), [interpretation](../science/interpretation.md), [scope](../science/noise_and_scope.md), and the [single-anchor bridge](WATROUS_BRIDGE.md).
