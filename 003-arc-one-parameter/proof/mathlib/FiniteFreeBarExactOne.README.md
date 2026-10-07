# Exactness at the first free term

`FiniteFreeBarExactOne.lean` transfers all twenty R-coordinates of each
A-valued coefficient of a vector in P1 into P2. This defines a genuine
R-linear contracting map h1; no A-linearity is asserted for h1.
Its coefficient at word (i,j) is the central image of the ith coordinate
of the original coefficient at j.

The full three-face boundary formula proves

`boundary2(h1(v)) + L1(zeroWordEquiv(boundary1(v))) = v`.

In particular, if boundary1(v) is zero, h1(v) is an explicit preimage
under boundary2. Combined with the already proved zero adjacent
composition, this gives `ker boundary1 = range boundary2` for every
actual character and arbitrary parameter q, retaining all A coefficients.

Nine printed audits, exact source hash and actual compilation/replay
results are recorded in the verification JSON. This proves exactness
at P1. Higher exactness, an all-degree projective resolution and an
Ext comparison remain open.
