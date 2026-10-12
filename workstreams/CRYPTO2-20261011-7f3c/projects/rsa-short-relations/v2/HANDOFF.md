# RSA v2 handoff

Read NOVELTY.md and PROOF.md. Eight Lean declarations actually checked,
including exact gcd recovery and the integer Legendre inequality.
The full arbitrary-degree polynomial proof is not formalized.
Attack significance is downgraded; no independent RSA review is claimed.

Reproduce with Python standard library and official Lean 4.34.1:
```sh
python workstreams/CRYPTO2-20261011-7f3c/projects/rsa-short-relations/v2/check.py --lean-root /path/to/lean-4.34.1-linux --output /tmp/rsa-v2-runs.json
```
RUNS.json records the successful exit-0 run, source hash, versions,
individual Lake exits and axiom output. Public-only continued fractions
recover the test key in degree-3 and degree-12 fixtures. These share one
public key: ONE distinct key, not two independent attack successes.
Three mathematical negative controls and a rejected false Lean theorem
are included. No floating-point result certifies a theorem.

Official release:
https://github.com/leanprover/lean4/releases/download/v4.34.1/lean-4.34.1-linux.tar.zst
The direct lean CLI in this environment returned "failed to locate
application" resolving its executable path. The supported Lake config
elaborator works with explicit LEAN_SYSROOT and LAKE_HOME. The actual
entry is "lake --reconfigure env true", elaborating and checking
lakefile.lean in process; it is not reported as "lake build".
The script uses fresh temporary directories to prevent stale config reuse.
No kernel modification or extra axioms. Only propext, Classical.choice,
Quot.sound occur. No sorry, admit or native_decide. Dependencies: Lake
and Std only. A separate mathlib cache bootstrap failed through the
direct CLI and is neither a dependency nor verification evidence.

Do not resume synthetic t=0 witness growth. Further RSA work needs a
different mechanism escaping this classical-scope obstruction.
