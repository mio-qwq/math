# The valuation-17 irregular SHA-256 support core is impossible

**Complete written finite proof with author replay; independent-agent
acceptance is separate.** This new result, with the unchanged accepted
v4/v5 support bridges, gives the necessary ceiling **v2(D)<=16** for
supports 12,6,7,13. No complete support is excluded, the global distance
lower bound remains 13, and no actual message blocks are supplied.

## 1. The exact three-pair object

For actual 32-bit ordered word pairs X,Y,R, let d be the modular input
difference, F the actual sigma0 derivative and G the actual sigma1
derivative. Both sigmas are always evaluated on the same members of
each pair. All equations below hold modulo N=2^32:

    d(X)=d(Y)=D!=0, d(R)=-D,
    F(X)=F(Y)=F(R),
    G(Y)-G(X)=2D, G(Y)-G(R)=D.                         (1)

The sigma bit definitions are

    f=ROTR7 xor ROTR18 xor SHR3,
    g=ROTR17 xor ROTR19 xor SHR10.

The original recurrence bridges, exact zero patterns, and pair
orientations for supports 12,6,7,13 are already proved in the unchanged
`../support12-v4/PROOF.md`. The common D is respectively `d18=d34`,
`d19=d35`, `d21=d37`, `d20=d36`. The accepted v5 proof excludes all
v2(D)>=18. This new stage therefore considers exactly v2(D)=17.

## 2. A new width reduction modulo 2^31

This is a new mathematical lemma, not an automatic consequence of an
older acceptance receipt. Put M=2^31 and suppose v2(D)=17. Every one
of the three pairs agrees in its low 17 input bits. In g the output
bits 22..29 depend only on input bits `j-15,j-13`, all below17, so
those output bits agree.

Output bit30 depends only on input bits15 and17. Input bit15 agrees,
while bit17 necessarily flips: adding an odd multiple of 2^17 toggles
it. The same statement holds for -D. Therefore bit30's contribution
to each ordinary g-output difference is either +2^30 or -2^30, and
both are 2^30 modulo M. Output bit31 contributes a multiple of M.
Consequently, for each of the three pairs,

    G_i = 2^30 + q_i (mod M), |q_i|<2^22,               (2)

where q_i is the ordinary integer difference between the two low22-bit
g images. No bound is asserted on the full ordinary g derivative.

Set A=q_Y-q_R and B=q_Y-q_X. The common quarter-word in (2) cancels,
and (1) reduced modulo M yields

    A=D (mod M), B=2D (mod M), |A|,|B|<2^23.

Thus B-2A is a multiple of M of absolute value below
`3*2^23<M`. It must be zero. It follows that |A|<2^22. The residue
D has valuation17, so A is a nonzero odd multiple of 2^17. Hence

    D = +/-q*2^17 + h*2^31 (mod N),
    q in {1,3,...,31}, h in {0,1}.                     (3)

Both lifts h=0 and h=1 are necessary because the width argument used
M, not N. Simultaneously reversing all three pairs negates every d,F,G
in (1). Since `-2^31=2^31 mod N`, this maps each negative signed q
to its positive representative with the same h. Therefore the 32
positive representatives in (3) exhaust the original problem. The
checker reconstructs every bit-row identity and checks the 64 signed
residue coverage and exact valuation of all 32 positive values.

Crucially, (3) only screens D. Every finite case below still imposes
**all four derivative equations modulo N**, including bit31 and the
full constant D in `G(Y)-G(R)=D`. None uses a mod-M relaxation of (1).

## 3. Full finite exclusion at the original modulus

The definition-based proof method is the same exact high-quotient,
Boolean carry and binary-row method already proved in the frozen v4
note. The author extension explicitly hash-pins that kernel before
reusing it; it does not import or assume any SMT answer.

For each representative, enumerate all 2^15 high input quotients of
the pairs with differences D and -D. Every quotient's exact input
XOR mask is computed with addition modulo N. Each mask class is
verified to equal its full binary cube, leaving lower17 bits free.
Thus neither wrapping additions nor top input bits are omitted.

