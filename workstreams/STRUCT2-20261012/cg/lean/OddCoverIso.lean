import StrongFold
import OddCoordinates

/-!
The original CG canonical double cover and its synchronized model are
isomorphic for every odd n. The source naming, adjacency and deck map
are proved in OddCoordinates; no isomorphism premise is assumed.
This is not the all-odd full automorphism or cousin-count classification.
-/

set_option Elab.async false

namespace Struct2.OddCoverIso

open OddCoordinates

def originalCDCModelIso (n : Nat) (hn : n % 2 = 1) :
    StrongFold.GraphIso (coordinateAdj n) (coverAdj n) where
  forward := toCover n
  backward := fromCover n
  left_inv := fromCover_toCover n hn
  right_inv := toCover_fromCover n hn
  preserves := toCover_adjacency n hn

theorem originalCDC_deck_intertwining (n : Nat) (hn : n % 2 = 1) (x : Coord n) :
    (originalCDCModelIso n hn).forward (coordinateDeck n x) =
      deck n ((originalCDCModelIso n hn).forward x) :=
  coordinateDeck_intertwines n hn x

#print axioms originalCDCModelIso
#print axioms originalCDC_deck_intertwining

end Struct2.OddCoverIso
