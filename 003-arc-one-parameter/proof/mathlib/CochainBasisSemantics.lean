import CochainClosure
import FiniteTableContraction

/-!
# Polynomial semantics of the five-term radical-basis certificate

The frozen packed closure identities are transported to actual finite sums
in F₂[X]. The transport uses bounds on each coefficient that is packed; it
does not truncate polynomial multiplication or repeat the table enumeration.

The conclusion concerns the eighteen specified radical basis labels. This
file does not construct a relative Hochschild complex, prove balancing, or
identify a Hochschild-cohomology or Ext class.
-/

namespace ARCCochainBasisSemantics

open ARCFiniteCore ARCBitPolynomial ARCBytePacking ARCTermSemantics
open ARCFiniteTableContraction
open scoped BigOperators

noncomputable section

/-- The cochain's genuine polynomial-valued structure coefficients. -/
def pConstants (a b c k : Fin 20) : Polynomial (ZMod 2) :=
  sumTerms (pTerms a.val b.val c.val) k.val

/-- The frozen radical-label enumeration, now as an actual twenty-label index. -/
def radicalBasis (a : Fin 18) : Fin 20 :=
  ⟨radicalIndex a, by
    unfold radicalIndex
    split_ifs <;> omega⟩

@[simp] theorem radicalBasis_val (a : Fin 18) :
    (radicalBasis a).val = radicalIndex a := rfl

/-- The existing small-coefficient certificate bounds each packed product. -/
theorem small_product_bound {s t : Nat} (hs : s < 16) (ht : t < 16) :
    pMul s t < 256 :=
  certificate_coefficient_product_bound ⟨s, hs⟩ ⟨t, ht⟩

private theorem p_term_bounds (a b c : Fin 20) (term : Nat × Nat)
    (hterm : term ∈ pTerms a.val b.val c.val) :
    term.1 < 20 ∧ term.2 < 16 := by
  have h : ∀ t ∈ pTerms a.val b.val c.val, t.1 < 20 ∧ t.2 < 16 := by
    simpa only [List.all_eq_true, Bool.and_eq_true, decide_eq_true_eq] using
      p_coefficient_and_output_bounds a b c
  exact h term hterm

private theorem t_term_bounds (a b : Fin 20) (term : Nat × Nat)
    (hterm : term ∈ tTerms a.val b.val) :
    term.1 < 20 ∧ term.2 < 16 := by
  have hout : ∀ t ∈ tTerms a.val b.val, t.1 < 20 := by
    simpa only [List.all_eq_true, decide_eq_true_eq] using t_output_basis_bound a b
  have hcoeff : ∀ t ∈ tTerms a.val b.val, t.2 < 16 := by
    simpa only [List.all_eq_true, decide_eq_true_eq] using t_coefficient_bound a b
  exact ⟨hout term hterm, hcoeff term hterm⟩

/-- A generic packed sparse contraction becomes a genuine finite contraction.
Repeated output labels are allowed. Only actually packed coefficient products
need to fit the byte blocks; the resulting polynomial sum is not truncated. -/
theorem scaled_fold_contraction (n : Nat) (terms : Terms) (family : Nat → Terms)
    (houtput : ∀ term ∈ terms, term.1 < n)
    (hproduct : ∀ term ∈ terms, ∀ inner ∈ family term.1,
      pMul term.2 inner.2 < 256) :
    decodeVec (terms.foldl (fun acc term =>
      Nat.xor acc (scaleEncode term.2 (family term.1))) 0) =
      fun k => ∑ j : Fin n, sumTerms terms j.val * sumTerms (family j.val) k := by
  have hfold := xorFoldl_semantics terms
    (fun term => scaleEncode term.2 (family term.1))
    (fun term => scale term.2 (sumTerms (family term.1))) 0
    (fun term hterm => decode_scaleEncode term.2 (family term.1)
      (hproduct term hterm))
  rw [decodeVec_zero, zero_add] at hfold
  rw [hfold]
  exact finite_list_contraction n terms houtput (fun j => sumTerms (family j))

