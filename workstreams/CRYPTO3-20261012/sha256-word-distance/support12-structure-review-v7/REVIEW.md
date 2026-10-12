# Independent mathematical review of support12-structure-v7

**PASS within the precise selected-local scope below.** This is a separate
AI review of written proofs and their finite dependencies, not human peer
review or proof-assistant formalization. No complete support is excluded
and no real 16-word message pair or distance-14 theorem is supplied.

The author snapshot consists of eight files plus `manifest.json`, whose
hash is `8a5d97b2f671ae416ed296267bc25df2835c053fa9d318b01bf5bc68c615288a`.
All eight recorded author hashes matched. The accepted proof hash is
`e5ac4955289a850266b4c6891f6cd1249324f4d6b840c6747212e556e08e1bb5`;
the certificate hash is
`383906352d2622e9dc071ca26a32d57355659ef683549072e632c47f817b60f6`.

## Independence and complete signature coverage

Before reading any author-v7 bytes, the reviewer reconstructed the original
support-12 lag rows, both anti-cycle identities, all 1,024 sigma0 valuation
systems, and the correct orientation of the three-pair image condition.
`PRECOMPARISON_MANIFEST.json` froze that blind work with hash
`3d2e2ab37250187ed2e9f643eb5475ee01e72ae7eca8a82c4485579f85410a2a`.
The independent table hash is
`7a1fa0d29d368e2c93d304e182f90ff48408640c6b42b82fe00992044f3f1a4e`.
The blind files remain byte-identical after comparison.

The original recurrence gives
`-E33=d26+F18` and `-E41-E34=F26+d18`.
Thus actual X at 18 and P at 26 have `(d,F)=(D,A),(-A,-D)`, with
D,A nonzero. The reviewer checked these identities directly at each
of supports 12,6,7,13 using shifts 0,1,3,2 and reconstructed all 48 rows
for each pattern. The additional original-row identity
`E_(42+r)-E_(33+r)=d_(42+r)+F_(18+r)` verifies A's second support interface.

For each signature `(k,l)`, the blind packet supplies either an input XOR
mask satisfying the original affine bit equations or an explicit XOR of
those original rows yielding `0=1`. It covers all 417 feasible and 607
infeasible systems. An independently derived homogeneous-form/rank test
agrees on all 1,024 cases. The author's witnesses and contradiction-row
selections were then checked directly and matched the blind **feasibility
table**, without requiring their masks or row selections to be identical.

The table intersected with its transpose has exactly 309 entries. Each
entry satisfies the necessary constraints

```
k+l <= 30, k<=23, l<=23,
l>=18 implies k=l-18<=5.
```

For k=16 the necessary l values are exactly `{0,1,...,10,12}`. These
are exact binary-signature restrictions and only necessary conditions
for the numerical coupled equations. Separate mask witnesses do not
match the actual D,A values between two pairs. Neither all 309 numerical
anti-cycles nor whole-support assignments have been constructed. The
older three-pair ceiling 16 is not newly re-proved in this review.

## Exact local image equivalences and reversal signs

For fixed D!=0 define
`I_D={(F_D(z),G_D(z)):z in Z/(2^32)}` using the same actual z,z+D
in both derivatives. The selected three-pair equations are exactly
equivalent to the existence of A,T with

```
(A,T-D), (A,T+D), (-A,-T) in I_D.
```

The blind original-row derivation obtains these pairs at 18,34,43 with
T=-d13. More generally the author's local core sets T=G(X)+D, which
requires no division by two. The third original pair has
`(d,F,G)=(-D,A,T)`; reversing it changes **all three** signs and supplies
the third forward-D image member `(-A,-T)`. The converse chooses actual
preimages of all three image points and reverses the third actual pair.
It proves exactly the stated local equations and carries its hidden
preimage obligations; it supplies no base-message completion.

