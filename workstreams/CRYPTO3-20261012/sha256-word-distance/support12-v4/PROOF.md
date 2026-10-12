# A stronger valuation ceiling for the irregular SHA-256 support core

**Complete written finite proof with author replay; independent-agent
acceptance is recorded separately.** This note improves a necessary
condition from `v2(D)<=20` to `v2(D)<=18`. It excludes no entire support,
does not improve the global distance lower bound 13, and supplies no
actual message pair or Lean formalization.

## Statement and exact object

Use the real 32-bit SHA-256 expansion

    W_t = g(W_(t-2)) + W_(t-7) + f(W_(t-15)) + W_(t-16), 16<=t<64,

where `f=ROTR7 xor ROTR18 xor SHR3`, `g=ROTR17 xor ROTR19 xor SHR10`.
All sums and differences of words are modulo `N=2^32`, and bit 0 is
least significant. Both initial blocks are arbitrary. Put
`d_i=W'_i-W_i`, `F_i=f(W'_i)-f(W_i)`, `G_i=g(W'_i)-g(W_i)`.
For a position outside the exact support all three differences vanish.

For each of these frozen supports, the indicated nonzero D satisfies
**v2(D)<=18**:

| Support index | Common difference D | Third difference -D |
|---|---|---|
| 12 | d18=d34 | d43 |
| 6 | d19=d35 | d44 |
| 7 | d21=d37 | d46 |
| 13 | d20=d36 | d45 |

The frozen support file is `../supports-v2.json`, SHA256
`02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf`.
It is inherited from CRYPTO2 commit
`80b71cb3b6a67c8f8aae80d9cd8b6ed87d74bd51`. No support enumeration
is repeated here.

## 1. Original equations imply the actual three-pair core

Write `E_t=d_t-G_(t-2)-d_(t-7)-F_(t-15)-d_(t-16)`. For support 12
the following integer combinations of the original equations give
exactly the displayed relations. No division by a nonunit occurs.

| Relation | Original-row combination |
|---|---|
| d18-d11=0 | E18 |
| d34-d18=0 | E34 |
| d43+d34=0 | -E50 |
| F34-F18=0 | E33-E42-E49 |
| F43-F18=0 | E33-E42-E58 |
| G34-G18-2d18=0 | E20+2E27-2E18-E36-E29 |
| G34-G43-d18=0 | -E36+E45+E27-E18 |

Consequently the actual word pairs at `x=18,y=34,r=43` satisfy

    d_x=d_y=D!=0, d_r=-D,
    F_x=F_y=F_r,
    G_y-G_x=2D, G_y-G_r=D.                         (1)

The same combinations shift by `+1,+3,+2` for supports `6,7,13`.
The checker reconstructs the lag set and zero pattern in each original
row, and checks all 28 combinations, including their actual t boundaries.
In particular the equality with the third sigma0 derivative uses t58
for support 12; it must not be dropped.

## 2. Width reduction covers the entire v2(D)>=19 stratum

Assume `2^19` divides D. Each of the three actual input pairs agrees
in its low 19 bits, including the pair whose difference is -D. In g,
an output bit `22<=j<=31` depends only on input bits `j-15,j-13`,
which lie below 19; its SHR10 term is absent. Thus the two g images
agree in output bits 22 through 31.

Let q_x,q_y,q_r be the ordinary signed integer g-image differences.
Then each satisfies `|q_i|<2^22`. Set `A=q_y-q_r` and `B=q_y-q_x`.
Equation (1) implies `A=D mod N`, `B=2D mod N`, while
`|A|,|B|<2^23`. Hence `B-2A` is a multiple of N of absolute value
less than `3*2^23<N`, so it is zero. Therefore `|A|=|B|/2<2^22`.
Since D is active, A is a nonzero multiple of `2^19`. It follows that

    D = +/- q*2^19 mod N,  q in {1,2,3,4,5,6,7}.            (2)

Swapping the primed and unprimed member of **all three** pairs negates
every derivative and converts (1) to itself with D replaced by -D.
It suffices to exclude the seven positive representatives. There are
no omitted half-word or wraparound cases: (2) was deduced modulo N
from actual integer image differences.

## 3. Exact finite exclusion of the seven representatives

`CERTIFICATE.json` and `check.py` give a finite, definition-based proof.
The complete checking argument is stated here so that the program's
empty-branch result has a precise mathematical interpretation.

### Input mask exhaustivity

For fixed D, let `k=v2(D)`. Every input pair has the form
`(x,x+D)` and shares its low k bits. Enumerate all `2^(32-k)` high
quotients a. Its exact XOR mask is

    alpha = (a xor ((a+D/2^k) mod 2^(32-k))) << k.

