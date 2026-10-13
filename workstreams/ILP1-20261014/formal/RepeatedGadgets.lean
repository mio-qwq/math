import ROBOperational

/-!
# Separator-free repeated four-job gadgets in the actual ROB model

For each k < q, block k is (4k, 4k+1, 4k+2, 4k+3). Its hidden
bit chooses offset 1 or 2 as the sole parent of offset 3. Each of the
first three jobs in a noninitial block depends on offsets 2 and 3 of
the preceding block. The Boolean sequence outside [0,q) is irrelevant.

Theorems below concern arbitrary q and bit sequences, not finite testing.
They prove strict block separation, an explicit legal two-cycle-per-block
schedule, and exact offline optimum 2q in the existing eager ROB model.
No probability, observation-history, or online lower bound is claimed.
-/

namespace ILP1.RepeatedGadgets

def parentOffset (bit : Bool) : Nat := if bit then 1 else 2

theorem parentOffset_bounds (bit : Bool) :
    1 ≤ parentOffset bit ∧ parentOffset bit ≤ 2 := by
  cases bit <;> decide

def dep {q : Nat} (bits : Nat → Bool) : Dependency (4 * q) := fun i j =>
  (i.val / 4 = j.val / 4 ∧
    i.val % 4 = parentOffset (bits (j.val / 4)) ∧ j.val % 4 = 3) ∨
  (i.val / 4 + 1 = j.val / 4 ∧
    (i.val % 4 = 2 ∨ i.val % 4 = 3) ∧ j.val % 4 < 3)

theorem dep_forward {q : Nat} (bits : Nat → Bool) : Forward (@dep q bits) := by
  intro i j hij
  have hp := parentOffset_bounds (bits (j.val / 4))
  rcases hij with ⟨hb, hi, hj⟩ | ⟨hb, hi, hj⟩ <;> omega

/-- Three alleged incoming predecessors must include a duplicate. -/
theorem indegree_at_most_two {q : Nat} (bits : Nat → Bool)
    (i j k target : Fin (4 * q))
    (hi : dep bits i target) (hj : dep bits j target) (hk : dep bits k target) :
    i = j ∨ i = k ∨ j = k := by
  have hv : i.val = j.val ∨ i.val = k.val ∨ j.val = k.val := by
    rcases hi with ⟨hib, hir, htr⟩ | ⟨hib, hir, htr⟩ <;>
    rcases hj with ⟨hjb, hjr, htr'⟩ | ⟨hjb, hjr, htr'⟩ <;>
    rcases hk with ⟨hkb, hkr, htr''⟩ | ⟨hkb, hkr, htr''⟩ <;> omega
  rcases hv with hij | hik | hjk
  · exact Or.inl (Fin.ext hij)
  · exact Or.inr (Or.inl (Fin.ext hik))
  · exact Or.inr (Or.inr (Fin.ext hjk))

/-- Construct the job with block index k and within-block offset r. -/
def job {q : Nat} (k : Nat) (hk : k < q) (r : Nat) (hr : r < 4) : Fin (4 * q) :=
  ⟨4 * k + r, by omega⟩

theorem job_block {q k r : Nat} (hk : k < q) (hr : r < 4) :
    (job k hk r hr).val / 4 = k := by
  simp only [job]
  omega

theorem job_offset {q k r : Nat} (hk : k < q) (hr : r < 4) :
    (job k hk r hr).val % 4 = r := by
  simp only [job]
  omega

def parentJob {q : Nat} (bits : Nat → Bool) (k : Nat) (hk : k < q) : Fin (4 * q) :=
  job k hk (parentOffset (bits k)) (by have := parentOffset_bounds (bits k); omega)

def lastJob {q : Nat} (k : Nat) (hk : k < q) : Fin (4 * q) := job k hk 3 (by decide)

theorem parent_edge {q : Nat} (bits : Nat → Bool) (k : Nat) (hk : k < q) :
    dep bits (parentJob bits k hk) (lastJob k hk) := by
  apply Or.inl
  simp [parentJob, lastJob, job_block, job_offset]

