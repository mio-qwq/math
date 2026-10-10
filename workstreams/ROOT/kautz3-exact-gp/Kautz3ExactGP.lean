import Mathlib.Tactic.NormNum
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Data.Fintype.EquivFin
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Data.Finset.Prod
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Aesop
import Mathlib.Data.Fintype.Prod
import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.Fin
import Mathlib.Data.Finset.Card
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Lean.Elab.Tactic.Omega

/- Exact general-position number of Ka(m,3) for every alphabet size m >= 3.
   Vertices are all three-letter words with unequal adjacent letters.
   The final theorem uses actual directed shortest simple paths. -/
namespace Kautz3

universe u
abbrev Triple (α : Type u) := α × α × α
def Legal {α : Type u} (x : Triple α) : Prop := x.1 ≠ x.2.1 ∧ x.2.1 ≠ x.2.2
instance {α : Type u} [DecidableEq α] (x : Triple α) : Decidable (Legal x) := by
  unfold Legal
  infer_instance
abbrev Vertex (α : Type u) := {x : Triple α // Legal x}
def first {α : Type u} (x : Vertex α) : α := x.1.1
def second {α : Type u} (x : Vertex α) : α := x.1.2.1
def third {α : Type u} (x : Vertex α) : α := x.1.2.2
def make {α : Type u} (a b c : α) (hab : a ≠ b) (hbc : b ≠ c) : Vertex α :=
  ⟨(a,b,c), hab, hbc⟩
theorem first_ne_second {α : Type u} (x : Vertex α) : first x ≠ second x := x.2.1
theorem second_ne_third {α : Type u} (x : Vertex α) : second x ≠ third x := x.2.2
def Edge {α : Type u} (x y : Vertex α) : Prop :=
  first y = second x ∧ second y = third x
instance {α : Type u} [DecidableEq α] (x y : Vertex α) : Decidable (Edge x y) := by
  unfold Edge
  infer_instance
def distance {α : Type u} [DecidableEq α] (x y : Vertex α) : ℕ :=
  if x = y then 0 else if Edge x y then 1 else if third x = first y then 2 else 3
def DistanceGP {α : Type u} [DecidableEq α] (S : Finset (Vertex α)) : Prop :=
  ∀ {x y z : Vertex α}, x ∈ S → y ∈ S → z ∈ S → x ≠ y → z ≠ x → z ≠ y →
    distance x z + distance z y ≠ distance x y
def squareSum (n : ℕ) : ℕ := ∑ i ∈ Finset.range n, i * i

end Kautz3

/- Actual directed walks, shortest simple paths and their GP equivalence. -/
namespace Kautz3

universe u
variable {α : Type u} [DecidableEq α]

omit [DecidableEq α] in
theorem edge_iff_original (x y : Vertex α) :
    Edge x y ↔ first y = second x ∧ second y = third x ∧ third y ≠ third x := by
  constructor
  · intro h
    refine ⟨h.1, h.2, ?_⟩
    rw [← h.2]
    exact (second_ne_third y).symm
  · intro h
    exact ⟨h.1, h.2.1⟩

inductive Walk : ℕ → Vertex α → Vertex α → Prop
  | nil (x : Vertex α) : Walk 0 x x
  | cons {n : ℕ} {x y z : Vertex α} :
      Edge x y → Walk n y z → Walk (n + 1) x z

theorem distance_self (x : Vertex α) : distance x x = 0 := by simp [distance]

theorem distance_le_three (x y : Vertex α) : distance x y ≤ 3 := by
  unfold distance
  split_ifs <;> omega

theorem distance_le_one_of_edge {x y : Vertex α} (h : Edge x y) :
    distance x y ≤ 1 := by
  unfold distance
  split_ifs <;> simp_all

theorem distance_le_two_of_overlap {x y : Vertex α} (h : third x = first y) :
    distance x y ≤ 2 := by
  unfold distance
  split_ifs <;> simp_all

theorem distance_eq_zero_iff (x y : Vertex α) : distance x y = 0 ↔ x = y := by
  unfold distance
  split_ifs <;> simp_all

/-- Each overlap case is realized by actual shift arcs, not an external distance table. -/
theorem distance_walk (x y : Vertex α) : Walk (distance x y) x y := by
  unfold distance
  split_ifs with hxy he hlast
  · subst y
    exact Walk.nil x
  · exact Walk.cons he (Walk.nil y)
  · have hc : third x ≠ second y := by
      rw [hlast]
      exact first_ne_second y
    let z : Vertex α := make (second x) (third x) (second y) (second_ne_third x) hc
    have h₁ : Edge x z := ⟨rfl, rfl⟩
    have h₂ : Edge z y := ⟨hlast.symm, rfl⟩
    exact Walk.cons h₁ (Walk.cons h₂ (Walk.nil y))
  · let z₁ : Vertex α := make (second x) (third x) (first y)
      (second_ne_third x) hlast
    let z₂ : Vertex α := make (third x) (first y) (second y)
      hlast (first_ne_second y)
    have h₁ : Edge x z₁ := ⟨rfl, rfl⟩
    have h₂ : Edge z₁ z₂ := ⟨rfl, rfl⟩
    have h₃ : Edge z₂ y := ⟨rfl, rfl⟩
    exact Walk.cons h₁ (Walk.cons h₂ (Walk.cons h₃ (Walk.nil y)))

/-- A zero-, one-, or two-step shift forces precisely the necessary overlap. -/
theorem distance_le_walk {n : ℕ} {x y : Vertex α} (h : Walk n x y) :
    distance x y ≤ n := by
  cases n with
  | zero =>
      cases h
      simp [distance]
  | succ n =>
      cases n with
      | zero =>
          cases h with
          | cons he ht =>
              cases ht
              exact distance_le_one_of_edge he
      | succ n =>
          cases n with
          | zero =>
              cases h with
              | cons h₁ ht =>
                  cases ht with
                  | cons h₂ ht =>
                      cases ht
                      exact distance_le_two_of_overlap (h₁.2.symm.trans h₂.1.symm)
          | succ n =>
              have h₃ := distance_le_three x y
              omega

omit [DecidableEq α] in
theorem Walk.append {m n : ℕ} {x y z : Vertex α}
    (p : Walk m x y) (q : Walk n y z) : Walk (m + n) x z := by
  induction p with
  | nil => simpa using q
  | cons he hp ih =>
      simpa [Nat.add_assoc, Nat.add_left_comm, Nat.add_comm] using Walk.cons he (ih q)

theorem distance_triangle (x y z : Vertex α) :
    distance x z ≤ distance x y + distance y z :=
  distance_le_walk ((distance_walk x y).append (distance_walk y z))

inductive SimplePath : ℕ → Vertex α → Vertex α → List (Vertex α) → Prop
  | nil (x : Vertex α) : SimplePath 0 x x [x]
  | cons {n : ℕ} {x y z : Vertex α} {l : List (Vertex α)} :
      Edge x y → SimplePath n y z l → x ∉ l → SimplePath (n + 1) x z (x :: l)

omit [DecidableEq α] in
theorem SimplePath.toWalk {n : ℕ} {x y : Vertex α} {l : List (Vertex α)}
    (h : SimplePath n x y l) : Walk n x y := by
  induction h with
  | nil x => exact Walk.nil x
  | cons he hp hnot ih => exact Walk.cons he ih

omit [DecidableEq α] in
theorem SimplePath.supportNodup {n : ℕ} {x y : Vertex α} {l : List (Vertex α)}
    (h : SimplePath n x y l) : l.Nodup := by
  induction h with
  | nil x => simp
  | cons he hp hnot ih => exact List.nodup_cons.mpr ⟨hnot, ih⟩

omit [DecidableEq α] in
theorem SimplePath.suffix {n : ℕ} {y z : Vertex α} {l : List (Vertex α)}
    (h : SimplePath n y z l) {x : Vertex α} (hx : x ∈ l) :
    ∃ k : ℕ, ∃ l' : List (Vertex α), SimplePath k x z l' ∧ k ≤ n := by
  induction h generalizing x with
  | nil y =>
      have heq : x = y := by simpa using hx
      subst x
      exact ⟨0, [y], SimplePath.nil y, Nat.le_refl 0⟩
  | @cons n y w z l he hp hnot ih =>
      rcases List.mem_cons.mp hx with heq | hmem
      · subst x
        exact ⟨n+1, y::l, SimplePath.cons he hp hnot, Nat.le_refl (n+1)⟩
      · obtain ⟨k,l',hk,hkn⟩ := ih hmem
        exact ⟨k,l',hk,by omega⟩

theorem walk_to_simple_path {n : ℕ} {x y : Vertex α} (h : Walk n x y) :
    ∃ k : ℕ, ∃ l : List (Vertex α), SimplePath k x y l ∧ k ≤ n := by
  induction h with
  | nil x => exact ⟨0,[x],SimplePath.nil x,Nat.le_refl 0⟩
  | @cons n x y z he hw ih =>
      obtain ⟨k,l,hp,hkn⟩ := ih
      by_cases hx : x ∈ l
      · obtain ⟨j,l',hj,hjk⟩ := hp.suffix hx
        exact ⟨j,l',hj,by omega⟩
      · exact ⟨k+1,x::l,SimplePath.cons he hp hx,by omega⟩

theorem shortest_simple_path (x y : Vertex α) :
    ∃ l : List (Vertex α), SimplePath (distance x y) x y l := by
  obtain ⟨k,l,hp,hk⟩ := walk_to_simple_path (distance_walk x y)
  have hd := distance_le_walk hp.toWalk
  have heq : k = distance x y := by omega
  subst k
  exact ⟨l,hp⟩

omit [DecidableEq α] in
theorem SimplePath.split_walk {n : ℕ} {x y : Vertex α} {l : List (Vertex α)}
    (hp : SimplePath n x y l) {z : Vertex α} (hz : z ∈ l) :
    ∃ m k : ℕ, Walk m x z ∧ Walk k z y ∧ m + k = n := by
  induction hp generalizing z with
  | nil x =>
      have heq : z = x := by simpa using hz
      subst z
      exact ⟨0,0,Walk.nil x,Walk.nil x,rfl⟩
  | @cons n x w y l he hp hnot ih =>
      rcases List.mem_cons.mp hz with heq | hmem
      · subst z
        exact ⟨0,n+1,Walk.nil x,Walk.cons he hp.toWalk,by omega⟩
      · obtain ⟨m,k,hm,hk,hmk⟩ := ih hmem
        exact ⟨m+1,k,Walk.cons he hm,hk,by omega⟩

/-- Listed walks carry the middle vertex through concatenation; minimal ones are paths. -/
inductive ListedWalk : ℕ → Vertex α → Vertex α → List (Vertex α) → Prop
  | nil (x : Vertex α) : ListedWalk 0 x x [x]
  | cons {n : ℕ} {x y z : Vertex α} {l : List (Vertex α)} :
      Edge x y → ListedWalk n y z l → ListedWalk (n+1) x z (x::l)

omit [DecidableEq α] in
theorem ListedWalk.toWalk {n : ℕ} {x y : Vertex α} {l : List (Vertex α)}
    (h : ListedWalk n x y l) : Walk n x y := by
  induction h with
  | nil x => exact Walk.nil x
  | cons he hp ih => exact Walk.cons he ih

omit [DecidableEq α] in
theorem ListedWalk.first_mem {n : ℕ} {x y : Vertex α} {l : List (Vertex α)}
    (h : ListedWalk n x y l) : x ∈ l := by
  cases h <;> simp

omit [DecidableEq α] in
theorem SimplePath.toListedWalk {n : ℕ} {x y : Vertex α} {l : List (Vertex α)}
    (h : SimplePath n x y l) : ListedWalk n x y l := by
  induction h with
  | nil x => exact ListedWalk.nil x
  | cons he hp hnot ih => exact ListedWalk.cons he ih

omit [DecidableEq α] in
theorem ListedWalk.append_with_middle {m n : ℕ} {x y z : Vertex α}
    {l₁ l₂ : List (Vertex α)} (p : ListedWalk m x y l₁) (q : ListedWalk n y z l₂) :
    ∃ l : List (Vertex α), ListedWalk (m+n) x z l ∧ y ∈ l := by
  induction p with
  | nil => exact ⟨l₂,by simpa using q,q.first_mem⟩
  | @cons m x w y l he hp ih =>
      obtain ⟨l,hl,hy⟩ := ih q
      refine ⟨x::l,?_,List.mem_cons_of_mem x hy⟩
      simpa [Nat.add_assoc,Nat.add_left_comm,Nat.add_comm] using ListedWalk.cons he hl

theorem ListedWalk.shortest_is_simple {n : ℕ} {x y : Vertex α} {l : List (Vertex α)}
    (h : ListedWalk n x y l) : n = distance x y → SimplePath n x y l := by
  induction h with
  | nil x => intro _; exact SimplePath.nil x
  | @cons n x w y l he hw ih =>
      intro hmin
      have htail := distance_le_walk hw.toWalk
      have hedge := distance_le_one_of_edge he
      have htri := distance_triangle x w y
      have heq : n = distance w y := by omega
      have hp := ih heq
      have hnot : x ∉ l := by
        intro hx
        obtain ⟨k,l',hk,hkn⟩ := hp.suffix hx
        have hlower := distance_le_walk hk.toWalk
        omega
      exact SimplePath.cons he hp hnot

def OriginalGeneralPosition (S : Finset (Vertex α)) : Prop :=
  ∀ {n : ℕ} {x y : Vertex α} {l : List (Vertex α)},
    SimplePath n x y l → x ∈ S → y ∈ S →
      (∀ k : ℕ, ∀ l' : List (Vertex α), SimplePath k x y l' → n ≤ k) →
        ∀ {z : Vertex α}, z ∈ l → z ∈ S → z = x ∨ z = y

theorem distanceGP_iff_original (S : Finset (Vertex α)) :
    DistanceGP S ↔ OriginalGeneralPosition S := by
  constructor
  · intro h n x y l hp hx hy hmin z hz hzS
    by_cases hzx : z = x
    · exact Or.inl hzx
    by_cases hzy : z = y
    · exact Or.inr hzy
    obtain ⟨a,b,ha,hb,hab⟩ := hp.split_walk hz
    obtain ⟨l',hshort⟩ := shortest_simple_path x y
    have hnle := hmin (distance x y) l' hshort
    have hnge := distance_le_walk hp.toWalk
    have hn : n = distance x y := by omega
    have h₁ := distance_le_walk ha
    have h₂ := distance_le_walk hb
    have h₃ := distance_triangle x z y
    have hxy : x ≠ y := by
      intro heq
      have hz0 : distance x z ≠ 0 := by
        intro hzero
        exact hzx ((distance_eq_zero_iff x z).mp hzero).symm
      subst y
      have hd0 := distance_self x
      omega
    exact (h hx hy hzS hxy hzx hzy (by omega)).elim
  · intro h x y z hx hy hz hxy hzx hzy heq
    obtain ⟨l₁,p⟩ := shortest_simple_path x z
    obtain ⟨l₂,q⟩ := shortest_simple_path z y
    obtain ⟨l,hl,hzmem⟩ := p.toListedWalk.append_with_middle q.toListedWalk
    have hp := hl.shortest_is_simple heq
    have hmin : ∀ k : ℕ, ∀ l' : List (Vertex α), SimplePath k x y l' →
        distance x z + distance z y ≤ k := by
      intro k l' hpath
      rw [heq]
      exact distance_le_walk hpath.toWalk
    rcases h hp hx hy hmin hzmem hz with heq' | heq'
    · exact hzx heq'
    · exact hzy heq'

#print axioms edge_iff_original
#print axioms distance_walk
#print axioms distance_le_walk
#print axioms distance_triangle
#print axioms walk_to_simple_path
#print axioms shortest_simple_path
#print axioms ListedWalk.shortest_is_simple
#print axioms distanceGP_iff_original

end Kautz3

/- Finite counting: peak construction, independent-set injection,
   selected-arc incidence bounds and induction by alphabet deletion. -/

namespace Kautz3

open scoped BigOperators

universe u v

theorem count_vertex_ext {α : Type u} {x y : Vertex α}
    (h₁ : first x = first y) (h₂ : second x = second y)
    (h₃ : third x = third y) : x = y := by
  apply Subtype.ext
  exact Prod.ext h₁ (Prod.ext h₂ h₃)

theorem count_vertex_eq_iff {α : Type u} (x y : Vertex α) :
    x = y ↔ first x = first y ∧ second x = second y ∧ third x = third y := by
  constructor
  · intro h
    subst y
    exact ⟨rfl, rfl, rfl⟩
  · rintro ⟨h₁,h₂,h₃⟩
    exact count_vertex_ext h₁ h₂ h₃

@[simp] theorem count_first_make {α : Type u} (a b c : α)
    (hab : a ≠ b) (hbc : b ≠ c) : first (make a b c hab hbc) = a := rfl

@[simp] theorem count_second_make {α : Type u} (a b c : α)
    (hab : a ≠ b) (hbc : b ≠ c) : second (make a b c hab hbc) = b := rfl

@[simp] theorem count_third_make {α : Type u} (a b c : α)
    (hab : a ≠ b) (hbc : b ≠ c) : third (make a b c hab hbc) = c := rfl

@[simp] theorem count_distance_self {α : Type u} [DecidableEq α]
    (x : Vertex α) : distance x x = 0 := distance_self x

theorem count_distance_le_three {α : Type u} [DecidableEq α]
    (x y : Vertex α) : distance x y ≤ 3 := distance_le_three x y

theorem count_distance_ge_two {α : Type u} [DecidableEq α]
    {x y : Vertex α} (hne : x ≠ y) (he : ¬ Edge x y) : 2 ≤ distance x y := by
  simp only [distance, ite_eq_right hne, ite_eq_right he]
  split <;> omega

def CountIndependent {α : Type u} (S : Finset (Vertex α)) : Prop :=
  ∀ ⦃x y⦄, x ∈ S → y ∈ S → ¬ Edge x y

theorem count_independent_gp {α : Type u} [DecidableEq α]
    {S : Finset (Vertex α)} (hS : CountIndependent S) : DistanceGP S := by
  intro x y z hx hy hz hxy hzx hzy heq
  have h₁ := count_distance_ge_two (Ne.symm hzx) (hS hx hz)
  have h₂ := count_distance_ge_two hzy (hS hz hy)
  have h₃ := count_distance_le_three x y
  omega

theorem count_forbidden_123 {α : Type u} [DecidableEq α]
    {S : Finset (Vertex α)} (hS : DistanceGP S)
    {x y z : Vertex α} (hx : x ∈ S) (hy : y ∈ S) (hz : z ∈ S)
    (h₁ : distance x y = 1) (h₂ : distance y z = 2)
    (h₃ : distance x z = 3) : False := by
  have hxz : x ≠ z := by intro h; subst z; simp at h₃
  have hyx : y ≠ x := by intro h; subst y; simp at h₁
  have hyz : y ≠ z := by intro h; subst z; simp at h₂
  apply hS hx hz hy hxz hyx hyz
  omega

/- Actual injective alphabet maps preserve the closed distance formula. -/
def countRelabel {α : Type u} {β : Type v} (e : α ↪ β) (x : Vertex α) : Vertex β :=
  make (e (first x)) (e (second x)) (e (third x))
    (fun h => first_ne_second x (e.injective h))
    (fun h => second_ne_third x (e.injective h))

theorem count_relabel_injective {α : Type u} {β : Type v} (e : α ↪ β) :
    Function.Injective (countRelabel e) := by
  intro x y h
  apply count_vertex_ext
  · exact e.injective (congrArg first h)
  · exact e.injective (congrArg second h)
  · exact e.injective (congrArg third h)

@[simp] theorem count_relabel_distance {α : Type u} {β : Type v}
    [DecidableEq α] [DecidableEq β] (e : α ↪ β) (x y : Vertex α) :
    distance (countRelabel e x) (countRelabel e y) = distance x y := by
  have heq : countRelabel e x = countRelabel e y ↔ x = y :=
    (count_relabel_injective e).eq_iff
  simp only [distance, heq]
  simp only [Edge, countRelabel, count_first_make,
    count_second_make, count_third_make, e.injective.eq_iff]

theorem count_relabel_gp {α : Type u} {β : Type v}
    [DecidableEq α] [DecidableEq β] (e : α ↪ β)
    {S : Finset (Vertex α)} (hS : DistanceGP S) :
    DistanceGP (S.image (countRelabel e)) := by
  intro x y z hx hy hz hxy hzx hzy
  obtain ⟨a, ha, rfl⟩ := Finset.mem_image.mp hx
  obtain ⟨b, hb, rfl⟩ := Finset.mem_image.mp hy
  obtain ⟨c, hc, rfl⟩ := Finset.mem_image.mp hz
  have hab : a ≠ b := fun h => hxy (congrArg (countRelabel e) h)
  have hca : c ≠ a := fun h => hzx (congrArg (countRelabel e) h)
  have hcb : c ≠ b := fun h => hzy (congrArg (countRelabel e) h)
  simpa only [count_relabel_distance] using hS ha hb hc hab hca hcb

/- The lower set is defined by vertex inequalities, not by its desired size. -/
def middlePeak (m : ℕ) : Finset (Vertex (Fin m)) :=
  Finset.univ.filter fun x => first x < second x ∧ third x < second x

theorem middlePeak_independent (m : ℕ) : CountIndependent (middlePeak m) := by
  intro x y hx hy hE
  have hx' := (Finset.mem_filter.mp hx).2
  have hy' := (Finset.mem_filter.mp hy).2
  have hbad : second x < third x := by
    simpa only [hE.1, hE.2] using hy'.1
  exact (lt_asymm hx'.2 hbad)

theorem middlePeak_gp (m : ℕ) : DistanceGP (middlePeak m) :=
  count_independent_gp (middlePeak_independent m)

abbrev PeakCode (m : ℕ) := Σ b : Fin m, Fin b.val × Fin b.val

def peakEncode {m : ℕ} (t : PeakCode m) : Vertex (Fin m) :=
  make ⟨t.2.1.val, Nat.lt_trans t.2.1.isLt t.1.isLt⟩ t.1
    ⟨t.2.2.val, Nat.lt_trans t.2.2.isLt t.1.isLt⟩
    (by intro h; have hv := congrArg Fin.val h; dsimp at hv; omega)
    (by intro h; have hv := congrArg Fin.val h; dsimp at hv; omega)

theorem peakEncode_injective {m : ℕ} : Function.Injective (@peakEncode m) := by
  intro x y h
  rcases x with ⟨b, a, c⟩
  rcases y with ⟨b', a', c'⟩
  have hb : b = b' := congrArg second h
  subst b'
  have ha : a = a' := by
    apply Fin.ext
    exact congrArg (fun w => (first w).val) h
  have hc : c = c' := by
    apply Fin.ext
    exact congrArg (fun w => (third w).val) h
  subst a'
  subst c'
  rfl

theorem middlePeak_eq_image (m : ℕ) :
    middlePeak m = (Finset.univ : Finset (PeakCode m)).image peakEncode := by
  classical
  ext x
  constructor
  · intro hx
    have hp := (Finset.mem_filter.mp hx).2
    let t : PeakCode m := ⟨second x, ⟨(first x).val, hp.1⟩, ⟨(third x).val, hp.2⟩⟩
    refine Finset.mem_image.mpr ⟨t, Finset.mem_univ _, ?_⟩
    apply count_vertex_ext <;> apply Fin.ext <;> rfl
  · intro hx
    obtain ⟨t, _, rfl⟩ := Finset.mem_image.mp hx
    apply Finset.mem_filter.mpr
    refine ⟨Finset.mem_univ _, ?_⟩
    exact ⟨t.2.1.isLt, t.2.2.isLt⟩

theorem middlePeak_card (m : ℕ) : (middlePeak m).card = squareSum m := by
  classical
  rw [middlePeak_eq_image, Finset.card_image_of_injective _ peakEncode_injective]
  simp only [Finset.card_univ, PeakCode, Fintype.card_sigma, Fintype.card_prod,
    Fintype.card_fin]
  exact Fin.sum_univ_eq_sum_range (fun i => i * i) m

theorem exists_gp_squareSum {α : Type u} [Fintype α] [DecidableEq α] :
    ∃ S : Finset (Vertex α), DistanceGP S ∧ S.card = squareSum (Fintype.card α) := by
  classical
  let e : Fin (Fintype.card α) ↪ α := (Fintype.equivFin α).symm.toEmbedding
  refine ⟨(middlePeak (Fintype.card α)).image (countRelabel e),
    count_relabel_gp e (middlePeak_gp _), ?_⟩
  rw [Finset.card_image_of_injective _ (count_relabel_injective e), middlePeak_card]

theorem count_squareSum_succ (n : ℕ) : squareSum (n + 1) = squareSum n + n * n := by
  simp [squareSum, Finset.sum_range_succ]

theorem count_squareSum_scaled (n : ℕ) :
    6 * squareSum n + 3 * n * n = 2 * n * n * n + n := by
  induction n with
  | zero => simp [squareSum]
  | succ n ih =>
      rw [count_squareSum_succ]
      nlinarith

theorem squareSum_closed_form (n : ℕ) :
    squareSum n = n * (n - 1) * (2 * n - 1) / 6 := by
  have hmul : 6 * squareSum n = n * (n - 1) * (2 * n - 1) := by
    cases n with
    | zero => simp [squareSum]
    | succ n =>
        have h := count_squareSum_scaled (n + 1)
        have h₁ : n + 1 - 1 = n := by omega
        have h₂ : 2 * (n + 1) - 1 = 2 * n + 1 := by omega
        change 6 * squareSum (n + 1) = (n + 1) * (n + 1 - 1) * (2 * (n + 1) - 1)
        rw [h₁, h₂]
        nlinarith
  omega

/- An independent set injects into the middle-peak set by rotating each
   distinct-letter word, and exchanging the letters of a non-peak palindrome.
   These are symbolic cases, not enumeration of finite alphabets. -/
def countCanonical {m : ℕ} (x : Vertex (Fin m)) : Vertex (Fin m) :=
  if h : first x = third x then
    if first x < second x then x
    else make (second x) (first x) (second x)
      (Ne.symm (first_ne_second x)) (first_ne_second x)
  else if first x < second x ∧ third x < second x then x
  else if second x < first x ∧ third x < first x then
    make (third x) (first x) (second x) (Ne.symm h) (first_ne_second x)
  else make (second x) (third x) (first x) (second_ne_third x) (Ne.symm h)

theorem countCanonical_mem {m : ℕ} (x : Vertex (Fin m)) :
    countCanonical x ∈ middlePeak m := by
  apply Finset.mem_filter.mpr
  refine ⟨Finset.mem_univ _, ?_⟩
  have h₁ := first_ne_second x
  have h₂ := second_ne_third x
  have h₁v : (first x).val ≠ (second x).val := fun h => h₁ (Fin.ext h)
  have h₂v : (second x).val ≠ (third x).val := fun h => h₂ (Fin.ext h)
  by_cases h : first x = third x
  · by_cases hb : first x < second x
    · simp only [countCanonical, dite_eq_left h, ite_eq_left hb]
      exact ⟨hb, by simpa only [← h] using hb⟩
    · have hb' : second x < first x := by
        change (second x).val < (first x).val
        change ¬ (first x).val < (second x).val at hb
        omega
      simp only [countCanonical, dite_eq_left h, ite_eq_right hb, count_first_make,
        count_second_make, count_third_make]
      exact ⟨hb', hb'⟩
  · by_cases hm : first x < second x ∧ third x < second x
    · simp only [countCanonical, dite_eq_right h, ite_eq_left hm]
      exact hm
    · by_cases hf : second x < first x ∧ third x < first x
      · simp only [countCanonical, dite_eq_right h, ite_eq_right hm, ite_eq_left hf,
          count_first_make, count_second_make, count_third_make]
        exact ⟨hf.2, hf.1⟩
      · have h₃v : (first x).val ≠ (third x).val := fun he => h (Fin.ext he)
        have hc : second x < third x ∧ first x < third x := by
          change (second x).val < (third x).val ∧ (first x).val < (third x).val
          change ¬ ((first x).val < (second x).val ∧ (third x).val < (second x).val) at hm
          change ¬ ((second x).val < (first x).val ∧ (third x).val < (first x).val) at hf
          omega
        simp only [countCanonical, dite_eq_right h, ite_eq_right hm, ite_eq_right hf,
          count_first_make, count_second_make, count_third_make]
        exact hc

set_option maxRecDepth 4096 in
theorem countCanonical_collision {m : ℕ} {x y : Vertex (Fin m)}
    (h : countCanonical x = countCanonical y) :
    x = y ∨ Edge x y ∨ Edge y x := by
  rcases x with ⟨⟨a, b, c⟩, hab, hbc⟩
  rcases y with ⟨⟨d, e, f⟩, hde, hef⟩
  change a ≠ b at hab
  change b ≠ c at hbc
  change d ≠ e at hde
  change e ≠ f at hef
  have hab' : a ≠ b := hab
  have hbc' : b ≠ c := hbc
  have hde' : d ≠ e := hde
  have hef' : e ≠ f := hef
  have h₁ := congrArg first h
  have h₂ := congrArg second h
  have h₃ := congrArg third h
  clear h
  unfold countCanonical at h₁ h₂ h₃
  split_ifs at h₁ h₂ h₃ <;>
    simp_all [first, second, third, make, Edge, Legal]
  all_goals (subst_vars; (first | rfl | contradiction))

theorem independent_card_fin {m : ℕ} {S : Finset (Vertex (Fin m))}
    (hS : CountIndependent S) : S.card ≤ squareSum m := by
  classical
  have hcard : S.card ≤ (middlePeak m).card := by
    apply Finset.card_le_card_of_injOn countCanonical
    · intro x _
      exact countCanonical_mem x
    · intro x hx y hy hxy
      rcases countCanonical_collision hxy with h | h | h
      · exact h
      · exact False.elim (hS hx hy h)
      · exact False.elim (hS hy hx h)
  simpa only [middlePeak_card] using hcard

theorem independent_card {α : Type u} [Fintype α] [DecidableEq α]
    {S : Finset (Vertex α)} (hS : CountIndependent S) :
    S.card ≤ squareSum (Fintype.card α) := by
  classical
  let e : α ↪ Fin (Fintype.card α) := (Fintype.equivFin α).toEmbedding
  have hi : CountIndependent (S.image (countRelabel e)) := by
    intro x y hx hy hE
    obtain ⟨a, ha, rfl⟩ := Finset.mem_image.mp hx
    obtain ⟨b, hb, rfl⟩ := Finset.mem_image.mp hy
    apply hS ha hb
    exact ⟨e.injective hE.1, e.injective hE.2⟩
  have hc := independent_card_fin hi
  simpa only [Finset.card_image_of_injective _ (count_relabel_injective e)] using hc

/- Pure finite-matrix injection. Both hypotheses describing the exceptional
   branch are later obtained from the actual DistanceGP condition. -/
theorem count_matrix_injection {α : Type u} [DecidableEq α]
    (B : Finset α) (M E : Finset (α × α))
    (hM : M ⊆ B ×ˢ B) (hE : E ⊆ B ×ˢ B)
    (hoff : ∀ p ∈ E, p.1 ≠ p.2)
    (hdiag : ∀ p ∈ E, (p.2, p.1) ∈ M → (p.1, p.1) ∉ M)
    (hrow : ∀ p ∈ E, (p.2, p.1) ∈ M →
      ∀ q ∈ E, p.1 = q.1 → p = q) :
    M.card + E.card ≤ B.card * B.card := by
  classical
  let f : α × α → α × α := fun p =>
    if (p.2, p.1) ∈ M then (p.1, p.1) else (p.2, p.1)
  have hf : Set.MapsTo f E (((B ×ˢ B) \ M : Finset (α × α)) : Set (α × α)) := by
    intro p hp
    have hpB := Finset.mem_product.mp (hE hp)
    apply Finset.mem_sdiff.mpr
    by_cases hm : (p.2, p.1) ∈ M
    · simp only [f, ite_eq_left hm]
      exact ⟨Finset.mem_product.mpr ⟨hpB.1, hpB.1⟩, hdiag p hp hm⟩
    · simp only [f, ite_eq_right hm]
      exact ⟨Finset.mem_product.mpr ⟨hpB.2, hpB.1⟩, hm⟩
  have hinj : Set.InjOn f E := by
    intro p hp q hq hpq
    by_cases hm : (p.2, p.1) ∈ M <;> by_cases hn : (q.2, q.1) ∈ M
    · have hh : p.1 = q.1 := by simpa [f, hm, hn] using congrArg Prod.fst hpq
      exact hrow p hp hm q hq hh
    · have h₁ : p.1 = q.2 := by simpa [f, hm, hn] using congrArg Prod.fst hpq
      have h₂ : p.1 = q.1 := by simpa [f, hm, hn] using congrArg Prod.snd hpq
      exact False.elim (hoff q hq (h₂.symm.trans h₁))
    · have h₁ : p.2 = q.1 := by simpa [f, hm, hn] using congrArg Prod.fst hpq
      have h₂ : p.1 = q.1 := by simpa [f, hm, hn] using congrArg Prod.snd hpq
      exact False.elim (hoff p hp (h₂.trans h₁.symm))
    · apply Prod.ext
      · simpa [f, hm, hn] using congrArg Prod.snd hpq
      · simpa [f, hm, hn] using congrArg Prod.fst hpq
  have hcard := Finset.card_le_card_of_injOn f hf hinj
  have hMcard := Finset.card_le_card hM
  rw [Finset.card_sdiff_of_subset hM, Finset.card_product] at hcard
  rw [Finset.card_product] at hMcard
  omega

def middleMatrix {α : Type u} [DecidableEq α] (S : Finset (Vertex α)) (z : α) :
    Finset (α × α) :=
  (S.filter fun x => second x = z).image (fun x => (first x, third x))

def endMatrix {α : Type u} [DecidableEq α] (S : Finset (Vertex α)) (z : α) :
    Finset (α × α) :=
  (S.filter fun x => third x = z).image (fun x => (first x, second x))

theorem count_mem_middleMatrix {α : Type u} [DecidableEq α]
    (S : Finset (Vertex α)) (a b z : α) (haz : a ≠ z) (hbz : b ≠ z) :
    (a,b) ∈ middleMatrix S z ↔ make a z b haz (Ne.symm hbz) ∈ S := by
  constructor
  · intro h
    obtain ⟨x, hx, he⟩ := Finset.mem_image.mp h
    have h₁ : first x = a := congrArg Prod.fst he
    have h₃ : third x = b := congrArg Prod.snd he
    have hx' := Finset.mem_filter.mp hx
    have heq : x = make a z b haz (Ne.symm hbz) := count_vertex_ext h₁ hx'.2 h₃
    simpa only [heq] using hx'.1
  · intro h
    exact Finset.mem_image.mpr ⟨make a z b haz (Ne.symm hbz),
      Finset.mem_filter.mpr ⟨h, rfl⟩, rfl⟩

theorem count_mem_endMatrix {α : Type u} [DecidableEq α]
    (S : Finset (Vertex α)) (a b z : α) (hab : a ≠ b) (hbz : b ≠ z) :
    (a,b) ∈ endMatrix S z ↔ make a b z hab hbz ∈ S := by
  constructor
  · intro h
    obtain ⟨x, hx, he⟩ := Finset.mem_image.mp h
    have h₁ : first x = a := congrArg Prod.fst he
    have h₂ : second x = b := congrArg Prod.snd he
    have hx' := Finset.mem_filter.mp hx
    have heq : x = make a b z hab hbz := count_vertex_ext h₁ h₂ hx'.2
    simpa only [heq] using hx'.1
  · intro h
    exact Finset.mem_image.mpr ⟨make a b z hab hbz,
      Finset.mem_filter.mpr ⟨h, rfl⟩, rfl⟩

theorem count_matrix_forbid_diagonal {α : Type u} [DecidableEq α]
    {S : Finset (Vertex α)} (hS : DistanceGP S)
    (a b z : α) (hab : a ≠ b) (haz : a ≠ z) (hbz : b ≠ z)
    (he : make a b z hab hbz ∈ S)
    (hm : make b z a hbz (Ne.symm haz) ∈ S) :
    make a z a haz (Ne.symm haz) ∉ S := by
  intro hd
  have hba : b ≠ a := Ne.symm hab
  have hza : z ≠ a := Ne.symm haz
  apply count_forbidden_123 hS he hm hd <;>
    simp only [distance, count_vertex_eq_iff, Edge, first, second, third, make] <;>
    simp_all

theorem count_matrix_forbid_same_row {α : Type u} [DecidableEq α]
    {S : Finset (Vertex α)} (hS : DistanceGP S)
    (a b c z : α) (hab : a ≠ b) (hac : a ≠ c) (hbc : b ≠ c)
    (haz : a ≠ z) (hbz : b ≠ z) (hcz : c ≠ z)
    (he : make a b z hab hbz ∈ S)
    (hm : make b z a hbz (Ne.symm haz) ∈ S) :
    make a c z hac hcz ∉ S := by
  intro hc
  have hza : z ≠ a := Ne.symm haz
  apply count_forbidden_123 hS he hm hc <;>
    simp only [distance, count_vertex_eq_iff, Edge, first, second, third, make] <;>
    simp_all

def containsLetter {α : Type u} (z : α) (x : Vertex α) : Prop :=
  first x = z ∨ second x = z ∨ third x = z

instance {α : Type u} [DecidableEq α] (z : α) (x : Vertex α) :
    Decidable (containsLetter z x) := by
  unfold containsLetter
  infer_instance

def letterSet {α : Type u} [DecidableEq α]
    (S : Finset (Vertex α)) (z : α) : Finset (Vertex α) :=
  S.filter (containsLetter z)

theorem count_middleMatrix_card {α : Type u} [DecidableEq α]
    (S : Finset (Vertex α)) (z : α) :
    (middleMatrix S z).card = (S.filter fun x => second x = z).card := by
  unfold middleMatrix
  apply Finset.card_image_of_injOn
  intro x hx y hy hxy
  have hpair : (first x, third x) = (first y, third y) := hxy
  have h₁ := congrArg (Prod.fst : α × α → α) hpair
  have h₃ := congrArg (Prod.snd : α × α → α) hpair
  apply count_vertex_ext (α := α) (x := x) (y := y)
  · exact h₁
  · exact (Finset.mem_filter.mp hx).2.trans (Finset.mem_filter.mp hy).2.symm
  · exact h₃

theorem count_endMatrix_card {α : Type u} [DecidableEq α]
    (S : Finset (Vertex α)) (z : α) :
    (endMatrix S z).card = (S.filter fun x => third x = z).card := by
  unfold endMatrix
  apply Finset.card_image_of_injOn
  intro x hx y hy hxy
  apply count_vertex_ext (α := α) (x := x) (y := y)
  · exact congrArg (fun p : α × α => p.1) hxy
  · exact congrArg (fun p : α × α => p.2) hxy
  · exact (Finset.mem_filter.mp hx).2.trans (Finset.mem_filter.mp hy).2.symm

theorem missing_first_card {α : Type u} [Fintype α] [DecidableEq α]
    {S : Finset (Vertex α)} (hS : DistanceGP S) (z : α)
    (hfirst : ∀ x ∈ S, first x ≠ z) :
    (letterSet S z).card ≤ (Fintype.card α - 1) * (Fintype.card α - 1) := by
  classical
  let B : Finset α := Finset.univ.erase z
  let M := middleMatrix S z
  let E := endMatrix S z
  have hM : M ⊆ B ×ˢ B := by
    intro p hp
    obtain ⟨x, hx, rfl⟩ := Finset.mem_image.mp hp
    have hx' := Finset.mem_filter.mp hx
    have hlast : third x ≠ z := by
      intro h
      exact second_ne_third x (hx'.2.trans h.symm)
    simpa only [B, Finset.mem_product, Finset.mem_erase, Finset.mem_univ, and_true]
      using And.intro (hfirst x hx'.1) hlast
  have hE : E ⊆ B ×ˢ B := by
    intro p hp
    obtain ⟨x, hx, rfl⟩ := Finset.mem_image.mp hp
    have hx' := Finset.mem_filter.mp hx
    have hmiddle : second x ≠ z := by
      intro h
      exact second_ne_third x (h.trans hx'.2.symm)
    simpa only [B, Finset.mem_product, Finset.mem_erase, Finset.mem_univ, and_true]
      using And.intro (hfirst x hx'.1) hmiddle
  have hoff : ∀ p ∈ E, p.1 ≠ p.2 := by
    intro p hp
    obtain ⟨x, _, rfl⟩ := Finset.mem_image.mp hp
    exact first_ne_second x
  have hcoords : ∀ p ∈ E, p.1 ≠ z ∧ p.2 ≠ z := by
    intro p hp
    have hp' := hE hp
    simpa only [B, Finset.mem_product, Finset.mem_erase, Finset.mem_univ, and_true]
      using hp'
  have hdiag : ∀ p ∈ E, (p.2, p.1) ∈ M → (p.1, p.1) ∉ M := by
    rintro ⟨a,b⟩ he hm hd
    have hab : a ≠ b := hoff (a,b) he
    obtain ⟨haz, hbz⟩ := hcoords (a,b) he
    have h₁ := (count_mem_endMatrix S a b z hab hbz).mp he
    have h₂ := (count_mem_middleMatrix S b a z hbz haz).mp hm
    have h₃ := (count_mem_middleMatrix S a a z haz haz).mp hd
    exact count_matrix_forbid_diagonal hS a b z hab haz hbz h₁ h₂ h₃
  have hrow : ∀ p ∈ E, (p.2, p.1) ∈ M →
      ∀ q ∈ E, p.1 = q.1 → p = q := by
    rintro ⟨a,b⟩ he hm ⟨a',c⟩ hc hfirsteq
    dsimp at hfirsteq
    subst a'
    apply Prod.ext
    · rfl
    · by_contra hbc
      have hab : a ≠ b := hoff (a,b) he
      have hac : a ≠ c := hoff (a,c) hc
      obtain ⟨haz, hbz⟩ := hcoords (a,b) he
      have hcz : c ≠ z := (hcoords (a,c) hc).2
      have h₁ := (count_mem_endMatrix S a b z hab hbz).mp he
      have h₂ := (count_mem_middleMatrix S b a z hbz haz).mp hm
      have h₃ := (count_mem_endMatrix S a c z hac hcz).mp hc
      exact count_matrix_forbid_same_row hS a b c z hab hac hbc haz hbz hcz h₁ h₂ h₃
  have hbound := count_matrix_injection B M E hM hE hoff hdiag hrow
  have hsplit : letterSet S z =
      (S.filter fun x => second x = z) ∪ (S.filter fun x => third x = z) := by
    ext x
    simp only [letterSet, Finset.mem_filter, Finset.mem_union, containsLetter]
    constructor
    · rintro ⟨hx, h | h | h⟩
      · exact False.elim (hfirst x hx h)
      · exact Or.inl ⟨hx,h⟩
      · exact Or.inr ⟨hx,h⟩
    · rintro (⟨hx,h⟩ | ⟨hx,h⟩)
      · exact ⟨hx, Or.inr (Or.inl h)⟩
      · exact ⟨hx, Or.inr (Or.inr h)⟩
  have hdisjoint : Disjoint (S.filter fun x => second x = z)
      (S.filter fun x => third x = z) := by
    apply Finset.disjoint_left.mpr
    intro x hx hy
    exact second_ne_third x
      ((Finset.mem_filter.mp hx).2.trans (Finset.mem_filter.mp hy).2.symm)
  rw [hsplit, Finset.card_union_of_disjoint hdisjoint]
  rw [← count_middleMatrix_card S z, ← count_endMatrix_card S z]
  simpa only [B, M, E, Finset.card_erase_of_mem (Finset.mem_univ z), Finset.card_univ]
    using hbound

def countReverse {α : Type u} (x : Vertex α) : Vertex α :=
  make (third x) (second x) (first x)
    (Ne.symm (second_ne_third x)) (Ne.symm (first_ne_second x))

@[simp] theorem count_reverse_reverse {α : Type u} (x : Vertex α) :
    countReverse (countReverse x) = x := by
  apply count_vertex_ext <;> rfl

theorem count_reverse_injective {α : Type u} :
    Function.Injective (@countReverse α) := by
  intro x y h
  simpa only [count_reverse_reverse] using congrArg countReverse h

@[simp] theorem count_reverse_distance {α : Type u} [DecidableEq α]
    (x y : Vertex α) : distance (countReverse x) (countReverse y) = distance y x := by
  have heq : countReverse x = countReverse y ↔ y = x := by
    exact count_reverse_injective.eq_iff.trans eq_comm
  have hedge : Edge (countReverse x) (countReverse y) ↔ Edge y x := by
    simp [Edge, countReverse, eq_comm, and_comm]
  simp only [distance, heq, hedge]
  simp only [countReverse, count_first_make, count_third_make]
  simp only [eq_comm]
  by_cases h₁ : x = y <;> by_cases h₂ : Edge y x <;>
    by_cases h₃ : first x = third y <;> simp_all

theorem count_reverse_gp {α : Type u} [DecidableEq α]
    {S : Finset (Vertex α)} (hS : DistanceGP S) :
    DistanceGP (S.image countReverse) := by
  intro x y z hx hy hz hxy hzx hzy
  obtain ⟨a, ha, rfl⟩ := Finset.mem_image.mp hx
  obtain ⟨b, hb, rfl⟩ := Finset.mem_image.mp hy
  obtain ⟨c, hc, rfl⟩ := Finset.mem_image.mp hz
  have hba : b ≠ a := fun h => hxy (congrArg countReverse h.symm)
  have hcb : c ≠ b := fun h => hzy (congrArg countReverse h)
  have hca : c ≠ a := fun h => hzx (congrArg countReverse h)
  simpa only [count_reverse_distance, Nat.add_comm] using hS hb ha hc hba hcb hca

@[simp] theorem count_reverse_contains {α : Type u} (z : α) (x : Vertex α) :
    containsLetter z (countReverse x) ↔ containsLetter z x := by
  simp [containsLetter, countReverse, or_assoc, or_comm]

theorem count_reverse_letterSet {α : Type u} [DecidableEq α]
    (S : Finset (Vertex α)) (z : α) :
    letterSet (S.image countReverse) z = (letterSet S z).image countReverse := by
  ext x
  constructor
  · intro hx
    obtain ⟨hx, hz⟩ := Finset.mem_filter.mp hx
    obtain ⟨a, ha, rfl⟩ := Finset.mem_image.mp hx
    refine Finset.mem_image.mpr ⟨a, Finset.mem_filter.mpr ⟨ha, ?_⟩, rfl⟩
    exact (count_reverse_contains z a).mp hz
  · intro hx
    obtain ⟨a, ha, rfl⟩ := Finset.mem_image.mp hx
    obtain ⟨ha, hz⟩ := Finset.mem_filter.mp ha
    exact Finset.mem_filter.mpr
      ⟨Finset.mem_image.mpr ⟨a, ha, rfl⟩, (count_reverse_contains z a).mpr hz⟩

theorem missing_last_card {α : Type u} [Fintype α] [DecidableEq α]
    {S : Finset (Vertex α)} (hS : DistanceGP S) (z : α)
    (hlast : ∀ x ∈ S, third x ≠ z) :
    (letterSet S z).card ≤ (Fintype.card α - 1) * (Fintype.card α - 1) := by
  classical
  have hm : ∀ x ∈ S.image countReverse, first x ≠ z := by
    intro x hx
    obtain ⟨a, ha, rfl⟩ := Finset.mem_image.mp hx
    exact hlast a ha
  have h := missing_first_card (count_reverse_gp hS) z hm
  rw [count_reverse_letterSet, Finset.card_image_of_injective _ count_reverse_injective] at h
  exact h

theorem count_edge_ne {α : Type u} {x y : Vertex α} (h : Edge x y) : x ≠ y := by
  intro hxy
  subst y
  exact first_ne_second x h.1

theorem count_edge_distance {α : Type u} [DecidableEq α]
    {x y : Vertex α} (h : Edge x y) : distance x y = 1 := by
  simp [distance, count_edge_ne h, h]

/- This is the common symbolic obstruction for cases I and III.  The only
   selected word beginning at the appended letter can be the arc's source. -/
theorem selected_arc_first {α : Type u} [DecidableEq α]
    {S : Finset (Vertex α)} (hS : DistanceGP S)
    {x y : Vertex α} (hx : x ∈ S) (hy : y ∈ S) (hE : Edge x y)
    (hd : third y ≠ second x) :
    ∀ w ∈ S, first w = third y → w = x := by
  intro w hw hfirst
  by_contra hwx
  have hxw : x ≠ w := Ne.symm hwx
  have hyw : y ≠ w := by
    intro h
    exact hd (hfirst.symm.trans ((congrArg first h).symm.trans hE.1))
  have hnxy : ¬ Edge x w := by
    intro h
    exact hd (hfirst.symm.trans h.1)
  have hnyw : ¬ Edge y w := by
    intro h
    exact second_ne_third y (h.1.symm.trans hfirst)
  have hlast : third x ≠ first w := by
    intro h
    exact second_ne_third y (hE.2.trans (h.trans hfirst))
  apply count_forbidden_123 hS hx hy hw (count_edge_distance hE)
  · simp [distance, hyw, hnyw, hfirst]
  · simp [distance, hxw, hnxy, hlast]

theorem selected_arc_caseI_card {α : Type u} [Fintype α] [DecidableEq α]
    {S : Finset (Vertex α)} (hS : DistanceGP S)
    {x y : Vertex α} (hx : x ∈ S) (hy : y ∈ S) (hE : Edge x y)
    (hda : third y ≠ first x) (hdb : third y ≠ second x) :
    (letterSet S (third y)).card ≤ (Fintype.card α - 1) * (Fintype.card α - 1) := by
  apply missing_first_card hS
  intro w hw heq
  have hwx := selected_arc_first hS hx hy hE hdb w hw heq
  exact hda (heq.symm.trans (congrArg first hwx))

theorem selected_arc_caseII_card {α : Type u} [Fintype α] [DecidableEq α]
    {S : Finset (Vertex α)} (hS : DistanceGP S)
    {x y : Vertex α} (hx : x ∈ S) (hy : y ∈ S) (hE : Edge x y)
    (hdb : third y = second x) (hca : third x ≠ first x) :
    (letterSet S (first x)).card ≤ (Fintype.card α - 1) * (Fintype.card α - 1) := by
  have hrE : Edge (countReverse y) (countReverse x) := by
    exact ⟨hE.2.symm, hE.1.symm⟩
  have hr₁ : third (countReverse x) ≠ first (countReverse y) := by
    change first x ≠ third y
    rw [hdb]
    exact first_ne_second x
  have hr₂ : third (countReverse x) ≠ second (countReverse y) := by
    change first x ≠ second y
    rw [hE.2]
    exact Ne.symm hca
  have h := selected_arc_caseI_card (count_reverse_gp hS)
    (Finset.mem_image.mpr ⟨y, hy, rfl⟩) (Finset.mem_image.mpr ⟨x, hx, rfl⟩)
    hrE hr₁ hr₂
  change (letterSet (S.image countReverse) (first x)).card ≤ _ at h
  rw [count_reverse_letterSet, Finset.card_image_of_injective _ count_reverse_injective] at h
  exact h

theorem selected_arc_last {α : Type u} [DecidableEq α]
    {S : Finset (Vertex α)} (hS : DistanceGP S)
    {x y : Vertex α} (hx : x ∈ S) (hy : y ∈ S) (hE : Edge x y)
    (ha : first x ≠ second y) :
    ∀ w ∈ S, third w = first x → w = y := by
  intro w hw hlast
  have hrE : Edge (countReverse y) (countReverse x) := ⟨hE.2.symm, hE.1.symm⟩
  have h := selected_arc_first (count_reverse_gp hS)
    (Finset.mem_image.mpr ⟨y, hy, rfl⟩) (Finset.mem_image.mpr ⟨x, hx, rfl⟩)
    hrE ha (countReverse w) (Finset.mem_image.mpr ⟨w, hw, rfl⟩) hlast
  exact count_reverse_injective h

theorem count_forbidden_112 {α : Type u} [DecidableEq α]
    {S : Finset (Vertex α)} (hS : DistanceGP S)
    {x y z : Vertex α} (hx : x ∈ S) (hy : y ∈ S) (hz : z ∈ S)
    (h₁ : distance x y = 1) (h₂ : distance y z = 1)
    (h₃ : distance x z = 2) : False := by
  have hxz : x ≠ z := by intro h; subst z; simp at h₃
  have hyx : y ≠ x := by intro h; subst y; simp at h₁
  have hyz : y ≠ z := by intro h; subst z; simp at h₂
  apply hS hx hz hy hxz hyx hyz
  omega

/- A direct finite injection for two exceptional words and two missing
   diagonal middle-word cells. This will be applied to selected three-cycles. -/
theorem count_two_exception_card {α : Type u} [Fintype α] [DecidableEq α]
    (T : Finset (Vertex α)) (z b c : α) (u v : Vertex α)
    (huv : u ≠ v) (hbz : b ≠ z) (hcz : c ≠ z) (hbc : b ≠ c)
    (hmiddle : ∀ w ∈ T, w ≠ u → w ≠ v → second w = z)
    (hnob : ∀ w ∈ T, second w = z → first w = b → third w = b → False)
    (hnoc : ∀ w ∈ T, second w = z → first w = c → third w = c → False) :
    T.card ≤ (Fintype.card α - 1) * (Fintype.card α - 1) := by
  classical
  let f : Vertex α → α × α := fun w =>
    if w = u then (b,b) else if w = v then (c,c) else (first w, third w)
  have hfu : f u = (b,b) := by simp [f]
  have hfv : f v = (c,c) := by simp [f, Ne.symm huv]
  have hfbu : ∀ w ∈ T, f w = (b,b) → w = u := by
    intro w hw hf
    by_cases hwu : w = u
    · exact hwu
    by_cases hwv : w = v
    · subst w
      have hcb : c = b := by
        simpa only [hfv] using congrArg (fun p : α × α => p.1) hf
      exact False.elim (hbc hcb.symm)
    · have hh : (first w, third w) = (b,b) := by simpa [f, hwu, hwv] using hf
      exact False.elim (hnob w hw (hmiddle w hw hwu hwv)
        (congrArg (fun p : α × α => p.1) hh)
        (congrArg (fun p : α × α => p.2) hh))
  have hfcv : ∀ w ∈ T, f w = (c,c) → w = v := by
    intro w hw hf
    by_cases hwu : w = u
    · subst w
      have hbc' : b = c := by
        simpa only [hfu] using congrArg (fun p : α × α => p.1) hf
      exact False.elim (hbc hbc')
    by_cases hwv : w = v
    · exact hwv
    · have hh : (first w, third w) = (c,c) := by simpa [f, hwu, hwv] using hf
      exact False.elim (hnoc w hw (hmiddle w hw hwu hwv)
        (congrArg (fun p : α × α => p.1) hh)
        (congrArg (fun p : α × α => p.2) hh))
  have hmap : Set.MapsTo f T
      (((Finset.univ.erase z) ×ˢ (Finset.univ.erase z) : Finset (α × α)) : Set (α × α)) := by
    intro w hw
    by_cases hwu : w = u
    · subst w
      simp [hfu, hbz]
    by_cases hwv : w = v
    · subst w
      simp [hfv, hcz]
    have hm := hmiddle w hw hwu hwv
    have h₁ : first w ≠ z := by simpa only [← hm] using first_ne_second w
    have h₃ : third w ≠ z := by simpa only [← hm] using Ne.symm (second_ne_third w)
    simp [f, hwu, hwv, h₁, h₃]
  have hinj : Set.InjOn f T := by
    intro x hx y hy hxy
    by_cases hxu : x = u
    · subst x
      exact (hfbu y hy (hxy.symm.trans hfu)).symm
    by_cases hxv : x = v
    · subst x
      exact (hfcv y hy (hxy.symm.trans hfv)).symm
    have hyu : y ≠ u := by
      intro h
      subst y
      exact hxu (hfbu x hx (hxy.trans hfu))
    have hyv : y ≠ v := by
      intro h
      subst y
      exact hxv (hfcv x hx (hxy.trans hfv))
    have hh : (first x, third x) = (first y, third y) := by
      simpa only [f, ite_eq_right hxu, ite_eq_right hxv,
        ite_eq_right hyu, ite_eq_right hyv] using hxy
    have hcoords := Prod.mk.inj hh
    exact count_vertex_ext hcoords.1
      ((hmiddle x hx hxu hxv).trans (hmiddle y hy hyu hyv).symm) hcoords.2
  have hcard := Finset.card_le_card_of_injOn f hmap hinj
  simpa only [Finset.card_product, Finset.card_erase_of_mem (Finset.mem_univ z),
    Finset.card_univ] using hcard

theorem selected_cycle_card {α : Type u} [Fintype α] [DecidableEq α]
    {S : Finset (Vertex α)} (hS : DistanceGP S)
    (a b c : α) (hab : a ≠ b) (hbc : b ≠ c) (hca : c ≠ a)
    (hu : make a b c hab hbc ∈ S) (hv : make b c a hbc hca ∈ S) :
    (letterSet S a).card ≤ (Fintype.card α - 1) * (Fintype.card α - 1) := by
  let u := make a b c hab hbc
  let v := make b c a hbc hca
  have hE : Edge u v := ⟨rfl,rfl⟩
  have hstart : ∀ w ∈ S, first w = a → w = u :=
    selected_arc_first hS hu hv hE hab
  have hend : ∀ w ∈ S, third w = a → w = v :=
    selected_arc_last hS hu hv hE (Ne.symm hca)
  have hnob : make b a b (Ne.symm hab) hab ∉ S := by
    intro hb
    apply count_forbidden_112 hS hb hu hv <;>
      simp [distance, Edge, count_vertex_eq_iff, hab, Ne.symm hab]
  have hnoc : make c a c hca (Ne.symm hca) ∉ S := by
    intro hc
    apply count_forbidden_112 hS hu hv hc <;>
      simp [distance, Edge, count_vertex_eq_iff, hab, hbc, Ne.symm hbc, Ne.symm hca]
  apply count_two_exception_card (letterSet S a) a b c u v (count_edge_ne hE)
    (Ne.symm hab) hca hbc
  · intro w hw hwu hwv
    obtain ⟨hwS, hwletter⟩ := Finset.mem_filter.mp hw
    rcases hwletter with h | h | h
    · exact False.elim (hwu (hstart w hwS h))
    · exact h
    · exact False.elim (hwv (hend w hwS h))
  · intro w hw hm hf ht
    have heq : w = make b a b (Ne.symm hab) hab := count_vertex_ext hf hm ht
    apply hnob
    simpa only [heq] using (Finset.mem_filter.mp hw).1
  · intro w hw hm hf ht
    have heq : w = make c a c hca (Ne.symm hca) := count_vertex_ext hf hm ht
    apply hnoc
    simpa only [heq] using (Finset.mem_filter.mp hw).1

theorem selected_digon_first {α : Type u} [DecidableEq α]
    {S : Finset (Vertex α)} (hS : DistanceGP S)
    (a b : α) (hab : a ≠ b)
    (hu : make a b a hab (Ne.symm hab) ∈ S)
    (hv : make b a b (Ne.symm hab) hab ∈ S) :
    ∀ w ∈ S, first w = a → w = make a b a hab (Ne.symm hab) := by
  let u := make a b a hab (Ne.symm hab)
  let v := make b a b (Ne.symm hab) hab
  have huv : Edge u v := ⟨rfl,rfl⟩
  have hvu : Edge v u := ⟨rfl,rfl⟩
  intro w hw hfirst
  by_contra hwu
  have huw : u ≠ w := Ne.symm hwu
  have hvw : v ≠ w := by
    intro h
    have : b = a := (congrArg first h).trans hfirst
    exact hab this.symm
  have hue : ¬ Edge u w := by
    intro h
    exact hab (hfirst.symm.trans h.1)
  have hduw : distance u w = 2 := by
    simp [distance, huw, hue, u, hfirst]
  by_cases hsecond : second w = b
  · have hvwe : Edge v w := ⟨hfirst,hsecond⟩
    exact count_forbidden_112 hS hu hv hw
      (count_edge_distance huv) (count_edge_distance hvwe) hduw
  · have hve : ¬ Edge v w := fun h => hsecond h.2
    have hdvw : distance v w = 3 := by
      simp [distance, hvw, hve, v, hfirst, Ne.symm hab]
    exact count_forbidden_123 hS hv hu hw (count_edge_distance hvu) hduw hdvw

theorem selected_digon_last {α : Type u} [DecidableEq α]
    {S : Finset (Vertex α)} (hS : DistanceGP S)
    (a b : α) (hab : a ≠ b)
    (hu : make a b a hab (Ne.symm hab) ∈ S)
    (hv : make b a b (Ne.symm hab) hab ∈ S) :
    ∀ w ∈ S, third w = a → w = make a b a hab (Ne.symm hab) := by
  intro w hw hlast
  have hu' : make a b a hab (Ne.symm hab) ∈ S.image countReverse := by
    exact Finset.mem_image.mpr ⟨make a b a hab (Ne.symm hab), hu, rfl⟩
  have hv' : make b a b (Ne.symm hab) hab ∈ S.image countReverse := by
    exact Finset.mem_image.mpr ⟨make b a b (Ne.symm hab) hab, hv, rfl⟩
  have h := selected_digon_first (count_reverse_gp hS) a b hab hu' hv'
    (countReverse w) (Finset.mem_image.mpr ⟨w, hw, rfl⟩) hlast
  exact count_reverse_injective h

theorem count_fixed_middle_card {α : Type u} [DecidableEq α]
    (T : Finset (Vertex α)) (B : Finset α) (z : α)
    (hm : ∀ w ∈ T, second w = z)
    (hf : ∀ w ∈ T, first w ∈ B) (ht : ∀ w ∈ T, third w ∈ B) :
    T.card ≤ B.card * B.card := by
  have h : T.card ≤ (B ×ˢ B).card := by
    apply Finset.card_le_card_of_injOn (fun w => (first w, third w))
    · intro w hw
      exact Finset.mem_product.mpr ⟨hf w hw, ht w hw⟩
    · intro x hx y hy hxy
      have hcoords := Prod.mk.inj hxy
      exact count_vertex_ext hcoords.1
        ((hm x hx).trans (hm y hy).symm) hcoords.2
  simpa only [Finset.card_product] using h

theorem selected_digon_incidence {α : Type u} [Fintype α] [DecidableEq α]
    {S : Finset (Vertex α)} (hS : DistanceGP S)
    (a b : α) (hab : a ≠ b)
    (hu : make a b a hab (Ne.symm hab) ∈ S)
    (hv : make b a b (Ne.symm hab) hab ∈ S) :
    (letterSet S a).card ≤ (Fintype.card α - 2) * (Fintype.card α - 2) + 2 := by
  classical
  let u := make a b a hab (Ne.symm hab)
  let v := make b a b (Ne.symm hab) hab
  let T := (letterSet S a) \ {u,v}
  let B : Finset α := (Finset.univ.erase a).erase b
  have hdata : ∀ w ∈ T,
      second w = a ∧ (first w ≠ a ∧ first w ≠ b) ∧ (third w ≠ a ∧ third w ≠ b) := by
    intro w hw
    obtain ⟨hwletter, hwnot⟩ := Finset.mem_sdiff.mp hw
    obtain ⟨hwS, hletter⟩ := Finset.mem_filter.mp hwletter
    have hwu : w ≠ u := by intro h; exact hwnot (by simp [h])
    have hwv : w ≠ v := by intro h; exact hwnot (by simp [h])
    have hfa : first w ≠ a := fun h => hwu (selected_digon_first hS a b hab hu hv w hwS h)
    have hfb : first w ≠ b := fun h => hwv
      (selected_digon_first hS b a (Ne.symm hab) hv hu w hwS h)
    have hta : third w ≠ a := fun h => hwu (selected_digon_last hS a b hab hu hv w hwS h)
    have htb : third w ≠ b := fun h => hwv
      (selected_digon_last hS b a (Ne.symm hab) hv hu w hwS h)
    have hm : second w = a := by
      rcases hletter with h | h | h
      · exact False.elim (hfa h)
      · exact h
      · exact False.elim (hta h)
    exact ⟨hm, ⟨hfa,hfb⟩, ⟨hta,htb⟩⟩
  have hsmall : T.card ≤ B.card * B.card := by
    apply count_fixed_middle_card T B a
    · intro w hw; exact (hdata w hw).1
    · intro w hw; simpa [B] using And.intro (hdata w hw).2.1.2 (hdata w hw).2.1.1
    · intro w hw; simpa [B] using And.intro (hdata w hw).2.2.2 (hdata w hw).2.2.1
  have hB : B.card = Fintype.card α - 2 := by
    have hb : b ∈ (Finset.univ : Finset α).erase a := by simp [Ne.symm hab]
    simp only [B, Finset.card_erase_of_mem hb,
      Finset.card_erase_of_mem (Finset.mem_univ a), Finset.card_univ]
    omega
  have hsub : letterSet S a ⊆ T ∪ {u,v} := by
    intro w hw
    by_cases hm : w ∈ ({u,v} : Finset (Vertex α))
    · exact Finset.mem_union_right _ hm
    · exact Finset.mem_union_left _ (Finset.mem_sdiff.mpr ⟨hw,hm⟩)
  have hcover := (Finset.card_le_card hsub).trans (Finset.card_union_le T {u,v})
  have hpair : ({u,v} : Finset (Vertex α)).card ≤ 2 := by
    rcases Finset.card_pair_eq_one_or_two (a := u) (b := v) with h | h <;> omega
  rw [hB] at hsmall
  omega

theorem selected_digon_card {α : Type u} [Fintype α] [DecidableEq α]
    {S : Finset (Vertex α)} (hS : DistanceGP S) (hm : 3 ≤ Fintype.card α)
    (a b : α) (hab : a ≠ b)
    (hu : make a b a hab (Ne.symm hab) ∈ S)
    (hv : make b a b (Ne.symm hab) hab ∈ S) :
    (letterSet S a).card ≤ (Fintype.card α - 1) * (Fintype.card α - 1) := by
  have h := selected_digon_incidence hS a b hab hu hv
  have heq : Fintype.card α - 1 = (Fintype.card α - 2) + 1 := by omega
  have hpos : 1 ≤ Fintype.card α - 2 := by omega
  rw [heq]
  nlinarith

def outsideLetter {α : Type u} [DecidableEq α]
    (S : Finset (Vertex α)) (z : α) : Finset (Vertex α) :=
  S.filter fun x => ¬ containsLetter z x

theorem letter_outside_card {α : Type u} [DecidableEq α]
    (S : Finset (Vertex α)) (z : α) :
    (letterSet S z).card + (outsideLetter S z).card = S.card :=
  Finset.card_filter_add_card_filter_not (s := S) (containsLetter z)

theorem count_card_three_cover {α : Type u} [Fintype α] [DecidableEq α]
    (hcard : Fintype.card α = 3) (a b c : α)
    (hab : a ≠ b) (hbc : b ≠ c) (hca : c ≠ a) :
    ∀ d : α, d = a ∨ d = b ∨ d = c := by
  classical
  have hthree : ({a,b,c} : Finset α).card = 3 := by
    simp [hab, hbc, Ne.symm hca]
  have hfull : ({a,b,c} : Finset α) = Finset.univ := by
    apply Finset.eq_of_subset_of_card_le (Finset.subset_univ _)
    simp [hthree, hcard]
  intro d
  have hd : d ∈ ({a,b,c} : Finset α) := by rw [hfull]; exact Finset.mem_univ d
  simpa only [Finset.mem_insert, Finset.mem_singleton] using hd

theorem count_outside_two_words {α : Type u} [DecidableEq α]
    (a b c : α) (hbc : b ≠ c)
    (hcover : ∀ d : α, d = a ∨ d = b ∨ d = c)
    (w : Vertex α) (hw : ¬ containsLetter a w) :
    w = make b c b hbc (Ne.symm hbc) ∨
      w = make c b c (Ne.symm hbc) hbc := by
  have hf : first w = b ∨ first w = c := by
    rcases hcover (first w) with h | h | h
    · exact False.elim (hw (Or.inl h))
    · exact Or.inl h
    · exact Or.inr h
  have hm : second w = b ∨ second w = c := by
    rcases hcover (second w) with h | h | h
    · exact False.elim (hw (Or.inr (Or.inl h)))
    · exact Or.inl h
    · exact Or.inr h
  have ht : third w = b ∨ third w = c := by
    rcases hcover (third w) with h | h | h
    · exact False.elim (hw (Or.inr (Or.inr h)))
    · exact Or.inl h
    · exact Or.inr h
  have h₁ := first_ne_second w
  have h₂ := second_ne_third w
  rcases hf with hf | hf <;> rcases hm with hm | hm <;> rcases ht with ht | ht
  all_goals try { exact False.elim (h₁ (hf.trans hm.symm)) }
  all_goals try { exact False.elim (h₂ (hm.trans ht.symm)) }
  all_goals first
    | exact Or.inl (count_vertex_ext hf hm ht)
    | exact Or.inr (count_vertex_ext hf hm ht)

theorem count_outside_card_two {α : Type u} [DecidableEq α]
    (S : Finset (Vertex α)) (a b c : α) (hbc : b ≠ c)
    (hcover : ∀ d : α, d = a ∨ d = b ∨ d = c) :
    (outsideLetter S a).card ≤ 2 := by
  let u := make b c b hbc (Ne.symm hbc)
  let v := make c b c (Ne.symm hbc) hbc
  have hsub : outsideLetter S a ⊆ {u,v} := by
    intro w hw
    have h := count_outside_two_words a b c hbc hcover w (Finset.mem_filter.mp hw).2
    simpa only [Finset.mem_insert, Finset.mem_singleton, u, v] using h
  have hc := Finset.card_le_card hsub
  rcases Finset.card_pair_eq_one_or_two (a := u) (b := v) with h | h <;> omega

theorem count_outside_card_one {α : Type u} [DecidableEq α]
    (S : Finset (Vertex α)) (a b c : α) (hbc : b ≠ c)
    (hcover : ∀ d : α, d = a ∨ d = b ∨ d = c)
    (hnot : ¬ (make b c b hbc (Ne.symm hbc) ∈ S ∧
      make c b c (Ne.symm hbc) hbc ∈ S)) :
    (outsideLetter S a).card ≤ 1 := by
  apply Finset.card_le_one.mpr
  intro x hx y hy
  obtain ⟨hxS,hxa⟩ := Finset.mem_filter.mp hx
  obtain ⟨hyS,hya⟩ := Finset.mem_filter.mp hy
  have hxc := count_outside_two_words a b c hbc hcover x hxa
  have hyc := count_outside_two_words a b c hbc hcover y hya
  rcases hxc with rfl | rfl <;> rcases hyc with rfl | rfl
  · rfl
  · exact False.elim (hnot ⟨hxS,hyS⟩)
  · exact False.elim (hnot ⟨hyS,hxS⟩)
  · rfl

theorem count_base_pal_extension {α : Type u} [Fintype α] [DecidableEq α]
    (hcard : Fintype.card α = 3) {S : Finset (Vertex α)} (hS : DistanceGP S)
    (a b c : α) (hab : a ≠ b) (hbc : b ≠ c) (hca : c ≠ a)
    (hu : make a b a hab (Ne.symm hab) ∈ S)
    (hv : make b a c (Ne.symm hab) (Ne.symm hca) ∈ S) : S.card ≤ 5 := by
  have hE : Edge (make a b a hab (Ne.symm hab))
      (make b a c (Ne.symm hab) (Ne.symm hca)) := ⟨rfl,rfl⟩
  have hi := selected_arc_caseI_card hS hu hv hE hca (Ne.symm hbc)
  have hnot : ¬ (make a b a hab (Ne.symm hab) ∈ S ∧
      make b a b (Ne.symm hab) hab ∈ S) := by
    rintro ⟨_,hw⟩
    apply count_forbidden_112 hS hw hu hv <;>
      simp [distance, Edge, count_vertex_eq_iff, hab, hbc, Ne.symm hab]
  have ho := count_outside_card_one S c a b hab
    (count_card_three_cover hcard c a b hca hab hbc) hnot
  have hs := letter_outside_card S c
  change (letterSet S c).card ≤ _ at hi
  simp only [hcard] at hi
  omega

theorem count_base_distinct_path {α : Type u} [Fintype α] [DecidableEq α]
    (hcard : Fintype.card α = 3) {S : Finset (Vertex α)} (hS : DistanceGP S)
    (a b c : α) (hab : a ≠ b) (hbc : b ≠ c) (hca : c ≠ a)
    (hu : make a b c hab hbc ∈ S)
    (hv : make b c b hbc (Ne.symm hbc) ∈ S) : S.card ≤ 5 := by
  have hE : Edge (make a b c hab hbc) (make b c b hbc (Ne.symm hbc)) := ⟨rfl,rfl⟩
  have hi := selected_arc_caseII_card hS hu hv hE rfl hca
  have hnot : ¬ (make b c b hbc (Ne.symm hbc) ∈ S ∧
      make c b c (Ne.symm hbc) hbc ∈ S) := by
    rintro ⟨hw,ht⟩
    apply count_forbidden_112 hS hu hw ht <;>
      simp [distance, Edge, count_vertex_eq_iff, hab, hbc, Ne.symm hbc, Ne.symm hca]
  have ho := count_outside_card_one S a b c hbc
    (count_card_three_cover hcard a b c hab hbc hca) hnot
  have hs := letter_outside_card S a
  change (letterSet S a).card ≤ _ at hi
  simp only [hcard] at hi
  omega

theorem count_base_cycle {α : Type u} [Fintype α] [DecidableEq α]
    (hcard : Fintype.card α = 3) {S : Finset (Vertex α)} (hS : DistanceGP S)
    (a b c : α) (hab : a ≠ b) (hbc : b ≠ c) (hca : c ≠ a)
    (hu : make a b c hab hbc ∈ S) (hv : make b c a hbc hca ∈ S) : S.card ≤ 5 := by
  have hi := selected_cycle_card hS a b c hab hbc hca hu hv
  have hnot : ¬ (make b c b hbc (Ne.symm hbc) ∈ S ∧
      make c b c (Ne.symm hbc) hbc ∈ S) := by
    rintro ⟨hw,ht⟩
    apply count_forbidden_112 hS hu hw ht <;>
      simp [distance, Edge, count_vertex_eq_iff, hab, hbc, Ne.symm hbc, Ne.symm hca]
  have ho := count_outside_card_one S a b c hbc
    (count_card_three_cover hcard a b c hab hbc hca) hnot
  have hs := letter_outside_card S a
  simp only [hcard] at hi
  omega

theorem count_base_digon {α : Type u} [Fintype α] [DecidableEq α]
    (hcard : Fintype.card α = 3) {S : Finset (Vertex α)} (hS : DistanceGP S)
    (a b : α) (hab : a ≠ b)
    (hu : make a b a hab (Ne.symm hab) ∈ S)
    (hv : make b a b (Ne.symm hab) hab ∈ S) : S.card ≤ 5 := by
  classical
  have hb : b ∈ (Finset.univ : Finset α).erase a := by simp [Ne.symm hab]
  have hnon : 0 < (((Finset.univ : Finset α).erase a).erase b).card := by
    simp only [Finset.card_erase_of_mem hb,
      Finset.card_erase_of_mem (Finset.mem_univ a), Finset.card_univ, hcard]
    omega
  obtain ⟨c,hc⟩ := Finset.card_pos.mp hnon
  have hcb : c ≠ b := (Finset.mem_erase.mp hc).1
  have hca : c ≠ a := (Finset.mem_erase.mp (Finset.mem_erase.mp hc).2).1
  have hi := selected_digon_incidence hS a b hab hu hv
  have ho := count_outside_card_two S a b c (Ne.symm hcb)
    (count_card_three_cover hcard a b c hab (Ne.symm hcb) hca)
  have hs := letter_outside_card S a
  simp only [hcard] at hi
  omega

theorem count_not_independent {α : Type u} {S : Finset (Vertex α)}
    (h : ¬ CountIndependent S) : ∃ x ∈ S, ∃ y ∈ S, Edge x y := by
  classical
  by_contra hn
  apply h
  intro x y hx hy he
  exact hn ⟨x, hx, y, hy, he⟩

/- The three-letter base is a symbolic selected-arc classification.  The
   digon branch uses the stronger incidence bound, not induction at size two. -/
theorem count_three_letter_bound {α : Type u} [Fintype α] [DecidableEq α]
    (hcard : Fintype.card α = 3) {S : Finset (Vertex α)}
    (hS : DistanceGP S) : S.card ≤ 5 := by
  classical
  by_cases hind : CountIndependent S
  · have h := independent_card hind
    rw [hcard] at h
    norm_num [squareSum] at h
    exact h
  obtain ⟨x,hx,y,hy,hE⟩ := count_not_independent hind
  rcases x with ⟨⟨a,b,c⟩,hab,hbc⟩
  rcases y with ⟨⟨b',c',d⟩,hb'c',hc'd⟩
  change b' = b ∧ c' = c at hE
  rcases hE with ⟨hb, hc⟩
  subst b'
  subst c'
  change make a b c hab hbc ∈ S at hx
  change make b c d hbc hc'd ∈ S at hy
  by_cases hdb : d = b
  · subst d
    by_cases hca : c = a
    · subst c
      exact count_base_digon hcard hS a b hab hx hy
    · exact count_base_distinct_path hcard hS a b c hab hbc hca hx hy
  · by_cases hda : d = a
    · subst d
      exact count_base_cycle hcard hS a b c hab hbc hc'd hx hy
    · have hcover := count_card_three_cover hcard a b d hab (Ne.symm hdb) hda
      have hca : c = a := by
        rcases hcover c with h | h | h
        · exact h
        · exact False.elim (hbc h.symm)
        · exact False.elim (hc'd h)
      subst c
      exact count_base_pal_extension hcard hS a b d hab (Ne.symm hdb) hda hx hy

theorem selected_arc_low_incidence {α : Type u} [Fintype α] [DecidableEq α]
    {S : Finset (Vertex α)} (hS : DistanceGP S) (hm : 3 ≤ Fintype.card α)
    {x y : Vertex α} (hx : x ∈ S) (hy : y ∈ S) (hE : Edge x y) :
    ∃ a : α, (letterSet S a).card ≤
      (Fintype.card α - 1) * (Fintype.card α - 1) := by
  classical
  rcases x with ⟨⟨a,b,c⟩,hab,hbc⟩
  rcases y with ⟨⟨b',c',d⟩,hb'c',hc'd⟩
  change b' = b ∧ c' = c at hE
  rcases hE with ⟨hb, hc⟩
  subst b'
  subst c'
  change make a b c hab hbc ∈ S at hx
  change make b c d hbc hc'd ∈ S at hy
  have he : Edge (make a b c hab hbc) (make b c d hbc hc'd) := ⟨rfl,rfl⟩
  by_cases hdb : d = b
  · subst d
    by_cases hca : c = a
    · subst c
      exact ⟨a, selected_digon_card hS hm a b hab hx hy⟩
    · exact ⟨a, selected_arc_caseII_card hS hx hy he rfl hca⟩
  · by_cases hda : d = a
    · subst d
      exact ⟨a, selected_cycle_card hS a b c hab hbc hc'd hx hy⟩
    · exact ⟨d, selected_arc_caseI_card hS hx hy he hda hdb⟩

/- Delete an actual letter.  These are finite sets of legal words over the
   subtype alphabet; no numerical recurrence is used as a definition. -/
def deleteLetterEmbedding {α : Type u} (a : α) : {x : α // x ≠ a} ↪ α :=
  ⟨Subtype.val, Subtype.val_injective⟩

def deleteLetterSet {α : Type u} [Fintype α] [DecidableEq α]
    (S : Finset (Vertex α)) (a : α) : Finset (Vertex {x : α // x ≠ a}) :=
  Finset.univ.filter fun x => countRelabel (deleteLetterEmbedding a) x ∈ S

theorem count_deleted_alphabet_card {α : Type u} [Fintype α] [DecidableEq α]
    (a : α) : Fintype.card {x : α // x ≠ a} = Fintype.card α - 1 := by
  simpa only [Fintype.card_subtype_eq] using
    Fintype.card_subtype_compl (fun x : α => x = a)

theorem deleteLetterSet_gp {α : Type u} [Fintype α] [DecidableEq α]
    {S : Finset (Vertex α)} (hS : DistanceGP S) (a : α) :
    DistanceGP (deleteLetterSet S a) := by
  intro x y z hx hy hz hxy hzx hzy
  have hxS := (Finset.mem_filter.mp hx).2
  have hyS := (Finset.mem_filter.mp hy).2
  have hzS := (Finset.mem_filter.mp hz).2
  have h := hS hxS hyS hzS
    (fun he => hxy (count_relabel_injective (deleteLetterEmbedding a) he))
    (fun he => hzx (count_relabel_injective (deleteLetterEmbedding a) he))
    (fun he => hzy (count_relabel_injective (deleteLetterEmbedding a) he))
  simpa only [count_relabel_distance] using h

def lowerDeletedVertex {α : Type u} (a : α) (w : Vertex α)
    (hw : ¬ containsLetter a w) : Vertex {x : α // x ≠ a} :=
  make
    ⟨first w, fun h => hw (Or.inl h)⟩
    ⟨second w, fun h => hw (Or.inr (Or.inl h))⟩
    ⟨third w, fun h => hw (Or.inr (Or.inr h))⟩
    (fun h => first_ne_second w (congrArg Subtype.val h))
    (fun h => second_ne_third w (congrArg Subtype.val h))

@[simp] theorem count_relabel_lowerDeletedVertex {α : Type u}
    (a : α) (w : Vertex α) (hw : ¬ containsLetter a w) :
    countRelabel (deleteLetterEmbedding a) (lowerDeletedVertex a w hw) = w := by
  apply count_vertex_ext <;> rfl

theorem count_deleted_relabel_no_letter {α : Type u}
    (a : α) (x : Vertex {b : α // b ≠ a}) :
    ¬ containsLetter a (countRelabel (deleteLetterEmbedding a) x) := by
  intro h
  rcases h with h | h | h
  · exact (first x).property h
  · exact (second x).property h
  · exact (third x).property h

theorem deleteLetterSet_image {α : Type u} [Fintype α] [DecidableEq α]
    (S : Finset (Vertex α)) (a : α) :
    (deleteLetterSet S a).image (countRelabel (deleteLetterEmbedding a)) =
      outsideLetter S a := by
  ext w
  constructor
  · intro hw
    obtain ⟨x,hx,rfl⟩ := Finset.mem_image.mp hw
    exact Finset.mem_filter.mpr
      ⟨(Finset.mem_filter.mp hx).2, count_deleted_relabel_no_letter a x⟩
  · intro hw
    obtain ⟨hwS,hwa⟩ := Finset.mem_filter.mp hw
    refine Finset.mem_image.mpr ⟨lowerDeletedVertex a w hwa, ?_, ?_⟩
    · apply Finset.mem_filter.mpr
      exact ⟨Finset.mem_univ _, by simpa only [count_relabel_lowerDeletedVertex] using hwS⟩
    · exact count_relabel_lowerDeletedVertex a w hwa

theorem deleteLetterSet_card {α : Type u} [Fintype α] [DecidableEq α]
    (S : Finset (Vertex α)) (a : α) :
    (deleteLetterSet S a).card = (outsideLetter S a).card := by
  have h := congrArg Finset.card (deleteLetterSet_image S a)
  rw [Finset.card_image_of_injective _
    (count_relabel_injective (deleteLetterEmbedding a))] at h
  exact h

/- The induction is over actual alphabet cardinality.  Each inductive call
   is a GP set over the subtype alphabet with one particular letter removed. -/
theorem count_upper_induction (n : ℕ) :
    ∀ (α : Type u) [Fintype α] [DecidableEq α], Fintype.card α = n → 3 ≤ n →
      ∀ S : Finset (Vertex α), DistanceGP S → S.card ≤ squareSum n := by
  induction n using Nat.strong_induction_on with
  | h n ih =>
    intro α instFin instDec hcard hn S hS
    by_cases hbase : n = 3
    · have h := count_three_letter_bound (hcard.trans hbase) hS
      have hs : squareSum n = 5 := by rw [hbase]; decide
      rw [hs]
      exact h
    by_cases hind : CountIndependent S
    · simpa only [hcard] using independent_card hind
    obtain ⟨x,hx,y,hy,hE⟩ := count_not_independent hind
    obtain ⟨a,ha⟩ := selected_arc_low_incidence hS (by omega) hx hy hE
    let β : Type u := {x : α // x ≠ a}
    have hβ : Fintype.card β = n - 1 := by
      change Fintype.card {x : α // x ≠ a} = n - 1
      rw [count_deleted_alphabet_card, hcard]
    have hlt : Fintype.card β < n := by omega
    have hge : 3 ≤ Fintype.card β := by omega
    have hc := ih (Fintype.card β) hlt β rfl hge
      (deleteLetterSet S a) (deleteLetterSet_gp hS a)
    rw [deleteLetterSet_card, hβ] at hc
    have hsplit := letter_outside_card S a
    rw [hcard] at ha
    have hsucc : n - 1 + 1 = n := by omega
    have hsum := count_squareSum_succ (n - 1)
    rw [hsucc] at hsum
    omega

theorem upper_bound {α : Type u} [Fintype α] [DecidableEq α]
    (hm : 3 ≤ Fintype.card α) {S : Finset (Vertex α)} (hS : DistanceGP S) :
    S.card ≤ squareSum (Fintype.card α) :=
  count_upper_induction (Fintype.card α) α rfl hm S hS

theorem original_upper_bound {α : Type u} [Fintype α] [DecidableEq α]
    (hm : 3 ≤ Fintype.card α) {S : Finset (Vertex α)}
    (hS : OriginalGeneralPosition S) : S.card ≤ squareSum (Fintype.card α) :=
  upper_bound hm ((distanceGP_iff_original S).mpr hS)

theorem exact_cardinality {α : Type u} [Fintype α] [DecidableEq α]
    (hm : 3 ≤ Fintype.card α) :
    ∃ S : Finset (Vertex α), OriginalGeneralPosition S ∧
      S.card = Fintype.card α * (Fintype.card α - 1) * (2 * Fintype.card α - 1) / 6 ∧
      ∀ T : Finset (Vertex α), OriginalGeneralPosition T → T.card ≤ S.card := by
  obtain ⟨S,hS,hcard⟩ := exists_gp_squareSum (α := α)
  refine ⟨S, (distanceGP_iff_original S).mp hS, ?_, ?_⟩
  · exact hcard.trans (squareSum_closed_form (Fintype.card α))
  · intro T hT
    rw [hcard]
    exact original_upper_bound hm hT

end Kautz3

#print axioms Kautz3.middlePeak_independent
#print axioms Kautz3.middlePeak_gp
#print axioms Kautz3.middlePeak_card
#print axioms Kautz3.exists_gp_squareSum
#print axioms Kautz3.squareSum_closed_form
#print axioms Kautz3.independent_card
#print axioms Kautz3.missing_first_card
#print axioms Kautz3.selected_cycle_card
#print axioms Kautz3.selected_digon_incidence
#print axioms Kautz3.count_three_letter_bound
#print axioms Kautz3.selected_arc_low_incidence
#print axioms Kautz3.deleteLetterSet_gp
#print axioms Kautz3.deleteLetterSet_card
#print axioms Kautz3.upper_bound
#print axioms Kautz3.original_upper_bound
#print axioms Kautz3.exact_cardinality
