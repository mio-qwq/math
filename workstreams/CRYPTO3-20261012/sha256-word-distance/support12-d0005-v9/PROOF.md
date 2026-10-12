# Fixed `D=0x00050000`: corrected fixture and two finite obstructions

**Status:** complete author-side finite certificates, with a standard-library
RUP checker.  Independent AI review is still separate.  This note neither
excludes every branch at this `D` nor constructs or excludes a message pair.

All arithmetic below is in `R=Z/(2^32)`.  Put

```
f(x)=ROTR7(x) xor ROTR18(x) xor SHR3(x),
g(x)=ROTR17(x) xor ROTR19(x) xor SHR10(x),
(d,F,G)(u,v)=(v-u, f(v)-f(u), g(v)-g(u)).
```

Use the constants

```
D = 00050000,  A = 40406e02,  T = 1ffd913e.
```

## 1. The supplied three positive pairs do not form the three-pair core

Direct evaluation from the definitions gives

| name | `u` | `v` | `d` | `F` | `G` |
|---|---|---|---|---|---|
| X | `0ffb000a` | `1000000a` | `D` | `A` | `1ff8913e` |
| Y | `0ffb0002` | `10000002` | `D` | `A` | `2002913e` |
| Q | `0ffb000e` | `1000000e` | `D` | `A` | `T` |

The numerical gaps are indeed

```
G(Y)-G(X)=2D,   G(Y)-G(Q)=D.
```

But the support-12 factor table needs its third oriented pair to have

```
(d,F,G)=(-D,+A,+T).
```

Reversing Q negates *all three* modular derivatives and instead gives

```
(-D,-A,-T)=(fffb0000,bfbf91fe,e0026ec2).
```

Thus X and Y are a valid twin candidate, but the claimed completion by Q
has an orientation/sign error.  Equivalently, a correct positive-orientation
third-image point would have to be

```
(D,-A,-T)=(00050000,bfbf91fe,e0026ec2).              (1)
```

## 2. Certified absence of the correct third-image point

`third_image.cnf` encodes an arbitrary 32-bit word x and exactly the three
equations

```
y  = x + D,
f(y) = f(x) - A,
g(y) = g(x) - T.                                     (2)
```

The additions are bit-exact ripple additions modulo `2^32`; overflow is
discarded only after bit 31.  Each full-adder relation is encoded by one
clause for every falsifying truth-table row.  Each output bit of f and g is
encoded by its original two rotations, shift and XOR parity relation.

The CNF has 355 variables and 2,203 clauses.  `third_image.drup` contains
7,662 added clauses and ends with the empty clause.  The stdlib-only checker
rebuilds (2) independently, requires exact clause equality, and checks every
proof addition by reverse unit propagation.  Hence (1) is not in the actual
joint derivative image.  In particular, this exact X/Y fixture cannot be
completed to the selected three-pair core.

## 3. Certified absence of the reciprocal sigma0 edge at this A

The fourth selected support-12 pair requires the reciprocal edge

```
D in R_A = { f(x+A)-f(x) : x in R }.                  (3)
```

`reciprocal.cnf` encodes

```
y = x + A,   f(y) = f(x) + D.                        (4)
```

It has 226 variables and 1,322 clauses.  `reciprocal.drup` contains 1,810
added clauses and ends with the empty clause.  The same independent rebuild
and RUP verification proves that (4) has no solution.  Therefore no selected
four-pair local assignment with this exact `(D,A)` can exist, independently
of the already failed third image.

This is only an exclusion of the fixed A branch.  It does **not** exclude
all possible A for `D=0x00050000`.

## 4. Certificate boundary and controls

Glucose4 from python-sat generates the DRUP traces but is not trusted for
the final result.  Deletion records are omitted; retaining clauses only
strengthens the database and preserves the RUP validity of later additions.
`check.py` imports only the Python standard library.

Controls checked by `check.py` include:

* the actual X word supplies a satisfiable joint-derivative control;
* for the reciprocal family, x=0 realizes the changed output difference
  `f(A)=0x17081d0c`;
* removing the final empty clause is rejected as an incomplete proof;
* a byte mutation of the frozen CNF fails the recorded digest;
* the reverse-Q sign error is explicitly required to differ from the target.

No uncertified solver `UNSAT` is used as a theorem.  These certificates are
finite local image results, not Lean formalizations, full 48-row support
certificates, base-schedule completions, distance-13 messages, or a proof of
distance at least 14.
