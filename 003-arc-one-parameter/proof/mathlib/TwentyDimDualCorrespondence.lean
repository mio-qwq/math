import TracePairSemantics

/-!
# Polynomial blocks of the concrete dual-extension table

The frozen dual-recurrence certificate is interpreted in genuine polynomial
structure constants. Zero coefficients are omitted without changing their
meaning. No new finite enumeration is used. An algebra comparison map and
the complete homological realization are separate subsequent statements.
-/

namespace ARCTwentyDimDualCorrespondence

open ARCFiniteCore ARCBitPolynomial ARCTermSemantics
open ARCFiniteTableContraction ARCTracePairSemantics ARCTwentyDimAssociativity

noncomputable section

/-- Sparse coordinates obtained from arbitrary natural-number coefficient codes. -/
def sparseCoefficients (n offset : Nat) (coeff : Nat → Nat) : Terms :=
  (List.range n).filterMap (fun j =>
    if coeff j = 0 then none else some (j + offset, coeff j))

theorem sumTerms_append (xs ys : Terms) :
    sumTerms (xs ++ ys) = sumTerms xs + sumTerms ys := by
  induction xs with
  | nil => simp
  | cons x xs ih => simp [ih, add_assoc]

private theorem sparseCoefficients_succ (n offset : Nat) (coeff : Nat → Nat) :
    sparseCoefficients (n + 1) offset coeff =
      sparseCoefficients n offset coeff ++
        (if coeff n = 0 then [] else [(n + offset, coeff n)]) := by
  simp only [sparseCoefficients, List.range_succ, List.filterMap_append]
  split_ifs <;> simp_all

