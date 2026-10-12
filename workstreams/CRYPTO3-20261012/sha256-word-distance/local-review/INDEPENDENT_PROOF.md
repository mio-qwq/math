# Independent proof and finite certificate for the local map x + sigma1(x)

Status: independently reconstructed AI review of local word lemmas; not human
peer review, not a theorem about the complete SHA-256 expansion distance.
No Lean formalization is claimed. The reconstruction and certificate below
were completed before inspecting the discoverer's proof or implementation.

## 1. Definition and claims

Words are integers in `[0, 2^32)`, with bit zero least significant. Put

```
g(x) = ROTR17(x) xor ROTR19(x) xor SHR10(x),
h(x) = x + g(x) modulo 2^32.
```

This is the SHA-256 small sigma1 function from NIST FIPS 180-4,
Section 4.1.2:
<https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf>.
The extra addition defining `h` is our local mathematical object.

The following statements hold for all 32-bit words `x,y`.

1. If `h(x)=h(y)` and `x=y modulo 8192`, then `x=y`.
2. If `h(x)=h(y)`, `x!=y`, and `x=y modulo 4096`, then
   `x xor y = 0xfbca7000`.
3. There are distinct words with equal `h` and equal low 12 bits. Thus
   13 is the least number of fixed low bits that makes every residue
   class injective for `h`.
4. If `y-x = +2^k` or `-2^k` modulo `2^32`, for any `0<=k<=31`,
   then `h(x)!=h(y)`.

The proofs combine elementary necessary conditions with small, exhaustive
finite classifications, all rebuilt from the displayed definition by
`check_independent.py`. The checker uses no SAT solver, external package,
discoverer code, or discoverer certificate.

## 2. A necessary condition on the two XOR masks

Suppose `h(x)=h(y)`, and set

```
d = x xor y,
e = g(x) xor g(y) = g(d).
```

The last equality follows because rotation, logical shift, and XOR are
linear over F2. For bit `i`, write

```
a_i = bit_i(y) - bit_i(x),
b_i = bit_i(g(y)) - bit_i(g(x)).
```

Each difference is in `{-1,0,1}`. Its absolute value is respectively
`d_i` or `e_i`. The collision gives

```
sum_{i=0}^{31} 2^i (a_i+b_i) = 0 modulo 2^32.
```

Consequently each lower partial sum through bit `i-1` is divisible by
`2^i`. Dividing that partial sum by `2^i` defines an integer signed carry
`c_i`. It satisfies

```
c_0 = 0,
c_i + a_i + b_i = 2 c_{i+1}.
```

Induction shows that every `c_i` is in `{-1,0,1}`: a sum of three such
integers lies in `[-3,3]`, and the even possibilities, divided by two,
are `-1,0,1`. The final carry `c_32` is unrestricted within this set;
it need not be zero because the addition is modular.

If `d_{i-1}=e_{i-1}=0`, the preceding equation becomes
`c_{i-1}=2 c_i`. Its only solution with both carries in `{-1,0,1}` is
zero. Thus the incoming carry at bit `i` is zero whenever the preceding
mask bit is inactive. The incoming carry at bit zero is also zero.
At such a bit, `d_i!=e_i` would make `a_i+b_i` either `+1` or `-1`,
contradicting the required evenness.

We have proved the following necessary condition:

> A bit with exactly one active mask cannot follow a bit with neither
> mask active, and bit zero cannot have exactly one active mask.

An equivalent unsigned expression is

```
((d xor e) & ~((d | e) << 1)) & 0xffffffff == 0.
```

The proof needs only necessity. It does not assert that surviving masks
give an actual collision: the bits of `g(x)` are correlated with those
of `x`, whereas this necessary condition discards these correlations.
For an additional implementation check, the independent verifier also
propagates the reachable signed-carry set for every classified mask,
allowing the two nonzero signs independently. Its first failure agrees
with the displayed mask condition in all 318 classified nonzero cases.

## 3. Equal low bits reduce the problem to a linear kernel

If `x=y modulo 2^b`, then `d` has its bottom `b` bits zero. Equality of
`h` also gives `g(y)-g(x)=-(y-x) modulo 2^32`, so `g(x)` and `g(y)`
have the same bottom `b` bits. Hence `e=g(d)` also has those bits zero.

Define the F2-linear map

```
F_b(d) = low_b(d) | (low_b(g(d)) << b).
```

Every collision with equal low `b` bits has `d` in `ker(F_b)`. The
matrix has 32 columns. Column `i` is `F_b(2^i)`, calculated by the
following per-output-bit formula:

```
bit_j(g(v)) = bit_{(j+17) mod 32}(v)
           xor bit_{(j+19) mod 32}(v)
           xor (bit_{j+10}(v) if j+10<32 else 0).
```

Column elimination retaining input combinations gives the following
complete kernels. Hexadecimal words in each row form a basis.

| b | Rank of F_b | Kernel dimension | Kernel basis |
|---|---:|---:|---|
| 13 | 26 | 6 | `00814000`, `08142000`, `112ac000`, `22558000`, `442a4000`, `8040a000` |
| 12 | 24 | 8 | `0040a000`, `00814000`, `040a1000`, `08142000`, `112ac000`, `22152000`, `40205000`, `80000000` |

