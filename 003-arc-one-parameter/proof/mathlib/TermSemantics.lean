import BytePacking

/-!
# Sparse-list polynomial vector semantics

These generic theorems interpret the frozen `encode` and `scaleEncode`
operations as sums of genuine F₂ polynomial vectors. Bounds are required
on each actually packed coefficient. Repeated basis labels are permitted.
No finite enumeration, algebra instance, or Hochschild complex is added.
-/

namespace ARCTermSemantics

open ARCFiniteCore ARCBitPolynomial ARCBytePacking

noncomputable section

abbrev PolyVector := Nat → Polynomial (ZMod 2)

/-- One actual polynomial coordinate, denoted by its natural-number code. -/
def singleTerm (j c : Nat) : PolyVector := fun i => if i = j then decode c else 0

/-- Interpret a sparse list as a sum; duplicate labels add in F₂[X]. -/
def sumTerms (terms : Terms) : PolyVector :=
  terms.foldr (fun term vec => singleTerm term.1 term.2 + vec) 0

/-- Pointwise multiplication by the genuine polynomial denoted by `s`. -/
def scale (s : Nat) (vec : PolyVector) : PolyVector := fun i => decode s * vec i

@[simp] theorem sumTerms_nil : sumTerms [] = 0 := rfl

@[simp] theorem sumTerms_cons (term : Nat × Nat) (terms : Terms) :
    sumTerms (term :: terms) = singleTerm term.1 term.2 + sumTerms terms := rfl

@[simp] theorem scale_zero (s : Nat) : scale s 0 = 0 := by
  funext i
  simp [scale]

theorem scale_add (s : Nat) (u v : PolyVector) :
    scale s (u + v) = scale s u + scale s v := by
  funext i
  simp [scale, mul_add]

/-- The frozen scalar multiplication interprets a scaled single coordinate. -/
theorem singleTerm_pMul (s j c : Nat) :
    singleTerm j (pMul s c) = scale s (singleTerm j c) := by
  funext i
  simp only [singleTerm, scale]
  split_ifs <;> simp [decode_pMul]

/-- Track the nonzero initial accumulator of the frozen encoder's left fold. -/
theorem encodeFoldl_semantics (terms : Terms) :
    ∀ acc : Nat, (∀ term ∈ terms, term.2 < 256) →
      decodeVec (terms.foldl
        (fun a term => Nat.xor a (pack term.1 term.2)) acc) =
      decodeVec acc + sumTerms terms := by
  induction terms with
  | nil =>
      intro acc h
      simp
  | cons term terms ih =>
      intro acc h
      have hc : term.2 < 256 := h term (List.mem_cons_self ..)
      have ht : ∀ t ∈ terms, t.2 < 256 := fun t hm =>
        h t (List.mem_cons_of_mem _ hm)
      rw [List.foldl_cons, ih _ ht, decodeVec_xor, decodeVec_pack term.1 term.2 hc]
      change (decodeVec acc + singleTerm term.1 term.2) + sumTerms terms =
        decodeVec acc + (singleTerm term.1 term.2 + sumTerms terms)
      exact add_assoc ..

/-- Arbitrary sparse lists of byte-bounded coefficients encode their true vector sum. -/
theorem decode_encode (terms : Terms) (h : ∀ term ∈ terms, term.2 < 256) :
    decodeVec (encode terms) = sumTerms terms := by
  simpa only [encode, decodeVec_zero, zero_add] using encodeFoldl_semantics terms 0 h

/-- Scaled left folds track arbitrary accumulators, with bounds on products. -/
theorem scaleEncodeFoldl_semantics (s : Nat) (terms : Terms) :
    ∀ acc : Nat, (∀ term ∈ terms, pMul s term.2 < 256) →
      decodeVec (terms.foldl
        (fun a term => Nat.xor a (pack term.1 (pMul s term.2))) acc) =
      decodeVec acc + scale s (sumTerms terms) := by
  induction terms with
  | nil =>
      intro acc h
      simp
  | cons term terms ih =>
      intro acc h
      have hc : pMul s term.2 < 256 := h term (List.mem_cons_self ..)
      have ht : ∀ t ∈ terms, pMul s t.2 < 256 := fun t hm =>
        h t (List.mem_cons_of_mem _ hm)
      rw [List.foldl_cons, ih _ ht, decodeVec_xor,
        decodeVec_pack term.1 (pMul s term.2) hc]
      change (decodeVec acc + singleTerm term.1 (pMul s term.2)) +
        scale s (sumTerms terms) = decodeVec acc + scale s (sumTerms (term :: terms))
      rw [singleTerm_pMul, sumTerms_cons, scale_add, add_assoc]

