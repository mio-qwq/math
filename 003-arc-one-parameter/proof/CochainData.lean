import FiniteCoreT

/-! The full 179-entry polynomial cochain, with finite supporting checks.
Only concrete bit-polynomial certificate identities are formalized. -/
namespace ARCFiniteCore
set_option maxRecDepth 20000
set_option maxHeartbeats 0
set_option exponentiation.threshold 4096

/-- Zero on every unlisted triple; the complete attributed 179-entry table. -/
def pTerms : Nat → Nat → Nat → Terms
  | 10, 4, 19 => [(16, 4)] -- EuNT, q^2
  | 10, 2, 13 => [(11, 4)] -- EyZX, q^2
  | 18, 19, 6 => [(14, 4)] -- FNtU, q^2
  | 17, 6, 11 => [(13, 4)] -- JtXZ, q^2
  | 19, 6, 10 => [(14, 4)] -- NtEU, q^2
  | 19, 6, 11 => [(15, 4)] -- NtXV, q^2
  | 11, 3, 17 => [(16, 4)] -- XzJT, q^2
  | 13, 1, 10 => [(12, 4)] -- ZxEY, q^2
  | 6, 10, 4 => [(9, 4)] -- tEun, q^2
  | 6, 11, 4 => [(8, 4)] -- tXuf, q^2
  | 6, 11, 5 => [(9, 4)] -- tXvn, q^2
  | 6, 11, 3 => [(7, 4)] -- tXzj, q^2
  | 6, 4, 18 => [(9, 4)] -- tuFn, q^2
  | 6, 4, 19 => [(8, 4)] -- tuNf, q^2
  | 6, 5, 19 => [(9, 4)] -- tvNn, q^2
  | 4, 18, 19 => [(16, 4)] -- uFNT, q^2
  | 5, 19, 19 => [(16, 4)] -- vNNT, q^2
  | 5, 6, 17 => [(4, 4)] -- vtJu, q^2
  | 1, 10, 2 => [(3, 4)] -- xEyz, q^2
  | 3, 17, 6 => [(1, 4)] -- zJtx, q^2
  | 10, 4, 14 => [(10, 2)] -- EuUE, q^1
  | 10, 4, 15 => [(11, 2)] -- EuVX, q^1
  | 10, 5, 15 => [(10, 2)] -- EvVE, q^1
  | 10, 1, 11 => [(10, 2)] -- ExXE, q^1
  | 10, 2, 12 => [(10, 2)] -- EyYE, q^1
  | 10, 3, 13 => [(10, 2)] -- EzZE, q^1
  | 18, 19, 9 => [(18, 2)] -- FNnF, q^1
  | 18, 15, 5 => [(18, 2)] -- FVvF, q^1
  | 18, 15, 1 => [(14, 2)] -- FVxU, q^1
  | 18, 6, 16 => [(18, 2)] -- FtTF, q^1
  | 18, 6, 12 => [(14, 2)] -- FtYU, q^1
  | 18, 6, 4 => [(9, 2)] -- Ftun, q^1
  | 18, 6, 1 => [(7, 2)] -- Ftxj, q^1
  | 17, 18, 6 => [(11, 2)] -- JFtX, q^1
  | 17, 19, 6 => [(13, 2)] -- JNtZ, q^1
  | 17, 14, 2 => [(11, 2)] -- JUyX, q^1
  | 17, 15, 2 => [(13, 2)] -- JVyZ, q^1
  | 17, 7, 10 => [(10, 2)] -- JjEE, q^1
  | 17, 7, 16 => [(16, 2)] -- JjTT, q^1
  | 17, 7, 11 => [(11, 2)] -- JjXX, q^1
  | 19, 18, 6 => [(14, 2)] -- NFtU, q^1
  | 19, 19, 6 => [(15, 2)] -- NNtV, q^1
  | 19, 14, 2 => [(14, 2)] -- NUyU, q^1
  | 19, 15, 2 => [(15, 2)] -- NVyV, q^1
  | 19, 7, 17 => [(19, 2)] -- NjJN, q^1
  | 19, 7, 13 => [(15, 2)] -- NjZV, q^1
  | 19, 9, 19 => [(19, 2)] -- NnNN, q^1
  | 19, 9, 15 => [(15, 2)] -- NnVV, q^1
  | 19, 6, 4 => [(8, 2)] -- Ntuf, q^1
  | 19, 6, 5 => [(9, 2)] -- Ntvn, q^1
  | 19, 6, 3 => [(7, 2)] -- Ntzj, q^1
  | 16, 6, 10 => [(10, 2)] -- TtEE, q^1
  | 16, 6, 11 => [(11, 2)] -- TtXX, q^1
  | 14, 4, 18 => [(18, 2)] -- UuFF, q^1
  | 14, 4, 14 => [(14, 2)] -- UuUU, q^1
  | 14, 5, 19 => [(18, 2)] -- UvNF, q^1
  | 14, 5, 15 => [(14, 2)] -- UvVU, q^1
  | 14, 1, 11 => [(14, 2)] -- UxXU, q^1
  | 14, 2, 4 => [(9, 2)] -- Uyun, q^1
  | 14, 2, 1 => [(7, 2)] -- Uyxj, q^1
  | 14, 3, 13 => [(14, 2)] -- UzZU, q^1
  | 15, 5, 19 => [(19, 2)] -- VvNN, q^1
  | 15, 5, 15 => [(15, 2)] -- VvVV, q^1
  | 15, 1, 10 => [(14, 2)] -- VxEU, q^1
  | 15, 1, 11 => [(15, 2)] -- VxXV, q^1
  | 15, 2, 4 => [(8, 2)] -- Vyuf, q^1
  | 15, 2, 5 => [(9, 2)] -- Vyvn, q^1
  | 15, 2, 3 => [(7, 2)] -- Vyzj, q^1
  | 15, 3, 13 => [(15, 2)] -- VzZV, q^1
  | 11, 1, 10 => [(10, 2)] -- XxEE, q^1
  | 11, 1, 11 => [(11, 2)] -- XxXX, q^1
  | 12, 4, 18 => [(16, 2)] -- YuFT, q^1
  | 12, 4, 14 => [(12, 2)] -- YuUY, q^1
  | 12, 5, 19 => [(16, 2)] -- YvNT, q^1
  | 12, 5, 15 => [(12, 2)] -- YvVY, q^1
  | 12, 1, 11 => [(12, 2)] -- YxXY, q^1
  | 12, 2, 10 => [(10, 2)] -- YyEE, q^1
  | 12, 2, 17 => [(17, 2)] -- YyJJ, q^1
  | 12, 2, 16 => [(16, 2)] -- YyTT, q^1
  | 12, 2, 11 => [(11, 2)] -- YyXX, q^1
  | 12, 2, 12 => [(12, 2)] -- YyYY, q^1
  | 12, 2, 13 => [(13, 2)] -- YyZZ, q^1
  | 12, 3, 13 => [(12, 2)] -- YzZY, q^1
  | 13, 1, 11 => [(13, 2)] -- ZxXZ, q^1
  | 13, 3, 10 => [(10, 2)] -- ZzEE, q^1
  | 13, 3, 17 => [(17, 2)] -- ZzJJ, q^1
  | 13, 3, 16 => [(16, 2)] -- ZzTT, q^1
  | 13, 3, 11 => [(11, 2)] -- ZzXX, q^1
  | 7, 17, 18 => [(18, 2)] -- jJFF, q^1
  | 7, 17, 14 => [(14, 2)] -- jJUU, q^1
  | 7, 17, 7 => [(7, 2)] -- jJjj, q^1
  | 7, 17, 9 => [(9, 2)] -- jJnn, q^1
  | 7, 12, 2 => [(7, 2)] -- jYyj, q^1
  | 7, 13, 5 => [(9, 2)] -- jZvn, q^1
  | 7, 13, 3 => [(7, 2)] -- jZzj, q^1
  | 9, 19, 18 => [(18, 2)] -- nNFF, q^1
  | 9, 19, 14 => [(14, 2)] -- nNUU, q^1
  | 9, 6, 16 => [(9, 2)] -- ntTn, q^1
  | 6, 17, 7 => [(6, 2)] -- tJjt, q^1
  | 6, 16, 19 => [(19, 2)] -- tTNN, q^1
  | 6, 16, 15 => [(15, 2)] -- tTVV, q^1
  | 6, 16, 6 => [(6, 2)] -- tTtt, q^1
  | 6, 12, 2 => [(6, 2)] -- tYyt, q^1
  | 6, 13, 3 => [(6, 2)] -- tZzt, q^1
  | 6, 3, 17 => [(9, 2)] -- tzJn, q^1
  | 4, 18, 15 => [(11, 2)] -- uFVX, q^1
  | 4, 18, 6 => [(2, 2)] -- uFty, q^1
  | 4, 19, 18 => [(16, 2)] -- uNFT, q^1
  | 4, 19, 14 => [(12, 2)] -- uNUY, q^1
  | 4, 19, 6 => [(0, 2)] -- uNte, q^1
  | 4, 14, 2 => [(2, 2)] -- uUyy, q^1
  | 4, 15, 2 => [(0, 2)] -- uVye, q^1
  | 4, 7, 17 => [(4, 2)] -- ujJu, q^1
  | 5, 19, 14 => [(10, 2)] -- vNUE, q^1
  | 5, 19, 15 => [(11, 2)] -- vNVX, q^1
  | 5, 19, 6 => [(2, 2)] -- vNty, q^1
  | 5, 15, 2 => [(2, 2)] -- vVyy, q^1
  | 5, 6, 16 => [(5, 2)] -- vtTv, q^1
  | 1, 10, 4 => [(5, 2)] -- xEuv, q^1
  | 1, 17, 18 => [(16, 2)] -- xJFT, q^1
  | 1, 17, 14 => [(12, 2)] -- xJUY, q^1
  | 1, 17, 7 => [(1, 2)] -- xJjx, q^1
  | 1, 17, 6 => [(0, 2)] -- xJte, q^1
  | 1, 16, 6 => [(1, 2)] -- xTtx, q^1
  | 1, 11, 4 => [(4, 2)] -- xXuu, q^1
  | 1, 11, 5 => [(5, 2)] -- xXvv, q^1
  | 1, 11, 2 => [(2, 2)] -- xXyy, q^1
  | 1, 11, 3 => [(3, 2)] -- xXzz, q^1
  | 1, 12, 2 => [(1, 2)] -- xYyx, q^1
  | 1, 13, 2 => [(0, 2)] -- xZye, q^1
  | 1, 13, 3 => [(1, 2)] -- xZzx, q^1
  | 1, 4, 18 => [(5, 2)] -- xuFv, q^1
  | 1, 4, 19 => [(4, 2)] -- xuNu, q^1
  | 1, 5, 19 => [(5, 2)] -- xvNv, q^1
  | 2, 1, 17 => [(4, 2)] -- yxJu, q^1
  | 2, 3, 17 => [(5, 2)] -- yzJv, q^1
  | 3, 17, 19 => [(16, 2)] -- zJNT, q^1
  | 3, 17, 15 => [(12, 2)] -- zJVY, q^1
  | 3, 12, 2 => [(3, 2)] -- zYyz, q^1
  | 3, 13, 4 => [(4, 2)] -- zZuu, q^1
  | 3, 13, 5 => [(5, 2)] -- zZvv, q^1
  | 3, 13, 2 => [(2, 2)] -- zZyy, q^1
  | 3, 13, 3 => [(3, 2)] -- zZzz, q^1
  | 10, 2, 17 => [(16, 8)] -- EyJT, q^3
  | 17, 6, 10 => [(12, 8)] -- JtEY, q^3
  | 6, 10, 2 => [(7, 8)] -- tEyj, q^3
  | 6, 2, 17 => [(8, 8)] -- tyJf, q^3
  | 17, 19, 7 => [(11, 1)] -- JNjX, q^0
  | 17, 15, 3 => [(11, 1)] -- JVzX, q^0
  | 19, 19, 7 => [(14, 1)] -- NNjU, q^0
  | 19, 15, 3 => [(14, 1)] -- NVzU, q^0
  | 19, 7, 12 => [(14, 1)] -- NjYU, q^0
  | 19, 7, 4 => [(9, 1)] -- Njun, q^0
  | 19, 7, 1 => [(7, 1)] -- Njxj, q^0
  | 19, 6, 1 => [(6, 1)] -- Ntxt, q^0
  | 16, 19, 6 => [(11, 1)] -- TNtX, q^0
  | 16, 15, 2 => [(11, 1)] -- TVyX, q^0
  | 15, 2, 1 => [(6, 1)] -- Vyxt, q^0
  | 15, 3, 12 => [(14, 1)] -- VzYU, q^0
  | 15, 3, 4 => [(9, 1)] -- Vzun, q^0
  | 15, 3, 1 => [(7, 1)] -- Vzxj, q^0
  | 12, 4, 19 => [(17, 1)] -- YuNJ, q^0
  | 12, 4, 15 => [(13, 1)] -- YuVZ, q^0
  | 7, 12, 4 => [(9, 1)] -- jYun, q^0
  | 7, 4, 19 => [(9, 1)] -- juNn, q^0
  | 7, 1, 17 => [(9, 1)] -- jxJn, q^0
  | 6, 1, 16 => [(9, 1)] -- txTn, q^0
  | 4, 19, 19 => [(17, 1)] -- uNNJ, q^0
  | 4, 19, 15 => [(13, 1)] -- uNVZ, q^0
  | 4, 19, 7 => [(2, 1)] -- uNjy, q^0
  | 4, 15, 3 => [(2, 1)] -- uVzy, q^0
  | 1, 17, 19 => [(17, 1)] -- xJNJ, q^0
  | 1, 17, 15 => [(13, 1)] -- xJVZ, q^0
  | 1, 16, 19 => [(16, 1)] -- xTNT, q^0
  | 1, 16, 15 => [(12, 1)] -- xTVY, q^0
  | 2, 1, 16 => [(5, 1)] -- yxTv, q^0
  | 3, 12, 4 => [(5, 1)] -- zYuv, q^0
  | 3, 4, 19 => [(5, 1)] -- zuNv, q^0
  | 3, 1, 17 => [(5, 1)] -- zxJv, q^0
  | _, _, _ => []

