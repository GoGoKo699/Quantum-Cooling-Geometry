# Learn Quantum Cooling Geometry

Start with three qubits on a line and one ideal reset contact. Local gates bring each unknown input to the contact, and noise keeps acting on qubits already reset. The task is to return the entire register clean at the same time. This guide connects the line to the geometric bound, uses a distance-one star to derive exact SWAP optimality, then adds bulk interactions to see how a controller can improve on routing.

The selected educational anchor is **John Watrous, *The Theory of Quantum Information* (Cambridge University Press, 2018)**. The [author's book page](https://jhwatrous.github.io/books-and-courses.html) provides the source; the [source bridge](WATROUS_BRIDGE.md) identifies the relevant portions of Chapters 2–4, translates notation, and supplies the missing local-causality and transport arguments. The book is a foundation for the channel language; the distance law and exact contact-throughput result are developed in this project's science pages.

| Reading goal | Route |
|---|---|
| See the task, one unavoidable late-noise event and a complete five-round protocol | [Worked three-qubit example](WATROUS_BRIDGE.md#a-complete-three-qubit-example) |
| Connect channels, trace/diamond error, unital noise and spectra to this project | [Watrous bridge](WATROUS_BRIDGE.md) |
| Follow the project's complete understanding map | [Exactly 30 milestones](MILESTONES.md) |
| Inspect the precise controls, noise timing and output requirement | [Scientific model](../science/model.md) |
| Read the controller-independent proof | [Converse](../science/converse.md) |
| Check the matching path/contact and slab constructions | [Geometry](../science/geometry.md) |
| See why distance-one leaves can overwhelm a single reset contact | [Worked star example](WATROUS_BRIDGE.md#when-short-routes-share-one-contact) |
| Derive the exact optimum, choose a feasible assignment and compile its SWAP schedule | [Assignment bridge](WATROUS_BRIDGE.md#from-a-layout-to-the-optimal-assignment) → [Contact throughput](../science/contact_throughput.md) |
| Compare SWAP with reversible compression through the same gateway | [Four-qubit compression example](WATROUS_BRIDGE.md#compress-sparse-errors-before-routing) → [Single-contact compression](../science/single_contact_compression.md) |
| Understand changes of noise, workspace or output task | [Noise and scope](../science/noise_and_scope.md) |
| Reproduce the finite calculations | [Verification](../verification/README.md) |

The milestone map is a common conceptual route through the project. It joins prerequisites to the mechanism, constructions and physical conclusions; it is not a requirement to finish a textbook before reading the result. The [science entrypoint](../science/README.md) provides a direct route for specialist readers.

Keep the common final time, every physical output, and the noise on idle qubits visible in each proof. On an independent bulk, the contact assignment optimizes all allowed controllers. On a bulk clique, the gateway still constrains routing, and additional bulk gates can compress the information sent through it.
