# Independent review: fixed `D=000f0000` three-pair core

## Decision

**ACCEPT**, limited exactly to the following fixed-`D` local statement:

> For `D=0x000f0000`, there are no 32-bit words `x,y,z` such that, with
> `A=F_D(x)` and `T=G_D(x)+D`, one has
> `F_D(y)=A`, `G_D(y)=T+D`, `F_D(z)=-A`, and `G_D(z)=-T` modulo `2^32`.

No conclusion is accepted here about full support 12, a message pair, or
distance 14.  The review decision also makes no broader factor-graph claim.

## Blind pre-audit result

Before opening the author generator, checker, CNF, DRUP, certificate, proof,
or run record, I substituted out `A,T` and independently encoded

```text
F_D(y) = F_D(x),
G_D(y) = G_D(x) + 2D,
F_D(z) + F_D(x) = 0,
G_D(z) + G_D(x) + D = 0.
```

Here `F_D` and `G_D` use the actual SHA-256 small sigmas and all additions
are ripple-carry addition modulo `2^32`.  The resulting independently
bit-blasted formula has 2,593 variables, 10,817 clauses, and SHA-256
`4cda87765cc2835ff78ce0bd61f0482d78c0ffcdab5941156a09b8ce254bf55a`.

The first independent SciPy/HiGHS MILP attempt reached its 300-second limit
with status `UNKNOWN`.  That formula was then solved directly by CaDiCaL
2.1.2, which returned `UNSATISFIABLE` (exit 20) after 3,324 conflicts and
0.07 seconds.  This result and formulation were frozen in `PREAUDIT.md`
before author-artifact inspection.

## Author CNF reconstruction

`audit.py` does not import the author code.  It independently reconstructs
the three input words, `A`, the sigma rows, the constant and word adders, and
all endpoint equalities from local truth tables.  Its variable allocation and
clause sequence match the author's `fourpair.cnf` byte-for-semantics exactly:

```text
variables  1259
clauses    9683
SHA-256    f16a99ee064edc1d95e7a248af07262bfd2ddd4c605dd5a1ec8d7587aa727a08
```

Despite its historical filename, the CNF contains only the selected
three-pair core under review; it contains no reciprocal word `u`.

All eight entries in the author's `SHA256.json` match the live bytes, and no
author file other than the manifest itself is omitted from that manifest.
The author's standard-library checker independently reproduced the same CNF
and returned `PASS`; CaDiCaL separately returned `UNSATISFIABLE` on the author
CNF.

## Deletion-free DRUP audit

The proof parser found 3,951 additions, no deletion line, no empty clause
before the last addition, and a final empty clause.  Proof SHA-256:

```text
1256df91a4d7d82865b39743943450f0adfdb2875c98cb55c4b1d8c1c68a7210
```

An independently implemented two-watched-literal unit-propagation checker
accepted every addition as RUP against the monotonically growing database,
including the final empty clause.  It rejected a control with literal 6 of
the first proof addition flipped.  Removing the final empty clause is also
rejected by the required proof-termination condition.

## Near-miss controls

Direct 32-bit evaluation independently confirms the author's witness satisfies
the five defining/equational conditions preceding the last one and fails only
`G_D(z)=-T`:

```text
x=5ff2e1be  y=5ff2e1a6  z=9ff20041
A=398179ec  T=a000e3b9
G_D(z)=5ff1e3b9 != 5fff1c47=-T
```

The reviewer CNF with the complete last equation omitted is independently SAT
(10,785 clauses, SHA-256
`64cd764ccdc9e7c9fc036f0bd4b2e4a3c256246b219a26682c80dfca5da8b70f`).
CaDiCaL supplied a different model, also checked by direct word arithmetic:

```text
x=3ffeb7ff  y=3ffeb7e7  z=3ff28bdf
A=46fe9924  T=e00fc3bd
G_D(z)=dfe8c3bd != 1ff03c43=-T
```

Thus the encoding is not contradictory before the decisive final equation.

## Replay

Run from the repository root:

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-d000f-review-v9/independent.py --emit-only
/workspace/scratch/668a9b2a5e45/gp2-private-deps/lean-4.34.1-linux/bin/cadical \
  workstreams/CRYPTO3-20261012/sha256-word-distance/support12-d000f-review-v9/independent.cnf
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-d000f-review-v9/audit.py
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-d000f-v9/check.py
```

Environment used: Python 3.12.14; CaDiCaL 2.1.2 compiled by clang++ 22.1.4;
Linux x86_64 kernel 6.18.44.
