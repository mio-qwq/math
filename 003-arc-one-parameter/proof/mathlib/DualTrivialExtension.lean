import Mathlib.LinearAlgebra.Dual.Basis
import Mathlib.Algebra.Algebra.Bilinear
import Mathlib.LinearAlgebra.FreeModule.Basic
import Mathlib.LinearAlgebra.Basis.Prod
import Mathlib.LinearAlgebra.Dimension.Constructions

/-!
# Dual-action trivial extensions

For any algebra over a commutative ring, the dual regular actions give an
associative unital trivial extension. The evaluation-at-one trace is symmetric
and separates vectors whenever the dual separates vectors of the original
algebra. This generic construction does not identify the fixed ARC table with
the extension and does not construct Hochschild cohomology or Ext.
-/

namespace ARCDualTrivialExtension

noncomputable section

variable {R A : Type*} [CommRing R] [Ring A] [Algebra R A]

/-- The left regular dual action: `(a φ)(c) = φ(c a)`. -/
def leftAction (a : A) (φ : Module.Dual R A) : Module.Dual R A :=
  φ.comp (LinearMap.mulRight R a)

/-- The right regular dual action: `(φ a)(c) = φ(a c)`. -/
def rightAction (φ : Module.Dual R A) (a : A) : Module.Dual R A :=
  φ.comp (LinearMap.mulLeft R a)

@[simp] theorem leftAction_apply (a c : A) (φ : Module.Dual R A) :
    leftAction a φ c = φ (c * a) := rfl

@[simp] theorem rightAction_apply (a c : A) (φ : Module.Dual R A) :
    rightAction φ a c = φ (a * c) := rfl

/-- The genuine product on the algebra and its module dual. -/
def extensionMul (x y : A × Module.Dual R A) : A × Module.Dual R A :=
  (x.1 * y.1, leftAction x.1 y.2 + rightAction x.2 y.1)

/-- Associativity follows from the actual algebra multiplication and dual
actions; no encoded data or finite checks are used. -/
theorem extensionMul_assoc (x y z : A × Module.Dual R A) :
    extensionMul (extensionMul x y) z = extensionMul x (extensionMul y z) := by
  apply Prod.ext
  · exact mul_assoc x.1 y.1 z.1
  · ext c
    simp [extensionMul, leftAction, rightAction, mul_assoc, add_assoc]

theorem extensionMul_one_left (x : A × Module.Dual R A) :
    extensionMul (1, 0) x = x := by
  apply Prod.ext
  · simp [extensionMul]
  · ext c
    simp [extensionMul, leftAction, rightAction]

theorem extensionMul_one_right (x : A × Module.Dual R A) :
    extensionMul x (1, 0) = x := by
  apply Prod.ext
  · simp [extensionMul]
  · ext c
    simp [extensionMul, leftAction, rightAction]

theorem extensionMul_add_left (x y z : A × Module.Dual R A) :
    extensionMul (x + y) z = extensionMul x z + extensionMul y z := by
  apply Prod.ext
  · simp [extensionMul, add_mul]
  · ext c
    simp [extensionMul, leftAction, rightAction, mul_add, map_add]
    abel

theorem extensionMul_add_right (x y z : A × Module.Dual R A) :
    extensionMul x (y + z) = extensionMul x y + extensionMul x z := by
  apply Prod.ext
  · simp [extensionMul, mul_add]
  · ext c
    simp [extensionMul, leftAction, rightAction, add_mul, map_add]
    abel

theorem extensionMul_zero_left (x : A × Module.Dual R A) :
    extensionMul 0 x = 0 := by
  apply Prod.ext
  · simp [extensionMul]
  · ext c
    simp [extensionMul, leftAction, rightAction]

theorem extensionMul_zero_right (x : A × Module.Dual R A) :
    extensionMul x 0 = 0 := by
  apply Prod.ext
  · simp [extensionMul]
  · ext c
    simp [extensionMul, leftAction, rightAction]

theorem extensionMul_smul_left (r : R) (x y : A × Module.Dual R A) :
    extensionMul (r • x) y = r • extensionMul x y := by
  apply Prod.ext
  · simp [extensionMul]
  · ext c
    simp [extensionMul, leftAction, rightAction, smul_add]

theorem extensionMul_smul_right (r : R) (x y : A × Module.Dual R A) :
    extensionMul x (r • y) = r • extensionMul x y := by
  apply Prod.ext
  · simp [extensionMul]
  · ext c
    simp [extensionMul, leftAction, rightAction, smul_add]

/-- Evaluation of the dual component at the actual unit of the algebra. -/
def trace (x : A × Module.Dual R A) : R := x.2 1

theorem trace_mul (x y : A × Module.Dual R A) :
    trace (extensionMul x y) = y.2 x.1 + x.2 y.1 := by
  simp [trace, extensionMul, leftAction, rightAction]

/-- The evaluation trace is symmetric for every pair of extension vectors. -/
theorem trace_symmetric (x y : A × Module.Dual R A) :
    trace (extensionMul x y) = trace (extensionMul y x) := by
  rw [trace_mul, trace_mul, add_comm]

