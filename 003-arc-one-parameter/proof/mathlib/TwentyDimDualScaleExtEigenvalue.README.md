# The canonical inverse-dual-scaling weight of the fixed Ext cubed class

Let R be a commutative characteristic-two ring, q any parameter and H a
unit. Write A for the actual twenty-coordinate algebra, S for the actual
f-character module, and F_H for restriction of A-scalars along the inverse
dual-scaling automorphism.

The general exact-functor/extMk naturality theorem identifies the class
represented by the mapped cocycle on the mapped specified resolution
with the actual canonical Ext.mapExactFunctor image. The complete
resolution and module-cocycle comparison therefore gives

```text
dualScaleExtTransportMap(q, H, 3)(fExtThree(q))
  = H_inverse * fExtThree(q).
```

Both actual f-character endpoints are transported back by the specified
underlying-identity isomorphism, in the established source-inverse and
target-forward directions. This computes the canonical transported
action, using the installed Ext module scalar action and the actual
Ext cubed class of the specified all-degree projective resolution.

R-linearity gives the same formula on every r times this fixed class.
The canonical image is nonzero whenever q cubed is nonzero. The scaling
formula holds even when q is zero; the nonzero conclusion requires the
stated nonzero hypothesis.

Only this class and its scalar multiples are computed. The file does not
prove Ext cubed is one-dimensional, that all Ext classes have this weight,
a parameter group-law coherence theorem, the full self-Ext profile, the
tensor-square realization or complete ARC.

Actual compilation, independent source replay, printed axiom audits and
the exact source hash are recorded in the companion verification JSON.
Dependency-ordered reproduction from this directory is:

```powershell
.\verify-cohomology.ps1 -Targets TwentyDimDualScaleExtEigenvalue
```
