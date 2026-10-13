# A counterexample to claw-free (1,1,3,3,4)-packing colorability

A connected simple cubic claw-free graph on 36 vertices admits no
(1,1,3,3,4)-packing coloring. It is not isomorphic to the exceptional
12-vertex graph H. This gives a negative answer to **Problem 1 in
Section 6 of Mortada, El Zein and Al Hajjar,
[arXiv:2608.02566v1](https://arxiv.org/html/2608.02566v1#S6)**.
The strict same-color distances are measured in the entire graph.

The proof is structural. Choose any existing high-colored point in each
triangle. This induces a proper core three-coloring. Every radius-four
representative forces a private neighbour for its core vertex. An odd
ring of diamonds has no such coloring. No enumeration of all five-color
functions or of all core three-color functions is used by the Lean proof.

`ClawFree11334.lean` proves the complete fixed witness in actual Mathlib
`SimpleGraph`, degree, `Walk`, connectedness and `edist` semantics.
The main theorem is `ClawFree11334.original_counterexample`.
Actual ROOT2 run: 2026-10-10T08:28:20.0309293+00:00 to 2026-10-10T08:29:15.2796926+00:00,
exit zero, zero warnings/errors/panics, 18 expected and observed axiom
audits, standard axioms only. Compiled source SHA256:

`afad6d3313c93fd5681be0ba0e25d302c73d019448681cb4c6552f8a0e0765b2`.

See [PROOF.md](PROOF.md) for the complete proof and the 12k-vertex family
for odd k>=3, and [INDEPENDENT_REVIEW.md](INDEPENDENT_REVIEW.md) for the
independent original-definition, object, mathematical and final-source
checks. The infinite family is a written theorem; Lean here covers k=3.

To replay with the pinned project from repository root:

```powershell
Push-Location 002-weighted-rectangular-pruning/proof/mathlib
lake env lean ../../../workstreams/ROOT/clawfree-11334-counterexample/ClawFree11334.lean
Pop-Location
python workstreams/ROOT/clawfree-11334-counterexample/verify_counterexample.py
```

The optional Python verifier includes the author's frozen finite check
(531441 projected assignments, 48 proper labelings and 3888 radius-four
representative choices), plus rejected damaged inputs, a weaker-palette
positive control and an even-ring positive control. ROOT did not repeat
this enumeration; its recorded output is explicitly author-provenanced.
The independent reviewer instead rebuilt the graph from formulas and
made one small 216-state check. The structural proof and Lean theorem
are independent of the solver's result.

No minimality, exact packing chromatic number, new graph-shape claim or
historical firstness is asserted. This does not refute the source's
(1,1,3,3,3) theorem or the separate general (1,1,2,3) problem.
The source's radius-five example has 18 vertices; it is not this graph.
Bounded literature checks and their uncertainties are in [HISTORY.md](HISTORY.md).

AI agents assisted discovery, mathematical derivation, independent
adversarial review, Lean implementation and technical writing. These are
AI-assisted checks, not human peer review; no AI is listed as a paper author.