/-- Trace nondegeneracy with the exact, explicit dual-separation hypothesis. -/
theorem trace_nondegenerate
    (hsep : ∀ a : A, (∀ φ : Module.Dual R A, φ a = 0) → a = 0)
    (x : A × Module.Dual R A)
    (hx : ∀ y : A × Module.Dual R A, trace (extensionMul x y) = 0) : x = 0 := by
  have ha : x.1 = 0 := hsep x.1 (fun φ => by
    simpa [trace_mul] using hx (0, φ))
  have hφ : x.2 = 0 := by
    ext a
    simpa [trace_mul] using hx (a, 0)
  exact Prod.ext ha hφ

/-- Every free module has the required separation by its coordinate duals. -/
theorem trace_nondegenerate_of_free [Module.Free R A]
    (x : A × Module.Dual R A)
    (hx : ∀ y : A × Module.Dual R A, trace (extensionMul x y) = 0) : x = 0 := by
  classical
  apply trace_nondegenerate _ x hx
  intro a ha
  apply (Module.Free.chooseBasis R A).eval_injective
  ext φ
  simpa using ha φ

/-- Separate type carrying the genuine trivial-extension multiplication. -/
def Carrier (R A : Type*) [CommRing R] [Ring A] [Algebra R A] :=
  A × Module.Dual R A

instance carrierAddCommGroup : AddCommGroup (Carrier R A) :=
  inferInstanceAs (AddCommGroup (A × Module.Dual R A))

instance carrierRing : Ring (Carrier R A) where
  __ := carrierAddCommGroup (R := R) (A := A)
  mul := extensionMul
  one := (1, 0)
  mul_assoc := extensionMul_assoc
  one_mul := extensionMul_one_left
  mul_one := extensionMul_one_right
  left_distrib := extensionMul_add_right
  right_distrib := extensionMul_add_left
  zero_mul := extensionMul_zero_left
  mul_zero := extensionMul_zero_right

instance carrierModule : Module R (Carrier R A) :=
  inferInstanceAs (Module R (A × Module.Dual R A))

instance carrierAlgebra : Algebra R (Carrier R A) :=
  Algebra.ofModule extensionMul_smul_left extensionMul_smul_right

@[simp] theorem carrier_mul (x y : Carrier R A) : x * y = extensionMul x y := rfl

@[simp] theorem carrier_one : (1 : Carrier R A) = (1, 0) := rfl

/-- A linear trace on the constructed algebra. -/
def traceLinear : Carrier R A →ₗ[R] R where
  toFun := trace
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

/-- The actual bilinear pairing obtained by tracing multiplication. -/
def tracePairing : Carrier R A →ₗ[R] Carrier R A →ₗ[R] R :=
  LinearMap.mk₂ R (fun x y => traceLinear (x * y))
    (by intros; simp only [add_mul, map_add])
    (by intros; simp only [smul_mul_assoc, map_smul])
    (by intros; simp only [mul_add, map_add])
    (by intros; simp only [mul_smul_comm, map_smul])

theorem tracePairing_symmetric (x y : Carrier R A) :
    tracePairing x y = tracePairing y x := trace_symmetric x y

theorem tracePairing_nondegenerate [Module.Free R A] (x : Carrier R A)
    (hx : ∀ y, tracePairing x y = 0) : x = 0 :=
  trace_nondegenerate_of_free x hx

/-- The extension has the lower basis and its coordinate dual as a genuine
module basis, not only an encoded trace-pairing table. -/
def carrierBasis {ι : Type*} [Fintype ι] [DecidableEq ι]
    (b : Module.Basis ι R A) : Module.Basis (Sum ι ι) R (Carrier R A) :=
  b.prod b.dualBasis

/-- Exchange a lower basis label with its dual label. -/
def dualSwap {ι : Type*} : Sum ι ι → Sum ι ι
  | Sum.inl i => Sum.inr i
  | Sum.inr i => Sum.inl i

/-- The genuine trace Gram matrix is exactly the basis/dual permutation
matrix, for every finite basis of every algebra under these hypotheses. -/
theorem tracePairing_basis {ι : Type*} [Fintype ι] [DecidableEq ι]
    (b : Module.Basis ι R A) (i j : Sum ι ι) :
    tracePairing (carrierBasis b i) (carrierBasis b j) =
      if j = dualSwap i then 1 else 0 := by
  calc
    _ = ((b.prod b.dualBasis) j).2 (((b.prod b.dualBasis) i).1) +
        ((b.prod b.dualBasis) i).2 (((b.prod b.dualBasis) j).1) :=
      trace_mul _ _
    _ = _ := by cases i <;> cases j <;> simp [dualSwap, Finsupp.single_apply, eq_comm]

/-- Exact doubling of the dimension for any finite coordinate basis. -/
theorem carrier_finrank {ι : Type*} [Fintype ι] [DecidableEq ι]
    [StrongRankCondition R] (b : Module.Basis ι R A) :
    Module.finrank R (Carrier R A) = 2 * Fintype.card ι := by
  rw [Module.finrank_eq_card_basis (carrierBasis b), Fintype.card_sum]
  omega

#print axioms extensionMul_assoc
#print axioms extensionMul_one_left
#print axioms extensionMul_one_right
#print axioms trace_mul
#print axioms trace_symmetric
#print axioms trace_nondegenerate
#print axioms trace_nondegenerate_of_free
#print axioms carrierRing
#print axioms carrierAlgebra
#print axioms tracePairing_symmetric
#print axioms tracePairing_nondegenerate
#print axioms carrier_finrank
#print axioms tracePairing_basis

end
end ARCDualTrivialExtension
