# Contraction identities in every degree

`FiniteFreeBarRecursiveContraction.lean` proves, for any preceding
actual A-linear map d and every vector v in P(n+1),

`nextBoundary(n,d)(H(n+1)(v)) = v + Hn(d(v))`.

The proof reassembles every coordinate of every A-valued word
coefficient. Insertion is used only R-linearly. Applied to the recursive
family, this gives the usual contraction identity in every positive
degree. At degree zero the actual augmentation has an explicit
R-linear scalar section, yielding the corresponding augmented identity.

Nine printed audits and actual compilation/independent replay records
are in the verification JSON. No degree bound or word enumeration is
used. This file supplies contraction identities; the all-degree zero
composites and kernel/range equalities are separate theorems.
