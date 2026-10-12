import Lake
import Std

open Lake DSL
package rsaScopeAudit

namespace RSAScopeAudit

theorem lift_identity (e N k s d r t u : Int)
    (hroot : 1 + k * (N - s) = e * d)
    (hquot : e * u = r * N + t) :
    k * (r * s + t) - r = e * (u * k - r * d) := by
  grind

theorem small_multiple_zero (e z : Int) (he : 0 < e)
    (hlow : -e < z) (hupp : z < e) (hdiv : e ∣ z) : z = 0 := by
  obtain ⟨a, ha⟩ := hdiv
  by_cases hp : 0 < a
  · have hm := Int.mul_le_mul_of_nonneg_left (show 1 ≤ a by omega) (Int.le_of_lt he)
    grind
  · by_cases hn : a < 0
    · have hm := Int.mul_le_mul_of_nonneg_left (show a ≤ -1 by omega) (Int.le_of_lt he)
      grind
    · have : a = 0 := by omega
      grind

theorem short_lift_recovers (e N k s d r t u X Y T : Int)
    (he : 0 < e) (hk : 0 < k) (hkX : k ≤ X)
    (hr : 0 < r) (hY : 1 ≤ Y) (hslo : -Y ≤ s) (hshi : s ≤ Y)
    (hrY : r * Y ≤ T) (htlo : -T ≤ t) (hthi : t ≤ T)
    (hshort : 3 * X * T < e)
    (hroot : 1 + k * (N - s) = e * d)
    (hquot : e * u = r * N + t) : u * k = r * d := by
  have hrY0 := Int.mul_le_mul_of_nonneg_left hY (Int.le_of_lt hr)
  have hT : 0 ≤ T := by grind
  have hrT : r ≤ T := by grind
  have hrslo := Int.mul_le_mul_of_nonneg_left hslo (Int.le_of_lt hr)
  have hrshi := Int.mul_le_mul_of_nonneg_left hshi (Int.le_of_lt hr)
  have hsumlo : -2*T ≤ r*s+t := by grind
  have hsumhi : r*s+t ≤ 2*T := by grind
  have hklo := Int.mul_le_mul_of_nonneg_left hsumlo (Int.le_of_lt hk)
  have hkhi := Int.mul_le_mul_of_nonneg_left hsumhi (Int.le_of_lt hk)
  have hkXT := Int.mul_le_mul_of_nonneg_right hkX hT
  have hXT := Int.mul_le_mul_of_nonneg_right (show 1 ≤ X by omega) hT
  have hb_lo : -e < k*(r*s+t)-r := by grind
  have hb_hi : k*(r*s+t)-r < e := by grind
  have hid := lift_identity e N k s d r t u hroot hquot
  have hz := small_multiple_zero e (k*(r*s+t)-r) he hb_lo hb_hi
    ⟨u*k-r*d, hid⟩
  have hz' : e * (u*k-r*d) = 0 := hid.symm.trans hz
  have hh := (Int.mul_eq_zero.mp hz').resolve_left (by omega)
  omega

theorem primitive_relation_divides (k d r u : Int)
    (hcop : Int.gcd k d = 1) (hcross : u*k=r*d) : k ∣ r := by
  have hd : k ∣ r*d := ⟨u, by grind⟩
  have hh := (Int.dvd_mul_gcd_iff_dvd_mul (k:=k) (n:=r) (m:=d)).2 hd
  simpa [hcop] using hh

theorem denominator_bound (e k r X Y : Int)
    (hk : 0 < k) (hr : 0 < r) (hX : k ≤ X) (hY : 0 ≤ Y)
    (hdiv : k ∣ r) (hshort : 3*X*r*Y < e) : 3*k*k*Y < e := by
  obtain ⟨a, ha⟩ := hdiv
  have ha_pos : 0 < a := by
    by_cases hp : 0 < a
    · exact hp
    · have hh := Int.mul_le_mul_of_nonneg_left (show a ≤ 0 by omega) (Int.le_of_lt hk)
      grind
  have hh := Int.mul_le_mul_of_nonneg_left (show 1 ≤ a by omega) (Int.le_of_lt hk)
  have hkr : k ≤ r := by grind
  have hx0 : 0 ≤ X := by omega
  have h1 := Int.mul_le_mul_of_nonneg_left hkr hx0
  have h2 := Int.mul_le_mul_of_nonneg_right hX (Int.le_of_lt hk)
  have h3 : k*k ≤ X*r := by grind
  have h4 := Int.mul_le_mul_of_nonneg_right h3 hY
  grind

theorem legendre_integer_bound (e N k s d Y : Int)
    (hk : 0 < k) (hs : 1 ≤ s) (hY : s ≤ Y)
    (hroot : 1+k*(N-s)=e*d) (hbound : 3*k*k*Y<e) :
    0 ≤ N*k-e*d ∧ 2*k*(N*k-e*d)<e := by
  have h1 := Int.mul_le_mul_of_nonneg_left hs (Int.le_of_lt hk)
  have h2 := Int.mul_le_mul_of_nonneg_left hY (Int.le_of_lt hk)
  have hz : 0 ≤ k*Y := by grind
  have h3 := Int.mul_nonneg (Int.le_of_lt hk) hz
  have h4 := Int.mul_le_mul_of_nonneg_left h2 (Int.le_of_lt hk)
  have hid : N*k-e*d=k*s-1 := by grind
  rw [hid]
  constructor
  · grind
  · have hi : 2*k*(k*s-1)=2*(k*(k*s))-2*k := by grind
    have hb : 3*k*k*Y=3*(k*(k*Y)) := by grind
    rw [hi]
    rw [hb] at hbound
    omega

theorem gcd_recovery (k d r u : Int)
    (hk : 0 < k) (hr : 0 < r) (hcop : Int.gcd k d = 1)
    (hcross : u*k=r*d) :
    r / (Int.gcd r u : Int) = k ∧ u / (Int.gcd r u : Int) = d := by
  obtain ⟨a, ha⟩ := primitive_relation_divides k d r u hcop hcross
  have ha_pos : 0 < a := by
    by_cases hp : 0 < a
    · exact hp
    · have hh := Int.mul_le_mul_of_nonneg_left (show a ≤ 0 by omega) (Int.le_of_lt hk)
      grind
  have hz : k*(u-a*d)=0 := by grind
  have hz' := (Int.mul_eq_zero.mp hz).resolve_left (by omega)
  have hu : u=a*d := by omega
  have hr' : r=a*k := by grind
  have hg : Int.gcd r u = a.natAbs := by
    rw [hr', hu, Int.gcd_mul_left, hcop, Nat.mul_one]
  have habs : (a.natAbs : Int) = a := Int.natAbs_of_nonneg (by omega)
  rw [hg, habs, hr', hu]
  constructor
  · exact Int.mul_ediv_cancel_left k (by omega)
  · exact Int.mul_ediv_cancel_left d (by omega)

theorem short_relation_scope (e N k s d r t u X Y T : Int)
    (he : 0 < e) (hk : 0 < k) (hkX : k ≤ X)
    (hr : 0 < r) (hs : 1 ≤ s) (hshi : s ≤ Y)
    (hrY : r*Y ≤ T) (htlo : -T ≤ t) (hthi : t ≤ T)
    (hshort : 3*X*T < e) (hcop : Int.gcd k d = 1)
    (hroot : 1+k*(N-s)=e*d) (hquot : e*u=r*N+t) :
    r / (Int.gcd r u : Int) = k ∧ u / (Int.gcd r u : Int) = d ∧
    3*k*k*Y < e ∧ 0 ≤ N*k-e*d ∧ 2*k*(N*k-e*d) < e := by
  have hcross := short_lift_recovers e N k s d r t u X Y T he hk hkX hr
    (by omega) (by omega) hshi hrY htlo hthi hshort hroot hquot
  have hrecover := gcd_recovery k d r u hk hr hcop hcross
  have hdiv := primitive_relation_divides k d r u hcop hcross
  have hx : 0 ≤ 3*X := by omega
  have hmul := Int.mul_le_mul_of_nonneg_left hrY hx
  have hs' : 3*X*r*Y<e := by grind
  have hb := denominator_bound e k r X Y hk hr hkX (by omega) hdiv hs'
  have hl := legendre_integer_bound e N k s d Y hk hs hshi hroot hb
  exact ⟨hrecover.1, hrecover.2, hb, hl⟩

#print axioms lift_identity
#print axioms small_multiple_zero
#print axioms short_lift_recovers
#print axioms primitive_relation_divides
#print axioms denominator_bound
#print axioms legendre_integer_bound
#print axioms gcd_recovery
#print axioms short_relation_scope

end RSAScopeAudit
