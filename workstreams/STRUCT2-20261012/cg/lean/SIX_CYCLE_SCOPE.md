# Universal six-cycle type invariant

`SixCycleInvariant.lean` proves a structural invariant of the actual CG
canonical double cover. It imports the previously compiled original
definition/model isomorphism and connected graph semantics; there are no
assumed automorphism lists, type-preservation premises or catalogue inputs.

## Exact proved scope

- In the coordinate model, no Z vertex lies on a simple six-cycle for
  **every n>=2**, including even coordinate parameters. The proof reduces
  an alleged cycle to two ring steps between distinct indices with equal
  centre residue. Residue commutes with cyclic successor, and two steps
  cannot fix a point of the centre cycle of length 2n>=4.
- Every X, Y and A vertex has an explicitly proved simple six-cycle.
  `has_six_cycle_iff_not_centre` therefore characterizes the centres by
  absence of six-cycles. All six vertices are pairwise distinct and all
  six defining adjacencies are checked symbolically.
- Arbitrary actual graph automorphisms preserve this property. Injectivity
  transports the no-repeated-vertex condition, and the actual adjacency
  equivalence transports the edges. This proves centre preservation.
- A vertex is a leaf exactly when it is adjacent to a centre. The remaining
  vertices are the ring vertices. Thus arbitrary automorphisms preserve
  **all three vertex types**, without assuming that preservation.
- `actualCDC_six_cycle_characterization` transfers the invariant to the
  **literal original CG canonical double cover at every odd n>=3**, using
  the proved forward/inverse maps and original adjacency, with original
  centres identified by their source constructor.
- `n_one_centre_exception` is a checked explicit six-cycle through a centre
  when n=1. This exception is retained; no all-odd group statement is
  extended to n=1.

The new invariant does not require classification of all six-cycles.
In particular, the Lean module does not yet assert that the displayed
cycles exhaust all six-cycles, or prove the full group order or cousin count.

## Actual verification

```
python verify_odd_cover.py --include-six-cycles --lean /path/to/lean-4.34.1-linux/bin/lean --build-dir /tmp/struct2-six-cycle-olean --output-dir /tmp/struct2-six-cycle-receipt
python check_six_cycle_invariant.py --max-n 101 --output /tmp/struct2-six-cycle-checks.json
```

The five-module dependency chain was rebuilt sequentially with Lean 4.34.1:
**71 axiom audits**, including 21 in the new module, no errors or warnings.
Only the standard propext, Classical.choice and Quot.sound axioms occur.
No sorry, custom axioms, native_decide or finite graph catalogue is used.
Exact sources, compiler, driver and output hashes are recorded under
`../../verification/20261013-cg-six-cycles/`.

The supplementary Python program imports only the frozen literal
`source_graph` and `cdc` constructors. Its unrestricted depth-six searches
check all vertices for 51 odd parameters through n=101. It confirms the
n=1 exception and rejects an isolated damaged ring vertex. The observed
count of two incident six-cycles at each noncentre for these finite orders
is recorded as a finite observation, not as the universal Lean theorem.
These are independently implemented computational checks, not independent
human review of the new formalization.

## Next proof gap

Restrict an arbitrary actual automorphism to the two ring components,
prove that the two ring actions agree through their matched leaves, and
derive the dihedral action together with the optional ring interchange.
The exhaustive strong-switch classes, conjugacy and exactly-two TF-cousin
conclusion remain written/previously reviewed but not fully formalized.
