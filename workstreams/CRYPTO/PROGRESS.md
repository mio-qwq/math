# Progress

## P0 — 第一阶段（2026-10-11）

已建立独立 clone 与分支，读取仓库协调说明及成果入口。其他 Agent 工作保留原状，全部新增文件位于 workstreams/CRYPTO。

三名文献分工完成15项算法/问题调查，保留原始来源、模型和全文缺口。主 Agent 补核2026 SHA-2摘要、2026-10-09 ChaCha全文、2025纠错全文、近期线性规则元数据和标准页。

已选择 ChaCha 三加法精确有符号相关为首个目标。此检查点调查/建模为 L0，尚无新攻击、原创定理或形式化证明。

第一阶段已发布至 `partner/dist-crypto`：commit `b3b24135d0c71fae7a97f48a8e1c00c73496fffd`，tree `0827505a11339a640862ad225f49a54c7d400257`。

## P1 — 特殊位的精确有符号相关

已完成两份独立普通数学证明。r,q>=1，r+q<n，i=r+q 时

\[
C_i=-\frac1{3\,2^r}-\frac1{7\,2^q}
+\frac4{3\,2^{3r+2q}}+\frac1{7\,2^{3r+q}}<0.
\]

标准32位、旋转16/12、输出位28给出

`-47180567524833621 / 1180591620717411303424`。

发现者原输入枚举覆盖10参数、6,492,160输入元组；独立程序覆盖n=3..5全部50旋转组合并保留每一输出位的完整带符号计数。另有25个独立阈值和比较。RFC8439季轮官方向量通过。证据和限定模型见[独立报告](projects/chacha-three-add/verification/VERIFICATION_REPORT.md)。

## P2 — 固定首字及符号分类

固定首字A、仅b,c,d独立均匀时，已推导并独立审读O(r)算术闭式。若A_low=A mod2^(r+q)，则特殊位的相关符号分类为：A_low=0时+C0；A_low=1时-C0；其余严格小于-C0，其中C0=2^-(2r+q)。因此没有零相关情形。一般证明来自三角波有限和，不由小参数统计外推。

四个ChaCha常量的标准特殊位精确分数由闭式与独立DP一致算出。81,924个公式域自检、56个先前独立原字端点及辅助有限和检查均通过。详见[固定字证明审查](projects/chacha-three-add/verification/FIXED_WORD_PROOF_REVIEW.md)。这不是固定秘密密钥模型；b,c仍均匀。

## P3 — 任意位的旋转消去和四状态求和

已经证明：任意合法n,r,q,i可消去中间均匀字，只保留至多n个四状态有符号矩。初版逐矩重算的单输出位成本O(n²)整数算术；状态/整数位成本有明确定义。固定首字的版本同样成立。更强同目标基线见P5。

独立原字计数给出216个均匀位比较、1274个条件位比较，全部相符；两个独立编写的DP产生的32位标准uniform+4常量表有160个精确分数，根端逐项比较通过。命令实际退出0，未使用随机采样。详见[一般证明](projects/chacha-three-add/GENERAL_REDUCTION.md)、[独立报告](projects/chacha-three-add/verification/GENERAL_VERIFICATION_REPORT.md)和[交叉记录](projects/chacha-three-add/tooling/results/standard_comparison.json)。

## P4 — 重叠上位区间

已从阈值矩得到i=r+q+k、0<=k<=q、i<n的闭式，形如A4^-k+B2^-k+D16^-k，覆盖标准输出位28..31。发现者有完整书面证明与有限矩检查；根端独立DP的324个参数、60个递推和4个标准分数已通过。最后独立文稿审读也已通过，verifier另有275参数、575个分块矩及14个旧原字值相符。域外反例已保存，不将公式推广到k>q。结合C003，指定均匀输入掩码的标准全部32位已有闭式，见[阶段报告](projects/chacha-three-add/RESULTS.md)。

## P5 — 具体先行方法重构与流式基线

第二个数学检查点已推送：commit `59a24dc5c1afeaf481bb77ac7f2228465c821f3b`，tree `9d4058b6e7470f3bbb9a96df3ac7b1c60fbddf9c`，父提交为b3b2413。

