# Two inverse boundaries are not consequences of the additive row module

**New exact researcher-authored candidate; not yet independently accepted
by another agent.** This note proves failure of one linear proof mechanism,
not failure of either proposed reverse implication for actual SHA-256
input blocks. No real 32-bit word-pair realization is supplied.

The source is the frozen support file with SHA256
`02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf`.
The earlier accepted `shift-review-v4/` remains byte-for-byte frozen.

## 1. Exact linear interface retained from all original recurrences

For actual SHA-256 expanded inputs, define in R = Z/(2^32)

    d_i = W'_i-W_i,
    F_i = sigma0(W'_i)-sigma0(W_i),
    G_i = sigma1(W'_i)-sigma1(W_i).

For each t=16,...,63 the original recurrence gives the row relation

    E_t = d_t-G_(t-2)-d_(t-7)-F_(t-15)-d_(t-16) = 0.              (1)

If i is outside the exact support, all three interfaces at i are zero.
For a frozen 13-word support there are therefore 39 potentially nonzero
interfaces, ordered as the thirteen d variables, thirteen F variables,
and thirteen G variables. No original recurrence is discarded. A single
shared F_i or G_i is used every time index i occurs; no different word
pair is chosen for different equations.

Let A_s be the integer 48-by-39 matrix of these rows for support s. The
row module over R consists of all R-linear combinations of these 48
rows. Membership of a boundary target in this module would prove that
boundary vanishes for every actual pair satisfying the support. However,
the converse does not follow: the additive interface forgets nonlinear
constraints tying d_i,F_i,G_i to the same two actual 32-bit words.

The inverse recurrence creates

    d_-1 = d_15-G_13-d_8-F_0.                                    (2)

For support 9, G_13=F_0=0, so the proposed shared prefix is equivalent
to target L_9=d_15-d_8 vanishing. If it vanished, right shift one would
produce exact support 0; no active tail is cropped. For support 12,
d_8=F_0=0, so the target is L_12=d_15-G_13. If it vanished, right shift
one would produce exact support 6. These conditional support statements
use the already proved legality and distinctness of translated actual
windows. Their boundary targets are the only new question here.

## 2. Exact unit elimination, with no division by nonunits

The generator uses only row swaps, negation of a row, and addition of
an integer multiple of another row. It pivots only on +1 or -1. Every
operation is unimodular over the integers and invertible over R. The
checker verifies the operations, their integer matrix U, and separately
the direct product U*A_s. It checks unit pivot columns and that all
remaining rows are exactly zero over the integers.

| Support | Original rows | Interface variables | Unit row rank | Free variables | Boundary residual |
|---:|---:|---:|---:|---:|---|
| 9 | 48 | 39 | 23 | 16 | F_9+G_22-G_57 |
| 12 | 48 | 39 | 25 | 14 | -G_13-G_29 |

The pivot rows generate the entire original row module. Their pivot
coordinates are the identity matrix, so a vector supported only on
the free columns belongs to that module only when it is zero. Both
displayed residuals have nonzero unit coefficients in free columns.
Consequently L_9 and L_12 are outside their respective row modules over
R as well as over the integers. No rational Gaussian division, solver
UNSAT verdict, or assumption about independently feasible derivatives
is used to assert a real-schedule impossibility.

The two reduced target identities can also be read directly as exact
integer combinations of original rows:

    L_9-(F_9+G_22-G_57)
        = -E_22+E_24-E_29-E_36-E_43-E_59,

    L_12-(-G_13-G_29) = -E_31.                                 (3)

For support 12, G_13 never appears in any of the 48 original rows:
the smallest index of a G term is 14. Thus the coefficient -1 at G_13
in L_12 is already a direct nonmembership obstruction. This fact does
not make G_13 an independently realizable derivative of actual words.
Also E_29 gives d_29=d_13 for this support. The missing nonlinear
condition would therefore impose opposing sigma1 derivatives on two
pairs having the same additive input difference; that relation remains
a real word-pair question.

## 3. Separating models satisfying every active nonzero interface

For extra precision, the certificate supplies two exact interface models
satisfying all 48 rows and having **all 39 active d,F,G values nonzero**.
Outside each frozen support all interfaces are zero. Thus the modeled d
support has exactly thirteen positions; no zero active difference is
used to evade the question. The tables use unsigned hexadecimal residues
modulo 2^32.

### Support 9

| Index | d | F | G |
|---:|---:|---:|---:|
| 1 | ffffe65f | 0000e6a9 | 000000f3 |
| 8 | ffffb31c | fff7e40f | 000002d9 |
| 9 | ffff1957 | 00000001 | 0000088b |
| 15 | ff250d95 | 00081bf1 | 000019a1 |
| 22 | ff250d95 | ffb70487 | 00004ce3 |
| 23 | fff7e40f | 00d83e70 | 0000e6a9 |
| 29 | ff250d95 | 0048fb79 | 00daf26b |
| 36 | ff250d95 | fffffffd | 0002b3fb |
| 37 | ffb70487 | 00c29e98 | 00081bf1 |
| 43 | ff250d95 | 00000003 | 00daf26b |
| 50 | ff250d95 | 00000009 | 001853d3 |
| 51 | fffffffd | 0000001b | 0048fb79 |
| 57 | ff250d95 | 00000051 | 00daf26b |

Here L_9=4280638073 modulo 2^32, which is nonzero. The certificate also
gives signed integer lifts satisfying all original rows exactly over Z,
with a nonzero integer boundary.

### Support 12

| Index | d | F | G |
|---:|---:|---:|---:|
| 10 | fffff775 | ffe7ac2d | 00000051 |
| 11 | 001853d3 | 00000882 | 000000f3 |
| 13 | fff7e40f | fffd3263 | 000002d9 |
| 15 | ffff1957 | ffffb31d | 0000088b |
| 18 | 001853d3 | 00000009 | ffefc81e |
| 20 | ffe7ac2d | 0002b3fc | 0000e6a9 |
| 26 | fffffff7 | ffe7ac2d | 000019a1 |
| 28 | fffd4c04 | ffe7ac2d | 00004ce3 |
| 29 | fff7e40f | 00000001 | 0000e6a9 |
| 34 | 001853d3 | 00000009 | 00206fc4 |
| 42 | fffffff7 | 00000003 | 0002b3fb |
| 43 | ffe7ac2d | 00000009 | 00081bf1 |
| 57 | 00000003 | 0000001b | 001853d3 |

Here L_12=4294907518 modulo 2^32, also nonzero. Again every row vanishes
both modulo 2^32 and for the certificate's corresponding integer lifts.

Each model is a separating witness: any linear combination of zero rows
evaluates to zero on it, while the target does not. This proves target
nonmembership without trusting the elimination algorithm. It even shows
that adding the active-interface nonzero conditions to this linear
relaxation does not force the shared prefix.

These are **interface countermodels only**. In particular, no actual
W_i,W'_i realizing their triples simultaneously is asserted, and no
initial sixteen-word block pair is supplied. Nonzero interfaces and all
additive recurrences do not imply the required f/g derivative semantics
or original base-schedule solvability.

## 4. Reproduction, negative controls, and stopping scope

The certificate contains all source rows, elementary integer operations,
U, the unit-reduced matrix, free/pivot columns, the original-row target
identities and exact separating models. The checker independently
reconstructs source rows and verifies every integer identity directly;
it does not import the generator and does not itself run Gaussian
elimination. Five damaged controls alter a source row, U, a target row
combination, an active model value, or the target itself. All are rejected.

Read-only commands from the repository root:

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/shift-symbolic-v5/build_module_certificate.py
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/shift-symbolic-v5/check_module_certificate.py
```

The first prints the deterministic certificate; the second prints the
deterministic check receipt for the frozen certificate. Neither overwrites
any file without `--output`. All computation uses Python's standard
library and exact integers. The frozen SHA256 manifest binds source,
data, proof and execution records.

The bounded task stops here: all 48 additive rows alone cannot complete
either inverse boundary. Further work would have to prove or refute
F_9+G_22-G_57=0 and G_13+G_29=0 using actual coupled derivatives and,
if needed, base-schedule equations. No blind SAT extension, real inverse
counterexample, extra excluded support, improvement of distance 13,
formal proof-assistant result, originality finding or publication is
claimed. This is a new candidate checked by separately written code,
not independent-agent acceptance of that candidate.
