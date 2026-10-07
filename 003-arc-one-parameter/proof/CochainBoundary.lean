import CochainData

/-! Constant and linear H coefficients of the complete twisted boundary.
Concrete bit-polynomial identities only; no arbitrary-field model is claimed. -/
namespace ARCFiniteCore
set_option maxRecDepth 20000
set_option maxHeartbeats 0

def gamma (a : Nat) : Nat :=
  if a = 4 ∨ a = 5 ∨ a = 6 ∨ a = 10 ∨ a = 11 ∨ a = 12 ∨
     a = 13 ∨ a = 14 ∨ a = 15 then 2 else 0

def boundarySum (upper : Bool) (a b : Nat) : Nat :=
  (List.finRange 18).foldl (fun acc w =>
    let index := radicalIndex w
    if decide (index ≥ 10) == upper then
      Nat.xor acc (pTimesT (pTerms a b index) (dualIndex index))
    else acc) 0

def boundaryConstantRight (a b : Nat) : Nat :=
  scaleEncode (if b ≥ 10 then gamma a else 0) (tTerms a b)

def boundaryLinearRight (a b : Nat) : Nat :=
  (tTerms a b).foldl (fun acc term =>
    let scalar := Nat.xor (gamma b)
      (Nat.xor (gamma term.1) (if b < 10 then gamma a else 0))
    Nat.xor acc (pack term.1 (pMul scalar term.2))) 0

/-- All 324 input pairs, constant coefficient in indeterminate H. -/
theorem twisted_boundary_constant :
    ∀ a b : Fin 18,
      boundarySum false (radicalIndex a) (radicalIndex b) =
      boundaryConstantRight (radicalIndex a) (radicalIndex b) := by decide

/-- All 324 input pairs, linear coefficient in indeterminate H. -/
theorem twisted_boundary_linear :
    ∀ a b : Fin 18,
      boundarySum true (radicalIndex a) (radicalIndex b) =
      boundaryLinearRight (radicalIndex a) (radicalIndex b) := by decide

#print axioms twisted_boundary_constant
#print axioms twisted_boundary_linear
end ARCFiniteCore
