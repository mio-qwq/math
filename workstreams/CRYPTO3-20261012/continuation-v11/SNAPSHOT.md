# CRYPTO3 stage-11 checkpoint

Recovery base: `2e7c43a3f4524588a23c2b773db6c5376e1c3751` on
`partner/dist-CRYPTO3-20261012`.  The universal lower bound remains **13**.
This stage neither constructs a distance-13 message pair nor proves a lower
bound of 14.

## Independently accepted message-equivalent normal form

The Stage-10 18-word candidate is now a complete written theorem with a blind
independent AI acceptance.  There exists a pair of genuine SHA-256 16-to-64
message schedules with exact support

```text
{10,11,13,15,18,20,26,28,29,34,42,43,57}
```

if and only if eighteen free 32-bit words satisfy thirteen retained derivative
equalities, the base equality `R33=0`, and seven nonzero conditions.  Nine of
the original twenty-two local derivative equalities are used as triangular
definitions, with unit coefficients and no division.

The seven nonzero classes are

```text
A, B, C, K, P+A, Q+T, Z.
```

They are necessary and sufficient for the thirteen listed positions to be the
exact support rather than only an upper bound on the support.

The position-57 merge is pointwise rather than existential.  The accepted base
sink lemma forces the first endpoint to `H`, while

```text
Z = Delta0(X42,P+A),  Delta1(H,Z)=B.
```

Thus a reverse construction yields two actual schedules whose first sixteen
words are message blocks; it does not merely assemble unrelated local word
pairs.

## Independent review mechanism

Before opening the author package, the reviewer froze a different normal form.
The blind form retains `Z` as its extra factor word, whereas the author form
retains `A`; the two forms eliminate different nine-equation subsets and leave
different thirteen-equation subsets.  The reviewer then compared both forms
against the common accepted 22-equation factor system and the accepted base
chart.  Deterministic symbolic checks, 10,000 auxiliary numeric substitutions,
the complete additive difference table, and four negative controls pass.
Random substitution is auxiliary and is not a proof premise.

## Exact boundary and next solver target

The accepted result is an exact reformulation, not a feasibility decision.
No SAT model, UNSAT certificate, message pair, distance-14 bound, Lean
formalisation, or human peer review is supplied.

The next preferred search object is a direct message-level model with the
sixteen first-message words and one root difference as primary words.  Expanding
the first schedule by the original recurrence makes all base equations hold by
construction; any SAT assignment must then be re-expanded for both messages and
checked for the exact thirteen-word support.  A factor-only solve remains useful
as a proposal generator, but cannot by itself certify a message pair.  Any
negative result must carry a separately checked DRAT/LRAT/RUP-style certificate;
timeouts and solver `unknown` results remain non-proofs.
