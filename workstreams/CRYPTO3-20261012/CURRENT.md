# CRYPTO3 continuation checkpoint

Branch: `partner/dist-CRYPTO3-20261012`. Recovery base:
`b7eb3becacf474a6978b6acb2879fce3d505e395`.
Stage 4 was uploaded and checked at
`f888115f03f2ef1e06189296378f6ca200d1264b`; stage 5 was uploaded and
checked at `24684c0207db415a60f7de57291d6aaf627eb287`. Later accepted
stages are recorded below and in their own frozen manifests. Stage 6
was uploaded and checked at `78d0b1395cbcfca1d647c8bfeb30493d2a351473`.
The original stage-2 README, publication status, manifests and reviewed
proof bytes are preserved. This checkpoint describes later work.

## Exact object and present global boundary

Two arbitrary, distinct sixteen-word blocks are expanded by the original
32-bit modular-addition SHA-256 schedule. Distance counts unequal words at
all 64 positions, including the input. The universal lower bound remains
**13**. There is no actual distance-13 message pair or bound of 14 here.

## Evidence recovery and independent acceptance

- The XZ transport copy restores all 12,444,726 original RUP bytes with
  SHA256 `cd1845cdde5fca010b4b8557bcb27947eb5aef50b45856619cce7d54608540c5`.
  All 203 listed stage-2 files match; with their manifest, this is the
  documented 204-file frozen release. All 21 isolated replay commands pass.
- [The inherited global gate](sha256-word-distance/inherited-gate-v4/)
  newly checks all 5,308,416 transition inequalities, all 65,535 nonzero
  initial states, all 65,536 terminal zeros, and the entire equality-path
  traversal of 735 nodes and 15 supports. The universal no-singleton
  reduction and the two old support exclusions receive written independent
  reconstruction. This closes the prior bounded-review replay gap.
- [Independent window review](sha256-word-distance/shift-review-v4/REVIEW.md)
  accepts the exact seven left maps, three right maps and `3 -> 14`.
  Every sixteen-word window of the uniquely extended actual recurrence
  remains a legal, distinct input pair. With the now checked inherited
  dependencies, distance-13 existence reduces to the six representatives
  **5, 8, 9, 10, 11, 12**. This excludes no additional representative.

## New independently accepted local results

| Exact support scope | New restriction | Current acceptance |
|---|---|---|
| 12, and 6/7/13 by directly checked recurrence bridges | **`v2(D)<=16`**, with `D=d18=d34` on support 12 | [Stage-6 independent acceptance](sha256-word-distance/support12-review-v6/REVIEW.md), 7,538,454 new complete three-mask cases; stages 4 and 5 remain explicit accepted dependencies |
| 10 and 11 | `min(v2(d18),v2(d34))<=15` | [Independent acceptance](sha256-word-distance/supports10-11-review-v4/REVIEW.md), complete 65,536-mask cover and both actual local sharpness fixtures |

The first bound progressed from 20 to 18, 17 and now 16. The second is a joint restriction;
neither individual valuation is asserted to be at most 15. These constrain
actual schedules having the named supports, but do not exclude a complete
support. Local sharpness fixtures are actual word pairs, not messages.

## Stage-8 accepted support-12 reductions and fixed residue

[The corrected full-row factorisation](sha256-word-distance/support12-full-factor-v9/PROOF.md)
and [its independent acceptance](sha256-word-distance/support12-full-factor-review-v8/REVIEW_V9.md)
now account for all 48 original support-12 difference rows. There are 25
nonzero rows and 23 identities; integer unit elimination has rank 25 and
free rank 14. Four boundary-private coordinates can be absorbed into their
own actual-pair factors, leaving an exact connected ten-scalar system of
thirteen same-word-pair conditions: nine full joint `(d,F,G)` memberships,
three exact `(d,F)` projections and one exact `(d,G)` projection. Feasibility
of this factor system is not asserted.

