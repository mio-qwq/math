# Invariant trace pairing and cyclic products

`TraceInvariance.lean` combines the proved associativity and trace symmetry to establish `beta(u*v,w) = beta(u,v*w)` and the cyclic trace identity `tau((u*v)*w) = tau((v*w)*u)`. It also proves zero, additive and scalar laws for the trace.

Both the polynomial vectors and every commutative characteristic-two specialization are covered. The linearity of the specialized coordinate trace needs only a commutative ring. There is no new table enumeration.

The eight printed audits compiled without warnings and use only the standard three axioms (the two specialized linearity audits use only `propext`). This file does not construct a homological complex or prove the ARC realization.

After building `TracePairSemantics.olean`, run `lake env lean TraceInvariance.lean` with this directory and its parent in `LEAN_PATH`.
