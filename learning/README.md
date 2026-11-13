# Learn Quantum Cooling Geometry

Start with three qubits on a line and one ideal reset contact. Local gates can bring each unknown input to the contact, but noise keeps acting on qubits that have already been reset. The key question is the accuracy of the entire physical register at the same final time. This guide connects that example to the general geometric bound.

The selected educational anchor is **John Watrous, *The Theory of Quantum Information* (Cambridge University Press, 2018)**. The [author's book page](https://jhwatrous.github.io/books-and-courses.html) provides the source; the [source bridge](WATROUS_BRIDGE.md) identifies the relevant portions of Chapters 2–4, translates notation, and supplies the missing local-causality and transport arguments. The book is a foundation for the channel language; the distance law is developed in this project's science pages.

| Reading goal | Route |
|---|---|
| See the task, one unavoidable late-noise event and a complete five-round protocol | [Worked three-qubit example](WATROUS_BRIDGE.md#a-complete-three-qubit-example) |
| Connect channels, trace/diamond error, unital noise and spectra to this project | [Watrous bridge](WATROUS_BRIDGE.md) |
| Follow the project's complete understanding map | [Exactly 30 milestones](MILESTONES.md) |
| Inspect the precise controls, noise timing and output requirement | [Scientific model](../science/model.md) |
| Read the controller-independent proof | [Converse](../science/converse.md) |
| Check the matching path/contact and slab constructions | [Geometry](../science/geometry.md) |
| Understand changes of noise, workspace or output task | [Noise and scope](../science/noise_and_scope.md) |
| Reproduce the finite calculations | [Verification](../verification/README.md) |

The milestone map is a common conceptual route through the project. It joins prerequisites to the mechanism, constructions and physical conclusions; it is not a requirement to finish a textbook before reading the result. The [science entrypoint](../science/README.md) provides a direct route for specialist readers.

Keep the load-bearing distinctions visible while reading: all physical outputs versus a selected clean subsystem; global error versus mean polarization; ideal cold contacts versus noisy transport; and a graph-wide converse versus a matching construction on the geometries actually proved.
