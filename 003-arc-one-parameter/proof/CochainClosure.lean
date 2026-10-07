import CochainClosure0
import CochainClosure1
import CochainClosure2

/-! All 104976 radical four-word coefficient identities, kernel checked.
Scope is the explicitly defined packed bit-polynomial differential. -/
namespace ARCFiniteCore
set_option maxRecDepth 20000
set_option maxHeartbeats 0

private theorem fin18_cases : ∀ a : Fin 18,
    a = 0 ∨ a = 1 ∨ a = 2 ∨ a = 3 ∨ a = 4 ∨ a = 5 ∨ a = 6 ∨ a = 7 ∨ a = 8 ∨ a = 9 ∨ a = 10 ∨ a = 11 ∨ a = 12 ∨ a = 13 ∨ a = 14 ∨ a = 15 ∨ a = 16 ∨ a = 17 := by decide

/-- Full closure, including every noncomposable radical input word. -/
theorem hochschild_closure_all :
    ∀ a b c d : Fin 18,
      hochschildClosure (radicalIndex a) (radicalIndex b)
        (radicalIndex c) (radicalIndex d) = 0 := by
  intro a
  rcases fin18_cases a with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact hochschild_closure_0
  · exact hochschild_closure_1
  · exact hochschild_closure_2
  · exact hochschild_closure_3
  · exact hochschild_closure_4
  · exact hochschild_closure_5
  · exact hochschild_closure_6
  · exact hochschild_closure_7
  · exact hochschild_closure_8
  · exact hochschild_closure_9
  · exact hochschild_closure_10
  · exact hochschild_closure_11
  · exact hochschild_closure_12
  · exact hochschild_closure_13
  · exact hochschild_closure_14
  · exact hochschild_closure_15
  · exact hochschild_closure_16
  · exact hochschild_closure_17

#print axioms hochschild_closure_all
end ARCFiniteCore
