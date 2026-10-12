# A fixed-residue joint-image obstruction at valuation 16

All arithmetic below is modulo `2^32` unless a smaller modulus is stated.
Write

```text
f = ROTR7 xor ROTR18 xor SHR3,
g = ROTR17 xor ROTR19 xor SHR10,
F_D(x) = f(x+D)-f(x),
G_D(x) = g(x+D)-g(x).
```

## Theorem

For `D=0x00010000`, there are no two 32-bit words `x,y` satisfying

```text
F_D(x) = F_D(y)                         (mod 2^32),
G_D(y) - G_D(x) = 2D                    (mod 2^31).
```

Consequently there is no `A,c` for which both

```text
c in B_(D,A),   c+2D in B_(D,A),
```

where `B_(D,A)={G_D(x):F_D(x)=A}`.  Thus the first two memberships in
the accepted v7 joint-image criterion already fail for this numerical
`D`; the third pair and reciprocal edge cannot restore feasibility.

The reversed orientation `D=0xffff0000` is excluded as well.  Reverse
both directed pairs: their `f` derivatives are both negated, and their
`g`-derivative gap becomes the required gap for `+0x00010000`.

This excludes only these two signed residues.  It does **not** exclude
all differences of exact valuation 16, any of the six full supports, or
any 16-word message pair.

## Exhaustive finite reduction

Adding `D=2^16` leaves the low 16 input bits fixed.  For each of the
`2^16` upper-half values `q`, the checker evaluates exactly

```text
alpha = (q<<16) xor ((q<<16)+D mod 2^32).
```

There are 16 distinct XOR masks.  For every mask the corresponding set
of upper-half words is checked exhaustively to be the affine cube encoded
by its constant coordinates.  The lower 16 bits remain free Boolean
variables.  Hence the 16 by 16 mask-pair traversal covers every possible
ordered pair `(x,y)`, rather than sampling words.

For each mask pair, each bit of the two modular derivative equations is
expanded from the original `f` or `g` bit row and the incoming integer
carry.  At most two Boolean row values occur at one step, so its full truth
table is enumerated.  Allowed truth-table values are recompressed into
affine equations only after the checker verifies that the reconstructed
set is exact.  Gaussian insertion either retains the affine branch or
returns an explicit XOR of original equations equal to `0=1`; every such
receipt is checked directly.

After all 32 bits of `F_D(x)=F_D(y)`, exactly 414 affine leaves remain.
After imposing the `g` gap through bits 0--29, exactly 20 leaves remain.
They have the following complete frontier:

| common input XOR mask | bit 30 of `g(mask)` | incoming carries | leaves |
|---|---:|---:|---:|
| `07ff0000` | 1 | -1, +1 | 2 each |
| `0fff0000` | 1 | -1, +1 | 2 each |
| `1fff0000` | 1 | -1, +1 | 2 each |
| `3fff0000` | 1 | -1, +1 | 2 each |
| `7fff0000` | 1 | -1, +1 | 2 each |

At bit 30 both derivative XOR bits are 1.  A toggled output bit contributes
`(u xor 1)-u = 1-2u`, which is odd.  The difference of the two derivative
contributions is therefore even.  The target `2D=0x00020000` has bit 30
zero, while every surviving incoming carry is odd.  The bit equation has
odd left side and cannot produce a next carry.  All 20 leaves die, proving
the theorem modulo `2^31`; full 32-bit equality is unnecessary.

## Sharp boundary control

The following actual words satisfy the full `f` equality and the `g` gap
through bit 29:

```text
x  = abff5552,  x+D = ac005552,
y  = 03ff0000,  y+D = 04000000,
F_D(x)=F_D(y)=400fe201,
G_D(y)-G_D(x)=c0020000.
```

The last gap is `0x00020000` modulo `2^30`, but `0x40020000` modulo
`2^31`.  Thus bit 30 is essential.  Here `v2(F_D(x))=0`, one of the
allowed v7 reciprocal-signature values, so the obstruction is genuinely
stronger than merely rejecting an already-forbidden valuation signature
for this fixed `D`.

## Replay and status

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-image-v8/check.py --negative
```

Only the Python standard library is used.  `CERTIFICATE.json` freezes the
frontier and boundary control; the checker reconstructs and compares them.
It also checks damaged witnesses plus three weakening controls: dropping
the decisive `g` bit leaves 20 branches, dropping one `f` bit leaves 20,
and replacing the nonzero gap by zero leaves 58.

This is a complete author finite proof for one fixed residue, pending the
separate independent-review receipt.  It is not Lean formalization, a
historical originality claim, a full support exclusion, distance at least
14, or a distance-13 message construction.

