# Research plan and acceptance criteria

The near-term priority is to close meaningful gaps between the verified finite ARC data and actual algebra/cochain statements. Prefer reusing proved identities to repeating finite enumeration. Continue publishing each completed, reviewed step.

| Stage | Intended result | Required evidence | Status |
| --- | --- | --- | --- |
| Algebra semantics | Actual unital characteristic-two algebra with 20-element basis and field dimension 20 | Prescribed multiplication and unit, all ring/algebra laws, Lean compilation and axiom audit | Published `aed7ae5` |
| Trace structure | Linear trace and symmetric invariant perfect pairing on the actual algebra | Explicit mutually inverse linear maps to the full R-linear dual | Proved and independently recompiled |
| Polynomial cochain closure | Genuine five-term identity on all inputs, including every characteristic-two specialization | Radical certificate plus corner support/normalization and idempotent inputs; finite linear extension | Full twenty-coordinate closure proved, including all idempotent inputs |
| Cycle obstruction | Actual q³ pairing and exclusion of every full vector-valued boundary | Universal arbitrary-cochain statement; correct nonvanishing condition | Proved on coordinates and actual bilinear algebra maps; q³ nonzero suffices |
| Cochain complex correspondence | Actual multilinear cochain differentials and a cycles-modulo-boundaries quotient | Full d2/d3 linear maps, zero composite, kernel/range quotient and zero-class criterion | Fixed cochain gives a nonzero class in the actual degree-three quotient when q³ is nonzero |
| Character-valued cochains | Actual e/f R-algebra characters, full scalar differential and nonzero projected class | AlgebraHom scalar compatibility, full-input closure, exclusion of every scalar bilinear boundary and kernel/range quotient | Generic character d3∘d2 proved; actual characters and scalar boundary bridge in progress |
| Homological realization | Required resolutions, stable profile, chain-level lifts and specialization control | Full proofs, including all-degree assertions and denominator conditions | Open; complete ARC not established |

The next stages depend on the preceding mathematical interfaces, not only on file order. A scalar internal-coboundary obstruction is not by itself an Ext or Hochschild nonvanishing theorem. A field specialization preserves identities but need not preserve an arbitrary nonzero witness.

Disjoint partner work remains valuable in 001 (Newton identities and constructing the complex blocks from the original Hadamard hypotheses) or 002 (the general weighted rectangular theorem). Check ownership before choosing any new file. Do not abandon the existing notes or change their claimed scope without explicit justification.

At each stage summary, report the actual published commits, what Lean proves, the substantive remaining gap, and the next smallest useful step. Update this plan when the evidence changes the preferred route.
