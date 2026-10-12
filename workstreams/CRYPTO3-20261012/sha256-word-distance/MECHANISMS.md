# Mechanisms under examination

The object is the actual FIPS 180-4 16-to-64 expansion over Z/(2^32),
with word distance counted over all 64 words and arbitrary distinct input
blocks. These notes record mathematical tests and their limits; they do
not assert that distance 13 is attained or that distance 14 is proved.

## A. Repeated cancellation in the regular support family

Before computation: derive every nontrivial modular difference equation
for the frozen supports, group only legally shifted equations, and retain
all boundary equations. Supports 0, 1, 2 and 4 are translations of a
repeated pattern; supports 8 and 9 have different initial boundaries.
The new question is whether repeated opposite sigma0 differences force
restrictions on the actual common base words, or a closed arithmetic
cycle, beyond the five independent-pair tail equations already tested.

The computation will print identities using distinct symbols for input
word differences, sigma0 differences and sigma1 differences. Symbolic
identities are necessary conditions; they cannot replace the base
expansion or the compatibility of both sigmas on the same word pair.
No input difference is set to 2^31 without a derived equation.

The source support list is frozen at commit
80b71cb3b6a67c8f8aae80d9cd8b6ed87d74bd51, path
workstreams/CRYPTO2-20261011-7f3c/projects/sha256-schedule-distance/v2/supports.json.

Derived from support 0: at t=16,23,30,37,44,51,58 the same nonzero
word difference D propagates along indices 9,16,23,30,37,44,51,58.
The zero equations t=32,46,60 give G_30=G_44=G_58=-D. Thus each of
these pairs is a collision of the map x -> x+sigma1(x). Before further
computation, test the new restricted mechanism: determine whether such a
collision can have difference +/-2^k. Its XOR input difference would be
a consecutive run starting at k, as would the output XOR difference.
This is a finite 32-bit linear-mask question with an elementary reduction;
it is not a zero-base search. A general collision, if found separately,
would only delimit this local mechanism, not construct a full schedule.

The interval-mask test leaves only alpha=0xffffffff, sigma1(alpha)=
0x003fffff at k=0. The only increment-by-one pairs having that XOR mask
are (0x7fffffff,0x80000000) and (0xffffffff,0); neither has sigma1
difference -1. Thus no +/-power-of-two difference satisfies the local
cancellation. A full proof/checker is to bind this reduction and its
finite mask check, not to trust a solver.

## B. Common low bits in a sigma1 cancellation

Before computation: if D is divisible by 2^k, both the input XOR
difference alpha and sigma1(alpha) must have their low k bits zero.
These are exact linear constraints on alpha, independent of the base
word. The low-17 projection has trivial kernel, immediately excluding
nonzero differences divisible by 2^17. At k=16, the remaining XOR mask
is 0x44ab0000 with image 0xe0110000; their lowest four quotient bits
cannot have opposite modular differences. Test whether the next
projection yields a stronger exact carry obstruction. Any SAT pair
will serve only as a sharpness boundary for this local cancellation,
not as a SHA message-pair witness.

## C. Coupling the sharp local boundary back to sigma0

The independent reconstruction found that, at common low 12 bits, only
the XOR mask 0xfbca7000 survives the necessary signed-carry test for an
h collision. Before computation: characterize the exact base-word fibres
for that fixed mask by branching over the actual signed carries and
retaining the linear relation between x and g(x). The resulting affine
pieces can constrain sigma0 on the same word pairs. This tests whether
the repeated schedule cancellations can coexist at the sharp local
boundary; it is not another unrestricted tail or zero-base search.

No actual schedule is inferred from a fibre. The intended use is either
a rigorous boundary exclusion, or a candidate for a subsequent lift that
retains every original base and difference recurrence.

A four-word query at this boundary initially returned UNSAT without an
independently checked certificate. That exploratory result is not used
in any theorem; mechanism E later supplies a separate complete proof.
The unrestricted four-word kernel is SAT. Therefore the generic coupling
is not an exclusion by itself; a local SAT fixture must be kept separate
from a schedule witness.

## D. A periodic assignment to all active word pairs