/-- Zero filtering preserves the exact decoded coefficient, with no byte bound. -/
theorem sumTerms_sparseCoefficients (n offset : Nat) (coeff : Nat → Nat) (k : Nat) :
    sumTerms (sparseCoefficients n offset coeff) (k + offset) =
      if k < n then decode (coeff k) else 0 := by
  induction n with
  | zero => simp [sparseCoefficients]
  | succ n ih =>
    rw [sparseCoefficients_succ, sumTerms_append]
    change sumTerms (sparseCoefficients n offset coeff) (k + offset) +
        sumTerms (if coeff n = 0 then [] else [(n + offset, coeff n)])
          (k + offset) = _
    have hsingle :
        sumTerms (if coeff n = 0 then [] else [(n + offset, coeff n)])
          (k + offset) = if k = n then decode (coeff n) else 0 := by
      by_cases hzero : coeff n = 0
      · simp [hzero, decode_zero]
      · simp [hzero, singleTerm, Nat.add_right_cancel_iff]
    rw [ih, hsingle]
    by_cases hlt : k < n
    · have hne : k ≠ n := by omega
      have hlt' : k < n + 1 := by omega
      simp [hlt, hne, hlt']
    · by_cases heq : k = n
      · subst k
        simp
      · have hlt' : ¬ k < n + 1 := by omega
        simp [hlt, heq, hlt']

/-- Shifted sparse coordinates have no component below the shift. -/
theorem sumTerms_sparseCoefficients_below (n offset : Nat) (coeff : Nat → Nat)
    (k : Nat) (hk : k < offset) :
    sumTerms (sparseCoefficients n offset coeff) k = 0 := by
  induction n with
  | zero => simp [sparseCoefficients]
  | succ n ih =>
    rw [sparseCoefficients_succ, sumTerms_append]
    change sumTerms (sparseCoefficients n offset coeff) k +
        sumTerms (if coeff n = 0 then [] else [(n + offset, coeff n)]) k = 0
    have hne : k ≠ n + offset := by omega
    rw [ih]
    by_cases hzero : coeff n = 0 <;> simp [hzero, singleTerm, hne]

private theorem sumTerms_zero_outside (terms : Terms) (k : Nat)
    (h : ∀ term ∈ terms, term.1 ≠ k) : sumTerms terms k = 0 := by
  induction terms with
  | nil => simp
  | cons term terms ih =>
    have hterm := h term (List.mem_cons_self ..)
    have htail : ∀ t ∈ terms, t.1 ≠ k := fun t ht =>
      h t (List.mem_cons_of_mem _ ht)
    simp [sumTerms_cons, singleTerm, Ne.symm hterm, ih htail]

/-- Lowercase and uppercase embeddings into the actual twenty-label table. -/
def lowerIndex (a : Fin 10) : Fin 20 := ⟨a.val, by omega⟩

def upperIndex (a : Fin 10) : Fin 20 := ⟨a.val + 10, by omega⟩

/-- Genuine polynomial structure constants of the original ten-label core. -/
def coreConstants (a b k : Fin 10) : Polynomial (ZMod 2) :=
  sumTerms (cTerms a.val b.val) k.val

private theorem lower_lower_terms (a b : Fin 10) :
    tTerms a.val b.val = cTerms a.val b.val := by
  have h := t_table_matches_dual_recurrence (lowerIndex a) (lowerIndex b)
  simpa [lowerIndex, tByDualRecurrence, a.isLt, b.isLt] using h

private theorem lower_upper_terms (a b : Fin 10) :
    tTerms a.val (b.val + 10) =
      sparseCoefficients 10 10 (fun j => coefficient (cTerms j a.val) b.val) := by
  have h := t_table_matches_dual_recurrence (lowerIndex a) (upperIndex b)
  have hb : ¬ b.val + 10 < 10 := by omega
  simpa [lowerIndex, upperIndex, tByDualRecurrence, sparseCoefficients,
    a.isLt, hb] using h

private theorem upper_lower_terms (a b : Fin 10) :
    tTerms (a.val + 10) b.val =
      sparseCoefficients 10 10 (fun j => coefficient (cTerms b.val j) a.val) := by
  have h := t_table_matches_dual_recurrence (upperIndex a) (lowerIndex b)
  have ha : ¬ a.val + 10 < 10 := by omega
  simpa [lowerIndex, upperIndex, tByDualRecurrence, sparseCoefficients,
    b.isLt, ha] using h

private theorem upper_upper_terms (a b : Fin 10) :
    tTerms (a.val + 10) (b.val + 10) = [] := by
  have h := t_table_matches_dual_recurrence (upperIndex a) (upperIndex b)
  have ha : ¬ a.val + 10 < 10 := by omega
  have hb : ¬ b.val + 10 < 10 := by omega
  simpa [upperIndex, tByDualRecurrence, ha, hb] using h

theorem lower_lower_lower (a b k : Fin 10) :
    tConstants (lowerIndex a) (lowerIndex b) (lowerIndex k) = coreConstants a b k := by
  change sumTerms (tTerms a.val b.val) k.val = _
  rw [lower_lower_terms]
  rfl

theorem lower_lower_upper (a b k : Fin 10) :
    tConstants (lowerIndex a) (lowerIndex b) (upperIndex k) = 0 := by
  change sumTerms (tTerms a.val b.val) (k.val + 10) = 0
  rw [lower_lower_terms]
  apply sumTerms_zero_outside
  have hbound : ∀ term ∈ cTerms a.val b.val, term.1 < 10 := by
    simpa only [List.all_eq_true, decide_eq_true_eq] using c_output_basis_bound a b
  intro term ht
  have h := hbound term ht
  omega

theorem lower_upper_lower (a b k : Fin 10) :
    tConstants (lowerIndex a) (upperIndex b) (lowerIndex k) = 0 := by
  change sumTerms (tTerms a.val (b.val + 10)) k.val = 0
  rw [lower_upper_terms]
  exact sumTerms_sparseCoefficients_below 10 10 _ k.val k.isLt

/-- Left multiplication by a core basis vector acts by the right regular transpose. -/
theorem lower_upper_upper (a b k : Fin 10) :
    tConstants (lowerIndex a) (upperIndex b) (upperIndex k) = coreConstants k a b := by
  change sumTerms (tTerms a.val (b.val + 10)) (k.val + 10) = _
  rw [lower_upper_terms, sumTerms_sparseCoefficients]
  simp only [k.isLt, ite_true, decode_coefficient, coreConstants]

theorem upper_lower_lower (a b k : Fin 10) :
    tConstants (upperIndex a) (lowerIndex b) (lowerIndex k) = 0 := by
  change sumTerms (tTerms (a.val + 10) b.val) k.val = 0
  rw [upper_lower_terms]
  exact sumTerms_sparseCoefficients_below 10 10 _ k.val k.isLt

/-- Right multiplication by a core basis vector acts by the left regular transpose. -/
theorem upper_lower_upper (a b k : Fin 10) :
    tConstants (upperIndex a) (lowerIndex b) (upperIndex k) = coreConstants b k a := by
  change sumTerms (tTerms (a.val + 10) b.val) (k.val + 10) = _
  rw [upper_lower_terms, sumTerms_sparseCoefficients]
  simp only [k.isLt, ite_true, decode_coefficient, coreConstants]

theorem upper_upper_lower (a b k : Fin 10) :
    tConstants (upperIndex a) (upperIndex b) (lowerIndex k) = 0 := by
  change sumTerms (tTerms (a.val + 10) (b.val + 10)) k.val = 0
  rw [upper_upper_terms]
  simp

theorem upper_upper_upper (a b k : Fin 10) :
    tConstants (upperIndex a) (upperIndex b) (upperIndex k) = 0 := by
  change sumTerms (tTerms (a.val + 10) (b.val + 10)) (k.val + 10) = 0
  rw [upper_upper_terms]
  simp

variable {R : Type*} [CommRing R] [CharP R 2]

def specializedCoreConstants (q : R) (a b k : Fin 10) : R :=
  specialize q (coreConstants a b k)

/-- All eight polynomial block equations survive every characteristic-two specialization. -/
theorem specialized_block_equations (q : R) (a b k : Fin 10) :
    specializedConstants q (lowerIndex a) (lowerIndex b) (lowerIndex k) =
      specializedCoreConstants q a b k ∧
    specializedConstants q (lowerIndex a) (lowerIndex b) (upperIndex k) = 0 ∧
    specializedConstants q (lowerIndex a) (upperIndex b) (lowerIndex k) = 0 ∧
    specializedConstants q (lowerIndex a) (upperIndex b) (upperIndex k) =
      specializedCoreConstants q k a b ∧
    specializedConstants q (upperIndex a) (lowerIndex b) (lowerIndex k) = 0 ∧
    specializedConstants q (upperIndex a) (lowerIndex b) (upperIndex k) =
      specializedCoreConstants q b k a ∧
    specializedConstants q (upperIndex a) (upperIndex b) (lowerIndex k) = 0 ∧
    specializedConstants q (upperIndex a) (upperIndex b) (upperIndex k) = 0 := by
  simp [specializedConstants, specializedCoreConstants,
    lower_lower_lower, lower_lower_upper, lower_upper_lower, lower_upper_upper,
    upper_lower_lower, upper_lower_upper, upper_upper_lower, upper_upper_upper, map_zero]

#print axioms sumTerms_sparseCoefficients
#print axioms sumTerms_sparseCoefficients_below
#print axioms lower_lower_lower
#print axioms lower_lower_upper
#print axioms lower_upper_lower
#print axioms lower_upper_upper
#print axioms upper_lower_lower
#print axioms upper_lower_upper
#print axioms upper_upper_lower
#print axioms upper_upper_upper
#print axioms specialized_block_equations

end
end ARCTwentyDimDualCorrespondence
