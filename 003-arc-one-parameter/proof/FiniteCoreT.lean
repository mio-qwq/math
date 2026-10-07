import FiniteCore

/-!
Twenty-letter trivial-extension table certificate.
Scope: exact packed bit-polynomial identities on every explicit basis
triple, not an abstract arbitrary-field algebra or complete ARC theorem.
Tables are OpenAI family 199, pinned and attributed in ../ATTRIBUTION.md.
-/
namespace ARCFiniteCore
set_option maxRecDepth 20000
set_option maxHeartbeats 0

def coefficient (terms : Terms) (index : Nat) : Nat :=
  terms.foldl (fun acc term =>
    if term.1 = index then Nat.xor acc term.2 else acc) 0

/-- Formal transpose recurrence defining the dual-ideal products. -/
def tByDualRecurrence (a b : Nat) : Terms :=
  if a < 10 then
    if b < 10 then cTerms a b else
      (List.range 10).filterMap (fun c =>
        let p := coefficient (cTerms c a) (b - 10)
        if p = 0 then none else some (c + 10, p))
  else if b < 10 then
    (List.range 10).filterMap (fun c =>
      let p := coefficient (cTerms b c) (a - 10)
      if p = 0 then none else some (c + 10, p))
  else []

/-- Complete sparse table; uppercase letters are indexed ten places higher. -/
def tTerms : Nat → Nat → Terms
  | 0, 0 => [(0, 1)] -- ee
  | 0, 1 => [(1, 1)] -- ex
  | 0, 2 => [(2, 1)] -- ey
  | 0, 3 => [(3, 1)] -- ez
  | 0, 4 => [(4, 1)] -- eu
  | 0, 5 => [(5, 1)] -- ev
  | 0, 10 => [(10, 1)] -- eE
  | 0, 11 => [(11, 1)] -- eX
  | 0, 12 => [(12, 1)] -- eY
  | 0, 13 => [(13, 1)] -- eZ
  | 0, 16 => [(16, 1)] -- eT
  | 0, 17 => [(17, 1)] -- eJ
  | 1, 0 => [(1, 1)] -- xe
  | 1, 2 => [(3, 2)] -- xy
  | 1, 4 => [(5, 1)] -- xu
  | 1, 11 => [(10, 1)] -- xX
  | 1, 13 => [(12, 1)] -- xZ
  | 1, 17 => [(16, 1)] -- xJ
  | 2, 0 => [(2, 1)] -- ye
  | 2, 1 => [(3, 1)] -- yx
  | 2, 4 => [(5, 1)] -- yu
  | 2, 12 => [(10, 1)] -- yY
  | 2, 13 => [(11, 2)] -- yZ
  | 2, 17 => [(16, 4)] -- yJ
  | 3, 0 => [(3, 1)] -- ze
  | 3, 13 => [(10, 1)] -- zZ
  | 4, 6 => [(2, 1), (1, 2)] -- ut
  | 4, 7 => [(3, 1)] -- uj
  | 4, 8 => [(4, 1)] -- uf
  | 4, 9 => [(5, 1)] -- un
  | 4, 14 => [(10, 1)] -- uU
  | 4, 15 => [(11, 1), (12, 1)] -- uV
  | 4, 19 => [(16, 3)] -- uN
  | 5, 6 => [(3, 2)] -- vt
  | 5, 8 => [(5, 1)] -- vf
  | 5, 15 => [(10, 1)] -- vV
  | 6, 0 => [(6, 1)] -- te
  | 6, 1 => [(7, 1)] -- tx
  | 6, 2 => [(7, 4)] -- ty
  | 6, 4 => [(9, 3)] -- tu
  | 6, 11 => [(14, 2)] -- tX
  | 6, 12 => [(14, 1)] -- tY
  | 6, 13 => [(15, 2)] -- tZ
  | 6, 16 => [(18, 1)] -- tT
  | 6, 17 => [(19, 2)] -- tJ
  | 7, 0 => [(7, 1)] -- je
  | 7, 13 => [(14, 1)] -- jZ
  | 7, 17 => [(18, 1)] -- jJ
  | 8, 6 => [(6, 1)] -- ft
  | 8, 7 => [(7, 1)] -- fj
  | 8, 8 => [(8, 1)] -- ff
  | 8, 9 => [(9, 1)] -- fn
  | 8, 14 => [(14, 1)] -- fU
  | 8, 15 => [(15, 1)] -- fV
  | 8, 18 => [(18, 1)] -- fF
  | 8, 19 => [(19, 1)] -- fN
  | 9, 6 => [(7, 2)] -- nt
  | 9, 8 => [(9, 1)] -- nf
  | 9, 15 => [(14, 1)] -- nV
  | 9, 19 => [(18, 1)] -- nN
  | 10, 0 => [(10, 1)] -- Ee
  | 11, 0 => [(11, 1)] -- Xe
  | 11, 1 => [(10, 1)] -- Xx
  | 11, 4 => [(16, 2)] -- Xu
  | 12, 0 => [(12, 1)] -- Ye
  | 12, 2 => [(10, 1)] -- Yy
  | 12, 4 => [(16, 1)] -- Yu
  | 13, 0 => [(13, 1)] -- Ze
  | 13, 1 => [(12, 2)] -- Zx
  | 13, 2 => [(11, 1)] -- Zy
  | 13, 3 => [(10, 1)] -- Zz
  | 13, 4 => [(17, 1)] -- Zu
  | 13, 5 => [(16, 2)] -- Zv
  | 14, 0 => [(14, 1)] -- Ue
  | 14, 4 => [(18, 1)] -- Uu
  | 15, 0 => [(15, 1)] -- Ve
  | 15, 1 => [(14, 1)] -- Vx
  | 15, 2 => [(14, 1)] -- Vy
  | 15, 4 => [(19, 1)] -- Vu
  | 15, 5 => [(18, 1)] -- Vv
  | 16, 6 => [(10, 1)] -- Tt
  | 16, 8 => [(16, 1)] -- Tf
  | 17, 6 => [(11, 1), (12, 4)] -- Jt
  | 17, 7 => [(10, 1)] -- Jj
  | 17, 8 => [(17, 1)] -- Jf
  | 17, 9 => [(16, 2)] -- Jn
  | 18, 8 => [(18, 1)] -- Ff
  | 19, 6 => [(14, 3)] -- Nt
  | 19, 8 => [(19, 1)] -- Nf
  | 19, 9 => [(18, 1)] -- Nn
  | _, _ => []

