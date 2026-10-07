import TableBasisSemantics

/-!
Sparse lists are converted to finite structure-constant contractions in
genuine F₂[X] vectors. Duplicate output labels are permitted. The generic
contraction proof needs only output-label bounds, not coefficient bounds.
The concrete associativity theorem imports the existing packed certificate
and its separately proved polynomial-vector semantic transport.
-/

namespace ARCFiniteTableContraction

open ARCFiniteCore ARCBitPolynomial ARCTermSemantics ARCTableBasisSemantics
open scoped BigOperators

noncomputable section

/-- A sparse weighted sum contracts through its combined structure constants.
Only the finite output-label bound is needed; duplicate labels add normally. -/
theorem finite_list_contraction (n : Nat) (terms : Terms)
    (hbound : ∀ term ∈ terms, term.1 < n) (g : Nat → PolyVector) :
    terms.foldr (fun term vec => scale term.2 (g term.1) + vec) 0 =
      fun k => ∑ j : Fin n, sumTerms terms j.val * g j.val k := by
  induction terms with
  | nil =>
      funext k
      simp
  | cons term terms ih =>
      have hterm : term.1 < n := hbound term (List.mem_cons_self ..)
      have htail : ∀ t ∈ terms, t.1 < n := fun t ht =>
        hbound t (List.mem_cons_of_mem _ ht)
      rw [List.foldr_cons, ih htail]
      funext k
      change decode term.2 * g term.1 k +
          (∑ j : Fin n, sumTerms terms j.val * g j.val k) =
        ∑ j : Fin n, (singleTerm term.1 term.2 j.val + sumTerms terms j.val) * g j.val k
      simp_rw [add_mul]
      rw [Finset.sum_add_distrib]
      congr 1
      symm
      let J : Fin n := ⟨term.1, hterm⟩
      calc
        (∑ j : Fin n, singleTerm term.1 term.2 j.val * g j.val k) =
            singleTerm term.1 term.2 J.val * g J.val k := by
          apply Finset.sum_eq_single J
          · intro b hb hne
            have hv : b.val ≠ term.1 := by
              intro h
              apply hne
              exact Fin.ext h
            simp [singleTerm, hv]
          · intro hJ
            simp at hJ
        _ = decode term.2 * g term.1 k := by simp [singleTerm, J]

/-- A finite family is extended by zero only to express the total list fold. -/
def extendFamily (n : Nat) (g : Fin n → PolyVector) : Nat → PolyVector :=
  fun j => if hj : j < n then g ⟨j, hj⟩ else 0

/-- Finite-indexed version of the generic sparse contraction. -/
theorem finite_list_contraction_fin (n : Nat) (terms : Terms)
    (hbound : ∀ term ∈ terms, term.1 < n) (g : Fin n → PolyVector) :
    terms.foldr (fun term vec => scale term.2 (extendFamily n g term.1) + vec) 0 =
      fun k => ∑ j : Fin n, sumTerms terms j.val * g j k := by
  rw [finite_list_contraction n terms hbound (extendFamily n g)]
  funext k
  congr 1
  funext j
  simp [extendFamily, j.isLt]

/-- Genuine left-associated basis multiplication is a finite contraction. -/
theorem leftVectorProduct_finite (n : Nat) (table : Nat → Nat → Terms) (a b c : Nat)
    (hbound : ∀ term ∈ table a b, term.1 < n) :
    leftVectorProduct table a b c =
      fun k => ∑ j : Fin n, sumTerms (table a b) j.val * sumTerms (table j.val c) k := by
  exact finite_list_contraction n (table a b) hbound (fun j => sumTerms (table j c))

/-- Genuine right-associated basis multiplication is a finite contraction. -/
theorem rightVectorProduct_finite (n : Nat) (table : Nat → Nat → Terms) (a b c : Nat)
    (hbound : ∀ term ∈ table b c, term.1 < n) :
    rightVectorProduct table a b c =
      fun k => ∑ j : Fin n, sumTerms (table b c) j.val * sumTerms (table a j.val) k := by
  exact finite_list_contraction n (table b c) hbound (fun j => sumTerms (table a j))

/-- The finite structure constants of the explicit twenty-label table. -/
def tConstants (a b k : Fin 20) : Polynomial (ZMod 2) :=
  sumTerms (tTerms a.val b.val) k.val

/-- All structure-constant associativity equations, in actual polynomial values. -/
theorem t_structure_constants_associativity (a b c k : Fin 20) :
    (∑ j : Fin 20, tConstants a b j * tConstants j c k) =
      ∑ j : Fin 20, tConstants b c j * tConstants a j k := by
  have hab : ∀ term ∈ tTerms a.val b.val, term.1 < 20 := by
    simpa only [List.all_eq_true, decide_eq_true_eq] using t_output_basis_bound a b
  have hbc : ∀ term ∈ tTerms b.val c.val, term.1 < 20 := by
    simpa only [List.all_eq_true, decide_eq_true_eq] using t_output_basis_bound b c
  have h := congrArg (fun v : PolyVector => v k.val) (t_basis_polynomial_associativity a b c)
  rw [leftVectorProduct_finite 20 tTerms a.val b.val c.val hab,
    rightVectorProduct_finite 20 tTerms a.val b.val c.val hbc] at h
  exact h

#print axioms finite_list_contraction
#print axioms finite_list_contraction_fin
#print axioms leftVectorProduct_finite
#print axioms rightVectorProduct_finite
#print axioms t_structure_constants_associativity

end
end ARCFiniteTableContraction
