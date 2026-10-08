import Mathlib.RingTheory.Jacobson.Ideal
import Mathlib.Tactic.Abel

/-!
# Square-zero ideals and the actual noncommutative Jacobson radical

An actual square-zero left ideal is contained in the ring Jacobson
radical. For a surjective ring homomorphism with square-zero kernel,
the actual source radical is exactly the preimage of the target radical.
The arguments use maximal left ideals and require no commutativity,
field, finiteness or characteristic hypothesis on the two rings.
-/

namespace ARCSquareZeroJacobson

variable {A B : Type*} [Ring A] [Ring B]

theorem squareZero_le_jacobson (I : Ideal A)
    (hI : ∀ x y : A, x ∈ I → y ∈ I → x * y = 0) : I ≤ Ring.jacobson A := by
  intro x hx
  rw [← Ideal.jacobson_bot]
  apply Ideal.mem_jacobson_iff.mpr
  intro y
  have ht : y * x ∈ I := I.mul_mem_left y hx
  have ht2 : (y * x) * (y * x) = 0 := hI _ _ ht ht
  refine ⟨1 - y * x, ?_⟩
  rw [Ideal.mem_bot, mul_assoc, sub_mul, one_mul, ht2, sub_zero]
  abel

/-- An ideal already contained in the ring radical has that radical as its Jacobson ideal. -/
theorem jacobson_eq_of_le (I : Ideal A) (hI : I ≤ Ring.jacobson A) :
    I.jacobson = Ring.jacobson A := by
  apply le_antisymm
  · have h := Ideal.jacobson_mono hI
    simpa only [← Ideal.jacobson_bot, Ideal.jacobson_idem] using h
  · exact Ideal.ringJacobson_le_jacobson

/-- Full radical equality for a surjection with an actual square-zero kernel. -/
theorem radical_comap (f : A →+* B) (hf : Function.Surjective f)
    (hker : ∀ x y : A, x ∈ RingHom.ker f → y ∈ RingHom.ker f → x * y = 0) :
    Ring.jacobson A = Ideal.comap f (Ring.jacobson B) := by
  rw [← Ideal.jacobson_bot (R := B), Ideal.comap_jacobson_of_surjective hf,
    ← RingHom.ker_eq_comap_bot f]
  exact (jacobson_eq_of_le (RingHom.ker f)
    (squareZero_le_jacobson (RingHom.ker f) hker)).symm

#print axioms squareZero_le_jacobson
#print axioms jacobson_eq_of_le
#print axioms radical_comap

end ARCSquareZeroJacobson
