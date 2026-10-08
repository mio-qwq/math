# Actual Gram bounds and four circulant block inverses

For an actual six-by-six complex matrix H=[C(a) C(b); C(c) C(e)], with
C(a) the Mathlib circulant a(i-j) on Fin 3, suppose all actual entries have
normSq one and H.conjTranspose*H=6 I. Then every raw three-point Fourier
amplitude of every block is nonzero, all four block determinants are nonzero,
and there exist four actual inverse matrices with all eight left/right
multiplication equations. No mode bound, nonzero mode, block inverse or
genericity condition is supplied as an additional hypothesis.

This closes the previous explicit mode-bound premise in
[the scalar zero-mode interface](zero-mode-obstruction.md), and formalizes
the block invertibility used in Section 2 of
[the complete written branch proof](direct-circulant-character.md).
It is a connected formal proof of classical Fourier/Gram ingredients;
historical originality is not established. Phase retrieval, its repeated-root
classification, real-rank cases and full block-product cancellation remain
unformalized. The general complete-companion symmetry/coupling question is open.

The subsequent [opposite-power source](mode-power-matching.md) also derives
matching powers of a/e and b/c from the single column Gram equation.
That separate three-audit module supplies a premise for future phase retrieval;
the classification itself remains unformalized.

The [Gram source](proof/CubeRootGramModes.lean) defines the actual raw amplitude

    mode(a,theta)=a0+a1 theta+a2 theta²,    theta³=1.

Only three actual Gram entries are needed per block pair. For the left pair,
the entries at (inl0,inl0), (inl0,inl1), (inl0,inl2) are respectively 6,0,0.
Their expansions are g0,g1,g2. Using star(theta)=theta², the exact polynomial
identity is

    cast(normSq mode(a,theta)+normSq mode(c,theta)) = g0+theta² g1+theta g2.

Thus normSq mode(a,theta)+normSq mode(c,theta)=6. The right actual columns
give normSq mode(b,theta)+normSq mode(e,theta)=6. Nonnegativity gives all
four bounds at most six. Combining actual entry flatness with the already
proved arbitrary-root zero-mode obstruction yields all four nonzero modes.
Both mode bounds and nonzero modes are derived from actual matrix equations.

The [inverse source](proof/CirculantInvertibility.lean) proves the actual
determinant identity for any primitive cube root omega:

    det C(a)=mode(a,1) mode(a,omega) mode(a,omega²).

It chooses omega=exp(2 pi i/3) using the pinned Mathlib primitive-root theorem;
the final block-inverse result has no root-existence premise. All three
factors are nonzero by the actual Gram theorem. The same proof treats b,c,e.
The formal conclusion constructs A',B',C',E' and proves

    C(a)A'=A'C(a)=I,  C(b)B'=B'C(b)=I,
    C(c)C'=C'C(c)=I,  C(e)E'=E'C(e)=I.

This is actual matrix invertibility, rather than just a list of nonzero
supplied eigenvalues or an assumed nonsingular determinant.

There are five Gram declarations and three determinant/inverse declarations.
The source-specific actual compiler records and audits accompany each file;
each has a separate reviewer replay. Lean 4.34.1 and fixed Mathlib
`d13f23b723b8a846827a245b89c10fc7d3f11612` are retained. These sources
reuse the separately verified character and unit-triple modules unchanged.

To replay from the existing `002-weighted-rectangular-pruning/proof/mathlib`
package, first obtain the pinned cache for the imports, then build the three
project import objects in a fresh temporary directory. Run these sequentially:

```powershell
$taskMubBuild=Join-Path ([System.IO.Path]::GetTempPath()) ("math-mub-gram-"+[guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $taskMubBuild | Out-Null
$taskMubSources='../../../004-mub-triplets/proof'
lake env lean --root=$taskMubSources -o "$taskMubBuild/CirculantCharacter.olean" "$taskMubSources/CirculantCharacter.lean"
lake env lean --root=$taskMubSources -o "$taskMubBuild/UnitTripleZeroSum.olean" "$taskMubSources/UnitTripleZeroSum.lean"
$env:LEAN_PATH=$taskMubBuild+[System.IO.Path]::PathSeparator+$env:LEAN_PATH
lake env lean --root=$taskMubSources -o "$taskMubBuild/CubeRootGramModes.olean" "$taskMubSources/CubeRootGramModes.lean"
lake env lean "$taskMubSources/CirculantInvertibility.lean"
```

No whole-matrix Fourier spectral theorem, phase retrieval or general MUB
resolution should be inferred from these eight formal declarations.
