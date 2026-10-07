import TwentyDimCochain
import TwentyDimAugmentation
import ScalarEvaluation
import Mathlib.Algebra.CharP.Two

/-!
# Idempotent compatibility and full-input cochain closure

The new finite checks concern only the 8,000 cochain input triples, their
corner support, normalization, and the two idempotent actions. The existing
radical four-word certificate is reused, not enumerated again.
-/

namespace ARCCochainIdempotentClosure

open ARCFiniteCore ARCBitPolynomial ARCTermSemantics ARCFiniteTableContraction
open ARCCochainBasisSemantics ARCCochainSpecialization ARCTwentyDimAssociativity
open ARCTwentyDimCochain ARCFiniteTrilinear
open scoped BigOperators

/-- Uppercase dual basis vectors exchange the two corner endpoints. -/
def tLeft (a : Nat) : Nat := if a < 10 then cLeft a else cRight (a - 10)
def tRight (a : Nat) : Nat := if a < 10 then cRight a else cLeft (a - 10)

def idempotentIndex (s : Fin 2) : Fin 20 := ⟨8 * s.val, by omega⟩

/-- Exactly 8,000 support checks, with no four-word closure enumeration. -/
theorem p_corner_certificate : ∀ a b c : Fin 20,
    (pTerms a.val b.val c.val).all (fun t =>
      tLeft t.1 = tLeft a.val && tRight t.1 = tRight c.val &&
      tRight a.val = tLeft b.val && tRight b.val = tLeft c.val) = true := by
  set_option maxRecDepth 20000 in
  set_option maxHeartbeats 0 in
  decide

theorem t_idempotent_left_certificate : ∀ s : Fin 2, ∀ a : Fin 20,
    tTerms (idempotentIndex s).val a.val =
      if tLeft a.val = (idempotentIndex s).val then [(a.val, 1)] else [] := by decide

theorem t_idempotent_right_certificate : ∀ s : Fin 2, ∀ a : Fin 20,
    tTerms a.val (idempotentIndex s).val =
      if tRight a.val = (idempotentIndex s).val then [(a.val, 1)] else [] := by decide

theorem p_normalized_certificate : ∀ s : Fin 2, ∀ a b : Fin 20,
    pTerms (idempotentIndex s).val a.val b.val = [] ∧
      pTerms a.val (idempotentIndex s).val b.val = [] ∧
      pTerms a.val b.val (idempotentIndex s).val = [] := by
  set_option maxRecDepth 20000 in
  set_option maxHeartbeats 0 in
  decide

noncomputable section

private theorem sumTerms_zero_no_output (terms : Terms) (k : Nat)
    (h : ∀ t ∈ terms, t.1 ≠ k) : sumTerms terms k = 0 := by
  induction terms with
  | nil => rfl
  | cons t terms ih =>
      have ht := h t (List.mem_cons_self ..)
      have htail : ∀ x ∈ terms, x.1 ≠ k := fun x hx => h x (List.mem_cons_of_mem _ hx)
      simp [sumTerms_cons, singleTerm, Ne.symm ht, ih htail]

private theorem p_corner_support (a b c k : Fin 20) (hp : pConstants a b c k ≠ 0) :
    tLeft k.val = tLeft a.val ∧ tRight k.val = tRight c.val ∧
      tRight a.val = tLeft b.val ∧ tRight b.val = tLeft c.val := by
  have hterms : ∀ t ∈ pTerms a.val b.val c.val,
      tLeft t.1 = tLeft a.val ∧ tRight t.1 = tRight c.val ∧
        tRight a.val = tLeft b.val ∧ tRight b.val = tLeft c.val := by
    simpa only [List.all_eq_true, Bool.and_eq_true, decide_eq_true_eq, and_assoc] using
      p_corner_certificate a b c
  by_contra hn
  apply hp
  apply sumTerms_zero_no_output
  intro t ht htk
  apply hn
  simpa only [htk] using hterms t ht

theorem pConstants_normalized (s : Fin 2) (a b k : Fin 20) :
    pConstants (idempotentIndex s) a b k = 0 ∧
      pConstants a (idempotentIndex s) b k = 0 ∧
      pConstants a b (idempotentIndex s) k = 0 := by
  have h := p_normalized_certificate s a b
  simp only [pConstants, h.1, h.2.1, h.2.2, sumTerms_nil, Pi.zero_apply, and_self]

theorem tConstants_idempotent_left (s : Fin 2) (a k : Fin 20) :
    tConstants (idempotentIndex s) a k =
      if tLeft a.val = (idempotentIndex s).val then (if a = k then 1 else 0) else 0 := by
  unfold tConstants
  rw [t_idempotent_left_certificate]
  split_ifs <;> simp_all [sumTerms, singleTerm, ARCScalarEvaluation.decode_one,
    Fin.val_inj, eq_comm]

