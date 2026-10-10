# Lean formalization interfaces for sequential edge-orderability

**Stage:** exact technical specification, NOT compiled Lean code and NOT a theorem certificate. Worker environment checked 2026-10-10: \`lean\`, \`lake\` and \`elan\` binaries unavailable, network bootstrap to GitHub unavailable. Do NOT claim proof execution, \`#print axioms\` audit or mathlib compatibility until a toolchain actually runs. Goal: formalize the complete original conjecture *without* \`sorry\` or new axioms, preserving its fixed colouring and global-order semantics.

**Mathematical freeze:** original independent written PASS on \`7168f6df66ba5518cd3420c4668eab5352e4be8c\`. Repaired textual/execution packet \`213bf8ccad0c72b24aa86bc522bf9ae3a7d74216\`; updated imports and replay recorded in \`reviews/EXECUTION_REPLAY_V2.md\`. No theorem has yet been compiled.

## Exact source semantics (theorem statement is the acceptance contract)

Let \`V\` be a finite decidable vertex type; let \`G : SimpleGraph V\`; let \`E = { e : Sym2 V // G.Adj e.out.1 e.out.2 }\` denote actual *unordered edges* (avoid double-counting oriented endpoint pairs). A fixed proper colouring \`w : E -> Colour\` means that two distinct edges incident with the same vertex always receive different colours. Let \`π : List E\` be a **single complete global ordering**, with \`π.Nodup\` and \`π.toFinset = Finset.univ\`. Define the induced colour sequence \`seq π w v\` as the list of colours of edges of \`π\` incident with vertex \`v\`, in that order.

**Primary target theorem, exact mathematics:** For every finite connected simple graph \`G\` that is neither \`K₂\` nor an even cycle and for *every* fixed proper edge colouring \`w\`, there exists such a complete \`π\` for which \`seq π w u ≠ seq π w v\` for **each** edge \`uv\`. No recolouring is allowed. Separate established author theorem (unequal adjacent palettes) must be proved/formalized, not introduced as an axiom.

The \`d\`-regular uniform-palette theorem is a logical subgoal, not a substitute for the primary theorem. Its contract is: any finite simple graph with \`d≥3\`, all degrees exactly \`d\`, and a proper colouring with \`d\` global colours admits a complete successful edge order.

## Suggested standalone lemma interfaces

1. **Component-avoiding transversal.** Given a simple finite graph Q with every vertex incident to some Q-edge, and a partition \`C : Fin k -> Finset V\` of the entire vertex set where \`2 ≤ card (C i)\`, produce \`r : Fin k -> V\` with \`r i ∈ C i\` and for every connected component \`S\` of Q, \`∃ v ∈ S, v ∉ range r\`. Preserve loops and parallel edges in the *auxiliary multigraph*: an ordinary \`SimpleGraph\` is inadequate for T, because the proof uses a 2-cycle made from two **distinct labelled parallel edges**. A convenient formal model is \`Fin k -> QComponent × QComponent\`, with incident edge labels rather than a simple adjacency predicate.
2. **Partial sinkless orientation.** For such a finite labelled multigraph T and a designated safe set, if every dangerous node has no loop and has degree≥2 **counting distinct edge labels**, produce an orientation of each labelled edge with at least one outgoing edge at every dangerous node. The proof splits components containing a safe target (orient spanning tree toward it) and components with all nodes dangerous (find edge-labelled cycle; orient it cyclically and remaining tree branches toward it). This is the essential combinatorial dependency of (1).
3. **Root-order forest.** For an induced subgraph Q[R] in which no Q-component is fully contained in R, produce a linear order on R such that for every root r there exists Q-neighbour outside R or later than r in R. Use the connected component's boundary vertex and a rooted spanning tree ordered child-before-parent.
4. **Two-colour factor.** From a proper \`Fin d\` edge colouring of a d-regular simple graph (d≥3), extract an explicit partition of vertices into disjoint alternating 0/1 **even cycles** of length≥4. No choice of a global Hamiltonian cycle is permitted.
5. **Global insertion correctness.** Given the selected roots and ordering, construct an actual list \`π\` of unordered edges. Prove (i) completeness/nodup; (ii) at roots, colours 0 and 1 are separated by an assigned remaining colour; (iii) at nonroots they are consecutive; (iv) nonroot/nonroot cycle neighbours have opposite relative order of 0 and 1; (v) same-colour edges between roots and/or nonroots are distinguished by their colour's position. Then prove the full regular theorem.
6. **Original-source conclusion.** Formalize the authors' unequal-adjacent-palette theorem as an actual theorem (not an assumed proposition), or provide a clearly scoped theorem restricted to uniform palettes until this dependency is available. Combine with the full regular theorem, the degree-one K₂ case, degree-two cycles and the vacuous edgeless one-vertex case.

## Negative cases that MUST be checked in a formalization

- Auxiliary parallel edges: Q with components \`{0,1}\`, \`{2,3}\`, parts \`{0,2}\` and \`{1,3}\` yields a dangerous auxiliary **2-cycle** of two labelled parallel edges. Collapsing it to a SimpleGraph invalidates the sinkless-orientation argument.
- A Q-component holding both candidates from one original part creates an auxiliary **loop** and is safe without orientation.
- Edgeless Q is an actual counterexample to the transversal lemma; its no-isolated-vertex assumption is indispensable.
- Root ordering cannot be arbitrary: a root adjacent only to another chosen root must precede some root to receive an assigned leftover-colour edge.
- G simplicity prevents a leftover-colour edge parallel to a consecutive 0/1 cycle edge; otherwise the nonroot colour adjacency signature may fail.
- Colouring \`w\` stays **fixed**; no identification of distinct original colours unless a justified global relabelling is explicitly bijective.

## Minimal build/audit protocol (future real runtime)

Read repository pinned Lean/Mathlib versions and compare existing packages; do not upgrade shared versions from this worker. First compile a standalone file implementing (1–3) with exact contracts and executable counterexample tests for invalid weakening. Build (4–5) only after the graph partition and edge-list semantics are stable. For every claimed theorem record the actual \`lake env lean\` command, exit code, compiler diagnostics, complete dependency manifest, SHA256 of the source, and \`#print axioms\` output. The final report must explicitly distinguish standard Mathlib axioms such as propext / Quot.sound from any additional assumption. No \`sorry\`, \`admit\`, \`native_decide\` substitutions for an uncovered universal property or a theorem statement that assumes its own conclusion.

**Current status:** this document is an implementation specification and mathematical scope guard, not a Lean formalization. Current decisive next step remains ROOT's independent *execution* re-acceptance of the corrected Python packet and eventual toolchain access.
