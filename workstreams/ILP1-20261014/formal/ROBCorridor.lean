import ROBWorkBounds

/-!
# The horizon-dependent corridor for the actual eager ROB model

For window B=W+excess, horizon H and budget S=H*W-N, every actual
completing trace at layer c has completed all indices below c*W-excess-S
and none at or above c*W+excess. Natural subtraction truncates at zero.
The proof derives all counting bounds from actual lane injections.

This module does not verify the Python corridor solver or the binomial
candidate-state count / parameterized runtime theorem.
-/

namespace ILP1.ROBCorridor

open ROBWorkBounds

/-- The left cutoff is a genuine program-prefix length; no indices outside
Fin n are silently omitted by the finite-domain containment statements. -/
theorem lower_cut_within_program (n w excess horizon c : Nat) (hc : c ≤ horizon) :
    c * w - excess - (horizon * w - n) ≤ n := by
  have hm := Nat.mul_le_mul_right w hc
  omega

/-- A completed-set prefix enclosure gives a genuine cardinality bound. -/
theorem completed_count_of_index_bound {n : Nat} (t : TimeAssignment n) (c cap : Nat)
    (hcap : ∀ i, t i < c → i.val < cap) : completedCount t c ≤ cap := by
  have hb := list_injection_length_le (completedJobs t c) (List.range cap)
    Fin.val (completedJobs_nodup t c)
    (fun _ _ _ _ heq => Fin.ext heq)
    (fun i hi => List.mem_range.mpr (hcap i ((mem_completedJobs t c i).1 hi)))
  simpa only [completedCount, List.length_range] using hb

/-- Bound the completed prefix by index capacity, and the remaining jobs
by their actual remaining cycle/lane slots. -/
theorem horizon_split_capacity {n w horizon : Nat} {t : TimeAssignment n}
    (hw : WidthBound t w) (hfinish : ∀ i, t i < horizon) (c cap : Nat)
    (hcap : ∀ i, t i < c → i.val < cap) : n ≤ cap + (horizon - c) * w := by
  have hp := completed_pending_partition t c
  have hc := completed_count_of_index_bound t c cap hcap
  have hr := pending_count_le hw hfinish c
  omega

/-- At the next boundary, every completed job lies below the current
exclusive ROB frontier. This includes all jobs completed in earlier cycles. -/
theorem completed_next_index_bound {n b c r : Nat} {t : TimeAssignment n}
    (hrob : CanonicalROB t b) (hp : RetirementPrefix t c r)
    (j : Fin n) (hj : t j < c + 1) : j.val < r + b := by
  apply Classical.byContradiction
  intro hnot
  have hrn : r < n := by have := j.isLt; omega
  have hblock := ((windowEdges_iff_canonicalROB t b).2 hrob) ⟨r, hrn⟩ j
    (by change r + b ≤ j.val; omega)
  have hundone := hp.2.2 hrn
  omega

/-- Complete-horizon capacity forces the true retirement frontier close to
the nominal work cut. All hypotheses are the actual model's predicates. -/
theorem retirement_frontier_lower {n w excess horizon c r : Nat}
    {dep : Dependency n} {t : TimeAssignment n}
    (hlegal : Legal dep (w + excess) w t) (hfinish : ∀ i, t i < horizon)
    (hc : c ≤ horizon) (hp : RetirementPrefix t c r) :
    c * w ≤ r + excess + (horizon * w - n) := by
  have hwork := work_bound hlegal.2.2 hfinish
  by_cases hend : c = horizon
  · have hr : r = n := by
      apply Classical.byContradiction
      intro hrne
      have hrn : r < n := by have := hp.1; omega
      have hf := hfinish ⟨r, hrn⟩
      have hu := hp.2.2 hrn
      omega
    rw [hend, hr]
    omega
  · have hnext : c + 1 ≤ horizon := by omega
    have hcap := horizon_split_capacity hlegal.2.2 hfinish (c + 1) (r + (w + excess))
      (fun j hj => completed_next_index_bound hlegal.2.1 hp j hj)
    have hsplit := horizon_mul_split hnext w
    simp only [Nat.add_mul, Nat.one_mul] at hsplit
    omega

