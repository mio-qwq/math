# Actual flat triples with real Fourier ratios

For two actual complex triples a,d with unit entries, suppose their raw
three-point Fourier modes are nonzero and satisfy

    star(mode(a,theta))*mode(d,theta)
       = star(mode(d,theta))*mode(a,theta),    theta^3=1.

Then the [Lean theorem](proof/CirculantRealRank.lean) proves

    phaseProduct(a)^2=phaseProduct(d)^2.

The products are the actual three entries, and modes are the actual raw
Fourier polynomials. Nonzero modes and the displayed real-ratio cross
equations are explicit hypotheses. The theorem derives the needed neighbor
sums and cubic-product identities from the entries; these identities are
not extra certificate inputs to the actual-triple endpoint.

This formalizes the real-rank ingredient of
[the written four-circulant proof](direct-circulant-character.md#6-real-rank-lemma-for-the-symmetric-minus-form).
The [final four-block module](flat-gram-cancellation.md) now derives these
hypotheses from the both-preserving retrieval branch and composes
unconditional flat-Gram cancellation. This real-mode source retains its
explicit inputs. General companion symmetry and MUB coupling remain separate.
Historical mathematical originality is not established.

Write m0,m1,m2 for the modes of a at 1,omega,omega^2, with omega a primitive
cube root, and n0,n1,n2 for d. The
[actual spectral identities](proof/CirculantSpectralProducts.lean) are

    27 phaseProduct(a)=m0^3+m1^3+m2^3-3m0 m1 m2,
    m0 star(m1)+m1 star(m2)+m2 star(m0)=0.

The first holds for arbitrary triples; the second follows from actual unit
entries, since its expansion is 3(a0 star(a0)+omega^2 a1 star(a1)+omega a2 star(a2)).
Both follow from the actual raw mode definition and omega^2+omega+1=0.

Set qi=ni/mi. The cross equations make each qi fixed by conjugation, and
the supplied nonzero modes make all denominators nonzero. Put
w0=m0 star(m1), w1=m1 star(m2), w2=m2 star(m0). Flatness gives both

    w0+w1+w2=0,
    q0 q1 w0+q1 q2 w1+q2 q0 w2=0.

The proof splits on K=w0 star(w1)-star(w0) w1. If K is nonzero,
the last equations and their conjugates imply q0=q1=q2=q. The two actual
cubic identities give p_d=q^3 p_a, and the unit products give q^6=1.
Their squares therefore agree.

If K=0, w1/w0 and w2/w0 are real. With r=m1/m0, s=m2/m0,
t=s/star(r), u=r star(s)/star(r), both t and u are real and t is nonzero.
Then s=t star(r) and (r star(r))u=t r^3 imply that r^3, s^3 and rs are
real. The actual cubic identities show that p_a/m0^3 and p_d/m0^3
are real. Two unit complex numbers on the same real line have equal
squares; the Lean proof obtains this by cross multiplication and the
actual unit-product equations. No choice of a phase, sign enumeration
or assumption of generic ratios is needed.

The first core theorem keeps its spectral inputs explicit; the final
actual-triple theorem supplies both neighbor equations and both cubic
identities from the actual entries. Each new source has two endpoint
audits, with actual author and separate reviewer compilations at identical
source hashes: zero errors/warnings and only propext, Classical.choice,
Quot.sound. The preceding project imports are reused unchanged.

Use Lean 4.34.1 and fixed Mathlib
`d13f23b723b8a846827a245b89c10fc7d3f11612` in the pinned 002 package.
Follow [the correlation import instructions](ratio-multiset-retrieval.md)
through Autocorrelation, then build the new spectral import and replay:

```powershell
lake env lean --root=$taskMubSources -o "$taskMubBuild/CirculantSpectralProducts.olean" "$taskMubSources/CirculantSpectralProducts.lean"
lake env lean "$taskMubSources/CirculantRealRank.lean"
```

The [adjoint-containing cases](adjoint-branch-cancellation.md) already have
a separate actual product-cancellation theorem. The
[completed four-block result](flat-gram-cancellation.md) now supplies the
both-preserving normalization and composes all alternatives.
