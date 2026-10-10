# Finite integrality slightly sharpens the limiting upper endpoint

B, 2026-10-10. Addendum to the unchanged DENSITY_LIMIT.md frozen0599b104ac0fe3f241a7a3ba4dfeae878c28951f. Same original Problem5.2 scope, pending independent review. This is a small refinement of the SAME partial theorem, not an additional solved problem.

Let f(m) have the definition in that proof. At m=11 the seven-window bound and integrality give

    f(11) <= floor(2(11)_4/7) = floor(15840/7) = 2262.

The already proved subalphabet monotonicity gives, for all m>=11,

    f(m)/(m)_4 <= f(11)/(11)_4 <=2262/7920=377/1320.

Consequently the density limit actually satisfies

    26/125 <= lambda_4 <=377/1320 <2/7.

The strict improvement is exactly2/7-377/1320=1/9240. A finite upper bound is floor(377(m)_4/1320)+m(m-1)(3m-5). This does not determine the density or the finite GP numbers. It does show that equality at2/7 is impossible, without assuming a stability theorem or running a larger optimization.

All ingredients are the written seven-window and subalphabet arguments. Exact integer/fraction arithmetic was actually run with Python3.12.14; see rounding_refinement.log. This is not a new independent mathematical review or Lean assertion.