/-- The upper strip bound is independent of a chosen completion horizon. -/
theorem completed_index_upper {n w excess : Nat} {dep : Dependency n}
    {t : TimeAssignment n} (hlegal : Legal dep (w + excess) w t)
    (c : Nat) (j : Fin n) (hj : t j < c) : j.val < c * w + excess := by
  obtain ⟨r, hp⟩ := retirementPrefix_exists t (t j)
  have hr := retirement_work_bound hlegal.2.2 hp
  have hwin := (hlegal.2.1 j r hp).2
  have hmul := Nat.mul_le_mul_right w (show t j + 1 ≤ c by omega)
  simp only [Nat.add_mul, Nat.one_mul] at hmul
  omega

theorem completed_index_lower {n w excess horizon : Nat} {dep : Dependency n}
    {t : TimeAssignment n} (hlegal : Legal dep (w + excess) w t)
    (hfinish : ∀ i, t i < horizon) (c : Nat) (hc : c ≤ horizon)
    (j : Fin n) (hj : j.val < c * w - excess - (horizon * w - n)) : t j < c := by
  obtain ⟨r, hp⟩ := retirementPrefix_exists t c
  have hr := retirement_frontier_lower hlegal hfinish hc hp
  exact hp.2.1 j (by omega)

/-- The full strip enclosure plus completed-cardinality interval, for every
legal time assignment completing by H and every cut c between 0 and H. -/
theorem legal_corridor {n w excess horizon : Nat} {dep : Dependency n}
    {t : TimeAssignment n} (hlegal : Legal dep (w + excess) w t)
    (hfinish : ∀ i, t i < horizon) (c : Nat) (hc : c ≤ horizon) :
    (∀ j, j.val < c * w - excess - (horizon * w - n) → t j < c) ∧
    (∀ j, t j < c → j.val < min n (c * w + excess)) ∧
    (c * w - (horizon * w - n) ≤ completedCount t c ∧ completedCount t c ≤ c * w) := by
  refine ⟨fun j hj => completed_index_lower hlegal hfinish c hc j hj, ?_, ?_⟩
  · intro j hj
    exact Nat.lt_min.mpr ⟨j.isLt, completed_index_upper hlegal c j hj⟩
  · exact ⟨completed_slack_lower hlegal.2.2 hfinish c hc, completed_count_le hlegal.2.2 c⟩

/-- Actual state semantics, with no unproved transition/strip bridge.
`trace_completed_list` identifies the cardinality list with this completed
state predicate, so the last conjunct counts the actual completed jobs. -/
theorem trace_corridor {n w excess horizon : Nat} {dep : Dependency n}
    {t : TimeAssignment n} (tr : ROBTrace dep (w + excess) w t)
    (hfinish : (tr.state horizon).retired = n) (c : Nat) (hc : c ≤ horizon) :
    (∀ j, j.val < c * w - excess - (horizon * w - n) → (tr.state c).completed j) ∧
    (∀ j, (tr.state c).completed j → j.val < min n (c * w + excess)) ∧
    (c * w - (horizon * w - n) ≤ completedCount t c ∧ completedCount t c ≤ c * w) := by
  obtain ⟨hl, hu, hcount⟩ := legal_corridor (trace_legal tr)
    ((trace_finished_iff tr horizon).1 hfinish) c hc
  exact ⟨fun j hj => (trace_completed_iff tr c j).2 (hl j hj),
    fun j hj => hu j ((trace_completed_iff tr c j).1 hj), hcount⟩

#print axioms lower_cut_within_program
#print axioms completed_count_of_index_bound
#print axioms horizon_split_capacity
#print axioms completed_next_index_bound
#print axioms retirement_frontier_lower
#print axioms completed_index_upper
#print axioms completed_index_lower
#print axioms legal_corridor
#print axioms trace_corridor

end ILP1.ROBCorridor
