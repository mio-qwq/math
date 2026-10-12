# A sharp two-pair joint-valuation restriction on supports 10 and 11

**Complete written proof, with a standard-library finite-dependency
checker. Awaiting a separate independent-agent review.** The actual
SHA-256 64-word distance bound remains 13. Neither support is excluded.
No full message pair, Lean formalization, attack, or priority claim is
supplied.

All word arithmetic is in `R=Z/(2^32)`. Define the actual SHA-256 maps

```
f(x)=ROTR7(x) xor ROTR18(x) xor SHR3(x),
g(x)=ROTR17(x) xor ROTR19(x) xor SHR10(x).
```

For an actual ordered pair `X=(x,x')`, put
`d(X)=x'-x`, `F(X)=f(x')-f(x)`, `G(X)=g(x')-g(x)`.
Both sigma differences always use the same actual operands.

**Local theorem.** Let `m` equal 1 or 2. Suppose actual word pairs X,Y
satisfy

```
x' != x,
d(Y)=-F(X),
F(Y)=-m*d(X)-G(X).
```

Then `d(X)` and `m*d(X)+G(X)` cannot both be divisible by `2^16`.
When both differences are nonzero, their minimum valuation is at most
15. The threshold 15 is sharp for each of these two local models.

**Exact support application.** For either of the frozen supports 10
and 11, every actual SHA-256 schedule pair has

```
min(v2(d18),v2(d34)) <= 15.
```

This is a joint restriction, not an individual upper bound on either
valuation. The support numbering is bound to the unchanged
`supports-v2.json`, SHA256
`02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf`.
The local theorem does not depend on completeness of the old support
classification. Only its support application uses the two specific
patterns; it applies to arbitrary base messages.

## 1. Derivation from the original recurrences

For an actual schedule pair, subtraction of the true modular recurrence
gives the equation

```
e_t=d_t-G_(t-2)-d_(t-7)-F_(t-15)-d_(t-16)=0,
16 <= t <= 63.
```

Outside the support, all three differences are zero. For support 10,
the required original equations reduce exactly to

| t | e_t=0 |
|---:|---|
| 20 | d20-G18=0 |
| 27 | d27-d20=0 |
| 33 | -d26-F18=0 |
| 34 | d34-d27-d18=0 |
| 41 | -d34-F26=0 |

Hence with X at index 18 and Y at 26, `d(Y)=-F(X)` and
`d34=d18+G18`, `F(Y)=-d34`. This is the local theorem with m=1.

For support 11, the exact equations are

| t | e_t=0 |
|---:|---|
| 18 | d18-d11=0 |
| 20 | d20-G18=0 |
| 27 | d27-d20-d11=0 |
| 33 | -d26-F18=0 |
| 34 | d34-d27-d18=0 |
| 41 | -d34-F26=0 |

These give `d34=2*d18+G18` and the same Y equation, so m=2.
Indices 18, 26 and 34 are active in both supports. In particular X is
unequal and both d18 and d34 are nonzero. The checker reconstructs
each equation from the original lag set, and verifies the exact integer
row combinations stored in the certificate. There is no division by a
nonunit and no unproved time shift.

## 2. A complete first-pair mask kernel

Assume, for contradiction, that `2^16` divides d(X) and
`E=m*d(X)+G(X)`. It then divides G(X) as well. Put

```
alpha=x xor x', beta=g(x) xor g(x')=g(alpha).
```

The low 16 bits of alpha and beta are zero. These 32 homogeneous
binary equations have rank 31, and their kernel has basis consisting
of the single word

```
K=44ab0000.
```

The certificate and checker verify rank of the original rows, membership
and independence of the basis. Since X is unequal, alpha is exactly K.
Its output XOR masks are

```
f(K)=c81c272a, g(K)=e0110000.
```