/-- Basis indices other than 0=e and 8=f. -/
def radicalIndex (a : Fin 18) : Nat := if a.val < 7 then a.val + 1 else a.val + 2

def tTimesP (a : Nat) (terms : Terms) : Nat :=
  terms.foldl (fun acc term =>
    Nat.xor acc (scaleEncode term.2 (tTerms a term.1))) 0

def pTimesT (terms : Terms) (d : Nat) : Nat :=
  terms.foldl (fun acc term =>
    Nat.xor acc (scaleEncode term.2 (tTerms term.1 d))) 0

def pApplyFirst (terms : Terms) (c d : Nat) : Nat :=
  terms.foldl (fun acc term =>
    Nat.xor acc (scaleEncode term.2 (pTerms term.1 c d))) 0

def pApplyMiddle (a : Nat) (terms : Terms) (d : Nat) : Nat :=
  terms.foldl (fun acc term =>
    Nat.xor acc (scaleEncode term.2 (pTerms a term.1 d))) 0

def pApplyLast (a b : Nat) (terms : Terms) : Nat :=
  terms.foldl (fun acc term =>
    Nat.xor acc (scaleEncode term.2 (pTerms a b term.1))) 0

/-- Every one of the five Hochschild differential terms, with no filtering. -/
def hochschildClosure (a b c d : Nat) : Nat :=
  Nat.xor (tTimesP a (pTerms b c d))
    (Nat.xor (pApplyFirst (tTerms a b) c d)
      (Nat.xor (pApplyMiddle a (tTerms b c) d)
        (Nat.xor (pApplyLast a b (tTerms c d))
          (pTimesT (pTerms a b c) d))))

