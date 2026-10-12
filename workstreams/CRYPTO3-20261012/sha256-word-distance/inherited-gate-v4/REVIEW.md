# Independent review of the inherited global distance gate

**Decision: accepted within the exact scope below.** The recovered
CRYPTO2 v1/v2 argument proves a universal actual SHA-256 schedule
word-distance lower bound of 13, gives a complete list of the fifteen
weight-13 supports in its necessary binary relaxation, and excludes
listed supports 3 and 14 for arbitrary actual base blocks. It proves
neither actual attainment of distance 13 nor a lower bound of 14.

This review combines independent mathematical examination and a new
standard-library checker that imports or executes no author checker,
optimizer, discovery module or solver. Source proofs and checkers were
read before implementation; this is independent reimplementation after
disclosure, not a claim of blind rediscovery. It is independent
AI-assisted review, not external human peer review or Lean verification.

## 1. Exact provenance and the new acceptance increment

The eight source files are copied byte for byte from commit
`80b71cb3b6a67c8f8aae80d9cd8b6ed87d74bd51`, at
`workstreams/CRYPTO2-20261011-7f3c/projects/sha256-schedule-distance/`:
v1 `PROOF.md`, `certificate.json`, `check.py`, and v2 `PROOF.md`,
`supports.json`, `exclusions.json`, `check.py`, `TAIL.json`.
`PROVENANCE.json` identifies every original Git blob and SHA256.
The new checker also reconstructs the Git blob hashes directly from
the copied bytes, so the check is available without Git or network.
No branch-containment assertion is made for the pinned commit.

The earlier CRYPTO3 `review/review.md` explicitly did not replay all
5,308,416 potential inequalities or the full 735-node classification.
This new run closes precisely that finite-evidence acceptance gap.
It is not discovery optimization or repetition for a restart alone.
None of the earlier frozen files is edited or retrospectively relabeled.

## 2. Actual modular addition implies the binary constraint

Let R be the residues modulo 2^32. Define f and g by the actual SHA-256
small sigmas, using rotations 7/18 and shift 3 for f, rotations 17/19
and shift 10 for g. For two actual schedules write

```
d_i = W'_i - W_i,
F_i = f(W'_i) - f(W_i),
G_i = g(W'_i) - g(W_i),
```

where the differences are in R. Subtracting the two original schedule
equations, without changing modular addition to XOR, gives

```
d_t = G_(t-2) + d_(t-7) + F_(t-15) + d_(t-16),  16 <= t < 64.
```

The two sigma functions are linear over the bit vector space F2^32.
The new checker builds their matrices from the rotation/shift definitions,
performs F2 row elimination, and obtains rank 32 for each. It reconstructs
all 64 inverse columns and compares them with the certificate. All 64
right-inverse and all 64 left-inverse basis compositions are verified.
Linearity extends these compositions to every bit vector; thus f and g
are bijections on words. This is bit-vector linearity, not linearity
over the additive residue group.

Consequently d_i, F_i and G_i vanish simultaneously. If exactly one
of the five coordinates t,t-2,t-7,t-15,t-16 differs, the displayed
modular equation has exactly one nonzero term. Cancellation in R gives
a contradiction. Distinct sixteen-word inputs give at least one active
coordinate before 16. Every actual pair therefore induces a nonzero
initial activity state satisfying the no-singleton constraint in all
48 rows. The converse is not asserted.

## 3. The full potential certificate and telescoping proof

Immediately before position t, encode the preceding sixteen activities
as q, with bit j for position t-16+j. The four sources use bits
14,9,1,0. Appending b gives q'=(q>>1)|(b<<15), cost b, and a permitted
edge exactly when the four source activities plus b do not total one.

The recovered potential has 49 rows of 65,536 nonnegative integer bytes.
Its 3,211,264 decompressed bytes have SHA256

```
1f04aa2b5ac13c5144e677cf75eb6d6af323d518abf96ec65a44a96fa07df23c
```

The new checker verifies V_64(q)=0 for every q, the initial inequality
popcount(q)+V_16(q)>=13 for every nonzero q, and

```
V_t(q) <= b + V_(t+1)(q')
```

for every permitted transition at every t=16,...,63. There are
110,592 permitted edges per row: fixing the four source bits and summing
their allowed output choices gives (1+4+2*(6+4+1))*4096. All 48 rows
are checked, for exactly 5,308,416 inequalities. No assertion that a
potential value is an optimal suffix cost is needed or trusted.

For any actual path, let s0=popcount(q16)+V16(q16)-13 and let
st=b_t+V_(t+1)(q_(t+1))-V_t(q_t). All these integers are nonnegative.
The telescoping identity, using V64=0, is

```
total activity weight - 13 = s0 + sum_(t=16)^63 st.
```

It proves the actual lower bound 13. The supplied weight-13 support
is checked against every original lag set, so the relaxation itself
has exact minimum 13. That object supplies no actual expanded pair.

## 4. Completeness of the equality classification

For total weight 13, the slack sum is zero, so every individual slack
is zero. Hence every minimum path starts in an initial equality state
and traverses only permitted equality edges. Conversely every such
complete path has total weight 13 by the same identity.

The new breadth-first checker retains activity tuples for complete
prefixes and reconstructs both states from their last sixteen bits;
it does not call the author's DFS/BFS functions. It checks both next
bits at every prefix and compares the entire terminal set with the
supplied list, checking distinctness as well as membership. The run
finds 15 initial equality states, 15 prefixes at each of 49 layers,
735 nodes including terminals, 1,440 candidate choices, 720 accepted
equality edges and exactly 15 terminal supports. All terminal weights
are 13. The supplied zero-based indexing is preserved.

