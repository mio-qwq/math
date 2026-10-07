import HochschildLowDegrees

/-!
# Actual linear maps between low-degree cochain modules

Degree-two, degree-three and degree-four cochains are nested R-linear maps
on an associative R-algebra. The unsigned four- and five-face formulas are
packaged as R-linear maps between these modules. In characteristic two
their composition is zero, by the existing low-degree cancellation proof.

This file constructs no quotient, higher-degree complex, bar resolution,
or comparison with Ext. The formulas are unsigned, so the stated complex
law explicitly requires characteristic two of the output algebra.
-/

namespace ARCHochschildCochainMaps

open ARCHochschildLowDegrees

/-- Bilinear degree-two cochains. -/
abbrev C2 (R A : Type*) [CommRing R] [Ring A] [Algebra R A] :=
  A →ₗ[R] A →ₗ[R] A

/-- Trilinear degree-three cochains. -/
abbrev C3 (R A : Type*) [CommRing R] [Ring A] [Algebra R A] :=
  A →ₗ[R] A →ₗ[R] A →ₗ[R] A

/-- Four-linear degree-four cochains. -/
abbrev C4 (R A : Type*) [CommRing R] [Ring A] [Algebra R A] :=
  A →ₗ[R] A →ₗ[R] A →ₗ[R] A →ₗ[R] A

variable {R A : Type*} [CommRing R] [Ring A] [Algebra R A]

noncomputable section

/-- The four-face formula is R-linear in the bilinear cochain itself. -/
def d2 : C2 R A →ₗ[R] C3 R A where
  toFun := differential2Linear
  map_add' G H := by
    ext x y z
    simp only [differential2Linear_apply, differential2, LinearMap.add_apply,
      mul_add, add_mul]
    ac_rfl
  map_smul' r G := by
    ext x y z
    simp only [differential2Linear_apply, differential2, LinearMap.smul_apply,
      smul_mul_assoc, Algebra.mul_smul_comm, smul_add, RingHom.id_apply]

@[simp] theorem d2_apply (G : C2 R A) (x y z : A) :
    d2 G x y z = differential2 (fun a b => G a b) x y z := rfl

theorem differential3_add_first (F : C3 R A) (x x' y z w : A) :
    differential3 (fun a b c => F a b c) (x + x') y z w =
      differential3 (fun a b c => F a b c) x y z w +
      differential3 (fun a b c => F a b c) x' y z w := by
  simp only [differential3, add_mul, map_add, LinearMap.add_apply]
  ac_rfl

theorem differential3_add_second (F : C3 R A) (x y y' z w : A) :
    differential3 (fun a b c => F a b c) x (y + y') z w =
      differential3 (fun a b c => F a b c) x y z w +
      differential3 (fun a b c => F a b c) x y' z w := by
  simp only [differential3, add_mul, mul_add, map_add, LinearMap.add_apply]
  ac_rfl

theorem differential3_add_third (F : C3 R A) (x y z z' w : A) :
    differential3 (fun a b c => F a b c) x y (z + z') w =
      differential3 (fun a b c => F a b c) x y z w +
      differential3 (fun a b c => F a b c) x y z' w := by
  simp only [differential3, add_mul, mul_add, map_add, LinearMap.add_apply]
  ac_rfl

theorem differential3_add_fourth (F : C3 R A) (x y z w w' : A) :
    differential3 (fun a b c => F a b c) x y z (w + w') =
      differential3 (fun a b c => F a b c) x y z w +
      differential3 (fun a b c => F a b c) x y z w' := by
  simp only [differential3, mul_add, map_add]
  ac_rfl

theorem differential3_smul_first (F : C3 R A) (r : R) (x y z w : A) :
    differential3 (fun a b c => F a b c) (r • x) y z w =
      r • differential3 (fun a b c => F a b c) x y z w := by
  simp only [differential3, smul_mul_assoc, map_smul,
    LinearMap.smul_apply, smul_add]

theorem differential3_smul_second (F : C3 R A) (r : R) (x y z w : A) :
    differential3 (fun a b c => F a b c) x (r • y) z w =
      r • differential3 (fun a b c => F a b c) x y z w := by
  simp only [differential3, smul_mul_assoc, Algebra.mul_smul_comm,
    map_smul, LinearMap.smul_apply, smul_add]

theorem differential3_smul_third (F : C3 R A) (r : R) (x y z w : A) :
    differential3 (fun a b c => F a b c) x y (r • z) w =
      r • differential3 (fun a b c => F a b c) x y z w := by
  simp only [differential3, smul_mul_assoc, Algebra.mul_smul_comm,
    map_smul, LinearMap.smul_apply, smul_add]

theorem differential3_smul_fourth (F : C3 R A) (r : R) (x y z w : A) :
    differential3 (fun a b c => F a b c) x y z (r • w) =
      r • differential3 (fun a b c => F a b c) x y z w := by
  simp only [differential3, Algebra.mul_smul_comm, map_smul, smul_add]

/-- The actual five-face formula of a trilinear cochain is four-linear. -/
def differential3Linear (F : C3 R A) : C4 R A where
  toFun x :=
    { toFun y :=
        { toFun z :=
            { toFun w := differential3 (fun a b c => F a b c) x y z w
              map_add' w w' := differential3_add_fourth F x y z w w'
              map_smul' r w := differential3_smul_fourth F r x y z w }
          map_add' z z' := by ext w; exact differential3_add_third F x y z z' w
          map_smul' r z := by ext w; exact differential3_smul_third F r x y z w }
      map_add' y y' := by ext z w; exact differential3_add_second F x y y' z w
      map_smul' r y := by ext z w; exact differential3_smul_second F r x y z w }
  map_add' x x' := by ext y z w; exact differential3_add_first F x x' y z w
  map_smul' r x := by ext y z w; exact differential3_smul_first F r x y z w

@[simp] theorem differential3Linear_apply (F : C3 R A) (x y z w : A) :
    differential3Linear F x y z w =
      differential3 (fun a b c => F a b c) x y z w := rfl

/-- The five-face formula is R-linear in the trilinear cochain itself. -/
def d3 : C3 R A →ₗ[R] C4 R A where
  toFun := differential3Linear
  map_add' F G := by
    ext x y z w
    simp only [differential3Linear_apply, differential3, LinearMap.add_apply,
      mul_add, add_mul]
    ac_rfl
  map_smul' r F := by
    ext x y z w
    simp only [differential3Linear_apply, differential3, LinearMap.smul_apply,
      smul_mul_assoc, Algebra.mul_smul_comm, smul_add, RingHom.id_apply]

@[simp] theorem d3_apply (F : C3 R A) (x y z w : A) :
    d3 F x y z w = differential3 (fun a b c => F a b c) x y z w := rfl

section CharacteristicTwo

variable [CharP A 2]

/-- Each actual bilinear cochain has zero composed coboundary. -/
@[simp] theorem d3_d2 (G : C2 R A) : d3 (d2 G) = 0 := by
  ext x y z w
  exact differential3_differential2 (fun a b => G a b) x y z w

/-- The low-degree cochain modules and actual linear maps form a complex
at degree three in characteristic two. -/
theorem d3_comp_d2 :
    (d3 : C3 R A →ₗ[R] C4 R A).comp (d2 : C2 R A →ₗ[R] C3 R A) = 0 := by
  ext G x y z w
  exact differential3_differential2 (fun a b => G a b) x y z w

end CharacteristicTwo

#print axioms d2
#print axioms differential3Linear
#print axioms d3
#print axioms d3_d2
#print axioms d3_comp_d2

end
end ARCHochschildCochainMaps
