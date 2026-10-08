# Multiplicative-order spectra and an exact finite certificate for the ARC construction

## Status and notation

The finite polynomial identities in Section 1 and the abstract theorem in
Section 2 are established here. Section 3 is a **conditional application** to
OpenAI family 199; it is not an independently verified unconditional ARC
counterexample. Source data and methods are attributed in `ATTRIBUTION.md`.

All fields below have characteristic two. Modules are finite dimensional and
are left modules. For a symmetric finite-dimensional algebra `A`, write
`underline Hom_A` for morphisms modulo maps factoring through projective
modules. The stable shift `[1]` is inverse syzygy. Positive stable Hom is
ordinary Ext. Tensor products are over the stated field unless a subscript
specifies an algebra. The order of a nonzero field element is its
multiplicative order, with value infinity when no positive power is one.

## 1. A finite polynomial certificate

Let `S=F_2[q]`, with `q` an indeterminate. Define an `S`-algebra `C`, free as an `S`-module,
on the basis

\[
 e,x,y,z,u,v,t,j,f,n
\]

by the following multiplication data. The orthogonal idempotents `e,f` sum
to the identity, and the corners are

\[
 eCe=\langle e,x,y,z\rangle,\quad eCf=\langle u,v\rangle,
 \quad fCe=\langle t,j\rangle,\quad fCf=\langle f,n\rangle.
\]

Aside from the corner idempotent actions, the nonzero products are

\[
\begin{gathered}
 xy=qz,\ yx=z,\ xu=yu=v,\ tx=j,\ ty=q^2j,\\
 ut=y+qx,\ vt=qz,\ uj=z,\ tu=(1+q)n,\ nt=qj,\ un=v.
\end{gathered}
\]

Every unlisted product is zero. Put `T=C` plus its `S`-linear dual as a
square-zero trivial extension. A capital basis letter denotes the dual of
its lowercase letter. Thus, for lowercase letters `a,b,c`, its remaining
structure coefficients are

\[
 \mu_{a,b^*}^{c^*}=\mu_{ca}^{b},\qquad
 \mu_{b^*,a}^{c^*}=\mu_{ac}^{b},\qquad
 \mu_{a^*,b^*}^{v}=0.
\]

Let `I=Se` plus `Sf` and let `r` be the span of all 18 basis letters other
than `e,f`. The relative three-cochain

\[
 p:r\otimes_I r\otimes_I r\longrightarrow T
\]

is specified completely by the 179 entries in `data/arc-core.json`.
An entry `["tyJf",3]`, for example, means `p(t,y,J)=q^3f`. Unlisted
entries are zero.

**Proposition 1 (finite identities).** These data define an associative
unital algebra `T`. Its trace given by the sum of the `E,F` coefficients is
symmetric and nondegenerate. The cochain `p` respects the endpoints, lowers
the number of dual letters by one, and has Hochschild differential zero.
For every nonzero scalar `H` after base change to a field, let `h_H` fix `C`
and scale its dual ideal by `H`. Put

\[
 z_H(a)=Hqa\quad\text{for }a\in\{u,v,t,E,X,Y,Z,U,V\},
 \qquad z_H(a)=0\quad\text{otherwise}.
\]

Then, for all `a,b` in `r`,

\[
 \sum_{w\in\mathcal B_r}p(a,b,h_H(w))w^*
 =a z_H(b)+z_H(ab)+z_H(a)h_H^{-1}(b).
\]

Moreover, for the `f`-simple `s`, the two-sided-simple relative bar element

\[
 \zeta=q^2[t|x|J]+[t|y|J]
\]

is a cycle, and its pairing with `p` is `q^3`. In particular, after
specializing to any field with `q` nonzero, the evaluated cohomology class
is nonzero in `Ext_T^3(s,s)`.

**Proof and certificate interpretation.** Integer bit `i` in the checker
represents the coefficient of `q^i`. Addition is bitwise XOR;
multiplication shifts and XORs according to convolution. These operations
give exact polynomial arithmetic in `F_2[q]`. A second implementation by
sparse exponent sets checks the arithmetic implementation on all pairs of
polynomials of degree at most seven; the underlying exact identities use
the displayed formulas, without a degree truncation.

The checker constructs every structure coefficient from the data and the
dual recurrences. It checks `(ab)c=a(bc)` on all `20^3=8000` basis triples
and checks the unit on every basis letter. Trilinearity then proves
associativity and the unit identities on arbitrary elements. On all basis
pairs the trace pairing equals `1` precisely on a letter and its dual, and
zero otherwise. Its matrix is therefore a symmetric permutation matrix,
which proves nondegeneracy over `S` and after every field specialization.

