import Std

/-!
# CG(3): original graph semantics and the six-cycle type invariant

This file uses Mizzi, arXiv:2603.27559v3, Definition 6.1 directly.
There is no imported graph catalogue or assumed automorphism list.
The scope is n = 3 only. The universal written automorphism proof and
the exact all-odd base classification are not formalized here.

All finite computations use kernel-reduced decide, not native_decide.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 8000000
set_option Elab.async false

namespace Struct2.Cg3

abbrev Base := Fin 30
abbrev Cover := Fin 60
abbrev Choice := Fin 3

def baseVertex (v : Nat) : Base :=
  ⟨v % 30, Nat.mod_lt _ (by decide)⟩

def coverVertex (v : Nat) : Cover :=
  ⟨v % 60, Nat.mod_lt _ (by decide)⟩

/- Ring vertices 0..17; centres 18+i; leaves 21+3*i+j, i,j < 3. -/
def sourceEdges : List (Base × Base) :=
  ((List.range 18).map fun t =>
    (baseVertex t, baseVertex ((t + 1) % 18))) ++
  (List.range 3).flatMap (fun i =>
    (List.range 3).flatMap (fun j =>
      [(baseVertex (18 + i), baseVertex (21 + 3 * i + j)),
       (baseVertex (21 + 3 * i + j), baseVertex (i + 3 * j)),
       (baseVertex (21 + 3 * i + j), baseVertex (i + 3 * j + 9))]))

def sourceAdj (x y : Base) : Bool :=
  sourceEdges.contains (x, y) || sourceEdges.contains (y, x)

def nextBase (x : Base) (choice : Choice) : Base :=
  let v := x.val
  if v < 18 then
    if choice.val = 0 then baseVertex ((v + 17) % 18)
    else if choice.val = 1 then baseVertex ((v + 1) % 18)
    else baseVertex (21 + 3 * (v % 3) + (v % 9) / 3)
  else if v < 21 then
    baseVertex (21 + 3 * (v - 18) + choice.val)
  else
    let i := (v - 21) / 3
    let j := (v - 21) % 3
    if choice.val = 0 then baseVertex (18 + i)
    else if choice.val = 1 then baseVertex (i + 3 * j)
    else baseVertex (i + 3 * j + 9)


def fastSourceAdj (x y : Base) : Bool :=
  (nextBase x 0 == y) || (nextBase x 1 == y) || (nextBase x 2 == y)

theorem fast_source_exact :
    ∀ x y : Base, fastSourceAdj x y = sourceAdj x y := by decide +kernel

/- The encoding 2*v+epsilon has the literal CDC layer epsilon. -/
def coverAdj (x y : Cover) : Bool :=
  (x.val % 2 != y.val % 2) &&
    fastSourceAdj (baseVertex (x.val / 2)) (baseVertex (y.val / 2))

theorem cdc_adjacency_is_original (x y : Cover) :
    coverAdj x y = ((x.val % 2 != y.val % 2) &&
      sourceAdj (baseVertex (x.val / 2)) (baseVertex (y.val / 2))) := by
  simp only [coverAdj, fast_source_exact]

def Adj (x y : Cover) : Prop := coverAdj x y = true

instance (x y : Cover) : Decidable (Adj x y) := inferInstanceAs
  (Decidable (coverAdj x y = true))

theorem original_edge_count : sourceEdges.length = 45 := by decide +kernel

theorem original_loopless : ∀ x : Base, sourceAdj x x = false := by decide +kernel

theorem original_symmetric (x y : Base) :
    sourceAdj x y = sourceAdj y x := by
  simp only [sourceAdj, Bool.or_comm]

theorem cdc_loopless : ∀ x : Cover, ¬ Adj x x := by decide +kernel

theorem cdc_symmetric : ∀ x y : Cover, Adj x y ↔ Adj y x := by decide +kernel

/- Three explicit neighbours, separately checked against the complete edge list.
   These are merely an efficient walk encoding until next_complete is proved. -/

def next (x : Cover) (choice : Choice) : Cover :=
  coverVertex (2 * (nextBase (baseVertex (x.val / 2)) choice).val
    + (1 - x.val % 2))

theorem next_complete :
    ∀ x y : Cover, Adj x y ↔ ∃ i : Choice, next x i = y := by decide +kernel

theorem next_distinct :
    ∀ (x : Cover) (i j : Choice), next x i = next x j → i = j := by decide +kernel

/- This is degree exactly three, expressed without a Mathlib cardinality API. -/
def DegreeThree (x : Cover) : Prop :=
  ∃ neighbors : Choice → Cover,
    (∀ i j, neighbors i = neighbors j → i = j) ∧
    (∀ y, Adj x y ↔ ∃ i, neighbors i = y)

theorem cdc_cubic (x : Cover) : DegreeThree x :=
  ⟨next x, next_distinct x, next_complete x⟩

/- A genuine graph-theoretic six-cycle: six distinct vertices and six edges. -/
def SixCycle (v₀ v₁ v₂ v₃ v₄ v₅ : Cover) : Prop :=
  [v₀, v₁, v₂, v₃, v₄, v₅].Nodup ∧
  Adj v₀ v₁ ∧ Adj v₁ v₂ ∧ Adj v₂ v₃ ∧
  Adj v₃ v₄ ∧ Adj v₄ v₅ ∧ Adj v₅ v₀

instance (v₀ v₁ v₂ v₃ v₄ v₅ : Cover) :
    Decidable (SixCycle v₀ v₁ v₂ v₃ v₄ v₅) := inferInstanceAs
  (Decidable ([v₀, v₁, v₂, v₃, v₄, v₅].Nodup ∧
    Adj v₀ v₁ ∧ Adj v₁ v₂ ∧ Adj v₂ v₃ ∧
    Adj v₃ v₄ ∧ Adj v₄ v₅ ∧ Adj v₅ v₀))

