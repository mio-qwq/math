# A divisibility restriction on four unresolved SHA-256 supports

**Candidate written lemma with checked finite constants, awaiting independent review.**
The 64-word distance lower bound remains 13. No support is fully
excluded by this lemma and no full expanded-message witness is supplied.

The frozen size-13 support indices are those in CRYPTO2 commit
`80b71cb3b6a67c8f8aae80d9cd8b6ed87d74bd51`, file
`workstreams/CRYPTO2-20261011-7f3c/projects/sha256-schedule-distance/v2/supports.json`.
All arithmetic is modulo N=2^32. Write f=sigma0, g=sigma1,
d_i=W'_i-W_i, F_i=f(W'_i)-f(W_i), G_i=g(W'_i)-g(W_i).

## Claimed restriction

For an actual expanded message pair on any support in the following
table, the common nonzero difference D=d_x=d_y is **not divisible by
2^21**. Equivalently, v2(D)≤20.

| Support index | x | y | r | Other indices p, q, u, v |
| --- | ---: | ---: | ---: | --- |
| 6 | 19 | 35 | 44 | 12, 21, 14, 30 |
| 7 | 21 | 37 | 46 | 14, 23, 16, 32 |
| 12 | 18 | 34 | 43 | 11, 20, 13, 29 |
| 13 | 20 | 36 | 45 | 13, 22, 15, 31 |

The table merely names recurrence locations, and must be checked against
the exact support file. No new support enumeration is needed.

## 1. Recurrence reduction

For support 6 the relevant equations are

| t | Reduced equation |
| ---: | --- |
| 19 | d19=d12 |
| 28 | d21=-d12 |
| 35 | d35=d19 |
| 21 | d21=G19+d14 |
| 30 | d30=d14 |
| 37 | 0=G35+d30+d21 |
| 46 | 0=G44+d30 |
| 51 | 0=d44+d35 |
| 34 | 0=d27+F19 |
| 43 | d43=d27 |
| 50 | 0=d43+F35 |

They imply

```
d19=d35=D != 0, d44=-D,
F19=F35,
G35-G19=2D, G35-G44=D.
```

The same equations shift by +2 for support 7 and +1 for support 13.
For support 12 they shift by -1 except the first equality d18=d11
is already the actual equation at t18; all displayed shifted reductions
remain valid. The external verifier must derive the equations from the
lag set {2,7,15,16}, not accept the table by label.

## 2. A sigma1 locality bound

If 2^21 divides b-a, the lower 21 input bits agree. For every output
bit j≥22, the two rotation inputs of g are j-15 and j-13, both less
than 21, and the SHR10 term is absent. Consequently the output words
g(a),g(b) have identical bits 22..31. Their ordinary signed integer
difference therefore lies strictly between -2^22 and 2^22.

Assume for contradiction that 2^21 divides D. Apply this observation
to the pairs at x,y,r (whose differences are D,D,-D). Let q_x,q_y,q_r
be their ordinary integer g-output differences, each of absolute value
less than 2^22. Set A=q_y-q_r and B=q_y-q_x. Then

```
A = D (mod N), B = 2D (mod N),
|A| < 2^23, |B| < 2^23.
```

Since B-2A is a multiple of N and |B-2A|<3·2^23<N, it must be zero.
Thus B=2A and |A|<2^22. As D is active and divisible by 2^21, A is
one of ±2^21. Therefore **D is congruent to ±2^21 modulo N**.

## 3. Excluding the remaining fixed difference

It remains to exclude four words x,x',y,y' satisfying

```
x'-x = y'-y = 2^21,
f(x')-f(x) = f(y')-f(y),
g(y')-g(y)-g(x')+g(x) = 2^22.
```

The negative difference follows by swapping primed and unprimed words.
The equations are invariant under that swap with every difference
negated.

The following argument is a complete written proof. The exploratory
SMT and 121-case traversal are not premises.

### 3.1. Input carry masks and a gap obstruction

Adding 2^21 changes a contiguous interval of bits from 21 to some
end e∈{21,…,31}. For e<31 the input bits 21,…,e-1 are 1 and bit e
is 0. For e=31, bits 21,…,30 are 1 and bit31 is unrestricted; this
includes wraparound. Put

    alpha_e = sum_(j=21)^e 2^j,  beta_e = g(alpha_e).

For two words having output XOR mask beta, their ordinary integer
output difference is exactly a signed sum of beta's set powers:

    sum_(beta_j=1) (1-2u_j)·2^j.

In particular its absolute value is at most beta as an unsigned integer.
The eleven masks are the following exact evaluations of the specified g.
The last column is used when comparing beta_e against beta_31.

| e | beta_e (hex) | Gap bit h |
| ---: | --- | ---: |
| 21 | 00000814 | 15 |
| 22 | 0000183c | 15 |
| 23 | 0000386c | 5 |
| 24 | 000078cc | 6 |
| 25 | 0000f98c | 7 |
| 26 | 0001fb0c | 8 |
| 27 | 0003fe0c | 9 |
| 28 | 0007f40c | 10 |
| 29 | 000fe00c | 11 |
| 30 | 001fc80c | 14 |
| 31 | 003f980c | — |

If neither input carry reaches bit31, then

    |G_y-G_x| ≤ 2 beta_30 = 0x003f9018 < 2^22,

so the required gap 2^22 is impossible. All these integer differences
have magnitude below N/2, so there is no extra multiple of N to consider.

If exactly one carry reaches bit31, use the listed gap bit h for the
other mask. Both masks have bit h-1 equal to zero, and exactly one
has bit h equal to one. Contributions below bit h then have absolute
value at most 2(2^(h-1)-1)<2^h. Since the desired gap 2^22 is zero
modulo 2^h, those lower contributions must sum to zero as integers.
The bit-h contribution is now ±2^h, contradicting the desired zero
modulo 2^(h+1). This argument is symmetric in the two masks. The table
contains every e<31, and every listed h is at most 15<22.

Therefore **both carries reach bit31**.

### 3.2. The remaining case gives an explicit XOR contradiction

Now both input XOR masks equal alpha=0xffe00000. Their common sigma
output masks are

    beta_f = f(alpha) = 0x1e03fff8,
    beta_g = g(alpha) = 0x003f980c.

Put z=x XOR y. Because both carries reach bit31, z21,…,z30 are zero.
The equality of the two ordinary f-derivatives forces equality of the
unprimed output bits at every set bit of beta_f. To see this, subtract
the signed-sum expressions and divide the resulting integer equality
by 2. A nonzero signed binary sum with coefficients in {-1,0,1} cannot
be zero, because its highest nonzero power exceeds the sum of all lower
powers. The modular equality is an ordinary equality here: twice
beta_f is less than N. Consequently

    f(z) AND beta_f = 0.                                      (A)

Likewise the g-derivative gap is 2^22. Dividing its integer signed-sum
identity by 2 gives 2^21. Since bit21 is beta_g's highest bit and all
lower weights sum to less than 2^21, the bit21 coefficient must be +1
and all other coefficients must be zero. Hence

    g(z) AND beta_g = 2^21.                                   (B)

The output-bit definitions of f and g give the following identity for
**every** 32-bit z, with all sums interpreted as XOR:

```
g(z)[21] = XOR(z[j] : j in {21,23,25,26,27,30})
         XOR XOR(f(z)[j] : j in {3,5,7,8,9,10,11,12,13,14,15,25,26})
         XOR g(z)[2] XOR g(z)[3].
```

It can be verified by expanding each sigma output bit and cancelling
repeated input bits in F2. Every raw z bit on the right is zero because
both carries reach bit31. Every displayed f bit is zero by (A), and
g(z)[2]=g(z)[3]=0 by (B). Thus g(z)[21]=0, contrary to (B). This
excludes the fixed positive difference, completes the negative case
by priming swap, and proves the claimed restriction.

The small `STRUCTURAL-CERTIFICATE.json` contains the eleven masks, ten
gap positions, two exact masks and this XOR identity. The direct-bit
checker verifies all constants and all 44 recurrence substitutions.
The longer discovery traversal is retained only as cross-check evidence.
There is no SHA Lean formalization in this result.

## 4. Why an omitted equation would break the argument

The four-word twin core alone permits D=2^31+2^21. One exact witness is

```
x  = 2147483648, x' = 2097152,
y  = 697319424,  y' = 2846900224.
```

The direct-bit checker verifies the two matching input differences,
matching sigma0 derivatives and sigma1 derivative gap 2D. This witness
does not satisfy a supplied complete schedule. It shows why the
additional relation G_y-G_r=D must not be omitted when reducing the
high-divisibility stratum to D=±2^21.

The generic four-word twin core is also feasible with the words in
`TWIN-RUN.json`; the checker validates those and all stored positive
high-divisibility witnesses without importing a solver. An independent
pair witness remains a boundary result about this necessary model.

## Scope and ownership

This is a new necessary divisibility condition within the existing
actual-message question. It does not prove distance 14, attain distance
13, estimate a compression differential probability, or advance a hash
collision attack. The arithmetic and carry techniques are standard;
specific parameter priority is unconfirmed. The only support assumption
is the exact frozen zero pattern; all base-message words remain arbitrary.
