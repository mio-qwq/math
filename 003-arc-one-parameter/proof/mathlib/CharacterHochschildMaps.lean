import HochschildLowDegrees
import Mathlib.Algebra.Algebra.Hom

/-!
Low-degree Hochschild cochains with values in the character bimodule R.
The left and right actions of A on R are multiplication by an actual
R-algebra character eps : A →ₐ[R] R.  The displayed full differentials
are linear maps on all scalar-valued multilinear cochains.  In
characteristic two of R their composition is zero.  No bar resolution,
Ext identification, or application to a particular character is asserted.
-/

namespace ARCCharacterHochschildMaps

variable {R A : Type*} [CommRing R] [Ring A] [Algebra R A]

abbrev C2S (R A : Type*) [CommRing R] [Ring A] [Algebra R A] :=
  A →ₗ[R] A →ₗ[R] R

abbrev C3S (R A : Type*) [CommRing R] [Ring A] [Algebra R A] :=
  A →ₗ[R] A →ₗ[R] A →ₗ[R] R

abbrev C4S (R A : Type*) [CommRing R] [Ring A] [Algebra R A] :=
  A →ₗ[R] A →ₗ[R] A →ₗ[R] A →ₗ[R] R

/-- The four full faces for the character bimodule. -/
def differential2 (eps : A →ₐ[R] R) (G : A → A → R) (x y z : A) : R :=
  eps x * G y z + G (x * y) z + G x (y * z) + G x y * eps z

/-- The five full faces for the same character bimodule. -/
def differential3 (eps : A →ₐ[R] R) (F : A → A → A → R)
    (x y z w : A) : R :=
  eps x * F y z w + F (x * y) z w + F x (y * z) w +
    F x y (z * w) + F x y z * eps w

section CharacteristicTwo

variable [CharP R 2]

/-- Cancellation holds even before imposing linearity on the input function.
Only the coefficient ring, not the source algebra, is required to have
characteristic two. -/
theorem differential3_differential2 (eps : A →ₐ[R] R)
    (G : A → A → R) (x y z w : A) :
    differential3 eps (differential2 eps G) x y z w = 0 := by
  simp only [differential3, differential2, map_mul, mul_add, add_mul, mul_assoc]
  abel_nf
  simp only [CharTwo.two_zsmul, zero_add]

end CharacteristicTwo

noncomputable section

variable (eps : A →ₐ[R] R)

