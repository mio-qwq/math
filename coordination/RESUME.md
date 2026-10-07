# Resume checkpoint

Snapshot: 2026-10-08, Asia/Shanghai. Always verify the live Git and filesystem state; later commits take precedence.

## Published and independently checked

- The current verified update constructs actual character modules, proves their simplicity over fields, constructs degreewise finite free/projective candidate bar terms, and proves their full A-linear Hom/word-value equivalence.
- `55e9ad2`: every augmentation-kernel word of length at least six vanishes at every parameter; module-name cache retrieval fixed and tested.
- `51682ab`: actual e/f R-algebra characters and a nonzero full scalar f-character degree-three cochain class whenever q³ is nonzero, independently excluding every scalar bilinear boundary; dependency-ordered replay script.
- `0428ad3`: full twenty-dimensional input closure, nonzero actual algebra-valued degree-three Hochschild cochain class when q³ is nonzero, and generic character-valued differentials.
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
| Primary | `FiniteFreeBarHom.lean`, documentation and verification records | Full actual A-linear Hom/word-value equivalence compiled and independently reviewed; publishing the module milestone |
| Algebra agent | `TwentyDimNilpotenceSharp.lean` | Independent module replays completed; preparing a small fivefold nonzero witness under an explicit parameter condition |
| Audit agent | `FiniteFreeBarAugmentation.lean` | Actual character module and field simplicity completed; preparing augmentation and first-step kernel/image correspondence |
| Discrete agent | `CochainWordEquiv.lean` | Degreewise free/projective terms completed; preparing full scalar multilinear cochain/word-coefficient equivalences |

Completed and independently recompiled in the current update: `TwentyDimFrobenius.lean` (perfect trace duality), `CochainBasisSemantics.lean` (actual polynomial five-term radical-basis closure), `CochainSpecialization.lean`, `CochainCycleSemantics.lean` (universal internal scalar boundary obstruction), `FiniteTrilinear.lean`, `FiniteHochschild.lean`, `TwentyDimCochain.lean` (all radical-span vectors), and `CochainFullBoundary.lean` (arbitrary full vector-valued boundaries).

Subagents resumed after repeated usage/network interruptions. Their work remains on disk. Inspect each agent's current state and source before resuming; do not assume a request alone completed its task. Their first full task briefing included the user's original research prompt.

`CochainIdempotentClosure.lean` and `TwentyDimHochschildClass.lean` establish the actual algebra-valued class. `TwentyDimCharacters.lean`, `CharacterHochschildDegreeThree.lean`, and `TwentyDimCharacterClass.lean` establish the projected class in the full scalar character quotient, using all multilinear cochains and both endpoint faces. Its nonboundary proof handles arbitrary scalar bilinear maps independently. Both conclusions require q³ nonzero; in a ring without zero divisors, q nonzero suffices. `TwentyDimNilpotence.lean` now proves arbitrary kernel words of length at least six vanish; this is not a Jacobson-radical identification or a sharp bound. The Ext comparison and all-degree assertions remain open. New module drafts awaiting compilation must not be described as verified.

`CharacterModule.lean` and `CharacterModuleSimple.lean` construct real module instances and prove actual field simplicity. `FiniteFreeBarModules.lean` and `FiniteFreeBarHom.lean` give actual projective candidate terms and their full Hom parameterization. They still have no chain differential or exactness. A proposed augmentation presentation, multilinear-cochain equivalence and sharpness witness remain drafts until checked. Mathlib caches for SimpleModule.Basic and ModuleCat.Projective are now available; use module names with `lake exe cache get` inside this dependency package.

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