The first author factor package is deliberately preserved and
[independently rejected](sha256-word-distance/support12-full-factor-review-v8/REVIEW_V8.md):
it used zero-based `supports[11]`, replacing the required position 13 by 27,
while labelling the object support 12. Seven original rows change. Its
internally shared wrong constant explains why its row counts, rank and
damage controls passed. Corrected v9 binds `supports[12]` to three frozen
sources and rejects both the off-by-one binding and the `13 -> 27` mutation.

[The actual-base chart](sha256-word-distance/support12-base-lift-v8/PROOF.md)
has [independent acceptance](sha256-word-distance/support12-base-review-v8/REVIEW.md).
For arbitrary prescribed first words on support 12, five inactive anchors
`{9,12,14,19,22}` determine 46 other coordinates through distinct original
recurrences. A genuine schedule exists exactly when the two remaining
original residuals at rows 33 and 57 vanish. The blind reviewer found a
different five-anchor chart with the same residuals, exhausted all 272,052
sets below size five, and confirmed the author's first size-five success at
trial 1,498,469. Five variables and two equations do not imply a common zero.

[A fixed-residue finite proof](sha256-word-distance/support12-image-v8/PROOF.md)
and [independent reconstruction](sha256-word-distance/support12-image-review-v8/PROOF.md)
exclude the selected twin joint-image core for `D=+/-0x00010000`. For the
positive orientation, all 256 pairs of exact addition-XOR classes reduce
from 414 sigma0-compatible affine leaves to 20 leaves through sigma1 bit 29,
then to zero at bit 30 by odd-carry parity. Independent real boundary
fixtures show the system remains feasible modulo `2^30`. This excludes only
the two signed numerical residues, not the remaining exact-valuation-16
layer or the complete support.

[A separate full independent-pair probe](sha256-word-distance/support12-full-probe-v8/README.md)
kept all thirteen active pairs, all 48 difference rows and exact
`v2(d18)=16`. Its one preregistered Z3 4.15.3 check returned `unknown`
with reason `timeout` at 30 seconds. It has no model or UNSAT certificate,
omits base completion, and is stopped without retry or budget extension.

## Stage-9 accepted composition and valuation-16 finite window

[The residual/endpoint merge](sha256-word-distance/support12-base-residual-v9/PROOF.md)
and its [blind independent acceptance](sha256-word-distance/support12-base-residual-review-v9/REVIEW.md)
show that active first endpoint `u57` affects exactly coordinates
`{57,59,61,63}`.  Hence `R33` is independent of `u57`, while

```
H = sigma1(C55)+C50+sigma0(C42)+C41,
R57 = u57-H.
```

Row 57 therefore forces the unique value `u57=H`.  When the accepted factor
system is composed with the base chart, its projected `PG(z,b)` condition
must be replaced by the pointwise condition `sigma1(H+z)-sigma1(H)=b`.
This reduces the base obligation to `R33=0` plus the bound endpoint condition;
it does not prove either one soluble.

The exact affine/carry classification in
[the valuation-16 package](sha256-word-distance/support12-v16-general-v9/PROOF.md)
and its independent review covers every positive odd `q` in `1..31` at
`D=q*2^16`.  The selected twin condition is excluded for
`q={1,3,7,9,11,17,19,29,31}` and has 21 actual full-word local fixtures for
`q={5,13,15,21,23,25,27}`.  Thus the old `q=1` obstruction does not extend
uniformly across the valuation layer.

For all seven surviving q values, separately checked deletion-free DRUP
certificates exclude the required selected **three-pair** joint-image core.
The fixed `q=15` package and review are separate; a six-q batch covers
`{5,13,21,23,25,27}`.  Pair reversal gives the negative orientations.
Together, the selected three-pair core is now excluded for

```
D=+/-q*2^16, every odd q in 1..31.
```

This remains a finite window, not all exact-valuation-16 residues.  The
[corrected q=5 record](sha256-word-distance/support12-d0005-v9/PROOF.md)
preserves a caught sign error: reversing the proposed third word negates
`d,F,G` together, so the old three-pair candidate was invalid.  Independent
certificates also exclude its fixed correct third image and reciprocal edge.

