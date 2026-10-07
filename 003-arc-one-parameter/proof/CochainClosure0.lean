import CochainData

/-! Exact Hochschild-closure cases: all radical words, with no numeric
specialization of q and no exclusion of noncomposable input words. -/
namespace ARCFiniteCore
set_option maxRecDepth 20000
set_option maxHeartbeats 0

/-- All 18^3 words whose first radical index is 0. -/
theorem hochschild_closure_0 :
    ∀ b c d : Fin 18,
      hochschildClosure (radicalIndex 0) (radicalIndex b)
        (radicalIndex c) (radicalIndex d) = 0 := by decide
#print axioms hochschild_closure_0

/-- All 18^3 words whose first radical index is 1. -/
theorem hochschild_closure_1 :
    ∀ b c d : Fin 18,
      hochschildClosure (radicalIndex 1) (radicalIndex b)
        (radicalIndex c) (radicalIndex d) = 0 := by decide
#print axioms hochschild_closure_1

/-- All 18^3 words whose first radical index is 2. -/
theorem hochschild_closure_2 :
    ∀ b c d : Fin 18,
      hochschildClosure (radicalIndex 2) (radicalIndex b)
        (radicalIndex c) (radicalIndex d) = 0 := by decide
#print axioms hochschild_closure_2

/-- All 18^3 words whose first radical index is 3. -/
theorem hochschild_closure_3 :
    ∀ b c d : Fin 18,
      hochschildClosure (radicalIndex 3) (radicalIndex b)
        (radicalIndex c) (radicalIndex d) = 0 := by decide
#print axioms hochschild_closure_3

/-- All 18^3 words whose first radical index is 4. -/
theorem hochschild_closure_4 :
    ∀ b c d : Fin 18,
      hochschildClosure (radicalIndex 4) (radicalIndex b)
        (radicalIndex c) (radicalIndex d) = 0 := by decide
#print axioms hochschild_closure_4

/-- All 18^3 words whose first radical index is 5. -/
theorem hochschild_closure_5 :
    ∀ b c d : Fin 18,
      hochschildClosure (radicalIndex 5) (radicalIndex b)
        (radicalIndex c) (radicalIndex d) = 0 := by decide
#print axioms hochschild_closure_5

end ARCFiniteCore
