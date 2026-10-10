# Hamiltonian two-colour cycles yield rooted colour-universal cubic gadgets

**Original target:** Gorzkowska–Kwaśny, *Distinguishing adjacent vertices by ordering edges*, arXiv:2609.11832v1 (2026-09-10), Conjecture 10, https://arxiv.org/html/2609.11832v1. This is an analytic strengthening of \`ROOTED_GADGETS.md\`, not a full conjecture solution or historical priority claim. It removes dependence on exhausting 48 Heawood colourings for the universal statement.

## Theorem 1: Hamiltonian rooted-interface lemma

Let B=(U,W,E) be a finite simple **cubic bipartite graph** with a fixed proper three-edge-colouring by 0,1,2, and root r∈W. If the edges of colours **0 and 2** form one Hamiltonian cycle spanning B, then there exists a total order on U in which (i) the three colour-0,1,2 neighbours of r occur in that same order, and (ii) every other vertex w in W\\{r} reads its incident colours, in neighbour-U order, in a sequence **different from (0,1,2)**.

**Proof.** For each w in W let u_i(w) denote its unique colour-i neighbour in U. Define σ:U→U by σ(u₀(w))=u₂(w). Because the colour-0 and colour-2 matchings form a single alternating Hamilton cycle, σ is one cycle on U. Put a=u₀(r) and linearly order U as

    a, σ⁻¹(a), σ⁻²(a), ..., σ(a).

Here a is first and σ(a)=u₂(r) is last. The third neighbour u₁(r) is distinct from both because B is simple and cubic. Thus u₀(r)<u₁(r)<u₂(r), proving (i). For w≠r put x=u₀(w)≠a. In the displayed reverse cyclic order every arrow x→σ(x), except a→σ(a), points **backwards**. Therefore u₀(w)>u₂(w), so the three colours at w cannot appear in order (0,1,2), proving (ii). QED.

In particular, if B has the Hamiltonian-two-colour property for **every proper three-edge-colouring** (it is *2-factor Hamiltonian*), B−r is a **colour-universal rooted substitution gadget**. The odd-gadget 3-edge-cut matching parity lemma and general substitution proof in \`ROOTED_GADGETS.md\` then show that replacing a vertex of a cubic graph preserving universal sequential orderability still preserves the *all proper colourings* quantifier.

## Theorem 2: order 14 plus girth 6 forces Hamiltonian two-colour factors

Let B be a finite simple **cubic bipartite graph on 14 vertices with girth at least six**. For *every* proper three-edge-colouring, the union of any two colour classes is a **Hamiltonian 14-cycle**.

**Proof.** Each colour is a perfect matching. The union of two colours is a spanning 2-regular graph whose components are **even cycles**, each of length at least six. With 14 total vertices this is either one cycle of length 14, or disjoint cycles of lengths 6 and 8. In the latter case the remaining colour gives one extra matching edge incident to each vertex of those two cycles. None of these edges can be a chord within either cycle: a chord of C6 or C8 creates a cycle of length at most four or five, respectively, contrary to girth≥6. Hence all third-colour matching edges connect the two cycles, but the 6-cycle supplies six and the 8-cycle eight endpoints, impossible. Thus there is exactly one 14-cycle. QED.

The Heawood graph explicitly specified by neighbour lists in \`ROOTED_GADGETS.md\` is simple cubic bipartite on 14 vertices, has no four-cycle (two U vertices share at most one neighbour), and contains the explicit six-cycle

    1 -- 2 -- 3 -- 4 -- 9 -- 10 -- 1.

Its girth is therefore six. Theorems 1 and 2 establish that **every proper three-edge-colouring of Heawood** has a compatible rooted vertex order, without relying on computer enumeration. The exact exhaustive **48-colouring** check in \`code/verify_rooted_gadgets.py\` is an independent regression test, not a prerequisite for the theorem. For the cube gadget, which may have disconnected two-colour 2-factors, the separate exact **24-colouring** certificate still applies.

## Consequence for the original conjecture

The universal-vertex lemma gives K4 orderability under every proper edge colouring. The colour-universal substitution proof in \`ROOTED_GADGETS.md\` (including the odd-cut matching-parity condition) allows replacing all four K4 vertices by Heawood−root copies: the resulting simple cubic graph has 52 vertices, 78 edges, girth six and is nonbipartite. **Every fixed proper edge colouring** of that graph admits a good global edge order. Further replacements yield an **infinite family of nonbipartite, girth-at-least-six, cubic graphs** satisfying the universal quantifier of Conjecture 10. This does not cover all nonbipartite cubic graphs.

All arguments are exact and all assumptions are explicit. No contact with authors, Lean formalization, ROOT review, publication or priority assertion is claimed.
