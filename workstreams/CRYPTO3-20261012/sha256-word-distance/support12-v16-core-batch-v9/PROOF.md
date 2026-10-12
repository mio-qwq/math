# Six fixed `v2(D)=16` selected-core exclusions

Status: **six complete author-side finite certificates; independent AI
acceptance is pending**.

## Theorem proved by the certificates

Let all arithmetic be modulo `2^32`, and define the actual SHA-256
small-sigma derivatives

```text
F_D(w) = sigma0(w+D) - sigma0(w),
G_D(w) = sigma1(w+D) - sigma1(w).
```

For each

```text
q in {5,13,21,23,25,27},    D=q*2^16,
```

there are no 32-bit words `x,y,z` satisfying, with
`A=F_D(x)` and `T=G_D(x)+D`,

```text
F_D(y)=A,   G_D(y)=T+D,
F_D(z)=-A,  G_D(z)=-T.                              (1)
```

These are universal exclusions over `x,y,z` and hence over the derived
targets `A,T`; they do not merely exclude a previously observed fixture.
For `q=5`, this strengthens the separate fixed-`A` third-image obstruction.

The selected four-pair local criterion adds `F_A(u)=D` to (1).  Therefore
UNSAT of (1) also excludes that four-pair criterion at each listed `D`.

## Certificate construction

For every `q`, `generate.py` independently instantiates the same exact
Boolean circuit with the corresponding constant `D`.  Each CNF has 1,259
variables and 9,683 clauses.  Rotations and shifts use their original bit
indices; XORs are complete truth-table relations.  Additions are 32-stage
ripple-carry additions with carry-in zero and unrestricted final carry,
hence are exactly addition modulo `2^32`.

Glucose4 emitted a proof trace for every formula.  Deletion commands were
removed, leaving deletion-free DRUP: retaining clauses can only strengthen
the active database.  `check.py` imports no generator or solver library.
It reconstructs each CNF with separately written circuit code, requires
exact equality of all parsed clauses, verifies all proof additions by
reverse unit propagation, and requires a final empty clause.

| `q` | `D` | DRUP additions | CNF SHA-256 | DRUP SHA-256 |
|---:|---:|---:|---|---|
| 5 | `00050000` | 9,205 | `0d12389970748ee281e73f5cdac14311987c799a847bc87fb694ece1b46fa7f6` | `98636e3ab04227983dcfe68754ca2af7cf2e23fe99dd164b1ac508f55a8444ce` |
| 13 | `000d0000` | 6,720 | `1df928754d23acefa41d4ac7d7fc010e0ca49fe7f993816d3e413bc409f8cee5` | `9b86c318437dab55ae07bf2848f2bd84f87d883e6d115359d3182e26843ff0cc` |
| 21 | `00150000` | 5,879 | `75de735eae881cd13e9cc9ae08996d9ce81d31799b970914e555f2281e64b350` | `0c8ef607e98c1929b971aed54d683a68d4cadcc229f326494992f180e8bbbb4b` |
| 23 | `00170000` | 7,365 | `7710c2aff1e810c7f182bacf4e3adb035a5bb4daf404e68252f20cf4b6d13b5f` | `82ef370adf21a56e401cbced65122a3af2ea414540315ad182b50741b88de963` |
| 25 | `00190000` | 4,637 | `4240a078f2cc3d225bf76e45e05dcdbe9246a23945c3fe260e915c10f4c020c6` | `47271c2b31dee08ae331b0b1c6b1d0b964c932b0b555555cc1279ba9c24c7cb7` |
| 27 | `001b0000` | 7,319 | `a1361267d6e5b5f5560140a9d10344689a2cd25eeb80d987350b6e62eb7c8846` | `f2d46e4bbe630864ed1018983563f58d4b1b0e4a850d2919f606273bd9bf2e7e` |

All six standard-library checks return `PASS`.

## Controls

For every `q`, `RUN.json` contains a concrete assignment satisfying the
first five defining identities but failing the final `G_D(z)=-T` identity.
Thus removing that last equation makes each tested formula satisfiable; the
controls are evaluated directly from the 32-bit word definitions rather
than accepted from a solver model.

The checker also verifies separately for every proof that removing its
final empty clause leaves no conclusion and that a one-byte CNF mutation
does not match the frozen digest.

## Exact boundary

Every listed `q` is odd, so every listed nonzero `D` has `v2(D)=16`.
Nevertheless this is a finite six-point result.  It does not cover the
other odd residues modulo `2^16`, does not establish a symbolic theorem for
all `v2(D)=16`, and does not exclude the complete support-12 factor graph.
It is not a base-schedule completion, an actual message pair, a distance-13
construction, a distance-at-least-14 proof, or a Lean formalization.

The preliminary QF_BV observations were discovery only.  The evidence used
here is the frozen CNF/DRUP data and the standard-library checker replay.

