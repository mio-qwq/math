# Cycles modulo boundaries

`LowDegreeCohomology.lean` constructs the actual module quotient for any two composable linear maps with zero composite. The preceding map is restricted to the kernel of the next map, and its range is the boundary submodule inside the cycle module.

The class of a cycle is zero exactly when the representative lies in the image of the preceding map. A proved non-boundary therefore gives a nonzero quotient class. All three audits compile without warnings and use standard axioms. This is a generic module construction and makes no claim that a particular cochain is closed.