[The low-26 factor witness](sha256-word-distance/support12-factor-signature-v9/PROOF.md)
and its independent review establish a failure boundary.  The complete
thirteen-factor graph is satisfiable modulo `2^26` at `b=00010000`, using one
real 32-bit word pair for simultaneous `F/G` at each full factor.  Factors
34/43 also have a full-word two-factor witness with `v2(b)=16`.  Therefore
valuation signatures, exact low-26 carries, and that anti-symmetric fragment
cannot by themselves exclude the remaining layer.  No full 32-bit factor
solution or base-message lift is claimed.

## Frozen failure and next mathematical step

[Full-pair probe](sha256-word-distance/full-pair-probe-v4/MECHANISM.md)
retained all 48 independent-active-pair difference equations of support 5
at `v2(d17)=11`, with 13,369 Boolean variables and 46,690 clauses.
Glucose3 returned `unknown` at its 50,000-conflict budget (50,147 conflicts).
That bounded mechanism stops; the result is neither SAT nor UNSAT and
contains no base completion. No timeout is extended.

The [independently accepted width lemma](sha256-word-distance/width-review-v5/REVIEW.md)
gives an additional useful support-12 stratum. If `2^18`
divides D, sigma1 output bits 22..30 agree within each pair. Its bit 31
changes precisely when input bit 18 changes, giving the same modular
half-word contribution for differences D and -D. It cancels in both
sigma1 derivative gaps. The same integer-width argument reduces this
stratum to `D=+/-q*2^18`, `1<=q<=15`. The eight new odd quotients now have
a complete finite exclusion in [the frozen extension](sha256-word-distance/support12-extension-v5/PROOF.md)
and separate independent acceptance. Together with the stage-4 even cases,
this proves the ceiling 17. Local SMT UNSAT observations are not premises.
The original support-12 equations
also retain `d26=-F18` and `F26=-D`, a further sigma0-chain constraint.

[An independently checked linear-module obstruction](sha256-word-distance/shift-symbolic-review-v5/REVIEW.md)
shows why the tempting inverse maps `9 -> 0` and `12 -> 6` are not proved
by additive recurrence elimination alone. All 48 rows and exact integer
unit transformations were checked. The free-interface countermodels are
not actual word pairs and do not refute either true nonlinear reverse map.

The valuation-17 boundary is now completely excluded in
[the frozen stage-6 proof](sha256-word-distance/support12-boundary-v6/PROOF.md)
and independently accepted. Its new width argument modulo `2^31` screens
32 positive representatives plus their global pair reversals. The finite
proof retains every original constraint modulo `2^32`, including the
top output bit and both lifts. All 32 lossless XZ certificates recover
20,167,680 raw JSON bytes. Independent checking also constructs 32 actual
feasible twin-mask witnesses, so the third pair's exclusion is essential.
Fixed-difference SMT observations remain discovery only.

[One unrestricted actual six-word query](sha256-word-distance/support12-unrestricted-core-v6/STATUS.md)
retained all valuations and all coupled sigma bits. It returned `unknown`
with reason `timeout` after its one fixed 15-second check. No model or
UNSAT certificate was obtained; the stopped probe is not rerun by the
proof replay and does not decide the entire core.

## New accepted structure beyond valuation enumeration

[The joint-image result](sha256-word-distance/support12-structure-v7/PROOF.md)
and [its independent acceptance](sha256-word-distance/support12-structure-review-v7/REVIEW.md)
give an exact three-pair criterion. At fixed D, define the actual joint
image I_D of `(f(x+D)-f(x),g(x+D)-g(x))`. The selected core is feasible
exactly when some A,T have all three points `(A,T-D)`, `(A,T+D)`,
`(-A,-T)` in I_D. Here T=G(X)+D; there is no division by two. Actual
preimages remain required, so this is not an independent-derivative
relaxation or a measured computational speedup.

