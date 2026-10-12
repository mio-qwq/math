# Analytic structure of the actual support-12 pair core

This stage performs analytic work. It does not expand the 128-value
valuation16 case list, rerun an unrestricted SMT model, modify earlier
frozen sources, or make a Git mutation.

## Exact parameterization to investigate

For fixed nonzero D, put

    F_D(x)=f(x+D)-f(x), G_D(x)=g(x+D)-g(x) modulo2^32,
    I_D={(F_D(x),G_D(x)): x is an arbitrary32bit word}.

Reverse the third pair R to obtain a pair Z with input difference D.
Then the actual three-pair core is equivalent to existence of two
target scalars A,T such that all three points

    (A,T-D), (A,T+D), (-A,-T)

belong to I_D, with actual preimages supplying X,Y,Z. This reduces
the external interface search to two target parameters once D is fixed.
It does not prove image membership is easy or replace actual derivatives
with free values. Every preimage still evaluates both sigmas on the
same actual word pair. No base-schedule interpolation condition is
removed from a claim about real expanded messages.

## New analytic question

The original support12 recurrences t33 and t41 supply a fourth pair P
with d(P)=-A, F(P)=-D. Thus the actual support imposes an anti-cycle
of sigma0 derivatives in addition to the three-pair image criterion.
Examine its half-word strata D=2^31 or A=2^31 using the exact binary
permutation f and its inverse. Half-word addition has a unique XOR mask;
its image or inverse image therefore forces a specific valuation.

Before the small constant check, compute f(2^31), f^(-1)(2^31), and
their least significant set bits from the original bit equations. If
these valuations differ, an anti-cycle containing a half-word may be
impossible by a direct valuation contradiction. Such a lemma would
apply across all other differences and would not depend on SAT or
finite low-valuation enumeration.

Also examine whether the third pair can share endpoints with X or Y.
Any endpoint obstruction must distinguish aligned from crossed endpoint
equalities and retain modular half-word torsion, rather than divide by2.

Only the32-row binary inverse calculation and direct constant checks
are planned. Any new global support condition will be written fully
and paired with a separately checkable finite-dependency checker.
