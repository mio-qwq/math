# Ten affine contradictions for a fixed-mask SHA-256 boundary

**Candidate second proof, with a small exact finite certificate.**
Independent-agent review is recorded separately. This proof and checker
use neither a SAT solver nor a CNF/RUP certificate. No Lean formalization
or historical originality is claimed.

## 1. Exact theorem

Work with arbitrary 32-bit words, bit zero least significant, and all
word additions modulo `N=2^32`. Use the SHA-256 small sigma functions

```
f(x) = ROTR7(x) xor ROTR18(x) xor SHR3(x),
g(x) = ROTR17(x) xor ROTR19(x) xor SHR10(x).
```

These are the definitions in NIST FIPS 180-4, Section 4.1.2:
<https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf>.

**Theorem.** Put `K=0xfbca7000`. There are no words `p,p',q,q'`
satisfying all four requirements

```
q' = q xor K,
q + g(q) = q' + g(q'),                                  (E1)
p' + q = p + q',                                       (E2)
f(p') + f(q') = f(p) + f(q).                            (E3)
```

All base words remain arbitrary. The theorem concerns these local
equations. A connection to a complete message-schedule support needs
its own recurrence derivation; no entire support is excluded by this
statement alone.

The proof has three finite components, each directly reproducible:

1. A parameterization of every necessary mask `A=p xor p'`, with only
   17 free bits, followed by two elementary necessary carry tests.
2. An exact conversion of each fixed-mask derivative equation to an
   affine binary system, using a uniform carry table.
3. Ten small XOR contradictions covering all 132 remaining masks.

The final certificate contains 26 distinct binary equations and ten
templates, totaling 36 template-row occurrences. Its 132 mask-to-template
assignments require 384 elementary row-membership checks. The verifier
performs no Gaussian elimination: it reconstructs the needed equations
and XORs the supplied rows to obtain `0=1`.

## 2. All necessary input masks

Set `A=p xor p'` and `D=q'-q`. Equation (E2) gives `p'-p=D`.
For any unequal pair of words, the least set bit of their XOR is also
the 2-adic valuation of their nonzero additive difference. Indeed, if
that bit is `b`, the lower `b` bits agree and bit `b` differs, so the
difference is zero modulo `2^b` but nonzero modulo `2^(b+1)`.

The least set bit of `K` is 12. Consequently

```
A[0..11]=0, A[12]=1.                                    (2.1)
```

The exact sigma images of the fixed mask are

```
L=f(K)=0x828ee412, C=g(K)=0x763e9000.
```

The least set bit of `L` is 1. By XOR linearity, `L` is the XOR of
`f(q')` and `f(q)`, so their additive difference has valuation 1.
Equation (E3) makes the other sigma0 difference its negative, with
the same valuation. Thus `f(A)[0]=0` and `f(A)[1]=1`.
Using (2.1) in the standard output-bit equations gives

```
f(A)[0] = A[18],  f(A)[1] = A[19],
A[18]=0, A[19]=1.                                      (2.2)
```

Exactly 17 mask coordinates remain free: `13..17` and `20..31`.
Every candidate is represented once by an integer `0<=u<2^17`:

```
A(u) = 0x00081000 | ((u & 31) << 13) | ((u >> 5) << 20).
```

This includes the top bit freely and does not impose any condition on
the unprimed or primed base-word bits beyond the stated XOR mask.

### A necessary gap condition

For a word `x` and fixed XOR mask `a`, the ordinary integer difference
is exactly

```
(x xor a)-x = sum_i a_i(1-2x_i)2^i.
```

Suppose the sum of two such signed-mask expressions is zero modulo
`2^32`. Its incoming signed carries lie in `{-1,0,1}` and start at
zero. If both masks are inactive at the preceding bit, the outgoing
carry there must be zero: an even member of `{-1,0,1}` is zero.
A bit with exactly one active mask would then produce an odd sum,
which is impossible. Bit zero has the same restriction because its
incoming carry is zero.

Therefore any two masks `a,b` in a zero signed-sum relation must satisfy

