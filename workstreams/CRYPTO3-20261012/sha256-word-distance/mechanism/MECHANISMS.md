# SHA-256 word-distance mechanism probes

Object: the exact FIPS 180-4 32-bit modular message expansion. Every base
word remains arbitrary. Frozen support data is read from CRYPTO2 commit
`80b71cb3b6a67c8f8aae80d9cd8b6ed87d74bd51`; no claim of new support
enumeration or complete message-pair feasibility is made.

## Mechanism 1: exact cancellation relations before nonlinear search

Before computation, the proposed test is to derive every nontrivial
recurrence difference equation for irregular supports 5, 6, 7, 10, 11,
12, 13. Variables are `d_i = W'_i-W_i`, `f_i = sigma0(W'_i)-sigma0(W_i)`
and `g_i = sigma1(W'_i)-sigma1(W_i)` in Z/(2^32). The calculation will
use only odd-pivot modular elimination, preserving 2-power torsion;
unjustified division by 2 is forbidden. The new question is whether
early equations enforce a relation absent from the already feasible
five-equation tail, particularly a repeated-sigma cancellation or a
forced valuation. This is not a repetition of the old tail SAT query.

If a subsequent finite/SAT probe is useful, its exact new constraint
and interpretation will be recorded here before the run. A SAT solution
of independent word pairs remains only a relaxation witness; UNSAT is
not a published mathematical exclusion without independent proof.

The exact signed-component calculation yields no forced half-word in
these seven supports. Support 5 has a sigma0 two-cycle
`d34 = F19`, `F34 = -d19`. This isolated two-cycle is universally
feasible for every permutation of an even cyclic group, by the finite
sum obstruction written in `TWO_CYCLE_BOUNDARY.md`. Consequently a
two-cycle-only UNSAT search would be mathematically misguided.

## Mechanism 2: twin sigma0 derivatives with coupled sigma1 derivatives

Before computation, the proposed new test concerns a four-word core
from support 6 (and its valid shifts in 7, 13):

```
d19 = d35 = D != 0,
F19 = F35,
G35 - G19 = 2D.
```

These use early recurrence equations absent from the old five-equation
tail. In detail, t=19, 28, 35 give d19=d12=d35 and d21=-d19;
t=43, 50 give F35=-d27, while t=34 gives F19=-d27;
t=21, 30, 37 give G19=-D-d14 and G35=D-d14. The probe will
add `D != 2^31`, because the already established forced-half tail
exclusion handles that value. A satisfying assignment would invalidate
this core as a standalone route, without establishing a schedule.
An UNSAT/unknown answer would not prove any support excluded.

The unrestricted twin core is SAT in the recorded discovery run
(`TWIN-RUN.json`); its witness needs separate bit-formula verification.
Nevertheless, a direct integer bound proves a nontrivial restriction:
if 2^22 divides D then the sigma1 output pairs agree in bits 22..31,
so each raw output difference has absolute value at most 2^22-1.
The difference of these differences has absolute value below 2^23,
whereas nonzero 2D is a multiple of 2^23 modulo 2^32. Therefore
`2^22 | D` forces `D = 2^31` for an active twin core. The old universal
half-word chain excludes that value when the full support tail is imposed.

Before the next computation, the new test is sharpness of this valuation
restriction **only in the twin core**. Set D=2^21 and choose a carry through
the top input bit, alpha=0xffe00000. Seek a low-21-bit XOR translation z
which is zero on sigma0(alpha)'s active output coordinates, and flips
only bit 21 among sigma1(alpha)'s active coordinates. These are exact
linear equations over F2, independently checkable from the output-bit
definitions. If found, the resulting two derivative pairs have identical
sigma0 difference and sigma1 differences separated by 2D. This neither
reruns the old five-equation tail nor includes the actual base recurrence.

The restricted common-carry-mask translation construction is inconsistent
(30 F2 equations, rank 20 before the contradictory row). This is only a
failed sufficient construction, not a twin-core exclusion. A separate
fixed `D=2^21` query is now justified to decide whether the full core
achieves the proven valuation ceiling despite differing carry masks.

The fixed-D query returned UNSAT in 0.134 s. This is discovery only.
Before further calculation, the proposed proof mechanism is to reduce
the whole valuation-21 stratum to `D=2^21` and `D=2^31+2^21` (their
negatives follow by swapping primed/unprimed pairs). The absolute-value
bound forces these residues whenever v2(D)=21. Each addition of 2^21
has only 11 possible contiguous input-XOR carry masks. For each of 121
mask pairs, the two required modular output-difference equations will
be reduced by exact signed-sum carries to finite systems of F2 linear
equations. All possible carry branches are traversed; inconsistent
linear branches are discarded by exact Gaussian elimination. This
turns the new UNSAT clue into a small, independently reproducible
finite proof obligation, rather than another timeout extension.

The exact traversal rejects all 121 fixed-D cases; only the case where
both input carries reach bit31 needs F2 inconsistency (two branches).
The remaining cases fail already by signed-mask carry feasibility.
Before the next simplification, the new check is whether the sigma1
signed masks alone force both carries to reach bit31, and whether the
single surviving mask pair admits a short explicit F2 row identity.
If so, the written proof can replace most of the finite traversal by
a small arithmetic table and one inspectable XOR identity.

That simplification succeeded. `VALUATION_BOUND.md` now gives a full
written proof from eleven sigma1 masks, ten elementary gap positions and
one explicit 21-term XOR identity. `check_structural.py` verifies only
these finite dependencies and the 44 support substitutions; all six
damaged controls are rejected. The old 121-case traversal is no longer
a logical premise of the result.

## Mechanism boundary: can the complete local triple achieve valuation 20?

Before computation, the next decision is whether the local equations
used by the new proof can by themselves improve its `v2(D)<=20` bound.
The proposed query fixes D=2^20 and imposes all three relevant pairs:
`d_x=d_y=D`, `d_r=-D`, `F_x=F_y=F_r`,
`G_y-G_x=2D`, `G_y-G_r=D`. This adds the g relation missing from the
earlier twin-core positive example, and does not ask the old tail
question again. A real solution would demonstrate that the new
proof's valuation ceiling is sharp for this local core; it would not
be an actual schedule or discharge any remaining support.

The D=2^20 local-triple query returned UNSAT in 0.077 s (discovery only).
The locality argument in the written proof in fact gives |D|<2^22
whenever 2^19 divides D. Consequently the only untested positive
representative at valuation exactly 20 is 3·2^20. Checking that value
now resolves the sharpness decision for this one local-core stratum;
it is not a blind increase of the solver time limit.
