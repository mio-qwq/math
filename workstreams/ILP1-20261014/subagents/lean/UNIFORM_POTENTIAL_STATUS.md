# Conditional randomized-potential formalization checkpoint

Base local commit: `2f4196ee4ec7cb0f16b4c6433b2fe2faf9e7e384`.
`git fetch origin` completed before this increment. No old source or evidence
file is changed.

The theory subagent supplied the complete written proof at commit
`9199c455925b65cfd609955ded7d39279b6d6011`; the Lean subagent read it and
confirmed the local interface directly with the proof's author. The author
specifically confirmed that the good-successor alternative in the length-four,
equal-tail branch requires at least six remaining instructions. This guard is
included in the formal constructor.

New module: `formal/UniformYoungerPotential.lean`.
The actual finite strong induction proves potential nonnegativity and the
nonempty adjacent-equality invariant from nine exact local potential cases.
The target inequalities are not among the hypotheses. The module also proves
all five minimum/mean potential identities and the general forced-macro
identity using integer scaling.

Ten declarations actually compile on Lean 4.34.1; each audit contains only
`propext` and `Quot.sound`. The fresh receipt and exact source hash are in
`evidence/uniform-younger-potential/`.

**Coverage limit:** actual ROB executions have not been connected to
`MacroShape` in Lean. The complete randomized 5/4 theorem must therefore
remain labeled a written theorem with a conditional Lean induction kernel,
not a fully Lean-verified online result. A detailed interface table and all
missing bridges are in `formal/UNIFORM_YOUNGER_POTENTIAL.md`.

Next formal target: encode the scalar recurrence from the actual gap-one /
gap-two dependency bits and prove the three structural successor identities;
then relate the scalar expectation to a finite probability model of the
uniform-younger policy.
