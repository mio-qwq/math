# A stopping test for the coupled local valuation bound

Before computation, the question is whether the four-word condition used
by the reviewed coupled theorem permits valuation exactly 11. If it does,
the local theorem's valuation bound is sharp and any further restriction
on the seven schedule supports must use additional recurrence or base
equations. This is a test of a proved mechanism's boundary, not a claim
about the existence of a complete distance-13 schedule.

Use arbitrary 32-bit words p,p',q,q' and the original small sigmas f,g.
Impose exactly

    D = p'-p = q'-q,
    g(q')-g(q) = -D,
    f(p')-f(p) = -(f(q')-f(q)),
    D mod 4096 = 2048.

All equations are modulo 2^32. The last condition is v2(D)=11, and
implies D is nonzero. No base word is fixed and no power-of-two value of
D is imposed. One solver call is limited to 15 seconds. A satisfying
four-word object must be checked by separately written bit formulas.
An unknown result stops this test without extending the time limit; an
UNSAT result without an independently checkable proof is discovery only.

No original schedule support enumeration, previous tail query, zero-base
search, or base-message interpolation is performed by this test.
