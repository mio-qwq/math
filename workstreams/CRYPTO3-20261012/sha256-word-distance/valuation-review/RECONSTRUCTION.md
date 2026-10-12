# Independent reconstruction of the irregular-support valuation claim

This mathematical reconstruction was written before reading the discoverer's
`VALUATION_BOUND.md` or `STRUCTURAL-CERTIFICATE.json`. It is an independent
AI reconstruction, not external human peer review. It starts from the
standard SHA-256 functions and the four specified supports.

Words are modulo `2^32`, bit zero least significant, and

```
f(v) = ROTR7(v) xor ROTR18(v) xor SHR3(v),
g(v) = ROTR17(v) xor ROTR19(v) xor SHR10(v).
```

For an actual schedule pair, `d_i=W'_i-W_i`,
`F_i=f(W'_i)-f(W_i)`, and `G_i=g(W'_i)-g(W_i)`. The original
recurrence gives

```
d_t-G_(t-2)-d_(t-7)-F_(t-15)-d_(t-16)=0, 16<=t<64.
```

## 1. Recurrence origin of the shared constraints

For support indices `6,7,12,13`, respectively take
`u=19,21,18,20`, `x=u`, `y=u+16`, `r=u+25`.
Reading the frozen support list and retaining only active-index terms
gives the following eleven equations, identically for all four values
of `u`:

| t | Restricted recurrence, equal to zero |
|---|---|
| `u` | `d_u-d_(u-7)` |
| `u+2` | `d_(u+2)-G_u-d_(u-5)` |
| `u+9` | `-d_(u+2)-d_(u-7)` |
| `u+11` | `d_(u+11)-d_(u-5)` |
| `u+15` | `-d_(u+8)-F_u` |
| `u+16` | `d_y-d_u` |
| `u+18` | `-G_y-d_(u+11)-d_(u+2)` |
| `u+24` | `d_(u+24)-d_(u+8)` |
| `u+27` | `-G_r-d_(u+11)` |
| `u+31` | `-d_(u+24)-F_y` |
| `u+32` | `-d_r-d_y` |

These equations give

```
d_x=d_y=D, d_r=-D,
F_x=F_y,
G_y-G_x=2D, G_y-G_r=D.
```

The three indicated positions are active, so `D!=0`. Every used
recurrence index is within `[16,63]`. In particular, the derivation
does not shift an equation into the initial sixteen-word boundary.
An independent certificate will retain all 44 concrete equations and
integer linear combinations proving these five identities.

## 2. A short bound reduces 2^21 divisibility to one increment

Assume `2^21` divides `D`. All three input XOR masks are supported in
bits 21 through 31. From the standard definition their `g` images have
no set bit at or above 22. Thus each actual `G` has a unique ordinary
integer representative of absolute value strictly less than `2^22`.
Use those representatives below.

The relation `G_y-G_r=D` identifies a representative `delta` of `D`
with `|delta|<2^23`. The other relation says
`G_y-G_x=2*delta modulo 2^32`. Its left side has absolute value less
than `2^23`; the difference between the two sides has absolute value
less than `3*2^23<2^32`, so their congruence is an equality of integers.
Therefore `|delta|<2^22`.

Since `delta` is nonzero and divisible by `2^21`, it equals `+2^21`
or `-2^21`. Swapping both expansions changes all differences' signs
and preserves the equations, so it is enough to take `D=+2^21`.

This reduction uses the third word pair via `G_y-G_r=D`. It does not
silently replace an arbitrary high-valuation difference by a power of
two in the two-pair subsystem.

## 3. Interval masks and the sigma0 obstruction

Write `a=W_x`, `b=W_y`. Their partners are both obtained by adding
`2^21`. Therefore their XOR masks are intervals

```
A_j = 2^(j+1)-2^21, 21<=j<=31.
```

If both endpoints are at most 30, their `g` masks lie below bit 21.
Both ordinary `G` representatives then have absolute value less than
`2^21`, contradicting `G_y-G_x=2^22`. At least one endpoint is 31.