theorem tConstants_idempotent_right (s : Fin 2) (a k : Fin 20) :
    tConstants a (idempotentIndex s) k =
      if tRight a.val = (idempotentIndex s).val then (if a = k then 1 else 0) else 0 := by
  unfold tConstants
  rw [t_idempotent_right_certificate]
  split_ifs <;> simp_all [sumTerms, singleTerm, ARCScalarEvaluation.decode_one,
    Fin.val_inj, eq_comm]

variable {R : Type*} [CommRing R] [CharP R 2]

theorem specializedP_normalized (q : R) (s : Fin 2) (a b k : Fin 20) :
    specializedCochainConstants q (idempotentIndex s) a b k = 0 ∧
      specializedCochainConstants q a (idempotentIndex s) b k = 0 ∧
      specializedCochainConstants q a b (idempotentIndex s) k = 0 := by
  have h := pConstants_normalized s a b k
  simp [specializedCochainConstants, h.1, h.2.1, h.2.2]

theorem specializedB_idempotent_left (q : R) (s : Fin 2) (a k : Fin 20) :
    specializedConstants q (idempotentIndex s) a k =
      if tLeft a.val = (idempotentIndex s).val then (if a = k then 1 else 0) else 0 := by
  unfold specializedConstants
  rw [tConstants_idempotent_left]
  split_ifs <;> simp

theorem specializedB_idempotent_right (q : R) (s : Fin 2) (a k : Fin 20) :
    specializedConstants q a (idempotentIndex s) k =
      if tRight a.val = (idempotentIndex s).val then (if a = k then 1 else 0) else 0 := by
  unfold specializedConstants
  rw [tConstants_idempotent_right]
  split_ifs <;> simp

private theorem specializedP_support (q : R) (a b c k : Fin 20)
    (hp : specializedCochainConstants q a b c k ≠ 0) :
    tLeft k.val = tLeft a.val ∧ tRight k.val = tRight c.val ∧
      tRight a.val = tLeft b.val ∧ tRight b.val = tLeft c.val := by
  apply p_corner_support a b c k
  intro hz
  apply hp
  simp [specializedCochainConstants, hz]

@[simp] theorem specializedP_normalized_first (q : R) (s : Fin 2) (a b k : Fin 20) :
    specializedCochainConstants q (idempotentIndex s) a b k = 0 :=
  (specializedP_normalized q s a b k).1

@[simp] theorem specializedP_normalized_second (q : R) (s : Fin 2) (a b k : Fin 20) :
    specializedCochainConstants q a (idempotentIndex s) b k = 0 :=
  (specializedP_normalized q s a b k).2.1

@[simp] theorem specializedP_normalized_third (q : R) (s : Fin 2) (a b k : Fin 20) :
    specializedCochainConstants q a b (idempotentIndex s) k = 0 :=
  (specializedP_normalized q s a b k).2.2

private theorem guard_left (q : R) (s : Fin 2) (a b c k : Fin 20) :
    (if tLeft k.val = (idempotentIndex s).val then specializedCochainConstants q a b c k else 0) =
    if tLeft a.val = (idempotentIndex s).val then specializedCochainConstants q a b c k else 0 := by
  by_cases hp : specializedCochainConstants q a b c k = 0
  · simp [hp]
  · rw [(specializedP_support q a b c k hp).1]

private theorem guard_middle_first (q : R) (s : Fin 2) (a b c k : Fin 20) :
    (if tRight a.val = (idempotentIndex s).val then specializedCochainConstants q a b c k else 0) =
    if tLeft b.val = (idempotentIndex s).val then specializedCochainConstants q a b c k else 0 := by
  by_cases hp : specializedCochainConstants q a b c k = 0
  · simp [hp]
  · rw [(specializedP_support q a b c k hp).2.2.1]

private theorem guard_middle_second (q : R) (s : Fin 2) (a b c k : Fin 20) :
    (if tRight b.val = (idempotentIndex s).val then specializedCochainConstants q a b c k else 0) =
    if tLeft c.val = (idempotentIndex s).val then specializedCochainConstants q a b c k else 0 := by
  by_cases hp : specializedCochainConstants q a b c k = 0
  · simp [hp]
  · rw [(specializedP_support q a b c k hp).2.2.2]

private theorem guard_right (q : R) (s : Fin 2) (a b c k : Fin 20) :
    (if tRight k.val = (idempotentIndex s).val then specializedCochainConstants q a b c k else 0) =
    if tRight c.val = (idempotentIndex s).val then specializedCochainConstants q a b c k else 0 := by
  by_cases hp : specializedCochainConstants q a b c k = 0
  · simp [hp]
  · rw [(specializedP_support q a b c k hp).2.1]

omit [CharP R 2] in
private theorem sum_guard_delta (t : Fin 20 → Nat) (e : Nat) (v : Fin 20 → R)
    (k : Fin 20) :
    (∑ j, if t j = e then (if j = k then v j else 0) else 0) =
      if t k = e then v k else 0 := by
  classical
  rw [Finset.sum_eq_single k]
  · simp
  · intro j _ hj
    simp [hj]
  · simp