/-- Every root of the next block waits for every job of the previous block.
The two missing short-distance edges are supplied by the true dependencies. -/
theorem adjacent_root_separation {q w : Nat} {bits : Nat → Bool}
    {t : TimeAssignment (4 * q)} (h : Legal (dep bits) 3 w t)
    (i j : Fin (4 * q)) (hblocks : i.val / 4 + 1 = j.val / 4)
    (hroot : j.val % 4 < 3) : t i < t j := by
  by_cases hwindow : i.val + 3 ≤ j.val
  · exact ((windowEdges_iff_canonicalROB t 3).2 h.2.1) i j hwindow
  · apply h.1 i j
    exact Or.inr ⟨hblocks, by omega, hroot⟩

/-- Strict separation includes the hidden fourth job, via its parent. -/
theorem adjacent_block_separation {q w : Nat} {bits : Nat → Bool}
    {t : TimeAssignment (4 * q)} (h : Legal (dep bits) 3 w t)
    (i j : Fin (4 * q)) (hblocks : i.val / 4 + 1 = j.val / 4) : t i < t j := by
  by_cases hroot : j.val % 4 < 3
  · exact adjacent_root_separation h i j hblocks hroot
  · have hj3 : j.val % 4 = 3 := by omega
    have hjq : j.val / 4 < q := by have := j.isLt; omega
    let p := parentJob bits (j.val / 4) hjq
    have hpblock : p.val / 4 = j.val / 4 := by
      exact job_block hjq _
    have hpoffset : p.val % 4 = parentOffset (bits (j.val / 4)) := by
      exact job_offset hjq _
    have hproot : p.val % 4 < 3 := by
      have := parentOffset_bounds (bits (j.val / 4))
      omega
    have hip := adjacent_root_separation h i p (by omega) hproot
    have hpj : t p < t j := h.1 p j (Or.inl ⟨hpblock, hpoffset, hj3⟩)
    omega

/-- Arbitrarily far blocks also strictly separate; no idling assumption. -/
theorem block_separation {q w : Nat} {bits : Nat → Bool}
    {t : TimeAssignment (4 * q)} (h : Legal (dep bits) 3 w t)
    (i j : Fin (4 * q)) (hblocks : i.val / 4 < j.val / 4) : t i < t j := by
  by_cases hadj : i.val / 4 + 1 = j.val / 4
  · exact adjacent_block_separation h i j hadj
  · exact ((windowEdges_iff_canonicalROB t 3).2 h.2.1) i j (by omega)

theorem trace_block_separation {q w : Nat} {bits : Nat → Bool}
    {t : TimeAssignment (4 * q)} (tr : ROBTrace (dep bits) 3 w t)
    (i j : Fin (4 * q)) (hblocks : i.val / 4 < j.val / 4) :
    (tr.state (t j)).completed i := by
  exact (trace_completed_iff tr (t j) i).2 (block_separation (trace_legal tr) i j hblocks)

/-- While the oldest job of block k is incomplete, its hidden fourth job
has not entered the actual ROB. This is a state-level fact, not yet a
probabilistic or observation-history indistinguishability theorem. -/
theorem hidden_not_admitted {q w : Nat} {bits : Nat → Bool}
    {t : TimeAssignment (4 * q)} (tr : ROBTrace (dep bits) 3 w t)
    (k : Nat) (hk : k < q) (c : Nat)
    (ha : c ≤ t (job k hk 0 (by decide))) :
    (tr.state c).admitted ≤ (lastJob k hk).val := by
  have hp := trace_retirementPrefix tr c
  have hr : (tr.state c).retired ≤ 4 * k := by
    apply Classical.byContradiction
    intro hnot
    have hdone := hp.2.1 (job k hk 0 (by decide)) (by simp only [job]; omega)
    omega
  rw [trace_admitted tr c]
  have hm := Nat.min_le_right (4 * q) ((tr.state c).retired + 3)
  simp only [lastJob, job]
  omega

