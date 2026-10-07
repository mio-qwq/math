# Resume checkpoint

Snapshot: 2026-10-08, Asia/Shanghai. Always verify the live Git and filesystem state; later commits take precedence.

## Published and independently checked

- `6e326b3`: actual trilinear cochain and non-boundary statement on the installed algebra, plus surjective augmentation and kernel/span identification.
- `3a7515c`: perfect trace duality; actual polynomial/specialized cochain identities; all-vector closure on the eighteen-label span; full vector-valued boundary obstruction with nonzero q³; algebra replay script passed.
- `e0d3d68`: actual low-degree differential composite is zero, with bilinear-to-trilinear packaging.
- `aed7ae5`: actual unital `Ring` and `Algebra R`, explicit 20-element basis, finite/free module instances and field dimension 20; invariant trace and cyclic triple products.
- `77698ad`: concrete two-sided unit, symmetric left/right nondegenerate trace, and generic bilinear laws.
- `5af6c3f`: actual all-vector multiplication associativity over F₂ polynomials and every commutative characteristic-two specialization.
- Earlier notes 001 and 002 have their own written proofs and supporting Lean developments. Consult `FORMALIZATION.md` for exact scope.

The complete ARC homological realization is still open. Source attribution remains pinned to the original OpenAI commit recorded in each note.

## In progress and ownership

All source paths below are under `003-arc-one-parameter/proof/mathlib/`.

| Owner | File/task | State at checkpoint |
| --- | --- | --- |
| Primary | `HochschildDegreeThree.lean`, documentation and integration | Final quotient compiled successfully after supplying standard nested additive-group instances; application to the fixed cochain awaits all-input closure |
| Algebra agent | `CochainIdempotentClosure.lean` | Extending closure to basis inputs containing e/f, preferably through corner compatibility rather than another full enumeration |
| Audit agent | Independent review | Characteristic, actual cochain maps and generic quotient scope reviewed; assessing the f-simple/Ext bridge |
| Discrete agent | Independent quotient replay | `HochschildCochainMaps.lean` completed and checked; replaying the final `HochschildDegreeThree.lean` |

Completed and independently recompiled in the current update: `TwentyDimFrobenius.lean` (perfect trace duality), `CochainBasisSemantics.lean` (actual polynomial five-term radical-basis closure), `CochainSpecialization.lean`, `CochainCycleSemantics.lean` (universal internal scalar boundary obstruction), `FiniteTrilinear.lean`, `FiniteHochschild.lean`, `TwentyDimCochain.lean` (all radical-span vectors), and `CochainFullBoundary.lean` (arbitrary full vector-valued boundaries).

Subagents resumed after repeated usage/network interruptions. Their work remains on disk. Inspect each agent's current state and source before resuming; do not assume a request alone completed its task. Their first full task briefing included the user's original research prompt.

The current update adds `TwentyDimCharacteristic.lean`, `HochschildCochainMaps.lean`, `LowDegreeCohomology.lean`, and `HochschildDegreeThree.lean`, all compiled with standard axiom audits. The quotient uses the full multilinear cochain modules and full four/five-face differentials. No nonzero class for the fixed cochain is claimed until `CochainIdempotentClosure.lean` proves its differential vanishes on all inputs.

## Recovery sequence

1. Read this checkpoint and `ROADMAP.md`; run `git status --short`, `git log -6 --oneline`, `git fetch origin`, and `git branch -r`. Review new remote commits before integration.
2. Inspect incomplete source files and ask live subagents for their exact state. Reuse their work. If their runtime is gone or still limited, take over only after recording the ownership change.
3. Replay newly completed files in dependency order, inspect their statements and `#print axioms`, write source hashes and accurate scope, then commit only reviewed paths and push without force.
4. Update this checkpoint and `coordination/agents/primary.md`. Give the user a concise stage summary and continue with the next tractable proof gap.

PowerShell setup for an individual semantic file:

```powershell
Set-Location 'C:\Users\Administrator\Desktop\math\research\003-arc-one-parameter\proof\mathlib'
$env:PATH = 'C:\Users\Administrator\.elan\bin;' + $env:PATH
$env:LEAN_PATH = (Get-Location).Path + ';' + (Resolve-Path '..').Path
lake env lean Filename.lean
# Add -o Filename.olean when a later local module imports it.
```

The pinned package is Lean 4.34.1 and Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`. The ignored `.olean` files and local `.lake` dependencies are caches, not source deliverables. A full algebra semantic replay is supplied by `verify-semantics.ps1`; the separate larger Std closure replay is `../verify.ps1`.

The user requested interruption recovery and periodic stage summaries. A 30-minute heartbeat named “Lean 研究阶段总结与规划” is configured in the current chat. Its existence does not guarantee execution while the app, machine or account is unavailable; the repository checkpoint is the durable recovery source.
