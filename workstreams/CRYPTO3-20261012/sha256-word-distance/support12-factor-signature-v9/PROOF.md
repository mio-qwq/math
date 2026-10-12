# Support-12 joint-signature and low-26 factor witnesses

**Complete same-author finite witness proofs, pending independent review.**  The
results below prove that two natural necessary-condition relaxations are too
weak.  They do not solve the full 32-bit factor system and do not construct two
SHA-256 messages.

All full words are in `Z/(2^32)`.  Write

```text
f(x)=ROTR7(x) xor ROTR18(x) xor SHR3(x),
g(x)=ROTR17(x) xor ROTR19(x) xor SHR10(x).
```

For an ordered pair `(x,y)`, put

```text
d=y-x,  F=f(y)-f(x),  G=g(y)-g(x).
```

The accepted v9 factor theorem has ten shared scalars
`a,b,c,k,p,q,l,s,w,z` and thirteen factors numbered
`10,11,13,15,18,20,26,28,29,34,42,43,57`.  Nine factors retain the full
same-pair triple `(d,F,G)`; three retain `(d,F)` and one retains `(d,G)`.

## 1. The complete factor graph is satisfiable modulo `2^26`

Reduce the ten scalar expressions and every constrained component of each
actual pair modulo `2^26`, but continue to evaluate `f` and `g` on real 32-bit
words.  This is an exact quotient necessary condition for a full factor
solution.  It is stronger than a valuation CSP: it retains the numerical low
26 bits, all carries through bit 25, and the same actual XOR mask for both
sigma derivatives at every full `J` factor.

`CERTIFICATE.json` supplies ten scalar residues, with

```text
b = 00010000 (mod 2^26),
```

and thirteen independent real 32-bit word pairs.  Direct evaluation gives the
following valuation signatures.  A blank component is projected away by the
corresponding `PF` or `PG` factor.

| factor | kind | `v2(d)` | `v2(F)` | `v2(G)` |
|---:|:---:|---:|---:|---:|
| 10 | PF | 1 | 16 | |
| 11 | PF | 16 | 0 | |
| 13 | PF | 6 | 2 | |
| 15 | J | 2 | 1 | 1 |
| 18 | J | 16 | 0 | 6 |
| 20 | J | 16 | 0 | 2 |
| 26 | J | 0 | 16 | 0 |
| 28 | J | 0 | 16 | 1 |
| 29 | J | 6 | 3 | 2 |
| 34 | J | 16 | 0 | 6 |
| 42 | J | 0 | 0 | 0 |
| 43 | J | 16 | 0 | 6 |
| 57 | PG | 0 | | 16 |

Every constrained residue is nonzero below bit 26.  Hence its displayed
valuation is also the valuation of the full 32-bit derivative.  For every
full factor the checker additionally evaluates the one common mask
`alpha=x xor y` and verifies

```text
v2(alpha)=v2(d),
v2(f(alpha))=v2(F),
v2(g(alpha))=v2(G).
```

Thus this is not the invalid step of choosing independent sigma0 and sigma1
masks.  The same real pair supplies both derivatives.  The exact scalar
residues also witness every addition-valuation rule among `p+a`, `q+s`,
`b+c`, `b-c`, and `w+q+s`.

It follows immediately that any attempted exclusion using only the accepted
one-pair valuation signatures, even strengthened to the joint three-way mask
signature at each `J` factor and exact scalar addition valuations, cannot
exclude `v2(b)=16`.  More strongly, the full factor graph has no contradiction
in its exact low-26 quotient at the residue `b=2^16`.

This does **not** contradict the accepted fixed-residue twin obstruction for
the full value `D=0x00010000`.  The low-26 pairs may differ in their upper six
additive and derivative bits.  The accepted obstruction uses higher output
bits; those bits are precisely outside this quotient.

## 2. An exact valuation-16 witness for the `34/43` fragment

The two full factors 34 and 43 share

```text
34: (d,F,G)=( b, -p-a,  b-c),
43: (d,F,G)=(-b, -p-a,   -c).
```

The certificate gives the following exact 32-bit values:

```text
a=00000001, b=bfbf0000, c=5fef57d8, p=37788def,
-p-a=c8877210,  v2(b)=16.
```

Its actual pairs evaluate to

| factor | `d` | `F` | `G` |
|---:|---:|---:|---:|
| 34 | `bfbf0000` | `c8877210` | `5fcfa828` |
| 43 | `40410000` | `c8877210` | `a010a828` |

Here `40410000=-b`, `5fcfa828=b-c`, and `a010a828=-c` modulo
`2^32`.  Therefore both factors are satisfied exactly by real word pairs.
In particular, the appealing `34/43` anti-symmetry alone cannot exclude the
whole valuation-16 layer.  A proof eliminating that layer must use another
factor, a stronger cross-factor numerical condition, or base completion.

## 3. Verification and scope

Run from the repository root:

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-factor-signature-v9/check.py --negative
```

The checker uses only the Python standard library.  It reconstructs all
thirteen v9 factor expressions, evaluates every real pair, verifies the
low-26 congruences and common-mask valuations, checks the exact two-factor
witness, and rejects seven damaged controls.  Z3 was used only to discover
the low-26 witness; its model is not trusted by the verifier.

These are complete finite witness proofs of satisfiability for the stated
relaxations, with same-author checking.  Independent-agent acceptance and
Lean formalization are absent.  There is no full 32-bit thirteen-factor
solution, base-message lift, distance-13 message pair, distance-at-least-14
proof, hash collision, or publication claim.
