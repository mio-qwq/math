# Research plan and acceptance criteria

The near-term priority is to close meaningful gaps between the verified finite ARC data and actual algebra/cochain statements. Prefer reusing proved identities to repeating finite enumeration. Continue publishing each completed, reviewed step.

| Stage | Intended result | Required evidence | Status |
| --- | --- | --- | --- |
| Algebra semantics | Actual unital characteristic-two algebra with 20-element basis and field dimension 20 | Prescribed multiplication and unit, all ring/algebra laws, Lean compilation and axiom audit | Published `aed7ae5` |
| Trace structure | Linear trace and symmetric invariant nondegenerate bilinear form on the actual algebra; explicit duality if feasible | Transport coordinate laws to the actual wrapper type; verify any dual inverse | In progress |
| Polynomial cochain closure | Genuine five-term contraction identity for all radical basis quadruples | Decode the existing closure certificate with every coefficient/output bound justified | In progress |
| Cycle obstruction | Actual q³ pairing, annihilation of every internal scalar coboundary, and a nonzero-parameter obstruction over suitable domains | Universal arbitrary-cochain statement; use a no-zero-divisor hypothesis for nonvanishing | In progress |
| Cochain complex correspondence | Connect the coordinate formulas to an explicitly defined complex and the appropriate simple module | Corner balancing, radical closure, endpoint actions, differential identities and cohomology interpretation | Open |
| Homological realization | Required resolutions, stable profile, chain-level lifts and specialization control | Full proofs, including all-degree assertions and denominator conditions | Open; complete ARC not established |

The next stages depend on the preceding mathematical interfaces, not only on file order. A scalar internal-coboundary obstruction is not by itself an Ext or Hochschild nonvanishing theorem. A field specialization preserves identities but need not preserve an arbitrary nonzero witness.

Disjoint partner work remains valuable in 001 (Newton identities and constructing the complex blocks from the original Hadamard hypotheses) or 002 (the general weighted rectangular theorem). Check ownership before choosing any new file. Do not abandon the existing notes or change their claimed scope without explicit justification.

At each stage summary, report the actual published commits, what Lean proves, the substantive remaining gap, and the next smallest useful step. Update this plan when the evidence changes the preferred route.
