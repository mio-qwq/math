# The actual f-character module is neither projective nor injective

Let R be a commutative characteristic-two ring, q a parameter, A the
actual twenty-coordinate table algebra and S its actual f-character
module. When q cubed is nonzero, S is neither a projective nor an
injective object of the actual category of left A-modules.

Both conclusions use the previously proved nonzero actual Mathlib class
fExtThree in Ext(S,S,3). Projectivity of the source or injectivity of the
target would make this positive-degree Ext class zero, contradicting its
full specified-resolution nonboundary proof. The source uses the pinned
official positive-degree Ext vanishing theorems.

Over a ring without zero divisors, q nonzero suffices. In particular this
includes every characteristic-two field with q nonzero. The general
statement retains arbitrary commutative characteristic-two coefficient
rings satisfying the stated cube hypothesis.

The earlier field-only self-injectivity theorem concerns the regular
module A; the present obstruction concerns S. No infinite projective or
injective dimension, complete self-Ext profile, or nonprojectivity of the
final converted ARC object is claimed.

Actual compilation, independent source replay, three printed axiom
audits and the exact source hash are in the companion verification JSON.
Dependency-ordered reproduction from this directory is:

```powershell
.\verify-cohomology.ps1 -Targets TwentyDimCharacterHomologicalObstruction
```
