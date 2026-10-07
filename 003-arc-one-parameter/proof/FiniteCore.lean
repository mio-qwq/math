import Std

/-!
# Exact finite polynomial certificate for OpenAI family 199

The coefficient `n : Nat` denotes the F_2[q] polynomial with bit i the
coefficient of q^i. These theorems certify the explicitly defined finite
polynomial table. They do NOT formalize the complete ARC construction,
field interpretation, stable categories, or homological realization.
No `sorry`, extra axiom, `native_decide`, or trusted compiler evaluation.
Source tables: OpenAI commit adc7f1241b42e322a6451854ab7e4b4c146bf78a,
family 199, 03-algebra.tex and 09-cochain.tex. Data transcription is
attributed in ../ATTRIBUTION.md.
-/

namespace ARCFiniteCore

set_option maxRecDepth 20000
set_option maxHeartbeats 0

/-- Exact carryless polynomial convolution, with explicitly adequate fuel. -/
def pMulAux : Nat → Nat → Nat → Nat
  | 0, _, _ => 0
  | fuel + 1, a, b =>
      if b = 0 then 0 else
        Nat.xor (if b % 2 = 1 then a else 0)
          (pMulAux fuel (2 * a) (b / 2))

/-- For b > 0, log2(b)+1 is precisely its number of binary digits. -/
def pMul (a b : Nat) : Nat := pMulAux (Nat.log2 b + 1) a b

abbrev Terms := List (Nat × Nat)

/-- Basis order e,x,y,z,u,v,t,j,f,n. -/
def cLeft : Nat → Nat
  | 0 => 0
  | 1 => 0
  | 2 => 0
  | 3 => 0
  | 4 => 0
  | 5 => 0
  | 6 => 8
  | 7 => 8
  | 8 => 8
  | 9 => 8
  | _ => 0

def cRight : Nat → Nat
  | 0 => 0
  | 1 => 0
  | 2 => 0
  | 3 => 0
  | 4 => 8
  | 5 => 8
  | 6 => 0
  | 7 => 0
  | 8 => 8
  | 9 => 8
  | _ => 0

/-- The complete lower-case multiplication table, as sparse polynomial vectors. -/
def cNonunit : Nat → Nat → Terms
  | 1, 2 => [(3, 2)] -- xy
  | 2, 1 => [(3, 1)] -- yx
  | 1, 4 => [(5, 1)] -- xu
  | 2, 4 => [(5, 1)] -- yu
  | 6, 1 => [(7, 1)] -- tx
  | 6, 2 => [(7, 4)] -- ty
  | 4, 6 => [(2, 1), (1, 2)] -- ut
  | 5, 6 => [(3, 2)] -- vt
  | 4, 7 => [(3, 1)] -- uj
  | 6, 4 => [(9, 3)] -- tu
  | 9, 6 => [(7, 2)] -- nt
  | 4, 9 => [(5, 1)] -- un
  | _, _ => []

def cTerms (a b : Nat) : Terms :=
  if (a = 0 ∨ a = 8) ∧ cLeft b = a then [(b, 1)]
  else if (b = 0 ∨ b = 8) ∧ cRight a = b then [(a, 1)]
  else cNonunit a b

/-- Eight bits per output basis coordinate; all certified coefficients fit. -/
def pack (basisIndex coefficient : Nat) : Nat :=
  coefficient * 2 ^ (8 * basisIndex)

def encode (terms : Terms) : Nat :=
  terms.foldl (fun acc term => Nat.xor acc (pack term.1 term.2)) 0

def scaleEncode (scalar : Nat) (terms : Terms) : Nat :=
  terms.foldl (fun acc term => Nat.xor acc (pack term.1 (pMul scalar term.2))) 0

def leftProduct (table : Nat → Nat → Terms) (a b c : Nat) : Nat :=
  (table a b).foldl (fun acc term =>
    Nat.xor acc (scaleEncode term.2 (table term.1 c))) 0

def rightProduct (table : Nat → Nat → Terms) (a b c : Nat) : Nat :=
  (table b c).foldl (fun acc term =>
    Nat.xor acc (scaleEncode term.2 (table a term.1))) 0

/-- All 1000 triples, including units and every zero product. -/
theorem c_basis_associativity :
    ∀ a b c : Fin 10,
      leftProduct cTerms a.val b.val c.val =
      rightProduct cTerms a.val b.val c.val := by
  decide

/-- No coefficient carries into another packed basis coordinate. -/
theorem c_composed_coefficient_bound :
    ∀ a b c : Fin 10,
      (cTerms a.val b.val).all (fun x =>
        (cTerms x.1 c.val).all (fun y => pMul x.2 y.2 < 256)) = true := by
  decide

/-- Every output label in the fixed C table is one of its ten basis labels. -/
theorem c_output_basis_bound :
    ∀ a b : Fin 10, (cTerms a.val b.val).all (fun x => x.1 < 10) = true := by
  decide

/-- The triple product u t u is exactly (1+q) v. -/
theorem c_u_t_u :
    leftProduct cTerms 4 6 4 = pack 5 3 := by decide

theorem c_u_t_u_t :
    (cTerms 4 6).foldl (fun acc x =>
      Nat.xor acc ((cTerms 4 6).foldl (fun inner y =>
        Nat.xor inner (scaleEncode (pMul x.2 y.2) (cTerms x.1 y.1))) 0)) 0
      = pack 3 6 := by decide

#print axioms c_basis_associativity
#print axioms c_composed_coefficient_bound
#print axioms c_output_basis_bound
#print axioms c_u_t_u
#print axioms c_u_t_u_t

end ARCFiniteCore
