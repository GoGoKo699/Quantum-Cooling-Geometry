# Noise assumptions and physical scope

The [main law](model.md) is exact for independent depolarizing channels in discrete local rounds. This page identifies the mechanism that extends to other noise and the changes of task that remove the stated obstruction.

## A mixed-unitary residual is sufficient for the converse

The terminal-event proof uses two properties: a selected complete-depolarization event leaves a tracial qubit factor, and every other local noise map can be represented as a mixture of unitaries. Thus the same converse holds if each local noise map admits

```math
\mathcal N_{v,t}
=a_{v,t}\mathcal E_v+(1-a_{v,t})\mathcal U_{v,t},
\qquad 0\le a_{v,t}\le1,
```

where $`\mathcal U_{v,t}`$ is mixed-unitary and the local noise choices are independent. For a prescribed depth, the [terminal set](converse.md) gives

```math
\epsilon(\Psi_T)
\ge\frac12\left[
1-\prod_{(v,t)\in\mathcal L_T}(1-a_{v,t})
\right].
```

Choose one terminal complete depolarizer from its Bernoulli pattern and condition all other noise into unitary trajectories, exactly as in the original proof. This is a sufficient decomposition, not a physical noise flag available to the controller.

If $`a_{v,t}\ge a`$ uniformly, the shallow-case argument and terminal counting give the duration-independent graph bound with $`p`$ replaced by $`a`$.

A concrete example is an independent Pauli channel

```math
\mathcal P(\rho)=\sum_{P\in\{I,X,Y,Z\}}q_P P\rho P^\dagger,
\qquad q_P\ge0,\quad\sum_Pq_P=1.
```

Set $`a=4\min_Pq_P`$. Subtracting $`a/4`$ from each probability leaves a nonnegative Pauli mixture of total weight $`1-a`$, proving the required decomposition. A full-support Pauli channel therefore has a positive obstruction. This converse parameter need not equal the total probability of a nonidentity Pauli error.

This extension is a lower bound only. The depolarizing SWAP upper bound relies on the exact single-carrier state $`[I+(1-p)^aZ]/2`$. A mixed-unitary residual can introduce additional errors, so it is not assigned the same attainable error using only its complete-depolarization weight.

## Target-preserving noise can evade the floor

Pure phase-flip noise preserves $`|0\rangle`$. In the SWAP/reset conveyor, every output carrier is eventually reset and all later phase flips leave it in $`|0\rangle`$. The full channel then becomes exact pure replacement after a finite flush. Zero-temperature amplitude damping has the same target-preserving property.

These examples explain why a general statement about every unital noise channel or every weak bath would be false. The distance sum alone is not sufficient: the noise must contain the entropy-injecting component used by the converse. In particular, number dephasing that preserves a vacuum can help a static loss device remove particles, as described in [related work](../references/RELATED_WORK.md), without contradicting the present heating-induced floor.

## Every physical output is part of the task

The target requires all retained physical qubits to be pure at one common output time. Its complete-channel metric also removes their correlations with any input reference. The following resources change the task or its entropy outlets:

- A supplied clean bulk ancilla or protected side memory.
- Bulk measurement with an external classical record, or bulk reset.
- Discarding a dirty syndrome register or other physical workspace.
- Requiring only a selected subsystem or encoded logical state to be pure.
- Releasing output qubits at different times before later noise acts.
- Observing noise flags, selecting successful branches, or choosing a stopping time from measurement results.

Such protocols may be useful, but their error cannot be inferred from the present model. The theorem is not a bound on fault-tolerant logical computing or on the polarization of a single cooled qubit.

## Round timing and contact resources

The gates–noise–contacts ordering is load-bearing. Final noise on a contact can be removed immediately. If every site is a contact, perfect parallel reset after the final noise gives zero error for any $`p`$. The formulas retain this boundary through $`M=0`$.

Contacts are ideal CPTP resources. Their bath temperature, reset duration, heat, work and control implementation are not computed. No uniform continuous-time result is obtained by simply replacing $`p`$ with a rate times a gate duration; simultaneous dynamics and finite propagation tails would need a separate argument.

The phenomenon also occurs for classical bits with local reversible transport and unobserved heating. The quantum content of the converse is its validity under all allowed entangling and coherent compression operations, with a reference-stable output criterion. No quantum-over-classical speedup is claimed.
