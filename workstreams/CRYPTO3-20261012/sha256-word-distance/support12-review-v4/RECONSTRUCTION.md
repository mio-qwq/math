# Independent reconstruction of the support-12 ceiling

This review reconstructs the original recurrence and a different complete
finite model. `check_independent.py` was frozen and its full seven-case
run completed before any author candidate bytes were read. It imports
no author checker, generator, or discovery function. The only older
mathematical text read before reconstruction was the inherited
`mechanism/VALUATION_BOUND.md`; that contact and its exact hash are
recorded in `INITIAL_SOURCE_CONTACT.json`. Thus this is independent
reconstruction of the new ceiling, not a claim of having no prior
knowledge of the old three-pair core.

## Original recurrence bridge

For support 12, substitution of the exact active set in the original
lag set `{2,7,15,16}` gives:

| Original t | Reduced equation |
|---:|---|
| 18 | d18=d11 |
| 27 | 0=d20+d11 |
| 34 | d34=d18 |
| 20 | d20=G18+d13 |
| 29 | d29=d13 |
| 36 | 0=G34+d29+d20 |
| 45 | 0=G43+d29 |
| 50 | 0=d43+d34 |
| 33 | 0=d26+F18 |
| 42 | d42=d26 |
| 49 | 0=d42+F34 |
| 58 | 0=F43+d42 |

Only substitutions and additions are needed. They imply

    d18=d34=D != 0, d43=-D,
    F18=F34=F43,
    G34-G18=2D, G34-G43=D.

Shifts `+1,+3,+2` give supports 6,7,13. The independent checker
reconstructs all 48 reduced original rows and checks every boundary.
After author contact, a separate script also checks all 28 written
integer combinations in the author's proof. These do not divide by a
nonunit in Z/(2^32).

## Width and sign reduction

If v2(D)>=19, all three input pairs have the same low nineteen bits.
For output positions 22..31, sigma1 depends only on input positions
`j-15,j-13`, both below 19, with no shift term. Every actual ordinary
sigma1 image difference q therefore has absolute value less than 2^22.
Set A=q34-q43 and B=q34-q18. Then A=D and B=2D modulo 2^32,
and |A|,|B|<2^23. Thus B-2A is a multiple of 2^32 with absolute
value less than 3*2^23, so it is zero. In particular |A|<2^22.
Since A is a nonzero multiple of 2^19,

    D = +/- k*2^19 modulo 2^32, 1<=k<=7.

This also covers k=4 directly and does not depend on the old <=20
ceiling. A simultaneous priming swap negates all derivatives and
preserves the equations, so positive representatives suffice.

Reverse the third pair to put all three input pairs in the form
`(a,a+D),(b,b+D),(c,c+D)`. Their actual joint derivatives obey

    Fa=Fb=-Fc, Gb-Ga=2D, Gb+Gc=D.

Both signs of the third derivatives are essential. The model has 96
actual input bits: all sigma0 and sigma1 output rows on one base word
use the same 32 variables.

## Different finite exclusion engine

For each k, independently enumerate all 8192 high-input quotients
`a=0..8191` under addition by k modulo 8192. The mask fibre
`a xor ((a+k) mod 8192)=m` is checked against every quotient to be
exactly the cube fixed on coordinates `m & 4095`. The input bit31 is
unrestricted. Low nineteen bits are also unrestricted. This directly
includes overflow past input bit31.

For a sigma output XOR mask beta and unprimed masked output
U=(sigma(a) & beta), the ordinary output derivative equals beta-2U.
This is XOR linearity of sigma on the input mask, not additivity of
sigma on the difference D. Consequently the four core equations are
exactly:

    Af_a - Af_b = (beta_fa-beta_fb)/2              mod 2^31,
    Af_a + Af_c = (beta_fa+beta_fc)/2              mod 2^31,
    Ag_b - Ag_a = (beta_gb-beta_ga-2D)/2           mod 2^31,
    Ag_b + Ag_c = (beta_gb+beta_gc-D)/2            mod 2^31.

An odd numerator is impossible. Otherwise division by two here is
the exact elementary equivalence between `2X=2T mod 2^32` and
`X=T mod 2^31`; it is not division in the recurrence ring.

The engine interleaves all four masked addition/subtraction equations
over bits 0..30. At a bit with fixed incoming signed carry, it checks
the complete truth table of the present output bits. The allowed
group for each next carry is a singleton or an affine two-point line.
It imposes the corresponding fixed bits or XOR equation directly on
the original input variables. Signed subtraction carries remain in
{-1,0}; addition carries remain in {0,1}. The final carry is discarded,
as required by congruence modulo 2^31. Thus the corresponding original
32-bit arithmetic retains its modular wraparound.

Each added row is reduced over F2. The high-pivot implementation is
different from the author's low-pivot receipt implementation. A branch
is cut only on the contradiction 0=1, an empty exact truth table, or
the elementary ordinary sigma1 width bound. Sigma1 masks are below
2^22, and 2D<2^23, so the ordinary width cuts cannot discard a modular
solution differing by an extra multiple of 2^32.

| k | Masks per input pair | Triple mask cases | Feasible final systems |
|---:|---:|---:|---:|
| 1 | 13 | 2197 | 0 |
| 2 | 12 | 1728 | 0 |
| 3 | 23 | 12167 | 0 |
| 4 | 11 | 1331 | 0 |
| 5 | 32 | 32768 | 0 |
| 6 | 21 | 9261 | 0 |
| 7 | 31 | 29791 | 0 |

All 89,243 triples are checked. The result is independently recomputed
from definitions rather than inferred from stored solver verdicts.

## Controls and post-freeze comparison

The additional `negative_control.py` was written after author contact.
It imports only the already frozen independent engine. It verifies
every local carry-group compression against a separate full truth
table. It reproduces all 3389 twin-mask cases, finding exactly one
feasible mask pair, at k=5 and alpha_a=alpha_b=ffd80000. The actual
wrapped witness a=ffd80000, a'=0, b=ffd80040, b'=40 is accepted by
that exact twin model. Mutating b by XOR 1 is rejected. Its sigma0
derivative also disproves the invalid assumption F=sigma0(D).

`compare_author.py` imports no author code. It checks all seventeen
manifest entries, all positive input cubes and all 3389 case indices,
the complete 32-mask third-pair coverage, all 512 stored XOR identities,
and all 28 written original-row combinations. Corrupting a receipt RHS
or deleting a mask pair is detected in memory. It does not claim to
reproduce the author's specific branch-count statistics; the theorem
is accepted on the independent complete model and written review.
