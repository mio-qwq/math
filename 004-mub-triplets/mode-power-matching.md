# Actual opposite block Fourier power matching

Let H=[C(a) C(b); C(c) C(e)] be the actual six-by-six matrix formed from
four Mathlib order-three circulants. From the single actual equation
H.conjTranspose*H=6 I, the [Lean source](proof/CubeRootGramMatching.lean)
proves, for every complex theta with theta³=1,

    normSq(mode(a,theta)) = normSq(mode(e,theta)),
    normSq(mode(b,theta)) = normSq(mode(c,theta)).

Here mode(v,theta)=v0+v1 theta+v2 theta² is the raw amplitude from
[the Gram module](gram-block-invertibility.md). No flatness, nonzero mode,
block inverse, second Gram equation or supplied matching premise is used.
This connects the actual matrix hypothesis to the equal Fourier powers
needed by the phase-retrieval argument in
[the written branch proof, Section 3](direct-circulant-character.md#3-the-six-phase-retrieval-alternatives-with-multiplicity).
It does not yet prove that classification, its repeated-root case, or
the final phase-product cancellation. General MUB coupling remains open.
The mode-matching argument is classical; historical originality is not established.

The proof extracts the actual cross-block Gram entries at
(inl0,inr0), (inl0,inr1), (inl0,inr2), all zero. An exact root polynomial
identifies their Fourier combination with

    star(mode(a,theta))*mode(b,theta)
      + star(mode(c,theta))*mode(e,theta) = 0.

Writing x,y,z,w for the four mode norm squares respectively, taking
normSq gives x*y=z*w. The previously proved two column energies give
x+z=6 and y+w=6. Substituting z=6-x and w=6-y into the product equation
gives x+y=6, and hence x=w and y=z. The argument handles zero modes and
does not divide by one of them. It does not need H*H.conjTranspose=6 I
as an additional premise.

Three declarations cover the cross polynomial, actual cross-Gram
orthogonality and actual opposite-power matching. Actual author and
separate reviewer runs both returned exit zero with zero warnings/errors;
all three printed audits contain only propext, Classical.choice and Quot.sound.
Lean 4.34.1 and fixed Mathlib
`d13f23b723b8a846827a245b89c10fc7d3f11612` are retained.
Source-specific audit and authentic compiler observations accompany the source.

From the existing pinned 002 Mathlib package, build the three project
imports in the order and temporary directory described in
[the Gram/inverse reproduction instructions](gram-block-invertibility.md).
With the resulting import directory on LEAN_PATH, replay this final file:

```powershell
lake env lean ../../../004-mub-triplets/proof/CubeRootGramMatching.lean
```

The subsequent [correlation/multiset proof](ratio-multiset-retrieval.md)
now recovers actual correlations and actual unit ratio multisets with their
full multiplicities. The subsequent
[actual reconstruction](phase-retrieval-alternatives.md) now gives both
opposite-block cyclic-shift/adjoint alternatives. Combining those branches
and the real-rank proof remain gaps before full product cancellation.
No distinct-ratio assumption is used.