/-- Completing a block in two consecutive cycles forces its oldest job
and hidden parent to issue in the first of those cycles. -/
theorem two_cycle_block_forced {q w : Nat} {bits : Nat → Bool}
    {t : TimeAssignment (4 * q)} (h : Legal (dep bits) 3 w t)
    (k : Nat) (hk : k < q) (start : Nat)
    (hlower : ∀ r (hr : r < 4), start ≤ t (job k hk r hr))
    (hupper : ∀ r (hr : r < 4), t (job k hk r hr) < start + 2) :
    t (job k hk 0 (by decide)) = start ∧
    t (parentJob bits k hk) = start ∧ t (lastJob k hk) = start + 1 := by
  have ha := hlower 0 (by decide)
  have hp : start ≤ t (parentJob bits k hk) := hlower _ _
  have hd : t (lastJob k hk) < start + 2 := hupper 3 (by decide)
  have had := ((windowEdges_iff_canonicalROB t 3).2 h.2.1)
    (job k hk 0 (by decide)) (lastJob k hk) (by simp only [lastJob, job]; omega)
  have hpd := h.1 _ _ (parent_edge bits k hk)
  omega

def phase (bit : Bool) (r : Nat) : Nat :=
  if r = 0 ∨ r = parentOffset bit then 0 else 1

def lane (r : Nat) : Nat := if r = 0 ∨ r = 3 then 0 else 1

theorem phase_lt_two (bit : Bool) (r : Nat) : phase bit r < 2 := by
  unfold phase
  split <;> omega

theorem phase_zero (bit : Bool) : phase bit 0 = 0 := by simp [phase]

theorem phase_parent (bit : Bool) : phase bit (parentOffset bit) = 0 := by simp [phase]

theorem phase_three (bit : Bool) : phase bit 3 = 1 := by
  cases bit <;> decide

theorem lane_lt_two (r : Nat) : lane r < 2 := by
  unfold lane
  split <;> omega

/-- The finite four-job local table: each (phase,lane) pair is used once. -/
theorem phase_lane_injective (bit : Bool) :
    ∀ r s : Fin 4, phase bit r.val = phase bit s.val → lane r.val = lane s.val → r = s := by
  cases bit <;> decide

def schedule {q : Nat} (bits : Nat → Bool) : TimeAssignment (4 * q) := fun i =>
  2 * (i.val / 4) + phase (bits (i.val / 4)) (i.val % 4)

theorem schedule_blocks {q : Nat} (bits : Nat → Bool) (i j : Fin (4 * q))
    (hblocks : i.val / 4 < j.val / 4) : schedule bits i < schedule bits j := by
  have hi := phase_lt_two (bits (i.val / 4)) (i.val % 4)
  have hj := phase_lt_two (bits (j.val / 4)) (j.val % 4)
  simp only [schedule]
  omega

theorem schedule_respects {q : Nat} (bits : Nat → Bool) :
    Respects (@dep q bits) (schedule bits) := by
  intro i j hij
  rcases hij with ⟨hb, hi, hj⟩ | ⟨hb, _, _⟩
  · simp only [schedule, hb, hi, hj, phase_parent, phase_three]
    omega
  · exact schedule_blocks bits i j (by omega)

theorem schedule_window {q : Nat} (bits : Nat → Bool) : CanonicalROB (@schedule q bits) 3 := by
  apply (windowEdges_iff_canonicalROB (schedule bits) 3).1
  intro i j hdist
  by_cases hb : i.val / 4 = j.val / 4
  · have hi : i.val % 4 = 0 := by omega
    have hj : j.val % 4 = 3 := by omega
    simp only [schedule, hb, hi, hj, phase_zero, phase_three]
    omega
  · exact schedule_blocks bits i j (by omega)

theorem schedule_width {q : Nat} (bits : Nat → Bool) : WidthBound (@schedule q bits) 2 := by
  refine ⟨fun i => lane (i.val % 4), fun i => lane_lt_two (i.val % 4), ?_⟩
  intro i j ht hl
  have hi := phase_lt_two (bits (i.val / 4)) (i.val % 4)
  have hj := phase_lt_two (bits (j.val / 4)) (j.val % 4)
  have hb : i.val / 4 = j.val / 4 := by simp only [schedule] at ht; omega
  have hp : phase (bits (j.val / 4)) (i.val % 4) = phase (bits (j.val / 4)) (j.val % 4) := by
    simp only [schedule, hb] at ht
    omega
  have hlocal := phase_lane_injective (bits (j.val / 4))
    ⟨i.val % 4, by omega⟩ ⟨j.val % 4, by omega⟩ hp hl
  have hr : i.val % 4 = j.val % 4 := congrArg Fin.val hlocal
  apply Fin.ext
  omega

