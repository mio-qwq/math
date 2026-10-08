# Concrete dual-recurrence structure constants

`TwentyDimDualCorrespondence.lean` interprets the frozen twenty-label
dual-recurrence certificate as genuine polynomial structure constants.
Writing `B` for the ten-label core constants, lowercase indices for the
core and uppercase indices for its coordinate dual, Lean proves all eight
input/output blocks. The nonzero blocks are exactly

\[
 T_{a,b}^{k}=B_{a,b}^{k},\qquad
 T_{a,b^*}^{k^*}=B_{k,a}^{b},\qquad
 T_{a^*,b}^{k^*}=B_{b,k}^{a}.
\]

The other five blocks vanish. In particular, dual times dual is zero.
These are identities over `Polynomial (ZMod 2)` and after specialization
at every parameter in every commutative characteristic-two ring. No
nonzero-parameter or field hypothesis is needed.

The proof reuses `t_table_matches_dual_recurrence` and the existing output
bounds and coefficient decoder. Its generic sparse-coordinate lemma proves
that omitting zero coefficient codes preserves the exact decoded value,
with no byte bound. No new finite enumeration is used.

This supplies the structure-constant correspondence. It does not yet
construct a ring or algebra comparison isomorphism with
`DualTrivialExtension.Carrier`; that remains a subsequent step. It makes
no Ext or complete ARC claim. The motivating table is attributed in
`../../ATTRIBUTION.md` to OpenAI family 199 at the pinned source snapshot.

From this pinned package, after building the imported local modules:

```sh
LEAN_PATH=.:.. lake env lean -o TwentyDimDualCorrespondence.olean TwentyDimDualCorrespondence.lean
```

Actual checks: Lean 4.34.1, pinned Mathlib, exit 0, zero warnings, and
eleven printed audits using only `propext`, `Classical.choice`, `Quot.sound`.
No `sorry`, added axiom or `native_decide` is present. The adjacent
verification record fixes the exact source hash.

## Independent replay provenance

The source and original verification/audit records above are retained from
the contributed structural proof. A separate actual independent replay on
8 October 2026 accepted the identical source bytes with exit zero, no
warnings or errors, and the printed standard-axiom audits. See the
[selected replay record](SelectedStructuralReplay.verification.json) and
[scope and reproduction note](../../structural-bridge-replay.md).
Previously verified local prerequisites were reused in that replay;
earlier prerequisite runs are not recounted as fresh checks.
