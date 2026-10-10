# Adversarial cases for the component-avoidance proof

**Research note only.** Supplement to the complete Conjecture 10 proof candidate, frozen as Git blob \`84ab0860bb1fe9ca0812225bb01227f5b6d63d13\`. These examples explain why the two-candidate *auxiliary multigraph* must preserve **parallel edges and loops**. They are not a replacement for its universal lemma or an independent proof acceptance.

## 1. An indispensable 2-cycle from parallel edges

Let Q consist of two disjoint edges: \(0-1\) and \(2-3\). Partition \(V(Q)\) into two parts \(C_1=\{0,2\}\) and \(C_2=\{1,3\}\). Choose the only two candidates in each part.

- Q-components: \(S_A=\{0,1\}\), \(S_B=\{2,3\}\).
- Neither component is automatically safe: both vertices in each component are candidates belonging to **different** parts.
- The auxiliary graph T has **two distinct labelled parallel edges**, one for \(C_1\), one for \(C_2\), both between A and B. Both dangerous T-vertices have degree two.
- Direct the \(C_1\) edge \(A\to B\) and the \(C_2\) edge \(B\to A\). Select candidate 2 from \(C_1\) and candidate 1 from \(C_2\). Then \(R=\{1,2\}\) contains **neither** whole Q-component.

If one silently suppresses the parallel edge, T becomes a single ordinary edge. One endpoint necessarily has outdegree zero, and the supposed sinkless-orientation sublemma fails. The universal proof therefore genuinely needs a **multigraph including 2-cycles**. This is not merely an implementation detail.

## 2. A safe loop component

Again let Q consist of edges \(0-1\) and \(2-3\), now partition into \(C_1=\{0,1\}\), \(C_2=\{2,3\}\). Each auxiliary edge is a **loop** at its Q-component. Both components are safe because they contain both candidates from their own part. A loop's orientation does not matter: choosing one candidate necessarily leaves the other unselected. This is why the all-dangerous orientation argument correctly assumes no loops but the full auxiliary construction must still support them.

## 3. Why minimum positive degree is an actual hypothesis

If Q is **edgeless**, every Q-component is a singleton. No nonempty selected transversal can avoid containing the Q-component of one of its chosen vertices. The component-avoidance lemma as stated is false without the no-isolates assumption. In Theorem 3 that assumption comes from \(d\ge3\): the graph Q is \((d-2)\)-regular.

## 4. Why the roots need a second ordering step

Suppose the selected roots \(x,y\) are adjacent within Q and only \(y\) has a Q-neighbour \(z\notin R\). If one lists \(y\) **before** \(x\), the edge \(xy\) is assigned to \(y\), so \(x\) may have no Q-edge assigned to it. Instead root the Q[R] tree at boundary vertex \(y\) and list \(x\) before \(y\): then \(x\) owns \(xy\) and \(y\) owns \(yz\). Thus selecting roots alone is not sufficient: the *postorder root arrangement* is a logically distinct proof obligation.

## 5. Why graph simplicity is used in the final global order

For a nonroot vertex \(v_j\) on an alternating 0/1 cycle, a leftover-colour edge to the immediately preceding vertex \(v_{j-1}\) would be inserted after \(e_{j-1}\), **between** the two cycle edges of \(v_j\), spoiling its asserted signature. This cannot occur in the original **simple** graph because \(v_{j-1}v_j=e_{j-1}\) already exists with colour 0 or 1. Graph simplicity is a substantive hypothesis, not a removable cosmetic choice.

## Independent review priorities

Reconstruct these cases from the definitions, then verify the general implication: every dangerous auxiliary T-vertex has at least two **distinct incident labelled edges** and no loop; a connected loopless multigraph of minimum degree two contains a cycle of length at least two. Also check the selected-root forest property and every endpoint pair type. Finite numerical checks cannot replace the universal proof. No ROOT acceptance, Lean compilation, priority or publication is claimed.
