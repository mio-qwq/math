# Flat four-circulant Gram implies product and character cancellation

Let H=[C(a) C(b); C(c) C(e)] be the actual six-by-six matrix formed from
four order-three circulants, with C(a)_{ij}=a_{i-j}. Suppose every actual
entry has norm squared one and H*H=6I. The
[complete Lean endpoint](proof/CirculantCancellation.lean) proves

    p_a p_e+p_b p_c=0,
    chi_1(H)=chi_3(H)=chi_1(H*)=chi_3(H*)=0.

Here p_a is the product of the actual three entries of a, and chi_n is
the sum over the actual six columns of the nth power of the top-three
entry product divided by the bottom-three entry product. The adjoint is
the actual conjugate transpose. The partitions are the displayed blocks.
Only actual flatness and the single column Gram equation are inputs:
no supplied modes, inverse, phase alternatives, product cancellation or
second Gram equation is assumed at this final endpoint.

This closes the connected formalization of the
[written four-circulant theorem](direct-circulant-character.md). It proves
a symmetry-restricted theorem, not that an arbitrary MUB transition or
complete companion admits this symmetry, and not the general MUB triplet
classification or cubic/adjoint coupling conjecture. Historical
mathematical originality is not established.

## Proof connection

The preceding actual Gram, correlation and multiplicity-preserving
[retrieval proof](phase-retrieval-alternatives.md) gives genuine unit
phases alpha,beta and shifts l,j, with E a shifted scalar copy of A or A*,
and C a shifted scalar copy of B or B*. Overlapping forms and repeated
ratios are allowed. Any adjoint-containing case is already covered by
[the adjoint branch](adjoint-branch-cancellation.md).

The new [preserving branch](proof/CirculantPreservingBranch.lean) handles
E=alpha P_l A, C=beta P_j B. Choose a complex square root
v^2=-beta/alpha. Its norm squared is one, and
v star(beta) alpha=-star(v). Put a'=shift_(j-l)(a), d=v b.
At theta^3=1 let s=theta^(j-l), k=theta^j, h=theta^l, where the indices
are in Fin3. The actual positive Fourier shift gives s^2=star(k)h.
Multiplying the actual cross-mode Gram equation by v star(s) yields

    star(mode(a',theta))*mode(d,theta)
      =star(mode(d,theta))*mode(a',theta).

Actual Gram and flatness already exclude every original zero mode;
unit v and the root-of-unity shift preserve this property. Thus all
hypotheses of the [actual real-mode theorem](real-mode-product-squares.md)
are derived internally. It gives p_a^2=v^6 p_b^2. The actual matrix
alternatives give p_e=alpha^3 p_a and p_c=beta^3 p_b; cubing the square-root
equation gives alpha^3 v^6+beta^3=0. These equalities imply the claimed
four-product cancellation at its original scale.

The final source exhausts the genuine retrieval alternatives and derives
all four character equalities. The exact formulas are

    chi_n(H)=3((p_a/p_c)^n+(p_b/p_e)^n),
    chi_n(H*)=3((star(p_a)/star(p_b))^n+(star(p_c)/star(p_e))^n).

Flatness supplies every required nonzero denominator. Cancellation makes
the two ratios negatives for each formula, hence the n=1 and n=3 results.
The preserving source has one audited endpoint and the final source has
two; each passed an actual author run and a separate reviewer run at
identical source hashes, with zero errors/warnings and only propext,
Classical.choice and Quot.sound. Earlier verified prerequisites are reused.

## Reproduction

Use Lean 4.34.1 and pinned Mathlib
`d13f23b723b8a846827a245b89c10fc7d3f11612` in the existing 002 package.
Set the absolute source/build directories and LEAN_PATH as in
[the earlier import instructions](ratio-multiset-retrieval.md). Obtain the
pinned cache for Mathlib.Analysis.Complex.Polynomial.Basic. Build these
project sources in this dependency order; keep the companion olean files:

```powershell
lake exe cache get Mathlib.Analysis.Complex.Polynomial.Basic
$taskModules = @('CirculantCharacter','UnitTripleZeroSum','CubeRootGramModes',
  'CubeRootGramMatching','CirculantAutocorrelation','CirculantRatioPolynomial',
  'CirculantPhaseRetrieval','CirculantInvertibility','CirculantAdjointBranch',
  'CirculantSpectralProducts','CirculantRealRank','CirculantPreservingBranch')
foreach ($taskModule in $taskModules) {
  lake env lean --root=$taskMubSources -o "$taskMubBuild/$taskModule.olean" "$taskMubSources/$taskModule.lean"
  if ($LASTEXITCODE -ne 0) { throw "Import build failed: $taskModule" }
}
lake env lean "$taskMubSources/CirculantCancellation.lean"
```

The adjacent audit and verification files record the actual checked
source hashes, compiler observations and separate reviewer runs. This
milestone closes the displayed-block theorem; the general companion
symmetry and shared-partition questions remain separate research targets.
