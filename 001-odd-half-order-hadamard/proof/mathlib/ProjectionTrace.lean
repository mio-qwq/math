import Mathlib.LinearAlgebra.Trace
import Std

/-!
The projection trace obstruction over any characteristic-zero field.
The main paper must still supply the idempotent operator and its trace formula.
This file does not formalize the full complex-matrix theorem.
-/

namespace OddHalfOrder

theorem idempotent_odd_trace_obstruction
    {K M : Type*} [Field K] [CharZero K]
    [AddCommGroup M] [Module K M] [Module.Finite K M]
    (f : Module.End K M) (hf : IsIdempotentElem f)
    (m : Nat) (hodd : ∃ s : Nat, m = 2 * s + 1)
    (htrace : 2 * LinearMap.trace K M f = (m : K)) : False := by
  have hrank : LinearMap.trace K M f =
      (Module.finrank K (LinearMap.range f) : K) :=
    (LinearMap.IsIdempotentElem.isProj_range f hf).trace
  have hcast : ((2 * Module.finrank K (LinearMap.range f) : Nat) : K) = (m : K) := by
    rw [Nat.cast_mul, Nat.cast_ofNat, ← hrank]
    exact htrace
  have heq : 2 * Module.finrank K (LinearMap.range f) = m := Nat.cast_injective hcast
  obtain ⟨s, hs⟩ := hodd
  omega

#print axioms idempotent_odd_trace_obstruction

end OddHalfOrder