```
((a xor b) & ~((a | b) << 1)) & 0xffffffff == 0.          (2.3)
```

**Historical attribution.** Condition (2.3) is the zero-output-difference
special case of the classical modular-addition XOR-differential
criterion of Helger Lipmaa and Shiho Moriai, *Efficient Algorithms for
Computing Differential Properties of Addition*, FSE 2001, Algorithm 2
and Theorem 1 (page 7 of the
[author PDF](https://kodu.ut.ee/~lipmaa/papers/lm01/dpa.pdf);
[ePrint 2001/001](https://eprint.iacr.org/2001/001), final proceedings
version, last revised 2001-05-16). With their output difference set to
zero, their equal-bit mask is `T=~((a | b)<<1)`; its conjunction with
the additional shifted term `b<<1` vanishes. Their feasibility test
therefore reduces exactly to (2.3). The carry argument above supplies
a self-contained derivation of the necessary direction used here;
this mask screen is not a new method.

A minus sign on a signed difference changes its bit signs but not its
mask, so the same necessary condition applies to equality of two
differences. Apply (2.3) first to `A,K` using (E2), and then to
`f(A),L` using (E3).

The complete finite check of the displayed parameterization gives:

| Stage | Number of masks |
|---|---:|
| Every assignment to the 17 free coordinates | 131,072 |
| After (2.3) for the input masks `A,K` | 24,576 |
| After (2.3) also for `f(A),L` | 132 |

The complete 132-mask list and its partition are in Appendix A and
`CERTIFICATE.json`. The verifier regenerates the complete set from
the parameterization and the output-bit definition of `f`, and checks
that the partition contains every regenerated mask exactly once.
No optimal-support enumeration, solver answer, or search-time cutoff
is a premise of this classification.

## 3. A complete affine description of the signed carries

This section treats arbitrary fixed masks `a,b`. The bits `u_i,v_i`
may be arbitrary affine binary expressions in the base-word bits.
Consider the modular equality

```
sum_i [a_i(1-2u_i)+b_i(1-2v_i)]2^i = 0 mod 2^32.         (3.1)
```

Every lower partial sum is divisible by its next power of two. The
quotients define integer signed carries `c_i` satisfying

```
c_0=0,
c_i + a_i(1-2u_i)+b_i(1-2v_i) = 2 c_(i+1).             (3.2)
```

Induction gives `c_i in {-1,0,1}`: the even possibilities in `[-3,3]`,
divided by two, are precisely `-1,0,1`. In particular the carry parity
is fixed by the masks:

```
w_i = a_i xor b_i,
c_i=0 when w_i=0,
c_i=1-2t_i when w_i=1.
```

The initial condition requires `w_0=0`. For `0<=i<31`, write
`w'=a_(i+1) xor b_(i+1)`. Substitution in (3.2) gives the complete
transition table:

| Active masks at i | Ordinary next carry | Required binary equation | Next sign if w'=1 |
|---|---|---|---|
| neither | `0` | `w'=0` | impossible |
| both, base bits u,v | `1-u-v` | `u xor v=1 xor w'` | `t_(i+1)=u=v` |
| one, base bit u | `1-t_i-u` | `t_i xor u=1 xor w'` | `t_(i+1)=t_i=u` |

When `w'=0`, the two indicated binary arguments differ and the next
carry is zero. When `w'=1`, they agree and the next carry is `+1`
or `-1` with the stated sign. These alternatives are exhaustive.
Thus a nonzero carry sign can always be replaced by one displayed
base-bit expression; no case branch on its actual value is needed.
All remaining conditions are affine binary equations.

The table is exact in both directions. Necessity follows from (3.2).
Conversely, starting with `c_0=0`, the table constructs each ordinary
carry and forces its parity to be the mask parity at the next bit.
At bit 31 that known parity makes the sum even; any resulting integer
`c_32 in {-1,0,1}` is allowed. Telescoping (3.2) gives the sum in
(3.1) equal to `2^32 c_32`, as required.

**There is no requirement that the final carry vanish.** For example,
two positive signed contributions of `2^31` sum to zero modulo `2^32`
with final carry one. The checker explicitly verifies that boundary,
and checks all 18 cases in the local transition table.

## 4. Applying the table to the three equations

Take 64 binary variables, the 32 bits of `p` followed by the 32 bits of
`q`. For each candidate mask `A`, reconstruct `p'=p xor A` and
`q'=q xor K`. XOR linearity gives the output masks `f(A),L,C`.

The three applications of (3.1) are:

| Equation | First mask and bit form | Second mask and bit form |
|---|---|---|
| (E1) | `K`, `q_i` | `C`, `g(q)_i` |
| (E2) | `A`, `p_i` | `K`, `q_i xor 1` |
| (E3) | `f(A)`, `f(p)_i` | `L`, `f(q)_i` |

The complement in the (E2) row is essential:
`-(1-2q_i)=1-2(q_i xor 1)`. It implements the negative second
derivative, rather than replacing (E2) by a different sum equation.
Every bit form is affine because the sigma functions are XOR linear.

Section 3 therefore gives an affine system on the actual 64 base bits
for each fixed `A`. For each of the 132 masks, some of the resulting
equations are one of the ten contradictory templates in the next
section. This excludes every mask and proves the theorem.

## 5. The ten contradictions

All equations in this section are over F2. Put `z_i=p_i xor q_i`.
For families 6, 7, and 8 use the standard identity

```
f(z)[10]=z[17] xor z[28] xor z[13].                      (5.1)
```

| Family | Masks | Contradictory equations |
|---|---:|---|
| 0 | 22 | `q23 xor q24=0` and `q23 xor q24=1` |
| 1 | 27 | `q13 xor q14=0` and `q13 xor q14=1` |
| 2 | 1 | `q22 xor q23=0` and `q22 xor q23=1` |
| 3 | 37 | `p12 xor q12=1`, `p12 xor q13=0`, `q12 xor q13=0` |
| 4 | 18 | `p13 xor q13=1`, `p13 xor q14=0`, `q13 xor q14=0` |
| 5 | 4 | `p22 xor q22=1`, `p22 xor q23=0`, `q22 xor q23=0` |
| 6 | 12 | `z13=0`, `z17=0`, `z28=1`, `f(z)[10]=0` |
| 7 | 6 | `z13=1`, `z17=0`, `z28=1`, `f(z)[10]=1` |
| 8 | 2 | `z13=0`, `z17=0`, `z28=0`, `f(z)[10]=1` |
| 9 | 3 | The nine equations displayed below |

In family 9 the equations are

```
p15 xor p16 = 0,
p15 xor q14 = 1,
q13 xor q14 = 0,
p16 xor q17 = 0,
p28 xor q28 = 1,
q13 xor q15 xor q28 = 1,
p28 xor q29 = 1,
q15 xor q17 xor q30 = 0,
q29 xor q30 = 1.
```

In each family, XORing all displayed equations gives `0=1`; in
families 6 through 8, expand (5.1) first. Every template is therefore
a direct binary linear contradiction, independently of elimination
strategy. The certificate stores the same equations as 64-bit row
coefficients with one-bit right sides.

### Two illustrative derivations

For `A=293a1000`, the signed carry table applied to (E1) at bit 14
gives `q13 xor q14=0`. In (E2), bits 13 and 14 are active only in
the second mask, and its base form is `q_i xor 1`. The transition at
bit 14 gives `q13 xor q14=1`. This is family 1.

For `A=K`, all input mask parities in (E2) are zero. At every changed
input bit below 31 the carry rule gives `p_i=q_i`, including bits
13, 17, and 28. In (E3), both masks are `L`, and the same zero-carry
rule for a positive sum gives `f(p)[10] xor f(q)[10]=1`.
Linearity and (5.1) make this family 8's contradiction. No condition
on the final carry or on the top base-word bit is added.

For all the other masks, checking template applicability is equally
finite: reconstruct the three carry systems from Section 4 and check
that each displayed row is among their equations. `check.py` performs
those 384 row-membership checks from the original bit definitions.
Together with the complete mask partition, this verifies every premise
used in the ten XOR contradictions.

## 6. Reproduction, controls, and scope

From this directory run:

```
python -B check.py --negative
```

The check uses only the Python standard library. It rebuilds all
131,072 necessary-mask candidates, obtains the same 132 survivors,
checks the complete carry table and modular top-bit boundary, confirms
all 384 row memberships, and XORs the ten templates to `0=1`.
No Gaussian elimination, SAT solving, or external solver certificate
is part of verification. The discovery programs are not imported.

The actual run used Python 3.12.14 and exited zero. All 14 damaged
controls were rejected, including incorrect sigma constants, altered
`K`, the wrong derivative sign, a forced zero final carry, a missing
mask coordinate or mask case, a duplicate case, tampered binary rows,
an omitted XOR premise, a corrupted transition, and a false whole-
schedule scope. `RUNS.json` retains the actual commands, exit codes,
timings, stdout, stderr, and source hashes.

The exact final certificate is 13,098 bytes, with SHA256
`1428cce8b31378b67db8de32e4480bfedad608b0d62b0bee21742f3f09fa6389`.
The checker SHA256 is
`71c12525b4938650984a9c87394dcc0fdf5f65e848ec1b606732cd20ff0d0d4d`.
The package manifest binds the remaining source and evidence files.

This is a complete written reduction with a small, transparent finite
certificate. It is not a proof-assistant formalization. Generic carry
analysis is not claimed as a new method, and specific parameter
priority is unconfirmed. The theorem proves nonexistence for the stated
fixed-mask local system; applying it to schedule-distance bounds retains
the separate support and recurrence dependencies of that application.

## Appendix A. Complete mask partition

The following is the complete list of the 132 masks surviving the two
necessary tests in Section 2. Labels are hexadecimal unsigned words;
the number before each group is its contradiction-family identifier.

```text
0:
  1c3a7000 1c3af000 1c4a7000 1c5a7000 1c5af000 1c7a7000 1c7af000 8439b000
  843a7000 844a7000 8459b000 845a7000 8479b000 847a7000 9c3a7000 9c4a7000
  9c4ab000 9c5a7000 9c7a7000 d84a7000 f84a7000 fc4a7000
1:
  293a1000 294a1000 295a1000 297a1000 2f3a1000 2f4a1000 2f5a1000 2f7a1000
  373a1000 374a1000 375a1000 377a1000 483a1000 485a1000 487a1000 48ba1000
  48da1000 48fa1000 493a1000 495a1000 497a1000 4b3a1000 4b5a1000 4b7a1000
  4f3a1000 4f5a1000 4f7a1000
2:
  953bb000
3:
  4939d000 493a5000 493ad000 493bd000 4949d000 494ad000 494bd000 4959d000
  495a5000 495ad000 495bd000 4979d000 497a5000 497ad000 497bd000 4b3a5000
  4b5a5000 4b7a5000 4f3ad000 4f4ad000 4f5ad000 4f7ad000 56b9d000 56d9d000
  56f9d000 5939d000 593bd000 5949d000 594bd000 5959d000 595bd000 5979d000
  597bd000 953a5000 954a5000 955a5000 957a5000
4:
  583a3000 585a3000 587a3000 593a3000 595a3000 597a3000 5a3a3000 5a5a3000
  5a7a3000 5e3a3000 5e5a3000 5e7a3000 783a3000 785a3000 787a3000 7a3a3000
  7a5a3000 7a7a3000
5:
  955bb000 957bb000 9d4ab000 fb4a7000
6:
  1a3a7000 1a4a7000 1a5a7000 1a7a7000 1e3af000 1e5af000 1e7af000 9a3a7000
  9a4a7000 9a5a7000 9a7a7000 da4a7000
7:
  9a3bb000 9a4ab000 9a5bb000 9a7bb000 9dcab000 9e4ab000
8:
  fa4a7000 fbca7000
9:
  9a39b000 9a59b000 9a79b000
```
