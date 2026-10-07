# Research plan and acceptance criteria

The near-term priority is to close meaningful gaps between the verified finite ARC data and actual algebra/cochain statements. Prefer reusing proved identities to repeating finite enumeration. Continue publishing each completed, reviewed step.

| Stage | Intended result | Required evidence | Status |
| --- | --- | --- | --- |
| Algebra semantics | Actual unital characteristic-two algebra with 20-element basis and field dimension 20 | Prescribed multiplication and unit, all ring/algebra laws, Lean compilation and axiom audit | Published `aed7ae5` |
| Trace structure | Linear trace and symmetric invariant perfect pairing on the actual algebra | Explicit mutually inverse linear maps to the full R-linear dual | Proved and independently recompiled |
| Polynomial cochain closure | Genuine five-term contraction identity for all radical basis quadruples, including every characteristic-two specialization | Decode the existing closure certificate with every coefficient/output bound justified | Proved and independently recompiled; arbitrary radical-vector extension in progress |
| Cycle obstruction | Actual q³ pairing, annihilation of every internal scalar coboundary, and a nonzero-parameter obstruction over suitable domains | Universal arbitrary-cochain statement; use a no-zero-divisor hypothesis for nonvanishing | Internal scalar obstruction proved; extension to full vector-valued boundaries in progress |
| Cochain complex correspondence | Connect the coordinate formulas to an explicitly defined complex and the appropriate simple module | Corner balancing, radical closure, endpoint actions, differential identities and cohomology interpretation | Actual trilinear map, bilinear non-boundary, kernel/span closure and low-degree differential composite proved; full-input closure and standard cohomology object remain open |
| Homological realization | Required resolutions, stable profile, chain-level lifts and specialization control | Full proofs, including all-degree assertions and denominator conditions | Open; complete ARC not established |

The next stages depend on the preceding mathematical interfaces, not only on file order. A scalar internal-coboundary obstruction is not by itself an Ext or Hochschild nonvanishing theorem. A field specialization preserves identities but need not preserve an arbitrary nonzero witness.

Disjoint partner work remains valuable in 001 (Newton identities and constructing the complex blocks from the original Hadamard hypotheses) or 002 (the general weighted rectangular theorem). Check ownership before choosing any new file. Do not abandon the existing notes or change their claimed scope without explicit justification.

At each stage summary, report the actual published commits, what Lean proves, the substantive remaining gap, and the next smallest useful step. Update this plan when the evidence changes the preferred route.