Literature Agent从普通两进位核的短行向量恒等式，具体推出特殊位和上位公式的所有关键矩。这确认了该部分是已有框架的直接应用，不能认领新有限状态或谱分析方法；是否已有完全相同的旋转应用仍有全文缺口。

三个无掩码核的行列式均为1/16，允许共享可逆前缀。重建程序对每输出位使用O(n)精确有理算术和O(n)核心辅助位，全部n位分别求值为O(n²)算术。源码没有缓存全部前缀。该算法匹配216均匀原字值、1274固定字原字值、160标准值，共1650项；真实退出码0，计时范围内1.481秒。没有新增暴力枚举或随机采样。独立规格检查另核三个核、左右逆矩、18个既有原字例和21个插入矩，包含符号顺序与同位置BY负控制。

详见[方法比较](projects/chacha-three-add/literature/METHOD_COMPARISON.md)、[流式证明](projects/chacha-three-add/proofs/streaming_prefix_baseline.md)及[实际运行](projects/chacha-three-add/experiments/STREAMING_PREFIX_RUN.md)。这是L0基线完善。Fraction包含增长整数乘法和归一化，不能从O(n)算术次数推出O(n)位时间；也未作与不同工作量旧计时的速度倍率比较。

## P6 — 固定三个输入字的有界模型校准

固定a,b,c、仅d均匀的相关可化成一个常量符号乘E[(-1)^(borrow_j xorcarry_i)]。借位/进位的输入区间可以先精确平均独立前缀，再对共同输入位用四状态核。因此每位O(n)整数算术、O(n)核心辅助位，不需要32位枚举。这是已有方法直接应用，见[模型与证明](projects/chacha-three-add/scouting/fixed_abc/SCOUT.md)。

发现端预定17个小字宽固定例，枚举188个d，核对692个逐输入位恒等式与54个相关，真实退出0；六个标准宽度有限示例均由小状态精确计算。漏常量符号和误设独立性的负控制分别产生-1变+1、-1变0。不同输入分布的数值差异不构成攻击：对固定b,c的结果再平均，恰恢复之前固定a、均匀b,c,d模型。

[八组近邻查重](projects/chacha-three-add/scouting/fixed_abc/NOVELTY_REVIEW.md)已经完成，结论为L0归档并停止扩大此scout。独立验证器先在未读发现端证明/代码时，用7个预定参数、90个原始d输入核对23个输出位；随后普通文稿/源码审读与6个标准实例交叉计算均通过。独立阶段和披露后的普通审查分别固定manifest，见[最终复核](projects/chacha-three-add/scouting/fixed_abc/verification/ORDINARY_REVIEW_REPORT.md)。

## P7 — 自主转向与恢复入口

已经根据实际查重下调这个窄ChaCha掩码选题的原创优先级，保留初始调查并追加明确理由。Keccak近期查重进一步发现SAC2026已覆盖秩/自由度优化、投影重数、调和平均校正及精确单纤维计数；官方35页会议稿已固定字节并审读相关章节，最新ePrint修订仍未取得。

下一主线收窄为[同一Table6实例的全局投影计数界](projects/keccak-conditional-rank/OBJECTIVE.md)。文献R412/C388、核维数28与局部有效集合分解是待独立复算的输入，不是本项目已核验结论。一般二阶矩界和核方向枚举明确归L0；当前没有新的Keccak数学结果或运行该实例的实验。完整来源、版本与查重缺口见[近期审查](projects/keccak-conditional-rank/RECENT_LITERATURE.md)。

## 原创性与安全结论

[第二级原创性报告](projects/chacha-three-add/NOVELTY_REVIEW.md)比较十组近邻并写出等价掩码变换。M0与通用有限状态计数明确属既有理论；其余公式/分类尚未排除直接推论，尤其INDOCRYPT 2025等全文缺口尚存。**没有已通过原创性审查的L2，没有改进公开最佳攻击的证据。**

w也是完整quarter-round的第一输出字，因为剩余操作不再写它；这一语义不产生对其他输出、完整20轮或真实密钥的攻击结论。所有代码、证明、命令、环境和SHA-256均保存在本工作流内。主README与其他成员目录未改动。