The fourth original pair requires the reciprocal sigma0 edge `D in R_A`.
For support 12 use A=F18=-d26=-d42; the checked shifted bridges give
the corresponding parameter for supports 6,7,13. Put k=v2(D), l=v2(A).
All 1,024 one-pair binary-signature systems were classified by actual
mask witnesses or original-row XOR contradictions, then independently
reconstructed. The 309 transposed compatible signatures imply

```
k<=23, l<=23, k+l<=30;
l>=18 => k=l-18<=5;
k=16 => l in {0,1,...,10,12}.
```

These are necessary numerical constraints; the 309 signatures are not
309 realized reciprocal numerical pairs. With the fourth pair present,
neither endpoint of the third pair can coincide with an endpoint of
either first pair. The selected core needs at least five actual word
values. A finite-sum proof also shows that reciprocal sigma0 coupling
alone always has a nonzero solution for any permutation of an even
cyclic group. The joint sigma1 requirements and all other original
equations are therefore substantive remaining obligations.

[The uniform width lemma](sha256-word-distance/dyadic-width-v7/PROOF.md)
is [independently accepted](sha256-word-distance/dyadic-width-review-v7/REVIEW.md).
For every exact k=10,...,18, it gives
`D=+/-q*2^k+h*2^(k+14)`, with odd q from 1 to `2^(22-k)-1`
and all lifts h from 0 to `2^(18-k)-1`. Pair reversal permutes lifts
by `h -> -h`, rather than keeping h fixed. The shared-term bound
`|2q_R-q_Y-q_X|<=4*(2^22-1)` makes k=10 valid. At k=9 the same
representative formula covers the entire layer, so provides no screen.
No lower-layer finite exclusion is inferred from this lemma.

[The actual nonlinear inverse-boundary study](sha256-word-distance/actual-boundary-v6/PROOF.md)
now has [exact independent acceptance](sha256-word-distance/actual-boundary-review-v7/REVIEW.md).
Its generic sigma0 two-pair theorem excludes signed powers of two in
exponents 22..31. On support 12 it applies to d26=d42=-A; at exponents
22 and 23 this adds information beyond the accepted valuation-signature
ceiling 23. Fifty-five inverse masks give the complete local proof.
Four actual word pairs also satisfy the selected conservation condition
while leaving the inverse prefix `ffd519ca` nonzero. The other nine
active pairs and base equations are absent, so this does not refute
the actual reverse implication `12 -> 6`. All 48 original rows are
accounted for, including the 25 nonzero ones. The independent review
records a corrected implementation error in its first unsigned-sum
comparison; the author proof had no gap, and both source hashes and
the correction mechanism are preserved.

The next useful step is to solve or exclude the accepted ten-scalar,
thirteen-factor support-12 system on the remaining difference strata, then
compose any positive first-endpoint object with the exact two-residual base
chart. A positive independent-pair object is still not a message pair.
Further queries must incorporate new constraints and specify a new bounded
mechanism; stopped unknown queries and old failed construction families are
not continued by increasing their budgets.

Other agents' paths and `main` are outside this workstream. Branch uploads
may be unsigned; final signatures and main integration belong to ROOT.
No paper, DOI, Release, human peer review, historical priority or Lean
certification is created by this continuation.

Reproduction of the latest frozen continuation uses only Python's standard library:

```sh
python -B workstreams/CRYPTO3-20261012/continuation-v8/replay.py
```

The stage-4 gate is `continuation-v4/replay.py`; add its `--full-stage2`
only when the original 21 checks need another replay. The stage-5 gate
checks stage-4 integrity and all stage-5 proof, review and damage-control
gates in a temporary copy. The stage-6 gate checks prior integrity, all
32 new author and independent finite cases, and the stopped-probe record
without another solver query. The living checkpoint is not a frozen
proof artifact. The stage-7 gate checks prior integrity and the new
structure, width and actual-boundary proof/review commands; it does
not repeat earlier large enumerations. The stage-8 gate additionally checks
the rejected-v8/corrected-v9 factor review, accepted base chart, accepted
fixed-residue obstruction and stopped-query receipt without rerunning Z3.
Each continuation directory's snapshot and manifest binds its exact
accepted phase.
