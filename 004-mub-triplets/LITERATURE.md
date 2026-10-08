# Six-dimensional MUB questions: source and overlap review

Review date: 8 October 2026. A source's proof claim, available proof
artifacts and an independently verified conclusion are distinct evidence.
This review does not certify historical priority or global resolution.

## Precisely stated public questions

[Matolcsi, Matszangosz, Varga and Weiner,
Triplets of mutually unbiased bases](https://link.springer.com/article/10.1007/s10801-026-01506-x)
was published on 4 March 2026. Its Conjecture 1 classifies actual triplets
up to permutational unitary equivalence. Conjecture 2 asks for first-character
vanishing and a cubic-character product involving a transition H and H*.
They are stronger structural questions than determining the maximum number
of bases alone.

The journal version also states Conjecture 3 for the two-circulant Szollosi family:
it cannot occur in a MUB quadruplet. The paper explicitly explains that an
earlier exclusion proof was wrong. Its Proposition 4.2 requires both
Conjectures 2 and 3 to deduce the maximum of three. The relevant primary
correction is [McNulty and Weigert (2025)](https://arxiv.org/abs/2504.13067).
This correction does not construct four MUBs or show the conjectured
exclusion itself false.

## OpenAI's published claims and actual implementation

The OpenAI snapshot checked here is
`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`.
Its [main MUB paper](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026/build/sections/introduction.tex)
claims exclusion of four arbitrary bases by a complete computation under
stated arithmetic and compiler conditions. The
[execution section](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026/build/sections/execution.tex)
reports completion on 4 October 2026, despite the manuscript's 24 September
date. Its specified C++ verification sources, runner and execution archive
are absent from the checked paper subtree, which contains fifteen files.
We have not replayed or certified that exclusion. Missing artifacts at this
commit do not imply the reported computation never occurred or is incorrect.

The separate
[exact Fourier manuscript](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Exact-Fourier-certificates-for-complex-Hadamard-matrices-of-order-six-September-24-2026/build/paper.tex)
claims first-character vanishing outside Tao's class and an upper bound of
five. Its actual Lean endpoint
[MUB6.fourier_and_family_bound](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Analysis/MutuallyUnbiased/Main.lean)
has a proof body, and
[Results.Bounds](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Analysis/MutuallyUnbiased/Results/Bounds.lean)
implements the seven-basis exclusion and six-to-seven completion route.
The `sorry` in a ComparatorChallenges template must not be mistaken for
this solution: its JSON maps to the actual solution module.
Those endpoints were read, but this review did not compile or audit the
whole external dependency graph. They do not implement the upper bound
three or the cubic/adjoint coupling.

## Other relevant 2026 claims

[Cardenes Wuttig and Tindall, arXiv:2608.18053v2](https://arxiv.org/html/2608.18053v2)
claim finite-corner completeness for order-six Hadamard matrices. Their
Outlook distinguishes individual matrix classification from compatibility
of transitions sharing actual bases. This result is a possible input,
not a triplet or quadruplet classification by itself; we have not replayed
the external Lean project.

A [Szollosi-family exclusion candidate](https://github.com/ipitchford/szollosi-mub-exclusion)
and its [30 September 2026 archive](https://zenodo.org/records/23051062)
directly overlap Conjecture 3. Its author labels the work an unrefereed
candidate with internal replay. We have not independently accepted it.
Conjecture 3 must therefore carry a published proof-claim flag rather than
being represented as an untouched problem.

## Chosen structural target

The extra double-anticommutation route has a classical scope. The primary
[Szollosi paper, arXiv:0811.3930v2, Section 4](https://arxiv.org/pdf/0811.3930v2)
explicitly recalls Zauner's two-by-two unitary phase lemma and characterizes
four-circulant unitary matrices by two flat Fourier-phase factors. Its
Proposition 4.2 already supplies the complete companion construction;
the 2026 triplet paper recalls it in (4.3)-(4.5).
[The fixed-partition equivalence](four-circulant-route.md) makes the relation
to the prescribed spectral witness and a sixteen-pair phase test explicit.
This identifies a known symmetry class, not a new general MUB construction.
General companionship has not been proved to imply that symmetry.

The principal target recorded here is the remaining source-stated identity

    complete companion of H  =>  g_H(3alpha) g_H*(3alpha) = 0,
    alpha=(1,1,1,-1,-1,-1).

The OpenAI Fourier paper explicitly distinguishes this additional cubic
condition from its first-character theorem. Neither the maximum-three
claim nor individual Hadamard completeness supplies it automatically.
This is positive source evidence for a separate unresolved research target
in those works; an unsuccessful literature search alone would not establish
that no later proof exists.

[spectral-companion.md](spectral-companion.md) gives an exact spectral
formulation and a conditional branch. It does not silently adopt any of
the external proof claims above as independently verified prerequisites.