For each actual output mask beta=L(alpha), a changed output bit u
contributes `(u xor beta_j)-u` to the ordinary derivative. Apply all
Boolean assignments and their integer next carries to the equations
`F(Y)-F(X)=0`, `G(Y)-G(X)=2D`. Accumulate their exact affine equations
on the same original input bits. For every surviving branch and every
negative-difference mask of R, append `F(R)-F(Y)=0` and
`G(Y)-G(R)=D`. Final carries are unrestricted modulo N. Each carry
truth table is checked to equal its affine compression. Every linear
rejection stores an XOR of its original rows giving `0=1`.

Each mask case and every surviving branch are included in the following
complete coverage. Mask counts coincide between h=0 and h=1, but both
different input masks and full constants are checked separately.

| q | Masks per input pair, each h | Total two-mask cases, both h | Twin branches h=0 | Twin branches h=1 | Third masks tested, both h | Final branches |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 15 | 450 | 0 | 0 | 0 | 0 |
| 3 | 27 | 1458 | 0 | 3 | 81 | 0 |
| 5 | 38 | 2888 | 3 | 6 | 342 | 0 |
| 7 | 37 | 2738 | 0 | 0 | 0 | 0 |
| 9 | 47 | 4418 | 0 | 0 | 0 | 0 |
| 11 | 58 | 6728 | 0 | 27 | 1566 | 0 |
| 13 | 57 | 6498 | 2 | 29 | 1767 | 0 |
| 15 | 45 | 4050 | 4 | 60 | 2880 | 0 |
| 17 | 54 | 5832 | 0 | 8 | 432 | 0 |
| 19 | 75 | 11250 | 0 | 0 | 0 | 0 |
| 21 | 85 | 14450 | 0 | 0 | 0 | 0 |
| 23 | 74 | 10952 | 0 | 0 | 0 | 0 |
| 25 | 73 | 10658 | 0 | 0 | 0 | 0 |
| 27 | 83 | 13778 | 0 | 0 | 0 | 0 |
| 29 | 72 | 10368 | 0 | 0 | 0 | 0 |
| 31 | 51 | 5202 | 0 | 0 | 0 | 0 |

The 32 certificates contain all 111,718 two-mask cases and all 7,068
third-mask tests. There are 142 surviving twin branches, so the third
pair is not removed. Complete reconstruction uses 11,488,260 Boolean
carry edges and detects 172,481 binary conflicts, represented by
10,914 distinct XOR row receipts when deduplicated within each fixed-D
case. The counts are replay evidence; exhaustive masks, truth tables,
carry branches and actual row XORs supply the finite proof.

Every final branch is empty. It follows that (1) is impossible for
v2(D)=17. Combined with the unchanged v5 exclusion of all higher
valuations and the original support bridges, this proves the stated
necessary ceiling v2(D)<=16.

## 4. Evidence recovery and accurate scope

Each `CASE-q-h.json.xz` contains the complete JSON proof case, including
the exact masks, binary row receipts and all third-pair branches. Its
raw JSON SHA256 and compressed SHA256 are in `BUILD-q-h.json` and
the full replay receipt. The raw JSON totals 20,167,680 bytes and is
stored losslessly in 360,716 compressed bytes. No proof datum was
removed to obtain this size.

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-boundary-v6/check.py
```

Only the Python standard library is needed. The checker decodes each
compressed case, reconstructs it fully from original high quotients
and bit rows, compares every datum, and directly XORs every contradiction
receipt. `--q Q --h H` replays one original-modulus case. The `--build`
mode records discovery construction and is not required for replay.
Every case's original construction had a fixed 55-second process
budget; actual times were below 5.76 seconds, with no extension or
failed case. SMT UNSAT observations are not proof premises.

`AUTHOR-RECEIPT.json` and `manifest.json` bind source versions, older
dependencies, actual commands, checks and theorem scope. This author
extension must not be called independent-agent acceptance before a
separately frozen review receipt exists. The new width lemma also needs
that review; the prior <=17 receipt does not certify it by implication.

No fourth pair is used here. This neither proves the remaining low
valuation triples exist nor excludes an entire 13-word support.
Independently chosen active pairs still require a full active-pair
assignment and genuine base-schedule completion before one can claim
two actual messages. No Lean, historical-priority, SHA collision,
preimage attack, DOI, Release, or main-branch integration is asserted.