Adding the fourth actual pair with `(d,F)=(-A,-D)` is exactly equivalent
to adding `D in R_A`, where `R_A` is the actual sigma0 derivative image
at additive input difference A. Necessity reverses P to a forward-A pair.
Sufficiency chooses a real forward-A preimage and reverses it. The sigma1
derivative of this fourth pair and all unselected original equations are
still absent constraints. The fibre formulation with c=G(X), requiring
`c,c+2D in B_(D,A)` and `-c-D in B_(D,-A)`, is the same substitution
T=c+D. No independent derivative assignment or image-distribution
assumption occurs.

The reviewer verified all 64 inverse basis identities by direct rotations
and shifts for f and g. Binary linearity then gives right inverses on the
entire 32-dimensional space, and finite equal dimensions imply
bijectivity. Thus in the three-pair core A!=0 and T is outside
`{0,D,-D}`. The local existence criterion remains exact; its memberships
are not established for arbitrary D.

## Additional analytic claims, reviewed after the author snapshot

The finite dependencies `f(2^31)=0x11002000` and
`f(0x94857ee6)=2^31` were directly checked, together with valuations 13
and 1. Since f is bijective, the latter preimage is unique. If D=2^31,
X has input XOR mask 2^31, forcing v2(A)=13; P's output XOR mask is
2^31, forcing its input valuation v2(A)=1. This is impossible. Interchanging
X with the reversed P gives the corresponding obstruction A!=2^31.
This proof is specific to reciprocal sigma0 coupling and does not require
the 1,024-case table or an SMT result.

The endpoint exclusion is correct **when the fourth reciprocal condition
is present**. Write X=(x,x+D), R=(r,r-D), with equal f derivatives A.
If their first endpoints agree, injectivity gives x-D=x+D and hence
2D=0. If their second endpoints agree, equal derivatives and injectivity
first force agreement of their first endpoints, with the same conclusion.
If either crossed endpoint agrees, R is exactly the reverse of X, giving
2A=0. In the word ring a nonzero solution to 2D=0 or 2A=0 is 2^31,
already excluded above. The same argument applies to Y. Thus the two R
endpoints are disjoint from every X or Y endpoint. X and Y cannot share
an aligned endpoint, since that would make them the same pair, whereas
`G(Y)-G(X)=2D!=0`. Their union has at least three values and R adds two,
proving at least five distinct word values. This conclusion is not
claimed for a bare three-pair core without reciprocal coupling.

The finite-sum argument in Section 6 is also correct. For a permutation
f of an even cyclic group of order N, h(z)=f(z)-z has sum zero, while
the sum of all residues is N/2 modulo N. Therefore h cannot be a
permutation. On a finite equal-size domain it must have a collision
h(x)=h(y), x!=y. With D=y-x one gets f(y)-f(x)=D!=0; choosing
X=(x,y), A=D and P=(y,x) realizes the reciprocal sigma0 system alone.
This is a nonconstructive existence statement about two pairs. It
fulfills neither sigma1 joint-image obligations nor the remaining support
or base equations. It correctly prevents treating the reciprocal-only
model as globally impossible, and no historical novelty is claimed.

## Reproduction, faults, and accepted scope

```
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-structure-review-v7/check_signatures_independent.py
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-structure-review-v7/compare_author.py
```

Both commands are read only and pass. `--save` was used only to record
initial independent evidence and the final review receipt in this
directory. Neither checker imports author code or calls a solver.
The blind checker rejects six altered proof dependencies. The comparison
checker rejects seven altered author certificate dependencies, including
missing coverage, wrong witnesses or XOR contradictions, incorrect
transpose entries, damaged f/g inverse columns, and a wrong half-word
valuation. `RUN.json` pins both snapshots, source hashes and actual results.

The accepted statements are the exact selected-local image equivalences,
the complete one-pair binary signature classification, the reciprocal
necessary valuation restrictions, and the correctly conditional analytic
consequences above. They provide no complete support feasibility or
exclusion, real 13-word schedule witness, distance>=14 proof, hash attack,
Lean formalization, human peer review, originality finding, DOI, Release
or main integration. Previously frozen stages were left unchanged.
