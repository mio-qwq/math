# Independent polynomial optimality certificates for B=W+1

Status: WRITTEN_PROOF, INDEPENDENTLY_REVIEWED, and actually tested independent
checker. No Lean verification or originality claim is made. The argument uses
the precise eager, unit-latency ROB model and the non-delay/macro reduction
independently reviewed in `FORCED_MACRO_REVIEW.md`.

## Certificate and theorem

Fix a forward-DAG instance with `N>=0`, positive `W`, and `B=W+1`. A certificate
contains an integer `K`, one integer lower potential `f_i` for each clear
prefix `i=0,...,N`, and an explicit schedule of exactly `K` cycles. For a compact
encoding impose `0<=f_i<=N-i`. The checker requires:

1. The schedule passes direct operational ROB replay and executes all jobs.
2. `f_N=0` and `f_0=K`.
3. For every non-delay first action at every clear prefix `i`, independently
   simulate the unique nonclear continuation until its first later clear
   prefix `j`, with duration `ell`, and check `f_i<=ell+f_j`.

A supplied legal `K`-cycle schedule is globally optimal if and only if there
exist bounded potentials for which all checks accept. Every accepted concrete
certificate is sound. In particular, acceptance rules out every legal schedule
of at most `K-1` cycles. This existential statement does not say that arbitrary
potentials supplied with an optimal schedule must pass the checks.

**Soundness.** Every complete non-delay schedule decomposes into a path of the
regenerated macros. Adding the checked inequalities along that path telescopes:

\[
K=f_0\le\sum_{\text{path}}\ell+f_N=\text{path duration}.
\]

There exists a globally optimal non-delay schedule, so its duration `T*` is at
least `K`. Direct replay of the attaining schedule gives `T*<=K`. Consequently
`T*=K`, including the empty-program case.

**Completeness.** For an optimal schedule of duration `K`, choose `f_i` equal
to the exact remaining optimum from clear prefix `i`. The exact macro recurrence
implies every inequality, and `f_N=0`, `f_0=K`. Sequential execution of the
remaining jobs gives `0<=f_i<=N-i`. Thus an optimal schedule always has a
certificate of the prescribed form.

This checker does not demand equality at a selected outgoing macro, nor does it
demand that every tail potential equal its true optimum. Smaller feasible tail
potentials are allowed. For example, three independent jobs at `B=3,W=2` admit
the valid potential vector `[2,0,1,0]`; the true remaining optimum at prefix one
is one. The checker accepts that vector with an attaining two-cycle schedule.

## What is enumerated and certificate size

The checker regenerates the entire polynomial macro graph. It does not receive
or trust a submitted macro list, selected action whitelist, or claimed graph
coverage. There are `N+1` prefix nodes and at most `N min(B,N)` macro arcs.
This avoids full completed-state enumeration, but it does **not** avoid macro
graph traversal.

The certificate has `N+1` bounded potentials, exactly `N` issued job indices,
at most `N` action lists, and a canonical copy of the instance edges/resources.
It therefore uses `O(N+E)` integer words. More precisely, with the explicit edge
list and binary resource fields its bit length is
`O((N+E) log(N+1) + log(B+W) + 1)`; it is not generally linear in bits.
The macro traces and inequalities are regenerated and are absent from the
certificate. Omitting the instance copy when an external instance is already
bound would reduce the certificate's graph-dependent storage, but is not
required here.

The independent set-based checker conservatively takes
`O(N^2 min(B,N)(N+E))` time for regeneration, plus graph canonicalization.
This follows from at most `N` cycles per macro and at most `O(N+E)` work for
each direct ready scan. Its runtime is polynomial even when `W` is an input.
The faster counter-based macro implementation could improve this bound, but
the present checker does not import or invoke that optimizer.

## Checker API and binding

`macro_certificate.py` exposes:

```python
check_certificate(n, edges, window, width, certificate)
```

The external graph and resources are authoritative; the certificate's copy
must match them. The schema is `ilp1-c1-prefix-lower-v1`. The checker validates
the exact field set, integral bounds and graph representation, performs direct
ROB schedule replay, and then regenerates every macro independently. For an
inequality failure it returns the actual prefix, first action, endpoint, cost,
and the failed comparison. An accepted result includes the number of macro
inequalities actually checked.

The checker uses only its own set-based macro simulation and the independent
direct ROB replay from `constraint_solver.py`. It contains no optimization
call and no import from the theory or primary solver. `certificate_audit.py`
constructs positive examples using the independent prefix optimizer, and then
compares their claimed values with the separate time-variable CSP.

`c1_certificate_example.json` is a concrete three-cycle certificate for the
nine-job instance with edges `1->4,2->4,2->5,5->8`, at `B=4,W=3`. This is the
same instance on which the uniform-younger online policy has expectation
`37/9`; the certificate concerns its offline optimum, not that online policy.

## Actual adversarial and positive tests

Run from this directory:

```sh
python certificate_audit.py
```

The saved run contains 365 positive certificates and 2,198 regenerated macro
inequalities. The positive range comprises every forward DAG on `0<=N<=4`
at widths `1,...,4` (304 cases), 60 fresh binary-input random programs with
`5<=N<=15`, `1<=W<=8`, seed `2026101411`, and the nine-job example. Every
accepted claimed optimum also agrees with the independent time-variable CSP.
The valid non-exact-tail potential vector above was checked separately.

All 33 adversarial cases were rejected. They cover initial, intermediate,
negative, oversized, nonintegral, missing, and nonzero-terminal potentials;
graph and resource mismatch; an out-of-domain `B`; wrong schema and additional
macro whitelist; wrong schedule length; missing or repeated jobs; same-cycle
dependence; over-width and unadmitted issue; malformed types; and an invalid
external backward edge. Exact rejection reasons are saved in
`certificate_results.json`.

The targeted omitted-macro negative control is mathematical, not merely a
schema error. Take `N=4,B=3,W=2` and true edge `1->3`. The schedule
`{0,2},{1},{3}` is a legal three-cycle trace. Potentials `[3,2,1,1,0]` satisfy
the initial macro inequality along its selected first action `{0,2}`, since
that macro costs two cycles and ends at prefix three. A checker restricted to
the submitted choice would miss the error. The actual checker generates the
alternative first action `{0,1}`: its one-cycle macro ends at prefix two,
and the inequality would require `3<=1+1`. It rejects the certificate and
reports that concrete violated macro.

The actual run took 0.044073764998756815 seconds. Exact finish time, source
hashes, tested ranges, all negative outcomes, and the valid relaxed potential
example are preserved in `certificate_results.json`. These are finite checker
tests; the arbitrary-size certificate theorem is the telescoping proof above.
