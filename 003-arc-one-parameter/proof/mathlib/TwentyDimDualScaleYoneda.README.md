# Canonical twist transport and actual graded Yoneda powers

Let R be a commutative characteristic-two ring, q any parameter, H a
unit, A the actual twenty-coordinate algebra and S its actual f-character
module. The canonical inverse-dual-restriction transport on Ext(S,S,n)
preserves actual Yoneda composition in every pair of degrees:

```text
T_(a+b)(alpha.comp(beta)) = T_a(alpha).comp(T_b(beta)).
T_0(identity S) = identity S.
```

The endpoint argument is proved for every actual isomorphism of A-modules,
using associativity and cancellation in Mathlib Ext. Applying the official
exact-functor composition theorem then gives the canonical transport
statement, with both specified f-character endpoints retained.

The source defines actual graded powers of the fixed Ext cubed class:

```text
fYonedaPower(q,0) = identity S in Ext(S,S,0),
fYonedaPower(q,m+1) = fYonedaPower(q,m).comp(fExtThree(q))
                    in Ext(S,S,3*(m+1)).
```

The first power equals the specified actual fExtThree. The proved
canonical fixed-class eigenvalue and preservation of composition give

```text
T_(3*m)(fYonedaPower(q,m)) = (H_inverse)^m * fYonedaPower(q,m).
```

The same formula holds on every scalar multiple of each specified power.
These identities hold without a nonzero hypothesis on q. The previously
proved first-power nonvanishing requires q cubed to be nonzero; this source
does not assert nonvanishing of any power with m at least two. The weight
identity remains meaningful when a power is zero.

No dimension or full self-Ext profile, parameter group-law coherence,
tensor-square realization or complete ARC is claimed. Actual compilation,
independent source replay, printed axiom audits and the exact source hash
are recorded in the companion verification JSON.

Dependency-ordered reproduction from this directory is:

```powershell
.\verify-cohomology.ps1 -Targets TwentyDimDualScaleYoneda
```
