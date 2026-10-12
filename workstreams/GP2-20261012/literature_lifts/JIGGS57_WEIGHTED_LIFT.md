# A classical 57-word dictionary and its optimal block weights

GP2-20261012, 2026-10-12. The 57-word dictionary is classical. This note
supplies its exact lift to original Kautz general position, a convenient
all-parameter rational family, and an exact optimization of this fixed
dictionary's four block weights. It does not assert an optimal GP formula.

## 1. Original source and the exact finite template

B. H. Jiggs, *Recent Results in Comma-Free Codes*, Canadian Journal of
Mathematics 15 (1963), 178–187,
[DOI 10.4153/CJM-1963-021-1](https://doi.org/10.4153/CJM-1963-021-1),
prints a 57-word four-symbol dictionary on page 184, Section 3.
The actual printed page was rendered and visually read on 2026-10-12.
The source's historical assertion of maximality is not used in this note.

The exact transcription is `jiggs57_words.txt`, SHA256
`26d405621e125016c26edf662bd1d18cb721bb6b09976c421fa5093e531a1f14`:

```text
DBDD DDAD DDCD CCCB BCCB
DCCB ACCA DABD BABB DBCB
CACB DACB DCAD DACD DAAD
BCAD BAAD ACAB BAAA DCBD
BDAD BDCD CCCD BCCD DCCD
ACCD DABB BCAB ABCB DAAB
BBAD DCAB CACD DBAD ACAD
DBCD BAAB BCAA DCBB DBBD
DBBB CCCA BCCA DCCA ACCB
BABD BBCB BACB AACD BBCD
BACD DCAA ABAD DAAA AACB
ACAA ABCD
```

Call this dictionary `D`. It has no selected adjacent windows and is
comma-free. These two properties can be checked directly by comparing its
three-letter prefix and suffix sets and inspecting the three interior
windows in each of the `57^2` concatenations. A separate independent checker
also reads all `4^8=65536` eight-symbol words and verifies that none has
three selected four-window occurrences. All these checks concern this
explicit dictionary; no optimizer or exhaustive search over dictionaries
is needed.

Here is the universal implication of the finite certificate. If an
eight-symbol word had three selected starts among `0,...,4`, independence
would force the starts to be `0,2,4`. Its first and last selected words
would be two words of `D`, whose concatenation has a selected interior
window at position two, contrary to comma-freeness. This argument counts
occurrences even when the endpoint words coincide.

## 2. Lift to the original directed graph and exact counts

Partition an actual alphabet into four blocks with names `A,B,C,D`, and
select **all valid original Kautz vertices** whose block word is in the
displayed dictionary. Equal adjacent block labels are allowed; equal
adjacent actual letters remain forbidden.

An original arc shifts a word by one position and appends a letter different
from its former final letter. Every directed walk of at most four edges is
therefore read in at most eight consecutive letters. Also the original
directed diameter is at most four: append all target letters when its first
letter differs from the source's last letter, or use that common letter as
an overlap and append the final three target letters otherwise. Hence the
strict window property excludes three selected vertices on **every**
shortest directed path. The construction is original GP, including digons
and all permitted nonadjacent letter repetitions.

For nonnegative block sizes `n_A,n_B,n_C,n_D`, the exact size is

    sum_(w in D) n_(w0)
        product_(i=1..3) [n_(wi)-1_(wi=w_(i-1))].             (1)

The product enforces precisely the three adjacent-letter inequalities.
All other coincidences of actual letters are allowed.

For four equal blocks of size `q`, the numbers of templates with zero,
one, and two equal adjacent block pairs are `23,28,6`, respectively. Thus

    gp(Ka(4q,4)) >= 57q^4-40q^3+6q^2.                      (2)

More usefully, take block sizes `(5q,5q,3q,3q)`. Expanding (1) gives

    gp(Ka(16q,4)) >= 14733q^4-2528q^3+94q^2,   q>=1.       (3)

Consequently

    lambda_4 >= 14733/65536 = 0.2248077392578125.

For every integer `m>=16`, use any `16 floor(m/16)` letters with those
block proportions. The original suffix/prefix distance formula is unchanged
by adding the unused alphabet letters, so the same subset is GP in
`Ka(m,4)`. Formula (3) with `q=floor(m/16)` is therefore a bound for every
such `m`. Alternatively, round the four optimal weights below to a partition
of all `m` letters and use the exact polynomial (1).

## 3. The leading weighted polynomial

Let `a,b,c,d>=0`, with `a+b+c+d=1`, be the four limiting block proportions.
The leading coefficient in (1) is

    F(a,b,c,d) = sum_(w in D) product_(i=0..3) p_(wi).

Its exact compact form is

    F = [1-(a^2+b^2+c^2+d^2)^2]/4
        - abcd - acd^2 - bc^2d.                             (4)

To verify this identity combinatorially, all primitive four-rotation orbits
on `A,B,C,D` number sixty. The dictionary contains one representative from
each except the three orbits represented by

    ADCB, ADCD, BCDC.

All rotations have the same product weight. The total probability of words
of period dividing two is `(a^2+b^2+c^2+d^2)^2`. Dividing the remaining
weight by four counts each primitive orbit once, and the three missing
orbit weights are exactly the final three monomials in (4). The missing
orbits and all coefficients are also independently checked from the literal
57-word list. This is a finite polynomial identity, not a numerical fit.

## 4. An exact compression of the four block weights

Put

    u=a+b,  v=c+d,  r=a-b,  s=c-d.

Thus `u+v=1`, and the balanced-within-pairs vector is
`(u/2,u/2,v/2,v/2)`. Direct expansion of (4) gives the sum-of-squares identity

    16 [F(u/2,u/2,v/2,v/2)-F(a,b,c,d)]
      = 2u^2 r^2 + (u-v)^2 s^2 + v^2(r-s)^2
        + r^4 + 2r^2s^2 + (rs+s^2)^2.                      (5)

Every term on the right is nonnegative. Therefore there is always a
nondecreasing compression to `a=b=x`, `c=d=y`, with `x+y=1/2`.
In fact equality in (5) forces `r=s=0`: the term `r^4` first forces `r=0`,
and then `(rs+s^2)^2=s^4` forces `s=0`. Thus every maximizer has the paired
equalities, including the possible boundary cases.

Substituting `x=1/2-y` in (4) leaves the single-variable quartic

    f(y)=3/16+y/2-9y^2/4+4y^3-3y^4,   0<=y<=1/2.          (6)

Its derivative is

    f'(y)=[1-9y+24y^2-24y^3]/2.

The polynomial in brackets has derivative

    -9+48y-72y^2 = -72(y-1/3)^2-1 < 0.

It is positive at zero and negative at one half. Hence there is a unique
maximizer `rho in (0,1/2)`, characterized exactly by

    24rho^3-24rho^2+9rho-1=0.                               (7)

Define

    beta = 3/16+rho/2-9rho^2/4+4rho^3-3rho^4.

The maximum weighted density of this **fixed** 57-word dictionary is
exactly `beta`. Numerically,

    rho  = 0.18673085336460038...,
    beta = 0.2248081152168827... .

The equalities (4)–(7), not the decimal approximations, certify this
optimization. The rational proportions in (3) have `y=3/16`; they already
give a density within `4*10^-7` of beta and have a simple all-integer count.

## 5. Consequence and precise remaining gap

Choose integer block sizes whose ratios tend to
`(1/2-rho,1/2-rho,rho,rho)`. The exact count (1), divided by `m^4`, tends
to beta. Every resulting set is original GP by Section 2. Therefore

    beta <= lambda_4 <= 182/729,

where the upper bound is proved in `../pair_color_bound/PROOF.md`.
The interval has width approximately `0.0248489492549966`.

This does not show that an extremal strict code has four blocks, that the
classical dictionary is globally optimal after weighting, or that an
original GP set has this form. The sum-of-squares compression optimizes
only the explicit polynomial (4). The exact limit and all finite original
GP values remain undetermined.

## 6. Independent verification and provenance

The original 57 words were visually transcribed from the printed source;
its PDF is a source document, not a new project artifact or claimed
recomputed maximum. A separate construction reviewer checks all window
occurrences and rebuilds original shift/append adjacency and BFS distances
for fixed lifts. A different reviewer, who did not participate in discovering
the weights, reconstructs the rotation orbits and checks (3)–(7) by exact
arithmetic, including deliberate corruptions of inputs and coefficients.

These are written all-parameter arguments plus independent finite semantic
and algebraic checks. They are not a complete Lean formalization, a claim
of successful Lean compilation, external human peer review, or a historical
priority certification for either the dictionary or its uses.
