# TF 对称性的随机图编辑距离

**完整书面证明；独立研究 Agent 数学复核通过；无完整 Lean；历史原创性未确认。**

[Bychawski 原文 v1 Conjecture 6.5](https://arxiv.org/html/2406.06267v1)要求：对每个固定 epsilon>0，均匀标号简单随机图在至多 n(1-epsilon)/2 次无向边翻转内获得非平凡 TF 投射的概率趋于零。本交付证明这一原始全范围结论。它同时给出更强目标类（连通、非二分、开邻域无孪生）的最短编辑距离 D_n/n 在概率意义下趋于 1/2。

原命题的下界针对**所有非恒等有序 TF 对**；不能仅从更严格目标类的距离下界推出原命题。上界构造产生普通换位自同构，不是非对角 TF 不稳定性的构造。

- [完整证明](PROOF.md)：支持分层、独立比较、全局约束秩和显式 true-twin 编辑；必要熵引理与概率估计均在正文。
- [实际有限回归与验证范围](VERIFICATION.json)：冻结检查器、2,000 个定义层检查及损坏控制；不是极限证明的替代。
- [来源及展示修正](provenance.json)：原稿与后加入程序分别绑定，未回填历史验证。

复现有限检查：`python audit_bychawski_edit_distance.py`（仅 Python 标准库）。源代码与数学推导的历史冻结保留在 [C-audit 原提交](https://github.com/mio-qwq/math/tree/9ad1f91d953060d01a504481eb857daf57758ab0/workstreams/C-audit-1010)。独立 Agent 复核不是外部人类同行评审；本说明不分配论文署名，也不声称首创。