/-- The exact source rows, used to certify the count and faithful match cases. -/
def pEntries : List (Nat × Nat × Nat × Nat × Nat) := [
  (10, 4, 19, 16, 4),
  (10, 2, 13, 11, 4),
  (18, 19, 6, 14, 4),
  (17, 6, 11, 13, 4),
  (19, 6, 10, 14, 4),
  (19, 6, 11, 15, 4),
  (11, 3, 17, 16, 4),
  (13, 1, 10, 12, 4),
  (6, 10, 4, 9, 4),
  (6, 11, 4, 8, 4),
  (6, 11, 5, 9, 4),
  (6, 11, 3, 7, 4),
  (6, 4, 18, 9, 4),
  (6, 4, 19, 8, 4),
  (6, 5, 19, 9, 4),
  (4, 18, 19, 16, 4),
  (5, 19, 19, 16, 4),
  (5, 6, 17, 4, 4),
  (1, 10, 2, 3, 4),
  (3, 17, 6, 1, 4),
  (10, 4, 14, 10, 2),
  (10, 4, 15, 11, 2),
  (10, 5, 15, 10, 2),
  (10, 1, 11, 10, 2),
  (10, 2, 12, 10, 2),
  (10, 3, 13, 10, 2),
  (18, 19, 9, 18, 2),
  (18, 15, 5, 18, 2),
  (18, 15, 1, 14, 2),
  (18, 6, 16, 18, 2),
  (18, 6, 12, 14, 2),
  (18, 6, 4, 9, 2),
  (18, 6, 1, 7, 2),
  (17, 18, 6, 11, 2),
  (17, 19, 6, 13, 2),
  (17, 14, 2, 11, 2),
  (17, 15, 2, 13, 2),
  (17, 7, 10, 10, 2),
  (17, 7, 16, 16, 2),
  (17, 7, 11, 11, 2),
  (19, 18, 6, 14, 2),
  (19, 19, 6, 15, 2),
  (19, 14, 2, 14, 2),
  (19, 15, 2, 15, 2),
  (19, 7, 17, 19, 2),
  (19, 7, 13, 15, 2),
  (19, 9, 19, 19, 2),
  (19, 9, 15, 15, 2),
  (19, 6, 4, 8, 2),
  (19, 6, 5, 9, 2),
  (19, 6, 3, 7, 2),
  (16, 6, 10, 10, 2),
  (16, 6, 11, 11, 2),
  (14, 4, 18, 18, 2),
  (14, 4, 14, 14, 2),
  (14, 5, 19, 18, 2),
  (14, 5, 15, 14, 2),
  (14, 1, 11, 14, 2),
  (14, 2, 4, 9, 2),
  (14, 2, 1, 7, 2),
  (14, 3, 13, 14, 2),
  (15, 5, 19, 19, 2),
  (15, 5, 15, 15, 2),
  (15, 1, 10, 14, 2),
  (15, 1, 11, 15, 2),
  (15, 2, 4, 8, 2),
  (15, 2, 5, 9, 2),
  (15, 2, 3, 7, 2),
  (15, 3, 13, 15, 2),
  (11, 1, 10, 10, 2),
  (11, 1, 11, 11, 2),
  (12, 4, 18, 16, 2),
  (12, 4, 14, 12, 2),
  (12, 5, 19, 16, 2),
  (12, 5, 15, 12, 2),
  (12, 1, 11, 12, 2),
  (12, 2, 10, 10, 2),
  (12, 2, 17, 17, 2),
  (12, 2, 16, 16, 2),
  (12, 2, 11, 11, 2),
  (12, 2, 12, 12, 2),
  (12, 2, 13, 13, 2),
  (12, 3, 13, 12, 2),
  (13, 1, 11, 13, 2),
  (13, 3, 10, 10, 2),
  (13, 3, 17, 17, 2),
  (13, 3, 16, 16, 2),
  (13, 3, 11, 11, 2),
  (7, 17, 18, 18, 2),
  (7, 17, 14, 14, 2),
  (7, 17, 7, 7, 2),
  (7, 17, 9, 9, 2),
  (7, 12, 2, 7, 2),
  (7, 13, 5, 9, 2),
  (7, 13, 3, 7, 2),
  (9, 19, 18, 18, 2),
  (9, 19, 14, 14, 2),
  (9, 6, 16, 9, 2),
  (6, 17, 7, 6, 2),
  (6, 16, 19, 19, 2),
  (6, 16, 15, 15, 2),
  (6, 16, 6, 6, 2),
  (6, 12, 2, 6, 2),
  (6, 13, 3, 6, 2),
  (6, 3, 17, 9, 2),
  (4, 18, 15, 11, 2),
  (4, 18, 6, 2, 2),
  (4, 19, 18, 16, 2),
  (4, 19, 14, 12, 2),
  (4, 19, 6, 0, 2),
  (4, 14, 2, 2, 2),
  (4, 15, 2, 0, 2),
  (4, 7, 17, 4, 2),
  (5, 19, 14, 10, 2),
  (5, 19, 15, 11, 2),
  (5, 19, 6, 2, 2),
  (5, 15, 2, 2, 2),
  (5, 6, 16, 5, 2),
  (1, 10, 4, 5, 2),
  (1, 17, 18, 16, 2),
  (1, 17, 14, 12, 2),
  (1, 17, 7, 1, 2),
  (1, 17, 6, 0, 2),
  (1, 16, 6, 1, 2),
  (1, 11, 4, 4, 2),
  (1, 11, 5, 5, 2),
  (1, 11, 2, 2, 2),
  (1, 11, 3, 3, 2),
  (1, 12, 2, 1, 2),
  (1, 13, 2, 0, 2),
  (1, 13, 3, 1, 2),
  (1, 4, 18, 5, 2),
  (1, 4, 19, 4, 2),
  (1, 5, 19, 5, 2),
  (2, 1, 17, 4, 2),
  (2, 3, 17, 5, 2),
  (3, 17, 19, 16, 2),
  (3, 17, 15, 12, 2),
  (3, 12, 2, 3, 2),
  (3, 13, 4, 4, 2),
  (3, 13, 5, 5, 2),
  (3, 13, 2, 2, 2),
  (3, 13, 3, 3, 2),
  (10, 2, 17, 16, 8),
  (17, 6, 10, 12, 8),
  (6, 10, 2, 7, 8),
  (6, 2, 17, 8, 8),
  (17, 19, 7, 11, 1),
  (17, 15, 3, 11, 1),
  (19, 19, 7, 14, 1),
  (19, 15, 3, 14, 1),
  (19, 7, 12, 14, 1),
  (19, 7, 4, 9, 1),
  (19, 7, 1, 7, 1),
  (19, 6, 1, 6, 1),
  (16, 19, 6, 11, 1),
  (16, 15, 2, 11, 1),
  (15, 2, 1, 6, 1),
  (15, 3, 12, 14, 1),
  (15, 3, 4, 9, 1),
  (15, 3, 1, 7, 1),
  (12, 4, 19, 17, 1),
  (12, 4, 15, 13, 1),
  (7, 12, 4, 9, 1),
  (7, 4, 19, 9, 1),
  (7, 1, 17, 9, 1),
  (6, 1, 16, 9, 1),
  (4, 19, 19, 17, 1),
  (4, 19, 15, 13, 1),
  (4, 19, 7, 2, 1),
  (4, 15, 3, 2, 1),
  (1, 17, 19, 17, 1),
  (1, 17, 15, 13, 1),
  (1, 16, 19, 16, 1),
  (1, 16, 15, 12, 1),
  (2, 1, 16, 5, 1),
  (3, 12, 4, 5, 1),
  (3, 4, 19, 5, 1),
  (3, 1, 17, 5, 1)
]

