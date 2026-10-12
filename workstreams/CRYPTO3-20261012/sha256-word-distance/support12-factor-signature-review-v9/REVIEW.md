# Independent review: support-12 factor signatures v9

**ACCEPT, with the scope below.**  The author certificate is a valid exact
satisfying assignment for the complete corrected thirteen-factor graph after
projection modulo `2^26`, at fixed residue `b=2^16`.  Every factor is supplied
by an actual pair of 32-bit words.  The separate factors 34/43 witness is also
valid in the full 32-bit ring.

## Blind reconstruction and search

The accepted `support12-full-factor-v9` normal form independently reconstructs
the same graph:

```
10 PF(a,-b)                 11 PF(b,p)
13 PF(c,q)                  15 J(k,l,-a)
18 J(b,-p-a,-b-c)           20 J(-b,-q-s,-k)
26 J(p+a,-b,s)              28 J(q+s,-b,-l)
29 J(c,w,-k)                34 J(b,-p-a,b-c)
42 J(p+a,z,-w-q-s)          43 J(-b,-p-a,-c)
57 PG(z,b)
```

The independent bit-blasted instance uses 32-bit local words but constrains
only bits 0--25 of each retained `d/F/G` coordinate.  It has 13,997 variables,
57,032 clauses, and digest
`f94f9f26cba2d20ef88e7a52ff735ba3a9a5a8c9507484c398dbf862fb7545d3`.
Generic HiGHS and WalkSAT searches were stopped at the resource boundary with
status `UNKNOWN`; this is not evidence of unsatisfiability.  The positive
decision below comes from direct checking of the finite author witness and
does not depend on blind model discovery.  The frozen DIMACS is stored
losslessly as `independent.cnf.xz`.

An over-broad repository text search accidentally displayed author pair lines
before the freeze was written, so I do not claim pristine blind-discovery
provenance.  Those lines were not used to build the independently reconstructed
table or CNF, and the searches found no model.  This procedural caveat does not
affect the reproducible direct audit on which acceptance rests.

## Direct low-26 audit

The certificate's scalars are all valid 26-bit residues and have
`b=00010000`.  Independent recomputation gives:

| factor | kind | `d mod 2^26` | `F mod 2^26` | `G mod 2^26` |
|---:|:---:|---:|---:|---:|
| 10 | PF | `035dc0f6` | `03ff0000` | — |
| 11 | PF | `00010000` | `02621701` | — |
| 13 | PF | `03cd88c0` | `018c8fbc` | — |
| 15 | J | `03e44744` | `0123544e` | `00a23f0a` |
| 18 | J | `00010000` | `02402809` | `00317740` |
| 20 | J | `03ff0000` | `0162cdf9` | `001bb8bc` |
| 26 | J | `01bfd7f7` | `03ff0000` | `0110a24b` |
| 28 | J | `029d3207` | `03ff0000` | `02dcabb2` |
| 29 | J | `03cd88c0` | `02a8b5f8` | `001bb8bc` |
| 34 | J | `00010000` | `02402809` | `00337740` |
| 42 | J | `01bfd7f7` | `03b732eb` | `02ba1801` |
| 43 | J | `03ff0000` | `02402809` | `00327740` |
| 57 | PG | `03b732eb` | — | `00010000` |

For every pair I evaluated the FIPS definitions

```
sigma0(x)=ROTR7(x) xor ROTR18(x) xor SHR3(x)
sigma1(x)=ROTR17(x) xor ROTR19(x) xor SHR10(x)
```

both by word operations and by a separate output-bit loop.  The two
implementations agree.  The modular differences match the scalar expressions
in all retained coordinates.  Each of the nine `J` factors uses one common
`(x,y)` pair for both `F` and `G`; no independently chosen sigma masks are
spliced together.  All constrained low residues are nonzero, and the claimed
joint valuations and common-XOR-mask identities check directly.

The full outputs also demonstrate the projection boundary.  For example,
the common low residue `F=02402809` at factors 18, 34, and 43 comes from full
values `da402809`, `da402809`, and `aa402809`.  These differing top six bits
are legitimate because bits 26--31 are absent from every projected graph
equality.  The witness therefore proves low-26 residue feasibility, not a
full-32 thirteen-factor solution.

## Exact full-32 fragment

Direct evaluation of the separate factors 34 and 43 gives

| factor | `d` | `F` | `G` |
|---:|---:|---:|---:|
| 34 | `bfbf0000` | `c8877210` | `5fcfa828` |
| 43 | `40410000` | `c8877210` | `a010a828` |

Thus `d_34=b`, `d_43=-b`, the `F` values agree, `G_34=b-c`, and
`G_43=-c` modulo `2^32`, with `v2(b)=16`.  This accepts only the isolated
34/43 anti-symmetry claim, not the full graph at that value of `b`.

## Integrity and failure boundary

The independent audit and the author checker both reject all seven damaged
controls: wrong fixed `b`, damaged pair 18, damaged shared `p`, wrong factor
kind, wrong sigma0 rotation, damaged exact pair 43, and damaged common `F`.
All seven files recorded by the manifest match both byte count and SHA-256;
all three upstream hashes also match.

Consequently any sound local exclusion using no information above bit 25 of
these projected `J/PF/PG` constraints cannot eliminate this `b=2^16` case:
the exact quotient already has a concrete model.  This conclusion does not
establish feasibility of the full 32-bit thirteen-factor graph, compatibility
with one common base schedule, existence of two messages, a distance-13
construction, or any distance lower bound.

Reproduce the independent and author checks from the repository root:

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-factor-signature-review-v9/audit_author.py
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-factor-signature-v9/check.py --negative
```
