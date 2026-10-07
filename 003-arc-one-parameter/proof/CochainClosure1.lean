import CochainData

/-! Exact Hochschild-closure cases: all radical words, with no numeric
specialization of q and no exclusion of noncomposable input words. -/
namespace ARCFiniteCore
set_option maxRecDepth 20000
set_option maxHeartbeats 0

/-- All 18^3 words whose first radical index is 6. -/
theorem hochschild_closure_6 :
    ∀ b c d : Fin 18,
      hochschildClosure (radicalIndex 6) (radicalIndex b)
        (radicalIndex c) (radicalIndex d) = 0 := by decide
#print axioms hochschild_closure_6

/-- All 18^3 words whose first radical index is 7. -/
theorem hochschild_closure_7 :
    ∀ b c d : Fin 18,
      hochschildClosure (radicalIndex 7) (radicalIndex b)
        (radicalIndex c) (radicalIndex d) = 0 := by decide
#print axioms hochschild_closure_7

/-- All 18^3 words whose first radical index is 8. -/
theorem hochschild_closure_8 :
    ∀ b c d : Fin 18,
      hochschildClosure (radicalIndex 8) (radicalIndex b)
        (radicalIndex c) (radicalIndex d) = 0 := by decide
#print axioms hochschild_closure_8

/-- All 18^3 words whose first radical index is 9. -/
theorem hochschild_closure_9 :
    ∀ b c d : Fin 18,
      hochschildClosure (radicalIndex 9) (radicalIndex b)
        (radicalIndex c) (radicalIndex d) = 0 := by decide
#print axioms hochschild_closure_9

/-- All 18^3 words whose first radical index is 10. -/
theorem hochschild_closure_10 :
    ∀ b c d : Fin 18,
      hochschildClosure (radicalIndex 10) (radicalIndex b)
        (radicalIndex c) (radicalIndex d) = 0 := by decide
#print axioms hochschild_closure_10

/-- All 18^3 words whose first radical index is 11. -/
theorem hochschild_closure_11 :
    ∀ b c d : Fin 18,
      hochschildClosure (radicalIndex 11) (radicalIndex b)
        (radicalIndex c) (radicalIndex d) = 0 := by decide
#print axioms hochschild_closure_11

end ARCFiniteCore
