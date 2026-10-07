import CochainData

/-! Exact Hochschild-closure cases: all radical words, with no numeric
specialization of q and no exclusion of noncomposable input words. -/
namespace ARCFiniteCore
set_option maxRecDepth 20000
set_option maxHeartbeats 0

/-- All 18^3 words whose first radical index is 12. -/
theorem hochschild_closure_12 :
    ∀ b c d : Fin 18,
      hochschildClosure (radicalIndex 12) (radicalIndex b)
        (radicalIndex c) (radicalIndex d) = 0 := by decide
#print axioms hochschild_closure_12

/-- All 18^3 words whose first radical index is 13. -/
theorem hochschild_closure_13 :
    ∀ b c d : Fin 18,
      hochschildClosure (radicalIndex 13) (radicalIndex b)
        (radicalIndex c) (radicalIndex d) = 0 := by decide
#print axioms hochschild_closure_13

/-- All 18^3 words whose first radical index is 14. -/
theorem hochschild_closure_14 :
    ∀ b c d : Fin 18,
      hochschildClosure (radicalIndex 14) (radicalIndex b)
        (radicalIndex c) (radicalIndex d) = 0 := by decide
#print axioms hochschild_closure_14

/-- All 18^3 words whose first radical index is 15. -/
theorem hochschild_closure_15 :
    ∀ b c d : Fin 18,
      hochschildClosure (radicalIndex 15) (radicalIndex b)
        (radicalIndex c) (radicalIndex d) = 0 := by decide
#print axioms hochschild_closure_15

/-- All 18^3 words whose first radical index is 16. -/
theorem hochschild_closure_16 :
    ∀ b c d : Fin 18,
      hochschildClosure (radicalIndex 16) (radicalIndex b)
        (radicalIndex c) (radicalIndex d) = 0 := by decide
#print axioms hochschild_closure_16

/-- All 18^3 words whose first radical index is 17. -/
theorem hochschild_closure_17 :
    ∀ b c d : Fin 18,
      hochschildClosure (radicalIndex 17) (radicalIndex b)
        (radicalIndex c) (radicalIndex d) = 0 := by decide
#print axioms hochschild_closure_17

end ARCFiniteCore
