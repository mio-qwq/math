# CRYPTO3: actual SHA-256 schedule word distance

**Research candidate for integration; independently checked local results.**
The actual 64-word minimum distance is still known here only to be at
least **13**. No pair attaining 13, and no proof of a lower bound of 14,
is supplied by this release.

## Exact object

Two arbitrary, distinct vectors of sixteen 32-bit words are expanded by
the original SHA-256 modular-addition schedule to sixty-four words. The
distance counts differing words at all positions 0 through 63, including
the initial sixteen. There is no fixed-zero input, IV, padding,
independence, or random-message assumption. The definition is in
[FIPS 180-4, Sections 4.1.2 and 6.2.2](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf).

## Principal result: an exact local valuation ceiling

Write `f=sigma0`, `g=sigma1`, and `h(x)=x+g(x) mod 2^32`. For
arbitrary ordered pairs `(p,p')` and `(q,q')`, the three conditions

```
p'-p = q'-q = D != 0,
g(q')-g(q) = -D,
f(p')-f(p) = -(f(q')-f(q))
```

imply **v2(D)<=11**, where v2 is the number of trailing zero bits in
the nonzero residue. This local bound is sharp: the actual four words

```
p=0019f0ed, p'=973448ed, q=dff7f75f, q'=77124f5f
```

have `D=971a5800`, valuation 11, and satisfy every displayed equation.
They are a local object, not two input blocks. The
[proof with an independently checked RUP certificate](sha256-word-distance/coupled-boundary/PROOF.md),
[exact-version independent review](sha256-word-distance/coupled-review/REVIEW.md),
and [sharpness object](sha256-word-distance/coupled-sharpness/PROOF.md)
keep those scopes explicit. The frozen author proof predates the
completed review and sharpness object; its original pending-review
header is superseded by the separate review receipt, without changing
the reviewed bytes.

The reduction first proves that common low twelve bits in an h collision
force the single input XOR mask `fbca7000`. It then retains the common
additive difference and both sigma0 derivatives on their actual word
pairs. All 96 free input bits and every modular carry are represented in
the exact Boolean proof. A second, shorter affine-carry proof is supplied
in [coupled-short-proof](sha256-word-distance/coupled-short-proof/PROOF.md),
with its separate [independent reconstruction](sha256-word-distance/coupled-affine-review/REVIEW.md).
Its 13,098-byte certificate partitions 132 necessary masks among ten
contradictory templates. The checker reconstructs the mask coverage and
384 original-row occurrences, then directly XORs the templates; no
solver or Gaussian elimination is required for that check. The mask
feasibility test itself is explicitly attributed to the zero-output
special case of Lipmaa--Moriai's classical modular-addition criterion.

## Consequences for the exact frozen supports

For actual expansions let `d_i=W'_i-W_i`. The following table exhausts
the fifteen original support indices. Every new bound follows from
explicit original recurrence equations and applies to arbitrary base
blocks; none excludes an entire additional support.

| Support indices | Specified nonzero difference D | Status in this release |
|---|---|---|
| 0 | d30=d37=d44 | v2(D)<=11; D is not a signed power of two |
| 1 | d31=d38=d45 | Same |
| 2 | d32=d39=d46 | Same |
| 4 | d33=d40=d47 | Same |
| 5 | d17=-d8 | Same; the word pair at index 8 is reversed in both derivatives |
| 8, 9 | d29=d36=d43 | Same, with each boundary checked |
| 6 | d19=d35 | v2(D)<=20 |
| 7 | d21=d37 | v2(D)<=20 |
| 12 | d18=d34 | v2(D)<=20 |
| 13 | d20=d36 | v2(D)<=20 |
| 10, 11 | No new general difference restriction claimed | Remain open |
| 3, 14 | Earlier CRYPTO2 exclusions | Bounded independent written review and small dependency checks pass |

The first seven applications use 36 original recurrence substitutions,
including the [separate support-5 orientation](sha256-word-distance/coupled-boundary/SUPPORT5.md).
The four irregular-support bounds have a
[written proof](sha256-word-distance/mechanism/VALUATION_BOUND.md)
from output-width bounds, eleven carry masks and an explicit binary row
identity, with a separate
[independent review](sha256-word-distance/valuation-review/REVIEW.md).
No uncertified solver UNSAT is a premise of these bounds.

Conditional on the earlier complete support classification, exactly the
same thirteen indices remain: `0,1,2,4,5,6,7,8,9,10,11,12,13`.

## Further exact results and mechanism boundaries