For all `18^4=104976` radical four-words it computes

\[
 a p(b,c,d)+p(ab,c,d)+p(a,bc,d)+p(a,b,cd)+p(a,b,c)d
\]

and checks that every coefficient is the zero polynomial. Multilinearity
proves Hochschild closure on the entire relative bar term. Endpoint checks
justify balancing over `I`; the invalid endpoint words vanish as well.

For the boundary identity, write `epsilon_b=0` or `1` according as `b` is
lowercase or capital, and let `gamma_a=q` on the displayed nine-letter set,
zero otherwise. On the coefficient of output letter `v`, the right side
of the identity is

\[
 \bigl(H\gamma_b+H\gamma_v+H^{1-\epsilon_b}\gamma_a\bigr)
 \mu_{ab}^{v}.
\]

Both sides have only constant and linear terms in `H`. For each of the
`324` radical input pairs the checker verifies both polynomial
coefficients. Thus the identity holds for indeterminate `H`, and hence
for every nonzero specialization. This proof does not assume algebraic
independence of `q,H`.

The cycle differential has only its inner faces, since the radical kills
the endpoint simples. The exact products `tx=j`, `ty=q^2j`, `xJ=T`,
`yJ=q^2T` give zero differential by cancellation in characteristic two.
The checker verifies this and the pairing `q^2p(t,x,J)+p(t,y,J)=q^3f`.
A coboundary pairs to zero with a cycle. For `q` nonzero this pairing is
nonzero, proving the final assertion. This completes a finite,
independently replayable proof of precisely the identities stated here.

The positive grading assigns degrees `u,t=1`, `x,y,n=2`, `v,j=3`, `z=4`
and degree `5-deg(a)` to each dual letter. The checker verifies that every
nonzero product respects degree. Over a field the positive-degree ideal
is consequently nilpotent and has quotient `k^2`; it is the radical of
`T`. Also `(ut)^2=q(1+q)z`, which is nonzero when `q` is neither zero nor
one. These finite statements still do not identify all self-Ext degrees
or verify the later bimodule-cone realization.

## 2. The abstract extension-spectrum theorem

This section is independent of the particular algebra in Section 1.

Let `A` be a finite-dimensional symmetric algebra over `k`, `X` a finite
left `A`-module, and `F` a finite `A`-bimodule projective on each side.
Suppose that `v` is a stable map from `X` to `FX=F` tensor over `A` with `X`.
Set

\[
 H^a=\underline{\operatorname{Hom}}_A(X,X[a]),\qquad
 V^a=\underline{\operatorname{Hom}}_A(X,FX[a]),
\]

and define

\[
 \delta^a:H^a\oplus H^a\longrightarrow V^a,
 \qquad (g,j)\longmapsto F(g)v+v[a]j.
\]

Choose an actual representative `v_0` and an injection `i:X` into a finite
projective module `Q`. Define

\[
 \Lambda=\begin{pmatrix}A&0\\ F&A\end{pmatrix},\qquad
 Y=(FX\oplus Q)/\{(v_0(x),i(x)):x\in X\},\qquad
 Z=(X,Y,\iota),
\]

where `iota` is the injection from `FX` induced by the first summand.
A triangular-algebra module `(M,N,eta)` means that `eta:FM` to `N`
specifies the off-diagonal action.

**Lemma 2 (conversion exact sequence).** The module `Z` is
Gorenstein-projective, all `Ext_Lambda^a(Z,Lambda)` for `a>0` vanish, and
for every `a>0` there is an exact sequence

\[
 0\longrightarrow\operatorname{coker}\delta^{a-1}
 \longrightarrow\operatorname{Ext}_\Lambda^a(Z,Z)
 \longrightarrow\ker\delta^a\longrightarrow0.
 \tag{1}
\]

If `ker delta^0` is nonzero then `Z` is nonprojective.

**Proof.** Since `A` is symmetric, choose a complete projective resolution
`P` of `X` with `P_{-1}=Q`. Introduce the two column functors

\[
 E(M)=(M,FM,1),\qquad J(N)=(0,N,0).
\]