For Y=(y,y'), put `L=y xor y'`. Since `F(Y)=-E` has zero low
16 bits, f(L) has zero low 16 bits. The original 16 binary output rows
of f have rank 16. The 16 listed basis words in `CERTIFICATE.json`
therefore span *every* possible L, giving exactly 65,536 candidates.
Membership checks and full rank make this cover complete.

## 3. Exact necessary signed-bit carry checks

If U'=U xor B, their difference is

```
U'-U = sum_(i:B_i=1) (1-2*U_i)*2^i mod 2^32.
```

Apply this to input or sigma-output words. For any equation that sums
such differences to zero, relax the signs on each changed bit to
independent choices. This discards the common base-word constraints,
so an impossibility in the relaxed system is a valid necessary
contradiction.

For masks `B_1,...,B_r`, let `n_i` be the number of masks active at bit i.
Starting with `C_0={0}`, the exact relaxed carry recurrence is

```
C_(i+1) = { (c+t)/2 : c in C_i,
             t in {-n_i,-n_i+2,...,n_i}, c+t even }.
```

If a reachable set becomes empty, the modular sum is impossible. The
carry out of bit 31 is unrestricted: imposing zero there would wrongly
replace modular equality with integer equality. This test is exact for
independent signs, and only necessary for actual word pairs. This is
the standard signed-bit modular-addition method, not a new generic
cryptanalytic technique.

The first equation `d(Y)+F(X)=0` uses masks L and f(K).
The complete 65,536-mask cover leaves exactly five survivors:

| L | f(L) |
|---|---|
| 4804ddd6 | 92e50000 |
| 5804fff6 | d84d0000 |
| c814ddf6 | c3ef0000 |
| d805eee6 | ad090000 |
| d814ffd6 | 89470000 |

The checker reconstructs every kernel combination and every carry
transition. It does not import an SMT status or trust a count alone.
The full first-empty-bit histogram also matches the frozen certificate.

The second equation is `F(Y)+m*d(X)+G(X)=0`. Its masks are

```
f(L), K, g(K)         for m=1,
f(L), 2*K mod 2^32, g(K)  for m=2.
```

Multiplication by two just shifts the signed-bit input expression one
bit; the vanished bit-32 term is a multiple of 2^32. The retained signs
need not be independent in an actual pair, but allowing independent
signs still gives a valid necessary condition. Applying the same carry
recurrence to the five survivors gives

| L | First impossible bit, m=1 | First impossible bit, m=2 |
|---|---:|---:|
| 4804ddd6 | 16 | 27 |
| 5804fff6 | 16 | 24 |
| c814ddf6 | 16 | 27 |
| d805eee6 | 16 | 22 |
| d814ffd6 | 16 | 29 |

For m=1 the first failure is especially direct: the three masks each
have bit 16 set and all lower bits zero. The bit-16 signed sum is odd
with incoming carry zero. The m=2 cases use the same fully enumerated
32-step carry rule; each listed first-empty bit is directly replayed.
Every possible nonzero alpha and every possible L is now covered,
proving the local theorem and its support corollary.

## 4. The local threshold is sharp, with actual words

The following fixtures satisfy both displayed local equations exactly:

| m | x | x' | y | y' | d(X) | G(X) | E=m*d(X)+G(X) |
|---:|---|---|---|---|---|---|---|
| 1 | 95d39b84 | f32d1b84 | f1110800 | 9d1f33a7 | 5d598000 | 6ff68000 | cd500000 |
| 2 | 54cd8023 | 32330023 | 56112dbb | 021f616a | dd658000 | 70188000 | 2ae38000 |

In the first row the two valuations are 15 and 20. In the second they
are both 15. Both minima equal 15, so the local bound cannot be improved
without another constraint. The verifier computes both sigmas from their
original bit definitions and checks the two modular residuals, inequality
of both pairs, all stored interfaces and the valuations.

**These are four-word local fixtures.** They are not 16-word message
blocks, a complete assignment on all 13 active positions, or evidence
that either complete support is attainable.

## 5. Verification and failure boundaries

Run from the repository root:

```
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/supports10-11-v4/check.py --negative --save
```

`CERTIFICATE.json` supplies the finite constants and fixtures.
`check.py` is a second author implementation using direct sigma output
bit rows and carry transitions. Another agent's review is required
before describing the new result as independently accepted. Discovery
files retain solver versions, parameters, source hashes and exact scopes,
but none of their UNSAT statuses is a premise of the proof.

The k=15 independent-sign relaxation leaves 39 mask pairs for m=1 and
29 for m=2. Each bounded actual-word search finds a fixture on its first
case and stops. Those data accurately diagnose the mechanism boundary:
the two-pair core alone cannot improve the joint bound below 15. The
scientifically useful next step is to retain an additional actual word
pair or original base recurrence, rather than extending an SMT timeout
for this already sharp local model.