The checker reconstructs the 32 matrix columns, eliminates them, checks
that every basis vector maps to zero, checks independence of the basis
with a separate elimination order, and checks rank plus nullity equals
32. It then enumerates every nonempty subset of each basis. There are
exactly 63 nonzero masks for `b=13`, and 255 for `b=12`.

`independent_certificate.json` records every selector, resulting mask
`d`, full image `e=g(d)`, and first obstructing bit from Section 2.
It includes the columns and bases as well. The complete outcomes are:

| b | Nonzero masks | Rejected by Section 2 | Masks without that obstruction |
|---|---:|---:|---|
| 13 | 63 | 63 | none |
| 12 | 255 | 254 | `fbca7000` |

For `b=13`, any purported distinct collision would give a nonzero
kernel mask, but every such mask violates a proved necessary condition.
This proves claim 1. For `b=12`, the only possible nonzero mask is
`fbca7000`, proving claim 2. These are exhaustive classifications of
the stated necessary model, applied only in the direction that proves
the claims. They do not classify the actual input pairs in each fibre.

## 4. A real boundary pair

The following words were found independently by solving the exact
single-word equation for the sole surviving XOR mask, and then checked
with the separate bit-indexed implementation above.

| Quantity | Value |
|---|---|
| `x` | `cd027f2a` |
| `y` | `36c80f2a` |
| `g(x)` | `70437fbe` |
| `g(y)` | `067defbe` |
| `h(x)=h(y)` | `3d45fee8` |
| `x xor y` | `fbca7000` |
| `y-x modulo 2^32` | `69c59000` |
| Common bottom 12 bits | `f2a` |

The inputs are distinct and have equal low 12 bits, but their low 13
bits differ. The two exact additions modulo `2^32` prove claim 3
directly. No solver nonexistence result is used anywhere in this proof.
The example is a pair for the local map `h`, not a pair of 16-word
messages or a full SHA-256 expansion witness.

## 5. Additive power-of-two differences

It suffices to consider `y=x+2^k modulo 2^32`; negative differences
reduce to this case by interchanging the words. When adding `2^k`,
bits below `k` do not change. The bits from `k` through the first zero
at or above `k` toggle. If there is no such zero, all bits through 31
toggle and the addition wraps modulo `2^32`. In either case

```
d = x xor y = I(k,j) = 2^(j+1) - 2^k
```

for some `k<=j<=31`. If the two `h` values were equal, the words
`g(x),g(y)` would differ additively by `-2^k`; reversing their order
shows that their XOR mask must likewise be `I(k,l)` for some `l>=k`.
Therefore the necessary condition on interval masks is

```
g(I(k,j)) = I(k,l),  0<=k<=j<=31,  k<=l<=31.
```

There are `32+31+...+1=528` input intervals. The verifier computes
`g(I(k,j))` from the per-bit definition. A nonzero output has the
required interval shape precisely when its least significant set bit
is `k` and, writing `u=g(I(k,j)) >> k`, it satisfies
`u & (u+1) == 0`. All 528 cases are checked.

Only 22 have the required least significant set bit. They are
`k=0, j in {10,...,16,19,...,31}`, `k=1,j=17`, and `k=2,j=18`;
their exact images are retained in the certificate. Exactly one has
the full interval shape:

```
k=0, j=31, l=21,
d=ffffffff, g(d)=003fffff.
```

An addition by one toggles every bit only for the two ordered pairs
below. Their `h` values, independently computed from the definition,
are unequal:

| x | y | h(x) | h(y) |
|---|---|---|---|
| `7fffffff` | `80000000` | `801faffe` | `80205000` |
| `ffffffff` | `00000000` | `003ffffe` | `00000000` |

The first pair ends its carry run at bit 31; the second wraps beyond
bit 31. These exhaust the only interval case remaining, proving claim
4, including the modular boundary and `k=31`.

## 6. Reproduction and evidence

From the repository root, run:

```
python workstreams/CRYPTO3-20261012/sha256-word-distance/local-review/check_independent.py --selftest
```

Python 3.12.14 executed the checker successfully; `INDEPENDENT_RUN.json`
retains the actual command, exit code 0, elapsed time, stdout, and
stderr of its first certificate emission and verification. The normal
command above verifies the frozen certificate without rewriting it.
All eight controls were rejected: wrong rotation constant, damaged
kernel basis, missing kernel case, false obstructing bit, removal of
the low-12 survivor, damaged witness input, tampered sigma output, and
omission of the exceptional interval.

The initial verified versions were:

| Artifact | SHA256 |
|---|---|
| `check_independent.py` | `3273f3612a2295584563e24975c4eb507935ad98b4a1c28b0b0d7d3a4b5d3c9d` |
| `independent_certificate.json` | `5a884c9a2af33e15ea04ec1a62b40e30d733f4d6f42f13975dfcc05661b1d342` |

The manifest and review receipt supply the exact final file hashes and
the precise discoverer versions compared after this reconstruction.
The mathematical conclusion remains local: no full-schedule support
has been excluded here, and the currently established lower bound on
the actual 64-word SHA-256 schedule distance is not raised by these
lemmas alone.