Thus the complete fifteen-support classification is newly replayed,
not inferred merely because all fifteen listed supports are allowed.

## 5. Universal forced-halfword chain

Put H=2^31. A modular difference H toggles exactly the top bit, so it
is also XOR difference H. Therefore if x'-x=H, the output XOR mask
under f is f(H)=0x11002000, supported at bits 13,24,28. An additive
difference between words with that XOR mask is a signed sum of those
three powers. Its residue modulo 2^24, even after negation, is either
+2^13 or -2^13. The checker verifies all eight sign possibilities.

Suppose a'-a is one of those two residues modulo 2^24. The low thirteen
bits agree. The quotients floor(a/2^13) and floor(a'/2^13), reduced
modulo 128, differ by +1 or -1. In an increment or decrement of seven
bits, changing bit 6 entails changing bit 5, including wraparound.
The checker verifies all 256 quotient/direction cases. For
alpha=a XOR a', this says alpha19=1 implies alpha18=1.

Since alpha0,...,alpha12 are zero, the exact f output-bit equations
give f(alpha)0=alpha18 and f(alpha)1=alpha19. Its low two bits cannot
equal binary 10. For any words z,z', the condition z'-z=2 modulo 4
is equivalent to (z XOR z')=2 modulo 4: their low two-bit residues
differ precisely by toggling bit 1 with bit 0 fixed. All sixteen
residue pairs are also checked. It follows that f(a')-f(a) is not
2 modulo 4.

On the other hand, g(b')-g(b)=H implies g(b') XOR g(b)=H. Bit
linearity and the fully verified inverse give

```
b' XOR b = g^(-1)(H) = 0xc6eeaad6 = 2 modulo 4.
```

Then b'-b=2 modulo 4. This contradicts b'-b=f(a')-f(a).
Hence no six arbitrary words satisfy simultaneously

```
x'-x=H,
a'-a=epsilon*(f(x')-f(x)),  epsilon in {+1,-1},
b'-b=f(a')-f(a),
g(b')-g(b)=H.
```

This is an unconditional written carry proof; no solver UNSAT answer,
zero base assumption, or independent-carry premise is involved.

## 6. Applying the chain to supports 3 and 14

For support 3 take (u,x,a,r,b)=(27,34,42,43,57). For support 14 take
(25,32,40,41,55). Each is a tuple of active positions. The checker
rebuilds each row directly from the original difference recurrence
and discards only coordinates outside that support. In either case
the six rows yield

| Recurrence index | Exact reduced equation |
| --- | --- |
| x | d_x=d_u |
| r | d_r=d_u |
| r+7 | 0=d_r+d_x |
| x+15 | 0=d_a+F_x |
| b | d_b=F_a |
| b+2 | 0=G_b+d_r |

The first three equations give 2*d_u=0. Since u is active, d_u is
nonzero; the only nonzero residue annihilated by 2 is H. Thus
d_x=d_r=H, d_a=-F_x, d_b=F_a and G_b=-H=H, the impossible chain
with epsilon=-1. The twelve original-row substitutions are all
checked. The extra active position 62 in support 14 enters none of
its six equations. The remaining list is exactly
0,1,2,4,5,6,7,8,9,10,11,12,13.

This excludes two entire patterns for arbitrary actual bases. It does
not assert that any remaining pattern is attainable.

## 7. Exact failure boundaries retained

The v1 zero-base obstruction for support 0 is also mathematically
valid but narrower. Its rows 16,23,24,31 force f(v)=H for the active
v=W9, hence v=0x94857ee6. Rows 18,17,26 would require
f(-g(v))=g(H). The new evaluator verifies the unequal constants
0xabacb99f and 0x00205000. This excludes that zero-base attempt only.
It does not exclude support 0 for arbitrary bases.

The recovered `TAIL.json` is independently evaluated from all eight
actual word values. Its four active pairs satisfy all five equations

```
d_r=-d_x, F_r=F_x, d_a=-F_x, d_b=F_a, G_b=d_x,
```

but d_x is not H. It therefore refutes an overstrong version of the
tail exclusion with the forced-H premise removed, while remaining
consistent with the accepted chain. It is an independent-pair tail
object, not an input block, actual base expansion or full support
witness. No recorded solver timing or `sat` label is used as evidence
that the arithmetic equations hold.

## 8. New execution and controls

`RUN.json` records exit 0 on Python 3.12.14, a roughly 1.11-second
observed process duration, exact command, checker hash and output
hashes. `VERIFICATION.json` gives all checked counts and reconstructed
identities. The default command in `README.md` is read-only.

All fifteen controls are rejected: an altered inverse column, claimed
bound 14, altered raw hash, nonzero terminal value, insufficient
initial potential, violated transition inequality, omitted starting
state, omitted terminal support, duplicated terminal support, wrong
halfword inverse, altered case coordinate, omitted surviving index,
tampered tail word, Boolean word value and duplicate JSON key.

The three numeric potential controls intentionally exercise validators
directly on malformed raw bytes. Thus they verify the inequalities'
rejection behavior rather than merely failing a frozen hash check.
The transition corruption fails on its first edge; controls do not
repeat the complete multi-million-edge certificate traversal.

Acceptance is confined to the pinned sources and new checker/output
hashes in `RECEIPT.json` and `SHA256.json`. The review makes no claim
of historical originality, cryptanalytic advantage, actual distance-13
attainment, distance at least 14, full compression-function security,
Lean compilation or human peer review.
