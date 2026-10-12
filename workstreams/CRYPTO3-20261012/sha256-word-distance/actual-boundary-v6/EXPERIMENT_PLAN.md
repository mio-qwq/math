# Pre-experiment frozen plan: support-12 actual-word inverse boundary

Status before calculation: no result of the experiment below has been
computed. This plan is fixed before the first experiment execution.

Target: the actual-word nonlinear content of the missing prefix
`d_-1 = d15-G13 = -(G13+G29)` for support 12, where original equations
give `d13=d29`. All 48 original additive recurrences remain necessary;
the previous linear-module countermodel is not a real-word object.

First derive readable original-row conditions. In particular put
`a=d11=d18=d34`, `b=d26=d42`, `c=d13=d29`. Original rows imply
`F26=-a`, `F18=-b`, `F13+F29+G26+G42=0`.

**One bounded finite experiment.** Ask whether `b` can be a signed power
of two using only the first two actual-pair relations. For each
`k=0,...,31`, and each pair of endpoints `u,v=k,...,31`, use the exact
consecutive-run masks created by a signed-power increment. If the pair
at 26 has input XOR mask `I(k,u)`, then
`v2(a)=v2(sigma0(I(k,u)))`. If the pair at 18 has output difference
`-b`, its output XOR mask is `I(k,v)`, hence
`v2(a)=v2(sigma0^{-1}(I(k,v)))`. Screen the necessary equality of these
two valuations.

Budget: exactly sum_(k=0)^31 (32-k)^2 = **11,440** endpoint comparisons;
at most 528 evaluations in each direction; the 32 inverse-basis constants
are checked against original sigma0 bit equations. No SMT/SAT, unknown
query replay, seed sweep, timeout extension, or full-schedule search.
The experiment stops after this finite cover. Surviving endpoints are
necessary-mask candidates only, never real-pair solutions. Empty strata
give exact exclusions of the specified signed-power parameter stratum,
not an entire support or an improved global distance bound.

A separate analytic fixture may illustrate why the conservation equation
alone cannot imply `G13+G29=0`: actual word pairs may be built by applying
complement-and-reverse to a pair whose sigma0 XOR mask has only bits
29..31. Every supplied word is checked directly; such a fixture must be
explicitly separated from all thirteen active pairs and from complete
input blocks. If it fails another original-row condition, record that
failure mechanism precisely and stop that construction family.

Final scope: accept a rigorous new necessary reduction or bounded family
exclusion; leave the actual reverse shift unresolved unless every full
original recurrence and coupled real-word/base condition is closed.
