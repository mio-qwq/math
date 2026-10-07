# Symmetric and nondegenerate trace on all vectors

`TracePairSemantics.lean` defines the trace by `tau(v) = v(10) + v(18)`. Let `dual(a)` exchange the two halves of `Fin 20`. For the actual table multiplication, Lean proves

`tau(u * v) = sum_a u(a) * v(dual(a))`.

The proof decodes the frozen basis trace certificate using a general scalar coefficient-extraction lemma that allows duplicate labels and has no byte-size bound. Finite sum expansion extends it to all vectors. The dual permutation is an involution, which proves symmetry; testing against individual dual basis vectors proves left and right nondegeneracy.

These statements hold over `Polynomial (ZMod 2)` and after every specialization into any commutative characteristic-two ring. In particular, trace nondegeneracy here does not require q to be nonzero or the coefficient ring to be a field.

All twelve audited statements compiled without warnings. The involution uses `propext` and `Quot.sound`; the other audits use the standard three axioms. No new finite enumeration or axiom is introduced. A library algebra instance and the complete Hochschild/Ext realization remain separate tasks.

After building `TwentyDimAssociativity.olean`, run `lake env lean TracePairSemantics.lean` with this directory and its parent in `LEAN_PATH`.
