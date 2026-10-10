# 原不等式的无界差距：书面证明

此全参数族来自[冻结成果](https://github.com/mio-qwq/math/blob/6556271dcb99553af752c245438e517f4c01c1f0/workstreams/B/lower_gp_product/UNBOUNDED_GAP_PROOF.md)，已由未参与发现的代理独立推导并复核。下面全称论证是书面数学证明，**不在本目录固定 11×29 Lean 证明的形式化范围内**。

## Elementary unbounded-gap family

For each integer r>=6, construct G_r as two K_r graphs identified at one vertex c. Write the two remaining (r-1)-cliques as A,B and choose a in A,b in B. Construct H_r from landmarks z,u_0,u_1,v_0,v_1 and FOUR r-vertex cliques Q_ij exactly as in [PROOF.md](PROOF.md): each Q_ij is adjacent precisely to z,u_i,v_j outside itself, and the landmarks induce K5minus the two edges u_0u_1,v_0v_1. Thus

    |G_r|=2r-1, |H_r|=4r+5,
    gp^-(G_r)=r, gp^-(H_r)>=r.

The G_r classification from the fixed proof works verbatim: its maximal GP sets are the two K_r blocks and A union B, whose sizes are r,r,2r-2. True-twin saturation in H_r forces any maximal GP set meeting Q_ij to contain all r vertices. The same six maximal GP subsets within the five landmarks have outside extensions, so every maximal GP set meets a Q-clique. These are complete all-parameter arguments, not extrapolations from finite tests.

The FIVE product points

    (a,u_0),(a,u_1),(c,z),(b,v_0),(b,v_1)

remain GP and maximal. Their selected distances and every case in the fixed proof depend only on landmark roles and membership in A,B,Q_ij, never on the number of clones. All required classes are nonempty for r>=6. Therefore

    gp^-(G_r square H_r)<=5,       min{gp^-(G_r),gp^-(H_r)}=r.

The deficit from the ORIGINAL conjectured bound is at least r-5 and is UNBOUNDED. The ratio of product lowerGP to the smaller factor lowerGP is at most5/r, tending to0. No increasing unbounded function of the smaller factor parameter can serve as a universal lower bound. This conclusion is elementary and independent of the metric-cone theorem. It concerns lower GP, not the previously known lower-TERMINAL gap in the original Proposition1.

The r=6instance is exactly the frozen11by29counterexample. No smaller construction is needed for acceptance.


## 范围与依赖

本族严格表明原猜想的差距可以任意大，并非另一个原猜想解答。已证明的产品上界是 5，未在此证明其精确值。通用 min5 下界及据此得出的 sharp replacement 属于另一份成果，本文件不依赖该结论。有限参数检查不能替代上述全部 r≥6 的角色证明；历史首创性未确认。
