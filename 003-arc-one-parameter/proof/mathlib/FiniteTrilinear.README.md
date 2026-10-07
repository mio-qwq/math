# Finite trilinear evaluation

`FiniteTrilinear.lean` defines the actual triple-sum evaluation of arbitrary four-index structure constants over a commutative semiring and finite coordinate type. It proves addition, scalar and zero laws in each input, and shows that evaluation on three standard basis vectors recovers the prescribed structure constants.

The file packages evaluation as three nested R-linear maps. No particular cochain, closure identity or table enumeration is assumed. All eight printed audits compile without warnings and use only the standard three axioms.

Run `lake env lean FiniteTrilinear.lean` in the pinned package. Its role is to support later extension of the concrete cochain's basis identities to arbitrary vectors.