/-- Semantics of the left outer face: multiply a basis label by the cochain. -/
theorem tTimesP_polynomial (a b c d k : Fin 20) :
    decodeVec (tTimesP a.val (pTerms b.val c.val d.val)) k.val =
      ∑ j : Fin 20, pConstants b c d j * tConstants a j k := by
  have hout : ∀ term ∈ pTerms b.val c.val d.val, term.1 < 20 :=
    fun term hterm => (p_term_bounds b c d term hterm).1
  have hprod : ∀ term ∈ pTerms b.val c.val d.val,
      ∀ inner ∈ tTerms a.val term.1, pMul term.2 inner.2 < 256 := by
    intro term hterm inner hinner
    have ht := p_term_bounds b c d term hterm
    exact small_product_bound ht.2
      (t_term_bounds a ⟨term.1, ht.1⟩ inner hinner).2
  exact congrArg (fun v : PolyVector => v k.val)
    (scaled_fold_contraction 20 (pTerms b.val c.val d.val)
      (fun j => tTerms a.val j) hout hprod)

/-- Semantics of the first inner face. -/
theorem pApplyFirst_polynomial (a b c d k : Fin 20) :
    decodeVec (pApplyFirst (tTerms a.val b.val) c.val d.val) k.val =
      ∑ j : Fin 20, tConstants a b j * pConstants j c d k := by
  have hout : ∀ term ∈ tTerms a.val b.val, term.1 < 20 :=
    fun term hterm => (t_term_bounds a b term hterm).1
  have hprod : ∀ term ∈ tTerms a.val b.val,
      ∀ inner ∈ pTerms term.1 c.val d.val, pMul term.2 inner.2 < 256 := by
    intro term hterm inner hinner
    have ht := t_term_bounds a b term hterm
    exact small_product_bound ht.2
      (p_term_bounds ⟨term.1, ht.1⟩ c d inner hinner).2
  exact congrArg (fun v : PolyVector => v k.val)
    (scaled_fold_contraction 20 (tTerms a.val b.val)
      (fun j => pTerms j c.val d.val) hout hprod)

/-- Semantics of the middle inner face. -/
theorem pApplyMiddle_polynomial (a b c d k : Fin 20) :
    decodeVec (pApplyMiddle a.val (tTerms b.val c.val) d.val) k.val =
      ∑ j : Fin 20, tConstants b c j * pConstants a j d k := by
  have hout : ∀ term ∈ tTerms b.val c.val, term.1 < 20 :=
    fun term hterm => (t_term_bounds b c term hterm).1
  have hprod : ∀ term ∈ tTerms b.val c.val,
      ∀ inner ∈ pTerms a.val term.1 d.val, pMul term.2 inner.2 < 256 := by
    intro term hterm inner hinner
    have ht := t_term_bounds b c term hterm
    exact small_product_bound ht.2
      (p_term_bounds a ⟨term.1, ht.1⟩ d inner hinner).2
  exact congrArg (fun v : PolyVector => v k.val)
    (scaled_fold_contraction 20 (tTerms b.val c.val)
      (fun j => pTerms a.val j d.val) hout hprod)

/-- Semantics of the last inner face. -/
theorem pApplyLast_polynomial (a b c d k : Fin 20) :
    decodeVec (pApplyLast a.val b.val (tTerms c.val d.val)) k.val =
      ∑ j : Fin 20, tConstants c d j * pConstants a b j k := by
  have hout : ∀ term ∈ tTerms c.val d.val, term.1 < 20 :=
    fun term hterm => (t_term_bounds c d term hterm).1
  have hprod : ∀ term ∈ tTerms c.val d.val,
      ∀ inner ∈ pTerms a.val b.val term.1, pMul term.2 inner.2 < 256 := by
    intro term hterm inner hinner
    have ht := t_term_bounds c d term hterm
    exact small_product_bound ht.2
      (p_term_bounds a b ⟨term.1, ht.1⟩ inner hinner).2
  exact congrArg (fun v : PolyVector => v k.val)
    (scaled_fold_contraction 20 (tTerms c.val d.val)
      (fun j => pTerms a.val b.val j) hout hprod)