They are exact and preserve projectives. Both `E(P)` and `J(P)` are
totally acyclic: their Hom complexes into `Lambda` identify with sums of
`Hom_A(P,A)` and `Hom_A(P,F)`, which are exact because `A,F` are
projective-injective on the left. The stable map `v` lifts to a complete
chain map from `J(P)` to `E(P)`; its mapping cone is totally acyclic, and
its degree-zero cokernel is the displayed finite module `Z`.

For completeness, lifting a map on cokernels to a complete chain map
uses projectivity in positive indices and injectivity of projective
`A`-modules in negative indices. Two lifts differ by a chain homotopy
exactly when the original difference factors through a projective.
In positive degrees this is the usual projective-resolution description
of Ext. Thus complete Hom cohomology agrees with stable Hom and positive
Ext. These identifications respect composition.

There are no maps from `E(M)` to `J(N)`, whereas maps from `J(N)` to
`E(M)` are `Hom_A(N,FM)`. Consequently the complete endomorphism complex
of the cone has its diagonal quotient and a single off-diagonal
subcomplex. Its diagonal degree-`a` cohomology is `H^a` plus `H^a`; its
off-diagonal degree-`a+1` cohomology is `V^a`. The connecting map is
composition with the cone chain map on its two sides, hence is exactly
`delta^a`. The resulting long exact cohomology sequence gives (1).
Total acyclicity gives Gorenstein-projectivity and Ext vanishing into
`Lambda`. At degree zero the same sequence gives a surjection of stable
endomorphisms of `Z` onto `ker delta^0`. A projective module has zero
stable endomorphisms, proving the last assertion.

Here full Hom complexes use the product over all complete-resolution
indices; the cone has a finite number of blocks. Thus the blockwise
short exact sequence is split degree by degree, and no interchange
of an infinite direct sum with cohomology is needed.

**Theorem 3 (multiplicative-order classification).** In the setup of
Lemma 2, assume the following explicit additional hypotheses:

1. `H^0=k` and `V^0=kv`, with `delta^0(c,d)=(c+d)v`.
2. For every `m>=1`, `dim H^{3m}=m+1`; all other positive `H^a` vanish.
3. For every `a>0` there is an identification `V^a=(H^a)^2`. For fixed
   `h_1,h_2` in `k` nonzero, under that identification

\[
 \delta^{3m}(g,j)=(h_1^{-m}g+j,h_2^{-m}g+j).
 \tag{2}
\]

Let `d=ord(h_1/h_2)`. Then `Z` is a finite nonprojective
Gorenstein-projective module, with `Ext_Lambda^a(Z,Lambda)=0` for every
`a>0`. If `d` is infinite, every positive self-Ext of `Z` vanishes. If
`d` is finite, then for every positive integer `m`,

\[
 \dim_k\operatorname{Ext}_\Lambda^{3m}(Z,Z)
 =\dim_k\operatorname{Ext}_\Lambda^{3m+1}(Z,Z)
 =\begin{cases}m+1,& d\mid m,\\0,&d\nmid m,\end{cases}
 \tag{3}
\]

and all remaining positive self-Ext degrees vanish. Its positive
self-Ext dimension generating series is

\[
 \sum_{a\ge1}\dim_k\operatorname{Ext}_\Lambda^a(Z,Z)z^a
 =\frac{(1+z)z^{3d}(d+1-z^{3d})}{(1-z^{3d})^2}
 \tag{4}
\]

when `d` is finite, and is zero when `d` is infinite. The series has
integer coefficients; `d+1` in (4) is an integer dimension, not a
scalar in `k`.

**Proof.** The scalar matrix in (2) has determinant

\[
 h_1^{-m}+h_2^{-m}.
\]

It is nonsingular exactly when `(h_1/h_2)^m` is not one. In that case its
kernel and cokernel vanish. In the singular case its two rows coincide,
and each row is nonzero because its second entry is one. It has rank one,
and tensoring it with the identity of the `(m+1)`-dimensional space gives
kernel and cokernel dimension `m+1`.

In every other positive degree the source and target of `delta` are zero.
At degree zero `delta^0` is surjective with one-dimensional kernel.
Substitution into (1) proves (3), the degree-one vanishing, and all the
assertions about projectivity and Ext into `Lambda`. There is no overlap
between a degree `3m` and a degree `3m+1`. For finite `d` the surviving
terms are therefore

\[
 (1+z)\sum_{j\ge1}(jd+1)z^{3jd}.
\]

Using `sum_{j>=1}u^j=u/(1-u)` and
`sum_{j>=1}j u^j=u/(1-u)^2` proves (4).

