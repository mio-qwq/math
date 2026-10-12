# Independent result frozen before author-artifact inspection

Date: 2026-10-12 UTC.

At the time this note was frozen I had not opened or executed the author's
`support12-d000f-v9` generator, checker, CNF, DRUP, certificate, proof, or run
record.  An early repository-wide filename search accidentally displayed a
few matching author-path lines, including the theorem statement already given
in the review assignment, but no author encoding or evidence was used below.

## Independent formulation

All words and arithmetic are in `Z/(2^32)`.  With the FIPS SHA-256 small
sigmas

```text
sigma0(w) = ROTR7(w) xor ROTR18(w) xor SHR3(w),
sigma1(w) = ROTR17(w) xor ROTR19(w) xor SHR10(w),
F_D(w) = sigma0(w+D) - sigma0(w),
G_D(w) = sigma1(w+D) - sigma1(w),
D = 0x000f0000,
```

substitution of `A=F_D(x)` and `T=G_D(x)+D` gives the equivalent four word
identities

```text
F_D(y) = F_D(x),
G_D(y) = G_D(x) + 2D,
F_D(z) + F_D(x) = 0,
G_D(z) + G_D(x) + D = 0.
```

`independent.py` reconstructs these identities with little-endian Boolean
wires, exact Tseitin truth tables for XOR and majority, and ripple-carry
addition modulo `2^32`.  Its exact DIMACS has 2,593 variables and 10,817
clauses.  SHA-256:

```text
independent.py   d521119c5c739a9a02abd15aa4882de35e8876acfa125cc2d57b6a98bb5bccfa
independent.cnf  4cda87765cc2835ff78ce0bd61f0482d78c0ffcdab5941156a09b8ce254bf55a
```

## Independent result

CaDiCaL 2.1.2 returned `UNSATISFIABLE` (exit 20) on `independent.cnf` in
0.07 seconds, after 3,324 conflicts.  Therefore my pre-audit result is:

> There are no 32-bit `x,y,z` satisfying the fixed-`D` selected three-pair
> core above.

This conclusion is only for that fixed local core.

Command:

```sh
/workspace/scratch/668a9b2a5e45/gp2-private-deps/lean-4.34.1-linux/bin/cadical \
  workstreams/CRYPTO3-20261012/sha256-word-distance/support12-d000f-review-v9/independent.cnf
```

Environment: Python 3.12.14; CaDiCaL 2.1.2, compiled by clang++ 22.1.4;
Linux x86_64 kernel 6.18.44.

## Independent weakening control

Dropping only the complete final identity `G_D(z)=-T` gives a 2,593-variable,
10,785-clause SAT instance (`near_miss.cnf`, SHA-256
`64cd764ccdc9e7c9fc036f0bd4b2e4a3c256246b219a26682c80dfca5da8b70f`).
CaDiCaL returned the following model inputs, independently checked with direct
32-bit Python evaluation:

```text
x = 3ffeb7ff, y = 3ffeb7e7, z = 3ff28bdf
A = 46fe9924, T = e00fc3bd
F_D(y) = 46fe9924 = A
G_D(y) = e01ec3bd = T+D
F_D(z) = b90166dc = -A
G_D(z) = dfe8c3bd != 1ff03c43 = -T
```

Thus the circuit is not spuriously inconsistent before imposing the final
equation.
