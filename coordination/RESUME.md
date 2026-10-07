# Resume checkpoint

Snapshot: 2026-10-08, Asia/Shanghai. Always verify the live Git and filesystem state; later commits take precedence.

## Published and independently checked

- The current verified update constructs a nonzero class of the actual cochain in the full degree-three Hochschild cochain quotient whenever q³ is nonzero, after proving closure on all twenty-dimensional inputs. It also supplies generic character-valued degree-two/three differentials.
- `2abdb2d`: actual characteristic-two instance, full linear Hochschild differentials, and the actual degree-three cycles-modulo-boundaries quotient.
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
| Primary | `TwentyDimHochschildClass.lean`, documentation and integration | Actual full-input closure and nonzero quotient class compiled; publishing the independently reviewed milestone |
| Algebra agent | Independent replay | Full-input closure completed; reviewing and replaying character maps and the actual nonzero class |
| Audit agent | `CharacterHochschildDegreeThree.lean` | Generic character cochain quotient draft awaiting serial compilation; full character maps completed |
| Discrete agent | `TwentyDimCharacters.lean`, then scalar boundary bridge | Actual e/f R-algebra characters and projected scalar cochain draft awaiting serial compilation |

Completed and independently recompiled in the current update: `TwentyDimFrobenius.lean` (perfect trace duality), `CochainBasisSemantics.lean` (actual polynomial five-term radical-basis closure), `CochainSpecialization.lean`, `CochainCycleSemantics.lean` (universal internal scalar boundary obstruction), `FiniteTrilinear.lean`, `FiniteHochschild.lean`, `TwentyDimCochain.lean` (all radical-span vectors), and `CochainFullBoundary.lean` (arbitrary full vector-valued boundaries).

Subagents resumed after repeated usage/network interruptions. Their work remains on disk. Inspect each agent's current state and source before resuming; do not assume a request alone completed its task. Their first full task briefing included the user's original research prompt.

`CochainIdempotentClosure.lean` and `TwentyDimHochschildClass.lean` now close that gap: the fixed cochain is closed on all inputs, and its class is nonzero in the full multilinear degree-three quotient when q³ is nonzero. In a ring without zero divisors, q nonzero suffices. `CharacterHochschildMaps.lean` supplies the corresponding full character-valued differential maps. Character-specific scalar non-boundary, its quotient application, the Ext comparison and all-degree assertions are subsequent work. Drafts awaiting compilation must not be described as verified.

Compile large Lean files one at a time on this Windows host. Simultaneous heavy elaboration previously caused transient pagefile/import failures; sequential retries passed. Do not change system settings or repeat large frozen certificates to diagnose those transient errors.

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