/-- The explicit fast table equals the specified dual recurrence everywhere. -/
theorem t_table_matches_dual_recurrence :
    ∀ a b : Fin 20,
      tTerms a.val b.val = tByDualRecurrence a.val b.val := by decide

/-- The missing right-path bound for the ten-letter certificate. -/
theorem c_right_composed_coefficient_bound :
    ∀ a b c : Fin 10,
      (cTerms b.val c.val).all (fun x =>
        (cTerms a.val x.1).all (fun y => pMul x.2 y.2 < 256)) = true := by decide

/-- All 8000 basis triples for the twenty-dimensional table. -/
theorem t_basis_associativity :
    ∀ a b c : Fin 20,
      leftProduct tTerms a.val b.val c.val =
      rightProduct tTerms a.val b.val c.val := by decide

/-- Left-path composed coefficients fit into their eight-bit blocks. -/
theorem t_left_composed_coefficient_bound :
    ∀ a b c : Fin 20,
      (tTerms a.val b.val).all (fun x =>
        (tTerms x.1 c.val).all (fun y => pMul x.2 y.2 < 256)) = true := by decide

/-- Right-path composed coefficients also fit into their eight-bit blocks. -/
theorem t_right_composed_coefficient_bound :
    ∀ a b c : Fin 20,
      (tTerms b.val c.val).all (fun x =>
        (tTerms a.val x.1).all (fun y => pMul x.2 y.2 < 256)) = true := by decide

theorem t_output_basis_bound :
    ∀ a b : Fin 20, (tTerms a.val b.val).all (fun x => x.1 < 20) = true := by decide

def tracePair (a b : Nat) : Nat :=
  Nat.xor (coefficient (tTerms a b) 10) (coefficient (tTerms a b) 18)

def dualIndex (a : Nat) : Nat := if a < 10 then a + 10 else a - 10

/-- The trace pairing is exactly the identity under the star identification. -/
theorem t_trace_pairing :
    ∀ a b : Fin 20,
      tracePair a.val b.val = if b.val = dualIndex a.val then 1 else 0 := by decide

/-- Both actions of e+f are identities on each fixed basis vector. -/
theorem t_unit_actions :
    ∀ a : Fin 20,
      Nat.xor (encode (tTerms 0 a.val)) (encode (tTerms 8 a.val)) = pack a.val 1 ∧
      Nat.xor (encode (tTerms a.val 0)) (encode (tTerms a.val 8)) = pack a.val 1 := by
  decide

#print axioms t_table_matches_dual_recurrence
#print axioms c_right_composed_coefficient_bound
#print axioms t_basis_associativity
#print axioms t_left_composed_coefficient_bound
#print axioms t_right_composed_coefficient_bound
#print axioms t_output_basis_bound
#print axioms t_trace_pairing
#print axioms t_unit_actions
end ARCFiniteCore