/-- Semantics of the right outer face. -/
theorem pTimesT_polynomial (a b c d k : Fin 20) :
    decodeVec (pTimesT (pTerms a.val b.val c.val) d.val) k.val =
      ∑ j : Fin 20, pConstants a b c j * tConstants j d k := by
  have hout : ∀ term ∈ pTerms a.val b.val c.val, term.1 < 20 :=
    fun term hterm => (p_term_bounds a b c term hterm).1
  have hprod : ∀ term ∈ pTerms a.val b.val c.val,
      ∀ inner ∈ tTerms term.1 d.val, pMul term.2 inner.2 < 256 := by
    intro term hterm inner hinner
    have ht := p_term_bounds a b c term hterm
    exact small_product_bound ht.2
      (t_term_bounds ⟨term.1, ht.1⟩ d inner hinner).2
  exact congrArg (fun v : PolyVector => v k.val)
    (scaled_fold_contraction 20 (pTerms a.val b.val c.val)
      (fun j => tTerms j d.val) hout hprod)

/-- The actual five-term polynomial coefficient of the displayed differential. -/
def fiveTermCoefficient (a b c d k : Fin 20) : Polynomial (ZMod 2) :=
  (∑ j : Fin 20, pConstants b c d j * tConstants a j k) +
    ((∑ j : Fin 20, tConstants a b j * pConstants j c d k) +
      ((∑ j : Fin 20, tConstants b c j * pConstants a j d k) +
        ((∑ j : Fin 20, tConstants c d j * pConstants a b j k) +
          (∑ j : Fin 20, pConstants a b c j * tConstants j d k))))

/-- Interpret the full packed expression, including all five faces. -/
theorem hochschildClosure_polynomial (a b c d k : Fin 20) :
    decodeVec (hochschildClosure a.val b.val c.val d.val) k.val =
      fiveTermCoefficient a b c d k := by
  unfold hochschildClosure
  simp only [decodeVec_xor, Pi.add_apply]
  rw [tTimesP_polynomial a b c d k, pApplyFirst_polynomial a b c d k,
    pApplyMiddle_polynomial a b c d k, pApplyLast_polynomial a b c d k,
    pTimesT_polynomial a b c d k]
  rfl

/-- All radical-basis quadruples have zero genuine polynomial differential.
The frozen packed certificate is reused, without a second enumeration. -/
theorem radical_basis_five_term_zero (a b c d : Fin 18) (k : Fin 20) :
    fiveTermCoefficient (radicalBasis a) (radicalBasis b)
      (radicalBasis c) (radicalBasis d) k = 0 := by
  rw [← hochschildClosure_polynomial]
  change decodeVec (hochschildClosure (radicalIndex a) (radicalIndex b)
    (radicalIndex c) (radicalIndex d)) k.val = 0
  rw [hochschild_closure_all a b c d, decodeVec_zero]
  rfl

/-- Explicit finite-contraction form of the radical-basis closure theorem. -/
theorem radical_basis_polynomial_closure (a b c d : Fin 18) (k : Fin 20) :
    (∑ j : Fin 20, pConstants (radicalBasis b) (radicalBasis c) (radicalBasis d) j *
      tConstants (radicalBasis a) j k) +
    ((∑ j : Fin 20, tConstants (radicalBasis a) (radicalBasis b) j *
      pConstants j (radicalBasis c) (radicalBasis d) k) +
    ((∑ j : Fin 20, tConstants (radicalBasis b) (radicalBasis c) j *
      pConstants (radicalBasis a) j (radicalBasis d) k) +
    ((∑ j : Fin 20, tConstants (radicalBasis c) (radicalBasis d) j *
      pConstants (radicalBasis a) (radicalBasis b) j k) +
    (∑ j : Fin 20, pConstants (radicalBasis a) (radicalBasis b) (radicalBasis c) j *
      tConstants j (radicalBasis d) k)))) = 0 :=
  radical_basis_five_term_zero a b c d k

#print axioms scaled_fold_contraction
#print axioms tTimesP_polynomial
#print axioms pApplyFirst_polynomial
#print axioms pApplyMiddle_polynomial
#print axioms pApplyLast_polynomial
#print axioms pTimesT_polynomial
#print axioms hochschildClosure_polynomial
#print axioms radical_basis_five_term_zero
#print axioms radical_basis_polynomial_closure

end
end ARCCochainBasisSemantics