def HasSixCycle (v : Cover) : Prop :=
  ∃ v₁ v₂ v₃ v₄ v₅ : Cover, SixCycle v v₁ v₂ v₃ v₄ v₅

/- Search only the 3^5 neighbour-choice sequences, rather than 60^5 arbitrary
   vertex tuples. The following equivalence proves that no cycle is omitted. -/
def IndexedSixCycle (v : Cover) (a b c d e : Choice) : Prop :=
  let v₁ := next v a
  let v₂ := next v₁ b
  let v₃ := next v₂ c
  let v₄ := next v₃ d
  let v₅ := next v₄ e
  SixCycle v v₁ v₂ v₃ v₄ v₅

instance (v : Cover) (a b c d e : Choice) :
    Decidable (IndexedSixCycle v a b c d e) := inferInstanceAs
  (Decidable (SixCycle v (next v a)
    (next (next v a) b)
    (next (next (next v a) b) c)
    (next (next (next (next v a) b) c) d)
    (next (next (next (next (next v a) b) c) d) e)))

def IndexedHasSixCycle (v : Cover) : Prop :=
  ∃ a b c d e : Choice, IndexedSixCycle v a b c d e

instance (v : Cover) : Decidable (IndexedHasSixCycle v) := inferInstanceAs
  (Decidable (∃ a b c d e : Choice, IndexedSixCycle v a b c d e))

theorem indexed_iff_actual (v : Cover) :
    IndexedHasSixCycle v ↔ HasSixCycle v := by
  constructor
  · rintro ⟨a, b, c, d, e, h⟩
    exact ⟨next v a,
      next (next v a) b,
      next (next (next v a) b) c,
      next (next (next (next v a) b) c) d,
      next (next (next (next (next v a) b) c) d) e, h⟩
  · rintro ⟨v₁, v₂, v₃, v₄, v₅, h⟩
    obtain ⟨a, ha⟩ := (next_complete v v₁).mp h.2.1
    obtain ⟨b, hb⟩ := (next_complete v₁ v₂).mp h.2.2.1
    obtain ⟨c, hc⟩ := (next_complete v₂ v₃).mp h.2.2.2.1
    obtain ⟨d, hd⟩ := (next_complete v₃ v₄).mp h.2.2.2.2.1
    obtain ⟨e, he⟩ := (next_complete v₄ v₅).mp h.2.2.2.2.2.1
    refine ⟨a, b, c, d, e, ?_⟩
    simpa only [IndexedSixCycle, ha, hb, hc, hd, he] using h

def IsCentre (v : Cover) : Prop := 36 ≤ v.val ∧ v.val < 42

instance (v : Cover) : Decidable (IsCentre v) := inferInstanceAs
  (Decidable (36 ≤ v.val ∧ v.val < 42))

theorem indexed_six_cycle_classification :
    ∀ v : Cover, IndexedHasSixCycle v ↔ ¬ IsCentre v := by decide +kernel

/- This conclusion concerns the original adjacency and actual simple cycles.
   No cycle-invariance or type-separation statement is assumed. -/
theorem actual_six_cycle_iff_not_centre (v : Cover) :
    HasSixCycle v ↔ ¬ IsCentre v :=
  (indexed_iff_actual v).symm.trans (indexed_six_cycle_classification v)

def StrongSwitch (guide : Cover → Cover) : Prop :=
  (∀ v, guide (guide v) = v) ∧
  (∀ x y, Adj (guide x) (guide y) ↔ Adj x y) ∧
  (∀ v, (guide v).val % 2 ≠ v.val % 2) ∧
  (∀ v, ¬ Adj v (guide v))

def deck (v : Cover) : Cover :=
  coverVertex (2 * (v.val / 2) + (1 - v.val % 2))

def halfTurnBase (v : Base) : Base :=
  if v.val < 18 then baseVertex ((v.val + 9) % 18) else v

def reflectionBase (v : Base) : Base :=
  if v.val < 18 then baseVertex ((18 - v.val) % 18)
  else if v.val < 21 then baseVertex (18 + (3 - (v.val - 18)) % 3)
  else
    let a := (v.val - 21) / 3 + 3 * ((v.val - 21) % 3)
    let b := (9 - a) % 9
    baseVertex (21 + 3 * (b % 3) + b / 3)

def liftBase (permutation : Base → Base) (v : Cover) : Cover :=
  coverVertex (2 * (permutation (baseVertex (v.val / 2))).val + v.val % 2)

def companionGuide (v : Cover) : Cover := deck (liftBase halfTurnBase v)
def reflectionGuide (v : Cover) : Cover := deck (liftBase reflectionBase v)

theorem deck_strong : StrongSwitch deck := by
  unfold StrongSwitch
  decide +kernel

theorem companion_guide_strong : StrongSwitch companionGuide := by
  unfold StrongSwitch
  decide +kernel

theorem reflection_guide_strong : StrongSwitch reflectionGuide := by
  unfold StrongSwitch
  decide +kernel

#print axioms fast_source_exact
#print axioms cdc_adjacency_is_original
#print axioms original_edge_count
#print axioms original_loopless
#print axioms original_symmetric
#print axioms cdc_loopless
#print axioms cdc_symmetric
#print axioms next_complete
#print axioms next_distinct
#print axioms cdc_cubic
#print axioms indexed_iff_actual
#print axioms indexed_six_cycle_classification
#print axioms actual_six_cycle_iff_not_centre
#print axioms deck_strong
#print axioms companion_guide_strong
#print axioms reflection_guide_strong

end Struct2.Cg3
