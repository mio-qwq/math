# Arbitrary external-base transport and exact classification

`ExternalBaseTransport.lean` closes the converse left outside the preceding
switch classification. Its input is an arbitrary loopless symmetric graph
`H` and an actual graph isomorphism from the connected odd-parameter CG model
to the canonical double cover of `H`. The isomorphism is not assumed to
preserve the displayed bipartitions.

The formal construction proves:

* adjacency forces colour agreement (or disagreement) to propagate along
  walks, so connectedness makes an arbitrary cover isomorphism globally
  colour-preserving after at most composition with the target deck;
* conjugating that deck back produces an actual `Switch` of the CG model,
  with involutivity, adjacency preservation, colour reversal and
  nonadjacency all proved;
* restricting the colour-preserving isomorphism to one layer gives an actual
  graph isomorphism from `H` to the resulting fold;
* for every odd `n >= 3`, the transported switch belongs to the existing
  exhaustive three-fold classification. Thus `H` is isomorphic to one of
  `firstSwitch`, `secondSwitch` or `thirdSwitch`.

Together with the pairwise nonisomorphism theorems in
`StrongConjugacy.lean`, this proves that arbitrary external bases have exactly
the three already identified isomorphism classes: the original CG base and
two TF-cousins. No finiteness hypothesis is needed for the transport
argument, so the result is stronger than the finite statement required for
the CG application.

The theorem does not infer that an unrelated graph has this canonical double
cover. The premise is the explicit graph isomorphism
`GraphIso (modelGraph n hn).adj (coverAdj H)`. Nor does it claim a new
independent human review: this stage is kernel-verified and mechanically
replayed, while independent written acceptance remains pending.

Verification is recorded in
`verification/20261013-cg-external-base/verification.json`. A clean
twelve-module rebuild with the official Lean 4.34.1 release passes 164 named
axiom audits without errors or warnings. The axiom union is only `propext`,
`Classical.choice`, and `Quot.sound`; there is no `sorryAx`. The companion
literal-definition regression reuses the non-enumerative 3,744-parameter
strong-switch check and all three damage controls.

Two implementation failures were resolved before acceptance. Rewriting an
isomorphism equation directly through a dependent subtype proof produced an
ill-typed motive, so the proof first changes to equality of subtype values.
Likewise, adjacency preservation for transported vertices must apply the
isomorphism law in the reverse direction before simplifying both right
inverses. Failed elaborations are not part of the successful receipt.
