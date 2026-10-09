# Product cancellation in the actual adjoint branches

Let H=[A B; C E] be the actual six-by-six four-circulant matrix, with
A=C(a), B=C(b), C=C(c), E=C(e). Assume actual entry norm squares one and
H.conjTranspose*H=6 I. If either opposite pair has a genuine unit-phase
cyclic-shift adjoint alternative, the
[Lean theorem](proof/CirculantAdjointBranch.lean) proves

    p_a p_e+p_b p_c=0,    p_v=product of the actual first column v.

The extra alternative is either E=alpha P_l A* or C=beta P_j B*, with
unit alpha/beta, an actual cyclic permutation matrix and conjugate
transpose *. It is an explicit additional hypothesis. This closes all
three cases containing an adjoint when combined with
[the previous actual retrieval theorem](phase-retrieval-alternatives.md).
That theorem also permits a both-preserving case. Its
[actual real-mode product-square ingredient](real-mode-product-squares.md)
is formalized separately, and the [final module](flat-gram-cancellation.md)
now proves its normalization and unconditional cancellation. This source
retains its narrower adjoint-alternative hypothesis. General companion symmetry and general
MUB coupling remain outside the result; historical originality is not established.

For E=alpha P_l A*, the actual off-diagonal block of column Gram is

    A* B+C* E=0.

All displayed matrices and their adjoints are actual circulants and commute.
Thus the same equation becomes

    A* (B+alpha P_l C*)=0.

The previously verified actual flat-Gram inverse theorem constructs N with
A N=I. Taking its adjoint gives N* A*=I, which cancels the actual matrix
factor. An inverse is a conclusion of flat Gram, not an additional premise.
The remaining true matrix equation has first column

    b_i+alpha star(c_(l-i))=0.

At i=l-k, conjugating and multiplying by the unit alpha gives
c_k=-alpha star(b_(l-k)), hence C=-alpha P_l B*. No inverse of P_l is
needed, and this forces a common shift and opposite phase rather than
assuming independent choices of the two retrieval branches.

The actual bijection i -> l-i preserves the product of three entries, so

    p_e=alpha^3 star(p_a),
    p_c=(-alpha)^3 star(p_b).

Actual unit entries imply p_a star(p_a)=p_b star(p_b)=1, giving the claimed
cancellation. The C=beta P_j B* alternative follows by taking the adjoint
of the same cross equation, B* A+E* C=0, and applying the argument with
the two column blocks exchanged. A second Gram equation is not supplied.

The connected endpoint, including these internal matrix and product
identities, passed actual author and separate reviewer compilation at one
identical source hash: one audit, exit zero, zero warnings/errors, and only
propext, Classical.choice and Quot.sound. Eight previously verified project
imports are reused unchanged. This is scoped formalization of the written
branch proof, not a newly resolved general public conjecture.

Use the fixed Lean 4.34.1 and Mathlib
`d13f23b723b8a846827a245b89c10fc7d3f11612`. In the pinned 002 package,
follow [the phase-retrieval import instructions](phase-retrieval-alternatives.md).
With those objects on LEAN_PATH, also build Invertibility and PhaseRetrieval
in the temporary import directory, then replay this source:

```powershell
lake env lean --root=$taskMubSources -o "$taskMubBuild/CirculantInvertibility.olean" "$taskMubSources/CirculantInvertibility.lean"
lake env lean --root=$taskMubSources -o "$taskMubBuild/CirculantPhaseRetrieval.olean" "$taskMubSources/CirculantPhaseRetrieval.lean"
lake env lean "$taskMubSources/CirculantAdjointBranch.lean"
```

The [both-preserving normalization and final composition](flat-gram-cancellation.md)
now supply the actual real-mode hypotheses and join this endpoint to
prove unconditional product cancellation for the displayed block class.