theorem p_entry_count : pEntries.length = 179 := by decide

theorem p_entries_match :
    pEntries.all (fun (a,b,c,v,p) => pTerms a b c == [(v,p)]) = true := by decide

/-- Every cochain coefficient is <16, hence degree at most three. -/
theorem p_coefficient_and_output_bounds :
    ∀ a b c : Fin 20,
      (pTerms a.val b.val c.val).all (fun x => x.1 < 20 && x.2 < 16) = true := by
  decide

/-- Every algebra coefficient is <16 as well. -/
theorem t_coefficient_bound :
    ∀ a b : Fin 20, (tTerms a.val b.val).all (fun x => x.2 < 16) = true := by decide

/-- Each product of the small coefficients fits in the eight-bit block. -/
theorem certificate_coefficient_product_bound :
    ∀ a b : Fin 16, pMul a.val b.val < 256 := by decide

/-- The actual encoded pairing of the two-term bar cycle is q^3 f. -/
theorem cycle_pairing :
    Nat.xor (scaleEncode 4 (pTerms 6 1 17)) (encode (pTerms 6 2 17)) = pack 8 8 := by
  decide

/-- Encode the two internal faces of a three-letter two-sided-simple bar word. -/
def barInnerDifferential (scalar a b c : Nat) : Nat :=
  Nat.xor
    ((tTerms a b).foldl (fun acc term =>
      Nat.xor acc (pack (20 * term.1 + c) (pMul scalar term.2))) 0)
    ((tTerms b c).foldl (fun acc term =>
      Nat.xor acc (pack (20 * a + term.1) (pMul scalar term.2))) 0)

/-- Exact cancellation of all internal bar faces of q^2[t|x|J]+[t|y|J]. -/
theorem cycle_inner_differential_zero :
    Nat.xor (barInnerDifferential 4 6 1 17) (barInnerDifferential 1 6 2 17) = 0 := by
  decide

#print axioms p_entry_count
#print axioms p_entries_match
#print axioms p_coefficient_and_output_bounds
#print axioms t_coefficient_bound
#print axioms certificate_coefficient_product_bound
#print axioms cycle_pairing
#print axioms cycle_inner_differential_zero
end ARCFiniteCore