If the other endpoint is `j<31`, the equality `F_x=F_y` is already
impossible in the independent-sign relaxation. For two XOR masks `p,q`
whose signed sums are equal modulo `2^32`, a bit with exactly one
active mask cannot follow a bit with neither active mask. The proof
uses signed carries in `{-1,0,1}`; an inactive preceding bit resets
the carry to zero and the singleton bit would give an odd total.
It allows arbitrary final carry, as required by modular equality.

For `p=f(A_31)=1e03fff8` and `q=f(A_j)`, the following exact bits
provide that obstruction:

| j | f(A_j) | Obstructing bit |
|---:|---|---:|
| 21 | `00044008` | 25 |
| 22 | `000cc018` | 25 |
| 23 | `001dc038` | 25 |
| 24 | `003fc078` | 25 |
| 25 | `007bc0f8` | 19 |
| 26 | `00f3c1f8` | 20 |
| 27 | `01e3c3f8` | 21 |
| 28 | `03c3c7f8` | 22 |
| 29 | `0783cff8` | 23 |
| 30 | `0f03dff8` | 24 |

Thus both input XOR masks must be `A_31=ffe00000`. Their output masks
are

```
n=f(A_31)=1e03fff8,
m=g(A_31)=003f980c.
```

## 4. A binary linear contradiction for the last case

Put `z=a xor b`. Adding `2^21` toggles through bit 31 only when bits
21 through 30 of the base word are all one. Its top bit can be zero
(the carry ends there) or one (wraparound). Hence

```
z_i=0 for 21<=i<=30.
```

For two pairs with the same output XOR mask `n`, equality of their
additive `f` differences forces the base output bits to agree on `n`:

```
f(z) & n = 0.
```

Indeed, subtracting the two signed-mask formulas and dividing by two
gives a sum of distinct powers of two with coefficients in `{-1,0,1}`.
It is zero as an integer here because `n<2^29`. A highest nonzero
coefficient would dominate the sum of all lower powers, so all vanish.

Likewise `G_y-G_x=2^22` gives

```
g(z) & m = 00200000.
```

To see this, divide the two signed-mask differences by two. The result
is `sum_i m_i (g(a)_i-g(b)_i) 2^i = 2^21`. The top possible bit is
21. Its coefficient must be one; every lower coefficient must vanish
by the same highest-bit argument.

The following parity identity holds for every 32-bit word `z`:

```
parity(f(z) & 0600ffa8)
xor parity(g(z) & 0020000c)
xor parity(   z & 4ea00000) = 0.
```

It follows by substituting the standard output-bit equations. It can
also be verified on the 32 single-bit inputs because all three terms
are F2-linear. The first mask is a subset of `n`, the second a subset
of `m`, and the third uses only bits 21 through 30. Under the forced
conditions, the three terms are respectively `0,1,0`, a contradiction.

Therefore `2^21` cannot divide nonzero `D`, proving `v2(D)<=20` for
all actual pairs with any of the four supports. No satisfiability
solver or large old support enumeration is required by this proof.

Source definition: NIST FIPS 180-4, Sections 4.1.2 and 6.2.2,
<https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf>.

## Independent verification checkpoint

The independent certificate and verifier have now been completed and
executed before reading either discoverer file. `INDEPENDENT_RUN.json`
records Python 3.12.14, exit code zero, all 44 original recurrence rows,
20 exact integer linear-combination identities, 10 mixed-interval
exclusions, and all 32 basis checks of the universal parity identity.
All 14 damaged controls were rejected. The certificate contains the
complete finite data used above; no solver result is a proof dependency.

The initial exact checker and certificate hashes are:

```
check_valuation_independent.py
b9537d51976b705ba20bf3835c9e57812e5f32ff15d33d255de2ab55c7fd19c2

independent_valuation_certificate.json
7449074d5a957b348ee1a9b2221f1539b36a3500753a0622f9f1e2c04788af59
```

The later precise-version author comparison is recorded separately.