theorem differential2_add_first (G : C2S R A) (x x' y z : A) :
    differential2 eps (fun a b => G a b) (x + x') y z =
      differential2 eps (fun a b => G a b) x y z +
      differential2 eps (fun a b => G a b) x' y z := by
  simp only [differential2, add_mul, map_add, LinearMap.add_apply]
  ac_rfl

theorem differential2_add_second (G : C2S R A) (x y y' z : A) :
    differential2 eps (fun a b => G a b) x (y + y') z =
      differential2 eps (fun a b => G a b) x y z +
      differential2 eps (fun a b => G a b) x y' z := by
  simp only [differential2, add_mul, mul_add, map_add, LinearMap.add_apply]
  abel

theorem differential2_add_third (G : C2S R A) (x y z z' : A) :
    differential2 eps (fun a b => G a b) x y (z + z') =
      differential2 eps (fun a b => G a b) x y z +
      differential2 eps (fun a b => G a b) x y z' := by
  simp only [differential2, mul_add, map_add]
  abel

theorem differential2_smul_first (G : C2S R A) (r : R) (x y z : A) :
    differential2 eps (fun a b => G a b) (r • x) y z =
      r • differential2 eps (fun a b => G a b) x y z := by
  simp only [differential2, smul_mul_assoc, map_smul,
    LinearMap.smul_apply, smul_add]

theorem differential2_smul_second (G : C2S R A) (r : R) (x y z : A) :
    differential2 eps (fun a b => G a b) x (r • y) z =
      r • differential2 eps (fun a b => G a b) x y z := by
  simp only [differential2, smul_mul_assoc, Algebra.mul_smul_comm,
    map_smul, LinearMap.smul_apply, smul_add]

theorem differential2_smul_third (G : C2S R A) (r : R) (x y z : A) :
    differential2 eps (fun a b => G a b) x y (r • z) =
      r • differential2 eps (fun a b => G a b) x y z := by
  simp only [differential2, Algebra.mul_smul_comm, map_smul, smul_add]

/-- The four-face formula of a bilinear scalar cochain is trilinear. -/
def differential2Linear (G : C2S R A) : C3S R A where
  toFun x :=
    { toFun y :=
        { toFun z := differential2 eps (fun a b => G a b) x y z
          map_add' z z' := differential2_add_third eps G x y z z'
          map_smul' r z := differential2_smul_third eps G r x y z }
      map_add' y y' := by ext z; exact differential2_add_second eps G x y y' z
      map_smul' r y := by ext z; exact differential2_smul_second eps G r x y z }
  map_add' x x' := by ext y z; exact differential2_add_first eps G x x' y z
  map_smul' r x := by ext y z; exact differential2_smul_first eps G r x y z

@[simp] theorem differential2Linear_apply (G : C2S R A) (x y z : A) :
    differential2Linear eps G x y z =
      differential2 eps (fun a b => G a b) x y z := rfl

/-- The degree-two differential is linear in the cochain. -/
def d2 : C2S R A →ₗ[R] C3S R A where
  toFun := differential2Linear eps
  map_add' G H := by
    ext x y z
    simp only [differential2Linear_apply, differential2, LinearMap.add_apply,
      mul_add, add_mul]
    ac_rfl
  map_smul' r G := by
    ext x y z
    simp only [differential2Linear_apply, differential2, LinearMap.smul_apply,
      smul_mul_assoc, Algebra.mul_smul_comm, smul_add, RingHom.id_apply]

@[simp] theorem d2_apply (G : C2S R A) (x y z : A) :
    d2 eps G x y z = differential2 eps (fun a b => G a b) x y z := rfl

theorem differential3_add_first (F : C3S R A) (x x' y z w : A) :
    differential3 eps (fun a b c => F a b c) (x + x') y z w =
      differential3 eps (fun a b c => F a b c) x y z w +
      differential3 eps (fun a b c => F a b c) x' y z w := by
  simp only [differential3, add_mul, map_add, LinearMap.add_apply]
  ac_rfl

theorem differential3_add_second (F : C3S R A) (x y y' z w : A) :
    differential3 eps (fun a b c => F a b c) x (y + y') z w =
      differential3 eps (fun a b c => F a b c) x y z w +
      differential3 eps (fun a b c => F a b c) x y' z w := by
  simp only [differential3, add_mul, mul_add, map_add, LinearMap.add_apply]
  ac_rfl

theorem differential3_add_third (F : C3S R A) (x y z z' w : A) :
    differential3 eps (fun a b c => F a b c) x y (z + z') w =
      differential3 eps (fun a b c => F a b c) x y z w +
      differential3 eps (fun a b c => F a b c) x y z' w := by
  simp only [differential3, add_mul, mul_add, map_add, LinearMap.add_apply]
  abel

theorem differential3_add_fourth (F : C3S R A) (x y z w w' : A) :
    differential3 eps (fun a b c => F a b c) x y z (w + w') =
      differential3 eps (fun a b c => F a b c) x y z w +
      differential3 eps (fun a b c => F a b c) x y z w' := by
  simp only [differential3, mul_add, map_add]
  abel

theorem differential3_smul_first (F : C3S R A) (r : R) (x y z w : A) :
    differential3 eps (fun a b c => F a b c) (r • x) y z w =
      r • differential3 eps (fun a b c => F a b c) x y z w := by
  simp only [differential3, smul_mul_assoc, map_smul,
    LinearMap.smul_apply, smul_add]

theorem differential3_smul_second (F : C3S R A) (r : R) (x y z w : A) :
    differential3 eps (fun a b c => F a b c) x (r • y) z w =
      r • differential3 eps (fun a b c => F a b c) x y z w := by
  simp only [differential3, smul_mul_assoc, Algebra.mul_smul_comm,
    map_smul, LinearMap.smul_apply, smul_add]

theorem differential3_smul_third (F : C3S R A) (r : R) (x y z w : A) :
    differential3 eps (fun a b c => F a b c) x y (r • z) w =
      r • differential3 eps (fun a b c => F a b c) x y z w := by
  simp only [differential3, smul_mul_assoc, Algebra.mul_smul_comm,
    map_smul, LinearMap.smul_apply, smul_add]

theorem differential3_smul_fourth (F : C3S R A) (r : R) (x y z w : A) :
    differential3 eps (fun a b c => F a b c) x y z (r • w) =
      r • differential3 eps (fun a b c => F a b c) x y z w := by
  simp only [differential3, Algebra.mul_smul_comm, map_smul, smul_add]

/-- The five-face formula of a trilinear scalar cochain is four-linear. -/
def differential3Linear (F : C3S R A) : C4S R A where
  toFun x :=
    { toFun y :=
        { toFun z :=
            { toFun w := differential3 eps (fun a b c => F a b c) x y z w
              map_add' w w' := differential3_add_fourth eps F x y z w w'
              map_smul' r w := differential3_smul_fourth eps F r x y z w }
          map_add' z z' := by ext w; exact differential3_add_third eps F x y z z' w
          map_smul' r z := by ext w; exact differential3_smul_third eps F r x y z w }
      map_add' y y' := by ext z w; exact differential3_add_second eps F x y y' z w
      map_smul' r y := by ext z w; exact differential3_smul_second eps F r x y z w }
  map_add' x x' := by ext y z w; exact differential3_add_first eps F x x' y z w
  map_smul' r x := by ext y z w; exact differential3_smul_first eps F r x y z w

@[simp] theorem differential3Linear_apply (F : C3S R A) (x y z w : A) :
    differential3Linear eps F x y z w =
      differential3 eps (fun a b c => F a b c) x y z w := rfl

/-- The degree-three differential is linear in the cochain. -/
def d3 : C3S R A →ₗ[R] C4S R A where
  toFun := differential3Linear eps
  map_add' F G := by
    ext x y z w
    simp only [differential3Linear_apply, differential3, LinearMap.add_apply,
      mul_add, add_mul]
    ac_rfl
  map_smul' r F := by
    ext x y z w
    simp only [differential3Linear_apply, differential3, LinearMap.smul_apply,
      smul_mul_assoc, Algebra.mul_smul_comm, smul_add, RingHom.id_apply]

@[simp] theorem d3_apply (F : C3S R A) (x y z w : A) :
    d3 eps F x y z w = differential3 eps (fun a b c => F a b c) x y z w := rfl

variable [CharP R 2]

@[simp] theorem d3_d2 (G : C2S R A) : d3 eps (d2 eps G) = 0 := by
  ext x y z w
  exact differential3_differential2 eps (fun a b => G a b) x y z w

/-- The full character cochains form a complex at degree three. -/
theorem d3_comp_d2 : (d3 eps).comp (d2 eps) = 0 := by
  ext G x y z w
  exact differential3_differential2 eps (fun a b => G a b) x y z w

#print axioms differential3_differential2
#print axioms differential2Linear
#print axioms d2
#print axioms differential3Linear
#print axioms d3
#print axioms d3_comp_d2

end
end ARCCharacterHochschildMaps
