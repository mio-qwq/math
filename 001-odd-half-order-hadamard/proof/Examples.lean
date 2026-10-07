import Std

/-!
Kernel-checked finite exponent certificates for the examples in paper.md.
These certify cyclic difference counts and the Fourier-four phase invariant.
They do not yet construct complex matrices or prove the general rigidity theorem.
No `native_decide`, new axioms, or `sorry` are used.
-/

namespace OddHalfOrder.Examples

def cubicRows : List (List Nat) :=
  [[0, 0, 0, 0, 0, 0],
   [0, 0, 1, 2, 2, 1],
   [0, 1, 0, 1, 2, 2],
   [0, 2, 1, 0, 1, 2],
   [0, 2, 2, 1, 0, 1],
   [0, 1, 2, 2, 1, 0]]

def cubic (row column : Nat) : Nat :=
  (cubicRows.getD row []).getD column 0

def residueDifference (modulus x y : Nat) : Nat :=
  (x + modulus - y % modulus) % modulus

def differenceCount (size modulus : Nat) (matrix : Nat → Nat → Nat)
    (first second residue : Nat) : Nat :=
  ((List.range size).filter fun column =>
    residueDifference modulus (matrix first column) (matrix second column) == residue).length

def UniformRowDifferences (size modulus multiplicity : Nat)
    (matrix : Nat → Nat → Nat) : Prop :=
  ∀ first second : Fin size, first ≠ second →
    ∀ residue : Fin modulus,
      differenceCount size modulus matrix first.val second.val residue.val = multiplicity

theorem cubic_entries_are_residues :
    ∀ row column : Fin 6, cubic row.val column.val < 3 := by decide

theorem cubic_is_dephased :
    ∀ index : Fin 6, cubic 0 index.val = 0 ∧ cubic index.val 0 = 0 := by decide

/-- Every cubic row difference contains each residue exactly twice. -/
theorem cubic_uniform_rows : UniformRowDifferences 6 3 2 cubic := by
  unfold UniformRowDifferences
  decide

/-- The same statement is independently checked for column differences. -/
theorem cubic_uniform_columns :
    UniformRowDifferences 6 3 2 (fun row column => cubic column row) := by
  unfold UniformRowDifferences
  decide

theorem cubic_square_uniform_rows :
    UniformRowDifferences 6 3 2 (fun row column => 2 * cubic row column % 3) := by
  unfold UniformRowDifferences
  decide

theorem cubic_square_uniform_columns :
    UniformRowDifferences 6 3 2 (fun row column => 2 * cubic column row % 3) := by
  unfold UniformRowDifferences
  decide

def fourierFour (row column : Nat) : Nat := row * column % 4

/-- F4 row sums cancel opposite roots; not every difference is a permutation. -/
theorem fourier_four_opposite_root_counts :
    ∀ first second : Fin 4, first ≠ second →
      differenceCount 4 4 fourierFour first.val second.val 0 =
        differenceCount 4 4 fourierFour first.val second.val 2 ∧
      differenceCount 4 4 fourierFour first.val second.val 1 =
        differenceCount 4 4 fourierFour first.val second.val 3 := by decide

theorem fourier_four_is_dephased :
    ∀ index : Fin 4, fourierFour 0 index.val = 0 ∧ fourierFour index.val 0 = 0 := by decide

def rectangularResidue (modulus : Nat) (matrix : Nat → Nat → Nat)
    (row column baseRow baseColumn : Nat) : Nat :=
  residueDifference modulus
    (matrix row column + matrix baseRow baseColumn)
    (matrix row baseColumn + matrix baseRow column)

/-- The rectangular root-of-unity phase on rows and columns zero, one is i. -/
theorem fourier_four_rectangular_residue :
    rectangularResidue 4 fourierFour 1 1 0 0 = 1 := by decide

theorem fourier_four_rectangular_residue_not_binary :
    rectangularResidue 4 fourierFour 1 1 0 0 % 2 ≠ 0 := by decide

def phaseShift (matrix : Nat → Nat → Nat) (rows columns : Nat → Nat)
    (row column : Nat) : Nat :=
  (matrix row column + rows row + columns column) % 4

/-- Arbitrary fourth-root row and column phases preserve the rectangle. -/
theorem fourier_four_phase_invariant (rows columns : Nat → Nat) :
    rectangularResidue 4 (phaseShift fourierFour rows columns) 1 1 0 0 = 1 := by
  simp [rectangularResidue, residueDifference, phaseShift, fourierFour]
  omega

theorem fourier_four_no_binary_phase_shift (rows columns : Nat → Nat) :
    ¬ (∀ row column : Fin 4,
      phaseShift fourierFour rows columns row.val column.val % 2 = 0) := by
  intro h
  have h00 := h ⟨0, by decide⟩ ⟨0, by decide⟩
  have h01 := h ⟨0, by decide⟩ ⟨1, by decide⟩
  have h10 := h ⟨1, by decide⟩ ⟨0, by decide⟩
  have h11 := h ⟨1, by decide⟩ ⟨1, by decide⟩
  have hinvariant := fourier_four_phase_invariant rows columns
  simp [rectangularResidue, residueDifference, phaseShift, fourierFour] at *
  omega

#print axioms cubic_entries_are_residues
#print axioms cubic_is_dephased
#print axioms cubic_uniform_rows
#print axioms cubic_uniform_columns
#print axioms cubic_square_uniform_rows
#print axioms cubic_square_uniform_columns
#print axioms fourier_four_opposite_root_counts
#print axioms fourier_four_is_dephased
#print axioms fourier_four_rectangular_residue
#print axioms fourier_four_rectangular_residue_not_binary
#print axioms fourier_four_phase_invariant
#print axioms fourier_four_no_binary_phase_shift

end OddHalfOrder.Examples