theorem specialized_idempotent_first_zero (q : R) (s : Fin 2) (a b c k : Fin 20) :
    specializedFiveTermCoefficient q (idempotentIndex s) a b c k = 0 := by
  simp [specializedFiveTermCoefficient, specializedB_idempotent_left, mul_ite, ite_mul]
  rw [sum_guard_delta, guard_left]
  exact CharTwo.add_self_eq_zero _

theorem specialized_idempotent_second_zero (q : R) (s : Fin 2) (a b c k : Fin 20) :
    specializedFiveTermCoefficient q a (idempotentIndex s) b c k = 0 := by
  simp [specializedFiveTermCoefficient, specializedB_idempotent_left,
    specializedB_idempotent_right, ite_mul]
  rw [guard_middle_first]
  exact CharTwo.add_self_eq_zero _

theorem specialized_idempotent_third_zero (q : R) (s : Fin 2) (a b c k : Fin 20) :
    specializedFiveTermCoefficient q a b (idempotentIndex s) c k = 0 := by
  simp [specializedFiveTermCoefficient, specializedB_idempotent_left,
    specializedB_idempotent_right, ite_mul]
  rw [guard_middle_second]
  exact CharTwo.add_self_eq_zero _

theorem specialized_idempotent_fourth_zero (q : R) (s : Fin 2) (a b c k : Fin 20) :
    specializedFiveTermCoefficient q a b c (idempotentIndex s) k = 0 := by
  simp [specializedFiveTermCoefficient, specializedB_idempotent_right, mul_ite, ite_mul]
  rw [sum_guard_delta, guard_right]
  exact CharTwo.add_self_eq_zero _

private theorem basis_cases (k : Fin 20) :
    (∃ s : Fin 2, idempotentIndex s = k) ∨
      (∃ a : Fin 18, radicalBasis a = k) := by
  by_cases hk0 : k = 0
  · subst k
    exact Or.inl ⟨0, rfl⟩
  by_cases hk8 : k = 8
  · subst k
    exact Or.inl ⟨1, rfl⟩
  exact Or.inr (ARCTwentyDimAugmentation.radicalBasis_covers k hk0 hk8)

/-- Full twenty-label closure: idempotent cases use corner compatibility,
and the remaining case reuses the frozen radical certificate. -/
theorem specialized_all_basis_five_term_zero
    (q : R) (a b c d k : Fin 20) :
    specializedFiveTermCoefficient q a b c d k = 0 := by
  rcases basis_cases a with ⟨s, rfl⟩ | ⟨a, rfl⟩
  · exact specialized_idempotent_first_zero q s b c d k
  · rcases basis_cases b with ⟨s, rfl⟩ | ⟨b, rfl⟩
    · exact specialized_idempotent_second_zero q s (radicalBasis a) c d k
    · rcases basis_cases c with ⟨s, rfl⟩ | ⟨c, rfl⟩
      · exact specialized_idempotent_third_zero q s (radicalBasis a) (radicalBasis b) d k
      · rcases basis_cases d with ⟨s, rfl⟩ | ⟨d, rfl⟩
        · exact specialized_idempotent_fourth_zero q s (radicalBasis a)
            (radicalBasis b) (radicalBasis c) k
        · exact specialized_radical_basis_five_term_zero q a b c d k

theorem specialized_differential_all_basis_zero
    (q : R) (a b c d : Fin 20) :
    specializedDifferential3 q (basis a) (basis b) (basis c) (basis d) = 0 := by
  funext k
  rw [specialized_differential_basis_coefficient]
  exact specialized_all_basis_five_term_zero q a b c d k

omit [CharP R 2] in
private theorem span_id (U : Fin 20 → R) : ARCFiniteHochschild.span id U = U := by
  classical
  funext k
  simp [ARCFiniteHochschild.span, basis, Finset.sum_apply]

/-- The explicit cochain has zero five-face differential on all vectors,
over every commutative characteristic-two coefficient ring and parameter.
This extends the earlier radical-span identity without a 20^4 enumeration. -/
theorem specialized_all_vector_closure
    (q : R) (u v w z : Fin 20 → R) :
    specializedDifferential3 q u v w z = 0 := by
  have h := ARCFiniteHochschild.basis_span_closure
    (specializedConstants q) (specializedCochainConstants q) id
    (specialized_differential_all_basis_zero q) u v w z
  simpa only [span_id, specializedDifferential3] using h

#print axioms p_corner_certificate
#print axioms p_normalized_certificate
#print axioms tConstants_idempotent_left
#print axioms specializedP_support
#print axioms specialized_idempotent_first_zero
#print axioms specialized_idempotent_second_zero
#print axioms specialized_idempotent_third_zero
#print axioms specialized_idempotent_fourth_zero
#print axioms specialized_all_basis_five_term_zero
#print axioms specialized_differential_all_basis_zero
#print axioms specialized_all_vector_closure

end
end ARCCochainIdempotentClosure
