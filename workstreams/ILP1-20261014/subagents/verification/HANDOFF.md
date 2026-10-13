# Independent verification checkpoint

Agent: `/root/verification`, branch `partner/ilp1-verification-20261014`.
Exclusive write ownership remains this verification directory. Primary and
theory files are read-only from this worktree; the parent integrates commits.

Last committed checkpoint before this note:
`835b579470b6c2514821eac5d2bb1a7791bdb5da` (causal callback inspection).
The random-offset proof, code, evidence, README update, and this note are being
saved together immediately after that checkpoint. Obtain the actual resulting
commit with `git log -1 --format=%H`; no self-referential hash is asserted here.

## Strongest recent checked results

- Arbitrary-makespan exact prefix-macro optimization for `B=W+1`, with a
  reviewed `O(N min(B,N)(N+E))` implementation; general window excess gives an
  XP written algorithm. `FORCED_MACRO_REVIEW.md` separates proof and evidence.
- Polynomial optimality certificates using bounded integer lower potentials
  and a legal attaining schedule. `macro_certificate.py` regenerates every
  macro itself; 365 positive CSP checks and 33 rejected attacks are saved.
  The root has correctly clarified the theorem's existential quantifier over
  potentials during integration; do not overwrite that parent edit with the
  older phrasing in this branch's initial review file.
- Repeated finite-prefix-lookahead obstructions at `B=4,W=3` give randomized
  lower coefficient `1+1/[2(M+2)]` and deterministic `1+1/(M+2)` for
  `2M>=L`, resisting additive constants. Matching upper bounds are only for
  that promised family. Exactly `q` fixed-length advice bits are required
  to be optimal on all `q`-block bit-vector instances.
- The global deterministic chunk upper `1+9/(L+4)`, together with the repeated
  family, establishes optimal deterministic/randomized competitive excess
  `Theta(1/(L+1))` under the defined incoming-prefix observation model.
- Random-offset chunking improves the global expected upper to
  `1+(B-1)/(B+L)` for every fixed oblivious input. At `B=4,W=3` this is
  `1+3/(L+4)`. For the specified policy the coefficient is exactly sharp when
  `B>=2,W>=2,Q=B+L>=max(B,2B-3)`, using true fan-in/outdegree at most two.
  This sharpness is not a lower bound for the best online policy class.

All these new claims are written proofs with real independent review, not
Lean-verified statements. This subagent has run no Lean compilation and made
no historical novelty claim. The parent handles separate formalization and
literature audits.

## Saved negative controls and caveats

- Merely padding to a width-multiple can change the finite-window optimum.
- Uniform younger omission at `B=4,W=3` has the nine-job ratio `37/27>4/3`.
- Certificate checks confined to a submitted path miss an actual inflated
  `K=3` certificate; the independent checker rejects its omitted two-cycle macro.
- Removing repeated-lookahead barriers permits inter-block overlap, although
  the first tested `M=1,AA` optimum remains six. The mistaken expectation of a
  strict improvement was recorded rather than reported as a result.
- Random-offset chunking can be suboptimal even when `N<=Q`; only the default
  deterministic first chunk `Q` guarantees a single visible chunk is exact.
- The random-offset sharpness family's `B=4,L=0` costs `[4,5,6,5]` average to
  ratio `5/3`, not the generic upper `7/4`. The sufficient threshold matters.

## Reproduction and source provenance

Latest targeted run:

```sh
python random_offset_audit.py --primary-directory ../theory
```

It checks 278 graph/lookahead cases over all 1,672 offsets through the actual
callback wrapper, plus 84 sharpness resource cases over all 624 offsets.
All expectations use exact fractions. See `random_offset_results.json` for
seed, finish time, duration, source hashes, and access/issue counts.

Fixed primary sources:

- `chunk_lookahead.py` SHA-256
  `13b3374f6e9bbe388e5865d93b96f0053861db1b725e1e53e26fad427b2da5ed`.
- `forced_segment_dp.py` SHA-256
  `6798ccdf97277f16731bafb86afcd68fe5623620b8541304c750057b0093a21d`.

Independent theory review commits are
`fa9b97b77d544b9590b5e0a8c7a9cabc8f577c42` (repeated lookahead),
`d343d89826ec463a364aebeeaadcd67476e1ff91` (random offset), and
`a6be8665150497ecc6c0aca0c6149dad478d139f` (strategy sharpness).

## Resume without repeating completed large audits

Read this note, the actual git status, and the parent's latest task message.
No experiment remains running. Review any changed source hash before reusing
its evidence. The strongest unresolved mathematical target after these results
is the leading constant or exact finite-`L` minimax value of the unrestricted
online policy class; this policy's sharpness does not resolve it. Another
independent target is FPT versus XP in window excess alone. Follow the parent's
next priority and preserve all model and observation assumptions above.
