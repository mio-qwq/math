# Independent blind review of the support-12 18-word normal form

**ACCEPT, exact frozen author v11 package.**  The author manifest has SHA-256
`dc2c0a4d2f6bf9bf14c720c476a865d16d75aaf439c2d3a0de52fb63a5a7d8fe`.
The accepted claim is a bidirectional equivalence between exact support-12
SHA-256 16-to-64 schedule pairs and an 18-word system with fourteen word
equalities and seven nonzero conditions.  This is not an existence or
nonexistence result.

## Blind independence

Before reading the author v11 directory, this reviewer derived and
hash-froze a separate coordinate form from the accepted full-factor v9,
base v8, and residual-merge v9 results.  Both derivations start from the same
22 local derivative equalities at the thirteen active positions, but they
choose genuinely different triangular eliminations:

| item | blind freeze | author v11 |
|---|---|---|
| extra free factor word | `z` | `A=a` |
| first forced quantity | `b=D1(H,z)` | `B=-D0(X10,A)` |
| retained factor equations | `10F,18F,18G,20F,26F,28F,28G,29G,34F,34G,42F,42G,43F` | `15G,18F,18G,20F,20G,26F,28F,28G,34F,34G,42G,43F,57G` |

The blind form eliminates nine shared parameters; the author form uses nine
local equations to define `B,C,K,P,Q,L,T,W,Z`.  Each sequence is triangular
with a unit coefficient and uses no division.  Both independently leave
thirteen local factor equations.  Adding the sole base residual `R33=0`
gives fourteen word equalities in eighteen free 32-bit words.

The pre-author derivation, checker, and run remain byte-identical to their
freeze hashes.  Its standalone checker reconstructs the 47-row chart,
checks all difference rows, performs 10,000 definition-identity trials, and
includes four sign/incidence/endpoint/residual controls.

## Author formula audit

The author package contains exactly the three manifest members plus its
manifest.  Every file hash matches, and `check_symbolic.py` reproduces
`RUN.json` byte for byte.  Its canonical term audit verifies that precisely

```
10F,11F,13F,15F,26G,29F,29G,42F,43G
```

vanish by definition, while the other thirteen terms are exactly the
displayed normal-form equations.  The post-freeze reviewer checker rebuilt
the author's definitions independently and repeated the 22-to-13 comparison
on 10,000 deterministic 32-bit assignments.  It also reconstructed the
full additive difference table on every trial.

The seven distinct difference classes are exactly

```
A, B, C, K, P+A, Q+T, Z.
```

Every active difference is one of these or its negative, and each class
occurs.  Hence their seven nonzero conditions are necessary and sufficient
for the support to be exactly the thirteen frozen indices, not merely a
subset.

## Base endpoint and bidirectional quantifiers

The accepted sink lemma makes `H` and `R33` independent of the temporary
`u57`; replacing that chart input by `H` means rerunning the chart with the
new input, so rows 59, 61 and 63 are reconstructed as well.  Then
`R57=u57-H` vanishes and `R33=0` is the only remaining base equation.

At position 57 the author correctly uses the same forced first endpoint:

```
Z=D0(X42,P+A)=d57,
D1(H,Z)=B.
```

This is stronger than, and cannot be replaced by, a detached existential
`PG(Z,B)` witness.

For the forward implication, an actual pair supplies the twelve first
endpoints, five anchors and `A=a`; the nine selected factor equations force
all author definitions, while the remaining thirteen equations, `R33=0`
and the seven inequalities follow.  For the reverse implication, the base
chart yields a genuine first schedule; the nine definitions plus thirteen
retained equations realise every required `(d,F,G)` at the same endpoints;
the accepted full-factor theorem zeros all difference rows, so the second
sequence is also a genuine expansion of its first sixteen words.  The seven
inequalities give exact support.

## Acceptance boundary

Accepted: the exact 18-word reformulation, both logical directions, the
22-to-13 factor reduction, fourteen total word equalities, seven exact-support
inequalities, and the forced word-57 endpoint cascade.

Not accepted or inferred: satisfiability or unsatisfiability of the normal
form, an explicit pair of messages, distance-13 attainability, a distance-14
lower bound, Lean certification, or human peer review.  Unknown or future
solver outcomes remain non-proofs unless separately certified.
