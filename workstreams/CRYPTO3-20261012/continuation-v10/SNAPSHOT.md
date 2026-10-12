# CRYPTO3 stage-10 checkpoint

Recovery base: `f27fc2c292094375c5c935e7cd3b4a269eaf4906` on
`partner/dist-CRYPTO3-20261012`.  The global lower bound remains **13**.
This stage contains neither a real distance-13 message pair nor a proof of a
lower bound of 14.

## Independently accepted finite-window extension

For `D=q*2^16`, the exact selected three-pair joint-image core is now
independently excluded for every positive odd `q=33..63`.  Each of the sixteen
CNFs has 1,259 variables and 9,683 clauses.  An independent implementation
reconstructed every CNF byte-for-byte and checked all 87,220 deletion-free
DRUP additions by reverse unit propagation.  Truncated proofs, a removed
definition clause, and a mutated proof addition were rejected for every q.
The identity

```text
F_{-D}(w+D)=-F_D(w),  G_{-D}(w+D)=-G_D(w)
```

supplies the negative orientations.  Combining this stage with the accepted
Stage 9 window gives the finite theorem

```text
selected three-pair core is impossible for
D=+/-q*2^16, every odd q in 1..63.
```

This covers only 32 positive quotients out of the 16,384 positive odd
quotients in the exact valuation-16 layer.

## Exact classification and failure mechanism

An independently reconstructed affine/carry classifier exhausts the same new
q window.  The twin
condition is already impossible for

```text
q={33,35,45,47,49,51,53,55,57,59,61,63},
```

but has twelve actual full-word local fixtures for
`q={37,39,41,43}`.  The reviewer rebuilt the complete class cover before
reading author bytes, matched all leaf statistics and signatures, directly
checked 24 independently chosen/author local fixtures, and recorded the first
over-strict representative comparison as a failed run.  Thus a uniform
extension of the old top-bit obstruction again fails.  The direct three-pair
certificates above exclude all sixteen q without relying on this
classification.

## Candidate full base/factor normal form

A separate candidate reduction eliminates nine scalar words definitionally
from the accepted support-12 factor/base merge.  It proposes a normal form
with 18 free 32-bit words, 13 retained derivative equations plus `R33=0`, and
seven nonzero conditions.  Its key cascade is

```text
Z = Delta0(X42,P+A),  Delta1(H,Z)=B,
```

where the accepted sink lemma forces word 57 to the base value `H`.  A frozen
10,000-trial substitution audit and 64 endpoint controls pass.  This remains
an explicitly labelled candidate symbolic check: it is not yet a complete
written equivalence proof or independent acceptance.

## Exact scope and next step

The accepted q-window result concerns a local necessary subsystem.  It does
not exclude support 12, construct messages, decide distance 13, prove distance
at least 14, or provide Lean formalisation.  The next high-value step is to
promote and independently review the 18-word base/factor normal form, then
solve or certify a meaningful full-32-bit stratum of that message-equivalent
model rather than extending valuation-only relaxations indefinitely.