Thus, within this explicitly assumed stable-profile setup, total
positive self-Ext vanishing holds **if and only if** the twist ratio has
infinite multiplicative order. Finite orders in a field of characteristic
two are odd: an element of even order `2r` would satisfy
`(x^r-1)^2=0`, hence already satisfy `x^r=1`.

## 3. Conditional one-variable application to OpenAI family 199

Related prior work: Qiyue Tang's [Hexagon 2610.00143v1](https://hexagonmath.org/pdf/2610.00143v1),
Theorem 1.1 and Corollary 1.2, include the one-variable field extension
discussed below. It is not presented here as a new base-field
counterexample. Our application retains its explicit unverified
realization hypotheses; see [ATTRIBUTION.md](ATTRIBUTION.md).

The upstream manuscript chooses `k=F_2(q,H_1,H_2)` with three algebraically
independent variables. Its finite cochain identities need no such
independence, as Proposition 1 verifies. Its starting resolution uses
`q` nonzero and `1+q^m` nonzero for every positive integer `m`. These
conditions hold whenever `q` has infinite multiplicative order. Its final
comparison matrix uses only `H_1^m != H_2^m`, which is exactly the
infinite-order condition on `H_1/H_2`.

**Conditional Corollary 4.** Suppose the upstream all-degree resolution,
stable two-cone profile, lifted bimodule maps, and finite-fiber realization
continue to satisfy Theorem 3's hypotheses whenever `q` has infinite
multiplicative order and `H_1,H_2` are nonzero. Then the upstream
construction works over `F_2(t)` with

\[
 q=t,\qquad H_1=1,\qquad H_2=t.
\]

More generally it works over every characteristic-two field that is not
algebraic over `F_2`. Under the same realization hypothesis, arbitrary
nonzero twists satisfy exactly (3)-(4), including their resonant
finite-order cases.

**Proof under the stated hypothesis.** All `1+t^m` are nonzero in
`F_2(t)` and `t` has infinite order. So do the determinants `1+t^{-m}`.
Theorem 3 therefore gives the required positive vanishings. A field `K`
not algebraic over `F_2` contains a transcendental element `t`, giving an
injective field map `F_2(t)` to `K`. Finite projective resolutions and
complete projective resolutions remain exact under field extension;
termwise finite Hom commutes with the extension. Hence both Ext
vanishings and Gorenstein-projectivity pass to `K`. Nonprojectivity also
passes: any nonsplit finite projective-cover sequence represents a
nonzero Ext class, and faithful field extension preserves that class.

Every nonzero element algebraic over `F_2` lies in a finite field and has
finite order. Conversely, a finite-order element satisfies a polynomial
`X^n-1`, so is algebraic. Thus a characteristic-two field contains an
infinite-order element exactly when it is not algebraic over `F_2`.
This describes the parameter mechanism only; it says nothing about
possible counterexamples over algebraic fields from other constructions.

The [separate multiplication theorem](resonant-yoneda-algebra.md)
adds explicit polynomial-algebra and two-sided branch action hypotheses.
It identifies the positive Yoneda algebra at a finite twist resonance
with `R_+ + epsilon R_+`, for the corresponding Veronese R and
epsilon squared zero. It includes only scalar degree-zero endomorphisms
when adjoining a unit. The dimension hypotheses of Theorem 3 alone do
not imply this stronger conclusion.

**Remaining gap.** The finite checker proves neither the uniform
infinite resolution nor the stable two-cone profile or the chain-level
lift to a finite side-projective bimodule. Those are substantive
homological assertions. The proposed specialization requires them over
the one-variable field; mere specialization of arbitrary rational
matrices from the original three-variable field does not justify it,
because their denominators could vanish. One must reconstruct the
choices over the smaller field, or furnish uniform formulas for those
choices and check all their denominators. The source's construction
suggests reconstruction is possible, but this note does not mark that
remaining task as completed.

## Reproducibility and references

The exact data, source commit and source-file SHA-256 hashes are in
`data/arc-core.json`. Run `python checker/verify.py` using only Python's
standard library. The report records the fixed-input hash and the
enumeration counts, and explicitly declines verification of the entire
ARC realization.

OpenAI, *An explicit counterexample to the Auslander--Reiten conjecture*,
September 23, 2026, family 199, source commit
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`.
The particular finite tables and conversion sequence are prior upstream
material. The exact finite certificate, multiplicative-order spectrum,
generating-series computation and conditional specialization analysis are
the contributions recorded here. No literature-priority assertion is made.
