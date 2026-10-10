# Independent definition, mathematical, and Lean-source review

**Accepted scope:** this specific seven-vertex graph refutes the printed
arXiv:2603.25113v1 Section 5 Conjecture 3. Historical firstness is uncertain.
An AI agent uninvolved in discovery or Lean implementation carried out the
reviews below. This is not a human peer-review certification.

The original HTML definitions and Section 5, and the corresponding PDF
page, were checked. The conjecture has no local-girth hypothesis.
The three palette entries are distinct indices, with distances measured
in the original graph. The full graph was independently rebuilt under
the relabeling [a,b,c,z,x_a,x_b,x_c] and mapped to the implementation by
[0,1,3,2,6,4,5]. All nine edges and degree-three neighbor counts match.
The triangle/radius-two/five-cycle contradiction was reconstructed without
using the discovery search or accepting its internal status.

A separate standard-library check actually ran at
2026-10-10T07:29:49.200771–07:29:49.216594 UTC, exit zero. It performed
seven independent BFS runs, then checked all 2187 assignments directly
against the original distance conditions: zero valid colorings. It did
not import or execute B's discovery program or verifier. This check is
supplementary; the explicit odd-cycle argument is complete independently.

The final review read the whole Lean source, the actual ROOT2 execution
JSON, the complete 14-declaration axiom log, and the pinned Mathlib
definitions of degree, neighbor finset, connectedness, walks and `edist`.
The original counterexample declaration is

```lean
theorem original_counterexample :
    Subcubic graph ∧ Saturated graph 2 ∧ graph.Connected ∧
      ¬ ∃ c : Fin 7 → Fin 3, Packing112 graph c
```

No hypothesis assumes the graph lacks a coloring, assumes a distance
matrix, or restricts the excluded colorings. `Packing112` covers all
functions into three labels; radius is one for labels 0 and 1 and two
for label 2. `Saturated` filters the entire actual neighbor finset by
actual degree three. Every ordered vertex pair has a real walk of length
at most two. The actual five-cycles avoid each possible triangle vertex;
the unified proof does not omit a symmetry case.

**Reviewed and actually compiled source SHA256:**

`4cac2792bcd6551d6c32a463a8e47b5ec356639a63e945e1368b67d9e7594424`.

Actual run: 2026-10-10T07:34:11.2658292–07:34:26.5698672 UTC;
exit zero, zero warnings/errors/panics, 14 expected and 14 observed audits,
no nonstandard axioms. The public source hash matches both the pre-run
and post-run hashes. The reviewer inspected this actual execution; they
performed no additional Lean replay or repeated enumeration.

Only subsets of `propext`, `Classical.choice`, `Quot.sound` occur.
`short_walk` is a proved lemma used by audited declarations, not a
postulate. Ordinary `decide` checks finite graph facts and the 32 maps
from a five-cycle to two colors; no `native_decide` or admitted proof is
used. Actual graph-distance correspondence is complete.

The frozen discovery/input packet was worker B commit
`cb7aa737412caab6d126b552adf23aec13a5b056`, with unchanged later
mathematical freeze `fadb2d48073cde97306cf128a2d40f6381232958`.
The public `candidate.json` retains its exact n and edge list and replaces
discovery metadata by explicit vertex names; the standalone verifier
remains byte-identical to B's frozen verifier (SHA256
`7fe25d248e7bc772497effa491a1bd87e92cf46d8724d7302fb1ea6d1f9c25b9`).
The fresh independent check above did not use this verifier.

Multi-round source checks distinguish the earlier positive 1-saturated
(1,1,2) result and larger-palette 2-saturated results from this three-color
claim. Classical pyramid definitions confirm the graph shape is known.
Earlier gadgets and all historical packing literature have not been
exhaustively audited. Source-version and historical scope remain explicit;
no mathematical priority or global-first assertion follows from this review.