The earlier [local h theorem](sha256-word-distance/LOCAL_PROOF.md) proves
that a nontrivial h collision cannot share thirteen low input bits and
cannot have a signed-power-of-two difference. Its own low-bit bound is
sharp. The [independent low-12 classification](sha256-word-distance/local-review/INDEPENDENT_PROOF.md)
checks all 255 nonzero binary-kernel masks and identifies its unique
survivor. The principal result above uses the extra sigma0 coupling to
exclude that boundary.

For support 0, the [base-completion theorem](sha256-word-distance/base-lift/PROJECTION.md)
gives an exact equivalence between an actual pair of schedules and
actual active word pairs satisfying all 48 difference equations plus
one base interpolation problem. With the thirteen active first words
fixed, thirteen inactive anchor words determine 38 other words by
reversible original equations. The remaining ten original recurrences
are exact residual conditions. Their solvability is not asserted. A
different agent independently reconstructed the elimination and checked
the [exact version](sha256-word-distance/base-review/REVIEW.md).

The [active-pair construction note](sha256-word-distance/active-pair-construction/PROOF.md)
retains every early and late difference equation, gives an exact module
criterion and a five-word parameterization of one reversed-sigma chain.
A natural specified mask family fails already modulo 8. This stops that
construction mechanism; it does not exclude support 0. The separate
[independent review](sha256-word-distance/active-pair-review/REVIEW.md)
accepts the full module equivalence, reversed chain, boundary and mod-8
proof. Its scope explicitly excludes independent checking of the optional
32-Q/4-P fibre enumeration; those finite data have the discoverer's
checker and are not premises of the accepted module or mod-8 results.

The periodic three-pair construction returned `unknown` at its fixed
20-second limit and was stopped. The local sharpness witness above shows
why repeating the four-word condition alone cannot lower its ceiling
below 11. Additional original recurrence or base constraints are needed.
[MECHANISMS.md](sha256-word-distance/MECHANISMS.md) distinguishes proved
constraints, useful local objects, and stopped exploratory calculations.

Independent review here means reconstruction and checking by another AI
agent that did not discover the reviewed principal result. It is not
external human peer review. No Lean compilation or whole SHA
implementation formalization is claimed.

## Inherited results and exact dependencies

| Source | Frozen Git commit | Use |
|---|---|---|
| Project main | `61488e05c9fe41984f483853f99e79f5715dc893` | Mathematical entry points and accepted Ascon/circulant scope |
| CRYPTO2 | `80b71cb3b6a67c8f8aae80d9cd8b6ed87d74bd51` | SHA v1/v2, RSA v2, exact support numbering |
| CRYPTO/Sora | `551fcd76ebabe43971123d29d11a94319a3b0096` | Public claims and documented missing recovery objects |

The copied support bytes have SHA256
`02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf`.
Their path and origin are bound by
[source-provenance.json](sha256-word-distance/source-provenance.json).
The older potential certificate's 5,308,416 transition inequalities and
the 735-node equality-support traversal were not rerun in this release.
The bounded review distinguishes previous executions from new checks.

[SOURCE_GATE.md](sources/SOURCE_GATE.md) records primary literature,
latest-version and errata checks, and access limits. Existing linearized
bit-weight bounds and reduced-step collision results are different
objects. Generic carry/SAT methods have prior literature. Specific
historical priority remains unconfirmed.

The [post-result source gate](sources/POST_RESULT_GATE.md) repeats the
narrow comparison after the new local result. The useful secondary
[circulant equivalence review](sources/circulant-equivalence/REVIEW.md)
checks periodic quotients, branch-number inheritance and the graph-code
formulation against the accepted theorem and primary literature. It
neither claims priority nor repeats the old minor enumeration. Earlier
Ascon, RSA and missing-recovery-package scopes are recorded in the
[bounded inherited-work review](review/review.md).

## Verification and file integrity

See [VERIFY.md](VERIFY.md) for reproducible commands and signature scope.
[SHA256.json](SHA256.json) lists the exact files in this release; the
manifest does not hash itself. [VERIFICATION.json](VERIFICATION.json)
records the first signed release checks; subsequent replay evidence is
recorded separately in [STAGE2_VERIFICATION.json](STAGE2_VERIFICATION.json).
The independent receipts bind reviewed bytes and must not be silently
reused after changes. Solver discovery runs are preserved separately
from the standard-library proof replay.

The original source packages remain unchanged. Work in this directory
does not modify or integrate project main, and does not claim any attack
on SHA-256, Ascon AEAD, RSA, or ChaCha.
