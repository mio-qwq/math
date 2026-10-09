# Actual cyclic-shift and adjoint phase retrieval

For the actual six-by-six matrix H=[C(a) C(b); C(c) C(e)], assume only
unit norm squares of all actual entries and H.conjTranspose*H=6 I.
The [Lean proof](proof/CirculantPhaseRetrieval.lean) derives both pairs
of actual matrix alternatives:

    C(e)=alpha P_l C(a)  or  C(e)=alpha P_l C(a)*,
    C(c)=beta  P_j C(b)  or  C(c)=beta  P_j C(b)*.

Here alpha and beta have normSq one, l and j are in Fin 3, and * means
conjugate transpose. The actual permutation matrix P_l has entry one
exactly when i-j=l, so P_l e_j=e_(j+l). Matrix multiplication and
conjugate transpose are the ordinary Mathlib operations. Matching ratios,
phase alternatives, mode bounds and block inverses are not supplied as
additional premises to the final Gram theorem.

This completes the reconstruction in
[Section 3 of the written proof](direct-circulant-character.md#3-the-six-phase-retrieval-alternatives-with-multiplicity).
The subsequent [adjoint-branch proof](adjoint-branch-cancellation.md)
now closes every case with a genuine adjoint alternative as an extra premise.
The [actual real-mode lemma](real-mode-product-squares.md) also now proves
the real-rank ingredient. The [final cancellation module](flat-gram-cancellation.md)
now normalizes the both-preserving case and composes unconditional
Gram-to-product cancellation for the displayed block class. The general
complete-companion symmetry and six-dimensional MUB conjectures remain
outside this result. Historical mathematical originality is not established.

The preceding [ratio-multiset proof](ratio-multiset-retrieval.md) gives
equal three-occurrence cyclic ratio multisets for a/e and b/c. The new
generic matching lemma cancels occurrences from the two equal multisets,
including repeated values. Every matching of three occurrences is a
rotation i -> h+i or a reflection i -> h-i. Only the three finite indices
are split into cases; phases remain arbitrary complex unit numbers.
No distinct-ratio assumption or phase enumeration is used.

For ratio(v,i)=v(i)/v(i+1), define

    shift_l(a)(i)=a(i-l),
    shiftAdj_l(a)(i)=star(a(l-i)).

Their ratios are respectively ratio(a,i-l) and ratio(a,l-i-1).
Consequently rotation matching uses l=-h and reflection matching uses
l=h+1. The extra one in the reflection offset is essential. Equal ordered
ratios yield a common phase alpha=e(0)/v(0); every denominator is proved
nonzero from actual unit entries, and normSq(alpha)=1 follows from them.
The actual permutation-matrix identities then give the displayed matrix
alternatives. Repeated ratios can make alternatives coincide; the theorem
does not assert six distinct solutions or independent choices of two branches.

Three endpoint declarations have actual author and separate reviewer
compilations against the identical source hash: exit zero, zero warnings
and errors, and only propext, Classical.choice and Quot.sound. The generic
matching and matrix identities are included in these dependency audits.
The six previously verified project imports are reused unchanged.
These are classical phase-retrieval ingredients with a connected
project-local Lean implementation, not a newly solved public conjecture.

Use Lean 4.34.1 and Mathlib
`d13f23b723b8a846827a245b89c10fc7d3f11612` in the existing pinned 002 package.
Follow [the Gram import instructions](gram-block-invertibility.md) to put
Character, UnitTriple and Gram objects in a fresh temporary directory on
LEAN_PATH, and [the matching/correlation instructions](ratio-multiset-retrieval.md)
to build Matching and Autocorrelation. Then build Ratio and replay this file:

```powershell
lake env lean --root=$taskMubSources -o "$taskMubBuild/CirculantRatioPolynomial.olean" "$taskMubSources/CirculantRatioPolynomial.lean"
lake env lean "$taskMubSources/CirculantPhaseRetrieval.lean"
```

The source, audit output and actual compiler observations are versioned
together. A release timestamp anchors these exact artifacts; it does not
establish unreviewed historical mathematical priority.
