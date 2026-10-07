import Mathlib.Algebra.Algebra.Hom
import Mathlib.Algebra.Module.TransferInstance
import Mathlib.Algebra.Module.RingHom

/-!
An actual left module defined by an R-algebra character eps : A →ₐ[R] R.
The distinct wrapper keeps all new action instances on this module; it
does not install a global A-action on the underlying coefficient ring R.
The usual R-scalar action and the character A-action are compatible.
This file makes no simplicity, projective-resolution, or Ext claim.
-/

namespace ARCCharacterModule

variable {R A : Type*} [CommRing R] [Ring A] [Algebra R A]

/-- A distinct carrier for the left character module. -/
@[ext] structure CharacterModule (eps : A →ₐ[R] R) where
  val : R

variable (eps : A →ₐ[R] R)

/-- The wrapper has exactly the elements of the coefficient ring. -/
def valueEquiv : CharacterModule eps ≃ R where
  toFun := CharacterModule.val
  invFun := CharacterModule.mk
  left_inv x := by cases x; rfl
  right_inv r := rfl

instance characterAddCommGroup : AddCommGroup (CharacterModule eps) :=
  (valueEquiv eps).addCommGroup

instance characterNontrivial [Nontrivial R] : Nontrivial (CharacterModule eps) :=
  ⟨⟨CharacterModule.mk 0, CharacterModule.mk 1, fun h =>
    zero_ne_one (congrArg CharacterModule.val h)⟩⟩

/-- The transferred addition is the coefficient-ring addition. -/
def valueAddEquiv : CharacterModule eps ≃+ R where
  toEquiv := valueEquiv eps
  map_add' _ _ := rfl

/-- Restrict the scalar action through the actual character. -/
instance leftCharacterModule : Module A (CharacterModule eps) := by
  letI := (valueAddEquiv eps).module R
  exact Module.compHom (CharacterModule eps) eps.toRingHom

/-- Restrict the installed A-action along the algebra map. The character's
scalar compatibility proves below that this is the ordinary R-action.
This also keeps the two actions compatible when A and R coincide. -/
instance coefficientModule : Module R (CharacterModule eps) :=
  Module.compHom (CharacterModule eps) (algebraMap R A)

@[simp] theorem val_zero : (0 : CharacterModule eps).val = 0 := rfl

@[simp] theorem val_add (x y : CharacterModule eps) :
    (x + y).val = x.val + y.val := rfl

@[simp] theorem val_neg (x : CharacterModule eps) : (-x).val = -x.val := rfl

@[simp] theorem val_coefficient_smul (r : R) (x : CharacterModule eps) :
    (r • x).val = r * x.val := by
  change eps (algebraMap R A r) * x.val = r * x.val
  rw [eps.commutes]
  rfl

/-- The actual A-action is precisely multiplication by eps(a). -/
@[simp] theorem val_character_smul (a : A) (x : CharacterModule eps) :
    (a • x).val = eps a * x.val := rfl

/-- The value equivalence is linear for the retained R-scalar structure. -/
def valueLinearEquiv : CharacterModule eps ≃ₗ[R] R :=
  { valueAddEquiv eps with
    map_smul' := fun r x => val_coefficient_smul eps r x }

@[simp] theorem valueLinearEquiv_apply (x : CharacterModule eps) :
    valueLinearEquiv eps x = x.val := rfl

@[simp] theorem valueLinearEquiv_symm_apply (r : R) :
    (valueLinearEquiv eps).symm r = CharacterModule.mk r := rfl

/-- The same value map records A-linearity as semilinearity through eps. -/
def valueSemilinearMap : CharacterModule eps →ₛₗ[eps.toRingHom] R where
  toFun := CharacterModule.val
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

theorem valueSemilinearMap_bijective : Function.Bijective (valueSemilinearMap eps) :=
  (valueEquiv eps).bijective

instance characterScalarTower : IsScalarTower R A (CharacterModule eps) where
  smul_assoc r a x := by
    apply CharacterModule.ext
    simp only [val_character_smul, val_coefficient_smul]
    simp only [map_smul, smul_eq_mul, mul_assoc]

instance characterSmulComm : SMulCommClass R A (CharacterModule eps) where
  smul_comm r a x := by
    apply CharacterModule.ext
    simp only [val_character_smul, val_coefficient_smul]
    exact mul_left_comm r (eps a) x.val

/-- Scalar elements of A act by their original coefficient values. -/
theorem algebraMap_smul (r : R) (x : CharacterModule eps) :
    (algebraMap R A r) • x = r • x := by
  apply CharacterModule.ext
  simp only [val_character_smul, val_coefficient_smul]
  rw [eps.commutes]
  rfl

/-- Every coefficient occurs as a value of the actual character. -/
theorem character_surjective : Function.Surjective eps := by
  intro r
  refine ⟨algebraMap R A r, ?_⟩
  simp

#print axioms leftCharacterModule
#print axioms valueLinearEquiv
#print axioms valueSemilinearMap
#print axioms characterScalarTower
#print axioms characterSmulComm
#print axioms algebraMap_smul
#print axioms character_surjective

end ARCCharacterModule
