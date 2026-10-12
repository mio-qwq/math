# Pre-author freeze: fixed-`D` selected three-pair core

Date: 2026-10-12 UTC.

This note was written before reading any byte in
`support12-v16-core-batch-v9/`.  The theorem statement supplied by the
coordinator is the only author-batch information used here.

All word arithmetic below is in `Z/(2^32)`.  Put

```
f = sigma0,   g = sigma1,
F_D(u) = f(u + D) - f(u),
G_D(u) = g(u + D) - g(u).
```

For the directed `+D` pair based at `x`, define its first image coordinate
and the shifted second coordinate by

```
A = F_D(x),
T = G_D(x) + D.
```

The same-orientation twin based at `y` has the same first coordinate and its
second derivative is two increments above `G_D(x)`.  Thus

```
F_D(y) = A,
G_D(y) = T + D.
```

Reversing a directed pair negates both raw derivatives.  The third selected
forward-`D` member therefore has target coordinates

```
F_D(z) = -A,
G_D(z) = -T.
```

Consequently the independently frozen exact system is

```
A = F_D(x),             T = G_D(x) + D,
F_D(y) = A,             G_D(y) = T + D,
F_D(z) = -A,            G_D(z) = -T.
```

Equivalently, after eliminating `A,T`,

```
F_D(y) = F_D(x),
G_D(y) = G_D(x) + 2D,
F_D(z) = -F_D(x),
G_D(z) = -G_D(x) - D.
```

The signs are not interchangeable: reversing `D` swaps each pair's endpoints
and maps `F_D(u),G_D(u)` to the negatives of the corresponding derivatives
at the shifted base.  The audit will exercise this identity explicitly.

## Independent reconstruction fixed before comparison

For each `D = q*2^16`, `q in {5,13,21,23,25,27}`, construct Boolean words
for `x,y,z`, their exact modular `+D` successors, the two SHA-256 small-sigma
images, and modular derivative words.  Encode rotations/shifts from the
standard definitions, and encode addition/subtraction with fresh ripple
carry variables.  Assert the four eliminated equations above.

The independent implementation will:

1. emit normalized DIMACS from a locally written clause builder;
2. parse DIMACS independently of the builder and validate headers/literals;
3. check deletion-free DRUP by reverse-watch-free unit propagation, requiring
   every added clause to be RUP and the final empty clause to be present;
4. compare clause multisets, variable/clause counts and SHA-256 digests against
   the author objects only after this freeze;
5. reject altered targets (`+D` versus `-D`/reversed orientation), one removed
   base clause, one changed proof literal, a truncated proof, and a missing
   empty clause; and
6. run satisfiable near-miss controls by relaxing one of the two third-image
   coordinates, retaining concrete direct-word witnesses when available.

Scope frozen here is only these six fixed residues and this selected
three-pair core.  Even acceptance for every residue does not by itself prove
all `v2(D)=16`, full support completion, a message pair, or distance 14.