Before computation: test a constructive restriction on support 0. Assign
the same pair Q at active indices congruent to 2 modulo 14, P at indices
congruent to 9, and R at indices congruent to 10. Substitution into every
nontrivial difference recurrence reduces them to

    d_P=d_Q=D != 0, F_P=-F_Q=A != 0, G_Q=-D,
    d_R=A, G_R=-A, F_R=-G_P-D.

This is a three-pair modular system, with all sigmas computed on the
actual word pairs. It is a new restricted construction ansatz, not an
assumption in a universal theorem. If it is satisfiable, a separate
single-base interpolation system must still be solved and both complete
64-word schedules rebuilt. A failure of this ansatz does not exclude
support 0. No period is imposed on the inactive base words.

The bounded query returned `unknown` after 20 seconds, with reason
`timeout` (Z3 4.15.3). This supplies neither a solution nor an exclusion.
This particular query is stopped without extending its timeout.

## E. A proof-producing decomposition of the low-12 sigma0 coupling

Before computation: the exact fixed-mask h fibres in mechanism C have
only eight free bits per affine piece. Determine the distinct `(D,F)`
requirements they impose on a second pair p,p+D through
`sigma0(p+D)-sigma0(p)=-F`. First inspect the projection dimension; then
attempt an exact carry/linear-algebra split on the second pair. Every
branch must retain the original sigma0 bit equations, modular carries,
and arbitrary low base bits. A full branch cover and contradiction
certificate would establish the boundary exclusion independently of the
earlier solver status. Feasible branches would instead diagnose the
claimed UNSAT or the reduction. A node budget stops the proof search
without making a mathematical impossibility claim.

The reduction was instead frozen as a transparent 96-input-bit Boolean
circuit for the three exact modular equations. Its complete DRUP proof
has 19,460 RUP additions, all checked by the root watch-list verifier and
by a different agent's explicit-hint verifier. An independent audit
reconstructs the word-to-CNF correspondence and all low-12 dependencies.
The seven schedule bridges use 36 original recurrence substitutions,
including a separately justified reversal of the index-8 pair in support
5. Thus the local coupled system has v2(D)<=11, and so do those specified
support differences. No entire support is excluded.

The second proof mechanism conditions on fixed XOR masks and represents
each nonzero signed carry by a Boolean sign. The resulting exact local
carry transitions are affine over F2. A complete necessary screen leaves
132 masks, and explicit XOR row combinations reject them. This replaces
a large propositional certificate with a small binary-linear certificate;
the full RUP proof is retained as separate evidence. The mask screen is
the zero-output special case of Lipmaa--Moriai's classical modular-addition
XOR-differential criterion, as detailed in `../sources/POST_RESULT_GATE.md`.

## F. Sharpness fixes the boundary of the coupled local mechanism

Before computation, `coupled-sharpness/MECHANISM.md` fixes a single bounded
query at valuation exactly 11. Its purpose is to decide whether the same
three local equations can imply a stronger ceiling. The query produced
four words with D=971a5800 and valuation 11. Direct output-bit checks and
damaged controls confirm every equation, and a separate AI agent checks
the object independently. Thus 11 is the exact local ceiling. Continuing
the same four-word exclusion below 11 is mathematically blocked by this
object; further progress needs other original recurrence or base equations.

## G. Full nonperiodic interfaces and a stopped construction family

The active-pair construction work retains all 48 difference equations of
support 0 without identifying pairs by their residue class. It gives an
exact module criterion, with the left boundary kept, and a five-word
parameterization of its reversed-g chain. An attempted choice of R XOR
mask equal to the f image of a specified Q mask fails already modulo 8:
the required G52=F30 would equate residues in {1,7} with residues in {3,5}.
This excludes that specified mask family, not all modules or support 0.
The mechanism stops at this proof instead of sweeping seeds or extending
solver timeouts. Its exact note and finite data are in
`active-pair-construction/`.

The separate `base-lift/` theorem records the remaining base-message
obligation as ten original residual recurrences after 38 reversible
eliminations. It neither assumes nor proves their solvability. The local
word objects and failed construction families recorded above are never
promoted to complete expansions.