/-- Scaled encoding is genuine pointwise polynomial scaling, under the product bounds. -/
theorem decode_scaleEncode (s : Nat) (terms : Terms)
    (h : ∀ term ∈ terms, pMul s term.2 < 256) :
    decodeVec (scaleEncode s terms) = scale s (sumTerms terms) := by
  simpa only [scaleEncode, decodeVec_zero, zero_add] using
    scaleEncodeFoldl_semantics s terms 0 h

/-- Generic XOR accumulation becomes addition of the interpreted summands. -/
theorem xorFoldl_semantics {α : Type*} (items : List α)
    (codes : α → Nat) (vectors : α → PolyVector) :
    ∀ acc : Nat, (∀ item ∈ items, decodeVec (codes item) = vectors item) →
      decodeVec (items.foldl (fun a item => Nat.xor a (codes item)) acc) =
      decodeVec acc + items.foldr (fun item vec => vectors item + vec) 0 := by
  induction items with
  | nil =>
      intro acc h
      simp
  | cons item items ih =>
      intro acc h
      have hc := h item (List.mem_cons_self ..)
      have ht : ∀ t ∈ items, decodeVec (codes t) = vectors t := fun t hm =>
        h t (List.mem_cons_of_mem _ hm)
      rw [List.foldl_cons, ih _ ht, decodeVec_xor, hc, List.foldr_cons, add_assoc]

/-- Genuine vector interpretation of the left-bracketed sparse triple product. -/
def leftVectorProduct (table : Nat → Nat → Terms) (a b c : Nat) : PolyVector :=
  (table a b).foldr
    (fun term vec => scale term.2 (sumTerms (table term.1 c)) + vec) 0

/-- Genuine vector interpretation of the right-bracketed sparse triple product. -/
def rightVectorProduct (table : Nat → Nat → Terms) (a b c : Nat) : PolyVector :=
  (table b c).foldr
    (fun term vec => scale term.2 (sumTerms (table a term.1)) + vec) 0

/-- No new table computation: nested coefficient bounds suffice for left semantics. -/
theorem decode_leftProduct (table : Nat → Nat → Terms) (a b c : Nat)
    (h : ∀ x ∈ table a b, ∀ y ∈ table x.1 c, pMul x.2 y.2 < 256) :
    decodeVec (leftProduct table a b c) = leftVectorProduct table a b c := by
  simpa only [leftProduct, leftVectorProduct, decodeVec_zero, zero_add] using
    xorFoldl_semantics (table a b)
      (fun term => scaleEncode term.2 (table term.1 c))
      (fun term => scale term.2 (sumTerms (table term.1 c))) 0
      (fun term ht => decode_scaleEncode term.2 (table term.1 c) (h term ht))

/-- The independent right-path bounds suffice for right semantics. -/
theorem decode_rightProduct (table : Nat → Nat → Terms) (a b c : Nat)
    (h : ∀ x ∈ table b c, ∀ y ∈ table a x.1, pMul x.2 y.2 < 256) :
    decodeVec (rightProduct table a b c) = rightVectorProduct table a b c := by
  simpa only [rightProduct, rightVectorProduct, decodeVec_zero, zero_add] using
    xorFoldl_semantics (table b c)
      (fun term => scaleEncode term.2 (table a term.1))
      (fun term => scale term.2 (sumTerms (table a term.1))) 0
      (fun term ht => decode_scaleEncode term.2 (table a term.1) (h term ht))

#print axioms decode_encode
#print axioms decode_scaleEncode
#print axioms decode_leftProduct
#print axioms decode_rightProduct

end
end ARCTermSemantics