For each mask, the checker extracts the coordinates constant across
its quotient class. It checks that every quotient satisfies those
constraints and that the class cardinality is exactly that of the
resulting binary cube. Thus the constraints describe the *whole*
class, rather than a merely sufficient subset. The unconstrained low
bits remain arbitrary. For the third pair the quotient enumeration
uses -D modulo N. The top input bit is never required to stop a carry;
addition wrapping past bit 31 is included by construction.

### Output carry exhaustivity

For a binary linear word map L, set beta=L(alpha). At output bit j,
if the unprimed bit is u, the actual derivative bit contribution is
`(u xor beta_j)-u`. For two pairs, a requested derivative difference
`L(right')-L(right)-L(left')+L(left)=C mod N` is exactly the integer
carry recurrence

    carry_j + ((v xor beta_right,j)-v)
            - ((u xor beta_left,j)-u) - C_j = 2*carry_(j+1),
    carry_0=0.                                             (3)

The checker enumerates the at most four choices of the active u,v
bits at each step, groups them by their next carry, and computes every
binary affine equation constant on each group. It then checks by the
whole Boolean truth table that these equations describe exactly that
group. Groups that cannot be described exactly as such an affine
space are rejected by the checker as an implementation failure, not
silently approximated. Every actual group here passes that check.
The final carry is **unrestricted**: this is equality modulo N, not
ordinary equality or a no-wrap assumption.

Each output bit u or v is the exact XOR of original input bits in the
specified sigma output row. All rows for a word act on the same 32
input bits. Thus the f and g derivatives of a pair are never chosen
independently. Original binary equations are accumulated through (3).
Low-pivot Gaussian elimination is valid over F2; a rejected branch
comes with an explicit XOR of its original binary rows giving `0=1`.
The certificate stores 512 distinct such row receipts. The checker
reconstructs all branches and their receipts, then checks each receipt
again by direct XOR. Arithmetic branches without a valid next carry
are empty by their complete truth table.

### Complete case counts

For each positive D, first impose the two-pair conditions
`F_y=F_x` and `G_y-G_x=2D`. These suffice to exclude six values.
For q=5 retain every surviving binary branch, then enumerate all
third-pair masks and impose `F_r=F_y`, `G_y-G_r=D`.

| q | D (hex) | Input masks for each of x,y | Mask pairs | Surviving twin branches | Third masks checked | Final branches |
|---:|---|---:|---:|---:|---:|---:|
| 1 | 00080000 | 13 | 169 | 0 | 0 | 0 |
| 2 | 00100000 | 12 | 144 | 0 | 0 | 0 |
| 3 | 00180000 | 23 | 529 | 0 | 0 | 0 |
| 4 | 00200000 | 11 | 121 | 0 | 0 | 0 |
| 5 | 00280000 | 32 | 1024 | 1 | 32 | 0 |
| 6 | 00300000 | 21 | 441 | 0 | 0 | 0 |
| 7 | 00380000 | 31 | 961 | 0 | 0 | 0 |

There are exactly 3,389 complete two-mask cases. All are listed in
the certificate. The only surviving twin branch has
`alpha_x=alpha_y=ffd80000`; all 32 third-pair carry masks are listed.
Every final branch is empty. The reconstruction checks 1,419,762
Boolean carry edges and 3,618 binary contradictions, with the latter
deduplicated to 512 row receipts. These counts are replay evidence,
not a substitute for exhaustive branching and exact row checks.

By input exhaustivity, (3), and exact binary elimination, no solution
of (1) exists for any representative in (2). This contradicts the
assumption `v2(D)>=19` and proves the stated ceiling `v2(D)<=18`.

## 4. A positive boundary control explains the extra third pair

At D=`00280000`, the four words

    x=ffd80000, x'=00000000, y=ffd80040, y'=00000040

satisfy the full twin core exactly. Their common F is `e1fb700a`,
with `G_x=ffc069e9`, `G_y=001069e9`; their G gap is `00500000=2D`.
The checker directly evaluates these words using the original bit
definitions. This is a genuine counterexample to extending the twin
core alone to the new ceiling. It is not a message-pair witness.
The third actual pair and both its F and G relations in (1) are
essential to the q=5 exclusion.

## Reproduction and scope

From the repository root:

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-v4/check.py
```

Only the Python standard library is required. `check.py` imports none
of `explore.py`, `explore_triple.py`, or the old solver programs. It
reconstructs the certificate in full from the bit definitions before
comparison. Those two discovery programs and their runs are retained
as supplementary evidence; none is a logical premise of the proof.
The separately written checker is by the same author. It must not be
described as an independent-agent acceptance before that receipt exists.

This is a necessary local restriction on any actual 13-support pair.
The 13 active pairs and genuine base-schedule interpolation remain
unresolved; solving a local pair system would not discharge them.
No compression collision, preimage attack, historical-priority claim,
formal assistant theorem, DOI, Release, or main-branch integration is
supplied by this note.
