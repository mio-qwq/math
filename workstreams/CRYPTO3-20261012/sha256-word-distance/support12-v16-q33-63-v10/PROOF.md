# Exact valuation-16 classification for odd q=33..63

All arithmetic is modulo `2^32`.  Put `D=q*2^16`,
`F_D(x)=sigma0(x+D)-sigma0(x)` and
`G_D(x)=sigma1(x+D)-sigma1(x)`.  The selected twin condition is

```text
F_D(x)=F_D(y),   G_D(y)-G_D(x)=2D.
```

The exact affine/carry proof from the frozen q=1..31 classifier is reused
byte-for-byte (SHA-256
`a58fc79b82edce8c82d8838a0d197bdd77b9dc42a4d91c4250b0d3ae4d6d1d60`).
For every odd q from 33 through 63, `check.py` exhausts all upper-half
addition-XOR classes, proves each class is an exact affine cube, propagates
all 32 modular carry bits for both small sigmas, and checks every stored
linear contradiction receipt.  This is a complete cover, not sampling.

| q | input classes | F leaves | full twin leaves |
|---:|---:|---:|---:|
|33|65|11,317|0|
|35|97|54,829|0|
|37|118|59,524|4|
|39|107|49,761|2|
|41|117|50,677|2|
|43|138|68,938|4|
|45|127|64,609|0|
|47|95|16,817|0|
|49|94|16,934|0|
|51|125|55,589|0|
|53|135|60,083|0|
|55|114|45,998|0|
|57|103|45,295|0|
|59|113|44,273|0|
|61|92|39,578|0|
|63|61|12,035|0|

Thus the twin condition is already impossible for twelve q values.  The
remaining `q={37,39,41,43}` have twelve directly evaluated full-word local
fixtures.  Their existence is a useful negative result: the old top-bit
obstruction is not uniform.  The separate exact three-pair package excludes
the stronger core for every q in this window.

Pair reversal uses
`F_{-D}(w+D)=-F_D(w)` and `G_{-D}(w+D)=-G_D(w)`, so the classification for
negative D is identical.  This theorem concerns local word pairs only.  It
does not assert feasibility or infeasibility of the complete support, a
message pair, distance 13, or a lower bound of 14.  No Lean formalisation is
claimed.

Replay:

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-v16-q33-63-v10/check.py --jobs 4 --negative
```
