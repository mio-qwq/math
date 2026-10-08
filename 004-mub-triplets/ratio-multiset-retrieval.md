# Actual cyclic ratio multisets, with multiplicity

For an actual raw flat Hadamard6 displayed as four order-three circulants
H=[C(a) C(b); C(c) C(e)], the actual neighboring ratio multisets of a/e
and b/c are equal, including repeated values. Only unit norm squares of
the actual entries and H.conjTranspose*H=6 I are assumed. Matching powers,
matching correlations and matching ratio multisets are derived, not supplied.

For a triple v, set

    corr(v)=v0 star(v1)+v1 star(v2)+v2 star(v0),
    ratio(v,i)=v(i)/v(i+1),    i in Fin 3.

The actual ratio multiset has three occurrences ratio(v,0), ratio(v,1),
ratio(v,2). It is a Multiset, so equal values retain their multiplicities.
This closes the correlation and multiset part of
[the written phase-retrieval proof, Section 3](direct-circulant-character.md#3-the-six-phase-retrieval-alternatives-with-multiplicity).
The subsequent [actual reconstruction](phase-retrieval-alternatives.md)
now formalizes both cyclic-shift/adjoint alternatives. Combining the branches,
the real-rank argument and the final product cancellation remain unformalized.
No general MUB solution or historical mathematical originality is established.

The [autocorrelation source](proof/CirculantAutocorrelation.lean) first proves,
for any complex triple, with no flatness assumption,

    cast(normSq mode(v,theta))
      = cast(energy(v))+theta star(corr(v))+theta² corr(v),   theta³=1.

For any primitive cube root omega, the three raw powers recover correlation:

    3 corr(v) = cast(normSq mode(v,1))
                +omega cast(normSq mode(v,omega))
                +omega² cast(normSq mode(v,omega²)).

The coefficients and scale are for the actual raw transform. Internally
choosing a primitive root and using
[the actual opposite-power theorem](mode-power-matching.md) at all three
roots gives corr(a)=corr(e) and corr(b)=corr(c) from the single actual Gram
equation. No flatness, block inverse or second Gram premise is needed here.

The [ratio source](proof/CirculantRatioPolynomial.lean) uses actual unit
entries to prove every denominator nonzero, inverse=star, ratio product=1
and ratio sum=corr. Unit ratios with product one have pairwise product sum
equal to star(corr), so their actual monic cubic is

    t³-corr(v)t²+star(corr(v))t-1
       = (t-ratio(v,0))(t-ratio(v,1))(t-ratio(v,2)).

Equal correlations give identical polynomials. Pinned Mathlib's
Polynomial.roots_multiset_prod_X_sub_C recovers the entire three-occurrence
multiset from its product of linear factors. This preserves repeated roots
automatically; no simple-root assumption, numerical root solver or finite
phase enumeration occurs. Composing with actual flatness and Gram gives
the two actual opposite ratio-multiset equalities.

Each new source has three audited declarations and actual author plus
separate reviewer compiler records: all exits zero, zero warnings/errors,
and only propext, Classical.choice and Quot.sound. These are classical
Fourier and polynomial ingredients with connected project-local Lean proofs.
Lean 4.34.1 and Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`
remain fixed. The previously verified project modules are reused unchanged.

From the existing pinned 002 Mathlib package, follow
[the Gram import build instructions](gram-block-invertibility.md) to build
Character, UnitTriple and Gram in a fresh temporary directory on LEAN_PATH.
Then build the matching and correlation imports in this order and check ratio:

```powershell
lake env lean --root=$taskMubSources -o "$taskMubBuild/CubeRootGramMatching.olean" "$taskMubSources/CubeRootGramMatching.lean"
lake env lean --root=$taskMubSources -o "$taskMubBuild/CirculantAutocorrelation.olean" "$taskMubSources/CirculantAutocorrelation.lean"
lake env lean "$taskMubSources/CirculantRatioPolynomial.lean"
```

The subsequent [phase-retrieval source](proof/CirculantPhaseRetrieval.lean)
now proves occurrence-preserving three-term matching and actual unit-phase
reconstruction, with the adjoint ratio index l-i-1.
Repeated ratios may make some of the six possible alternatives coincide;
the current theorem does not assert six distinct solutions.