theorem schedule_legal {q : Nat} (bits : Nat → Bool) : Legal (@dep q bits) 3 2 (schedule bits) :=
  ⟨schedule_respects bits, schedule_window bits, schedule_width bits⟩

theorem schedule_horizon {q : Nat} (bits : Nat → Bool) (i : Fin (4 * q)) :
    schedule bits i < 2 * q := by
  have hi := i.isLt
  have hp := phase_lt_two (bits (i.val / 4)) (i.val % 4)
  simp only [schedule]
  omega

theorem feasible_two_per_block (q : Nat) (bits : Nat → Bool) :
    Feasible (@dep q bits) 3 2 (2 * q) :=
  ⟨schedule bits, schedule_legal bits, schedule_horizon bits⟩

/-- The true hidden edge in each block and the proved inter-block barrier
form a critical chain with two jobs per block, for every issue width. -/
theorem lastJob_lower_bound {q w : Nat} {bits : Nat → Bool}
    {t : TimeAssignment (4 * q)} (h : Legal (dep bits) 3 w t) :
    ∀ k, (hk : k < q) → 2 * k + 1 ≤ t (lastJob k hk) := by
  intro k
  induction k with
  | zero =>
    intro hk
    have hedge := h.1 _ _ (parent_edge bits 0 hk)
    omega
  | succ k ih =>
    intro hk
    have hprev : k < q := by omega
    have hlast := ih hprev
    have hbetween := block_separation h (lastJob k hprev) (parentJob bits (k + 1) hk)
      (by simp only [lastJob, parentJob, job_block]; omega)
    have hedge := h.1 _ _ (parent_edge bits (k + 1) hk)
    omega

theorem feasible_lower_bound {q w horizon : Nat} {bits : Nat → Bool}
    (h : Feasible (@dep q bits) 3 w horizon) : 2 * q ≤ horizon := by
  obtain ⟨t, hlegal, hfinish⟩ := h
  by_cases hq : q = 0
  · omega
  · have hlast : q - 1 < q := by omega
    have hlower := lastJob_lower_bound hlegal (q - 1) hlast
    have hupper := hfinish (lastJob (q - 1) hlast)
    omega

/-- A closed theorem about the actual finite DAG and the actual ROB model. -/
theorem optimal_two_per_block (q : Nat) (bits : Nat → Bool) :
    Optimal (@dep q bits) 3 2 (2 * q) :=
  ⟨feasible_two_per_block q bits, fun _ h => feasible_lower_bound h⟩

theorem operational_two_per_block (q : Nat) (bits : Nat → Bool) :
    ∃ tr : ROBTrace (@dep q bits) 3 2 (schedule bits),
      (tr.state (2 * q)).retired = 4 * q := by
  let tr := legalTrace (schedule_legal (q := q) bits)
  exact ⟨tr, (trace_finished_iff tr (2 * q)).2 (schedule_horizon bits)⟩

theorem trace_finished_lower_bound {q w horizon : Nat} {bits : Nat → Bool}
    {t : TimeAssignment (4 * q)} (tr : ROBTrace (dep bits) 3 w t)
    (hfinish : (tr.state horizon).retired = 4 * q) : 2 * q ≤ horizon := by
  exact feasible_lower_bound ⟨t, trace_legal tr, (trace_finished_iff tr horizon).1 hfinish⟩

#print axioms dep_forward
#print axioms indegree_at_most_two
#print axioms parent_edge
#print axioms adjacent_root_separation
#print axioms adjacent_block_separation
#print axioms block_separation
#print axioms trace_block_separation
#print axioms hidden_not_admitted
#print axioms two_cycle_block_forced
#print axioms schedule_respects
#print axioms schedule_window
#print axioms schedule_width
#print axioms schedule_legal
#print axioms schedule_horizon
#print axioms feasible_two_per_block
#print axioms lastJob_lower_bound
#print axioms feasible_lower_bound
#print axioms optimal_two_per_block
#print axioms operational_two_per_block
#print axioms trace_finished_lower_bound

end ILP1.RepeatedGadgets
