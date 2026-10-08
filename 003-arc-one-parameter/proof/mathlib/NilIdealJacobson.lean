import SquareZeroJacobson
import Mathlib.RingTheory.Nilpotent.Basic

/-!
# Full nil ideals and the actual noncommutative ring radical

A left ideal all of whose elements are nilpotent is contained in the ring
Jacobson radical. Individual nilpotence outside such an ideal does not
supply this statement. Any surjection with full kernel contained in the
radical identifies the whole source radical as the inverse image of the
whole target radical; a full nil kernel is sufficient.
-/

namespace ARCNilIdealJacobson

variable {A B : Type*} [Ring A] [Ring B]

theorem nilIdeal_le_jacobson (I : Ideal A)
    (hI : ∀ x : A, x ∈ I → IsNilpotent x) : I ≤ Ring.jacobson A := by
  intro x hx
  rw [← Ideal.jacobson_bot]
  apply Ideal.mem_jacobson_iff.mpr
  intro y
  have ht : y * x ∈ I := I.mul_mem_left y hx
  obtain ⟨z, hz⟩ := (hI (y * x) ht).isUnit_add_one.exists_left_inv
  refine ⟨z, ?_⟩
  rw [Ideal.mem_bot]
  rw [mul_add, mul_one] at hz
  rw [mul_assoc, hz, sub_self]

theorem radical_comap_of_ker_le (f : A →+* B) (hf : Function.Surjective f)
    (hker : RingHom.ker f ≤ Ring.jacobson A) :
    Ring.jacobson A = Ideal.comap f (Ring.jacobson B) := by
  rw [← Ideal.jacobson_bot (R := B), Ideal.comap_jacobson_of_surjective hf,
    ← RingHom.ker_eq_comap_bot f]
  exact (ARCSquareZeroJacobson.jacobson_eq_of_le (RingHom.ker f) hker).symm

theorem radical_comap_of_nil_ker (f : A →+* B) (hf : Function.Surjective f)
    (hker : ∀ x : A, x ∈ RingHom.ker f → IsNilpotent x) :
    Ring.jacobson A = Ideal.comap f (Ring.jacobson B) :=
  radical_comap_of_ker_le f hf (nilIdeal_le_jacobson (RingHom.ker f) hker)

theorem radical_eq_ker_of_nil_ker (f : A →+* B) (hf : Function.Surjective f)
    (hker : ∀ x : A, x ∈ RingHom.ker f → IsNilpotent x)
    (hB : Ring.jacobson B = ⊥) : Ring.jacobson A = RingHom.ker f := by
  rw [radical_comap_of_nil_ker f hf hker, hB, ← RingHom.ker_eq_comap_bot]

#print axioms nilIdeal_le_jacobson
#print axioms radical_comap_of_ker_le
#print axioms radical_comap_of_nil_ker
#print axioms radical_eq_ker_of_nil_ker

end ARCNilIdealJacobson
