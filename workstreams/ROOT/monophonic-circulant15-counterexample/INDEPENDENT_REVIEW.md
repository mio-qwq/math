# 原题语义与完整 Lean 源码的独立复核

**数学与原命题对应 PASS，无必须修复项。** 复核者未参与 Lean 源码撰写、修复或编译。
审查完成于 2026-10-10 12:36 UTC，完整读取全部定义及 25 个定理，从原论文与
实际 Mathlib 定义重新核对，随后检查公开整理后的源码、说明和实际收据。
本审查由独立 AI 代理完成，不是人工同行评审，也没有第二次独立编译。

原审查源 SHA256：`b65c6aaf21836a1ca434024dacac218582842fc306dc75c8c8844ad2c8e9c6ba`。
公开 [MonophonicCirculant15.lean](MonophonicCirculant15.lean) SHA256：`a558d4bd2d2e880eb56df757f8d5f720c6daf6e86d354c540ee6f9cf6f79edfe`。
公开整理仅修改开头一段开发注释；移除块注释后的全部执行文本逐字相同。
下文行号引用原审查源，不作为公开整理后的定位编号。

公开路径的实际编译于 12:31:00–12:31:34 UTC 完成，零错误、零警告、零 panic；
全部七项声明审计仅使用 `propext`、`Classical.choice`、`Quot.sound`。
收据绑定编译前后相同的公开源哈希，见 [lean-audit.json](lean-audit.json) 与
[lean-audit.log](lean-audit.log)。没有 `sorryAx`、自定义公理或 `native_decide`。
有限分类依靠普通 `decide` 的内核证明；任意长度路径的论证是一般定理。

原始对象和量词重新核读自 [arXiv:2106.06827v3](https://arxiv.org/html/2106.06827v3)
及 2025 期刊原文的公开索引。原 conjecture 要求每个 n≥11 存在一个循环图，
monophonic 集限制全部诱导简单路径。标准循环图是有限循环群的 Cayley 图，
可使用任意原顶点标签。期刊 PDF 本轮直接访问受限，未声称下载或遍读该全文；
准确来源和历史不确定性见 [HISTORY.md](HISTORY.md)。

## 任意长度 monophonic 条件及真实最大值

源码 L26–36 的两个谓词都量化任意端点 u,v 和任意 G.Walk u v，并同时要求 IsPath 与 IsChordless。没有 reachable 假设、geodesic 假设、长度界或 diameter 2 截断。

L38–73 的 iff 是真正的双向转换。由三个不同的 support 顶点取三个长度范围内索引，它们因顶点不同而索引不同；源码的比较分支覆盖六种线性顺序，重排选点即可调用 i<j<k 形式。逆向由 IsPath 索引注入性得到三个不同顶点，且索引界保证它们在 support。因而不会把同一顶点重复索引计成三个选点，也不会只检查选点之间某条特定路径。任意路径有三个选点当且仅当可以选出这种三点证据。**PASS。**

L76–80 的 mpNumber 使用 Nat.findGreatest，谓词是存在任意 Finset V，其基数为 k 且满足真实 MonophonicPosition；上界是 Fintype.card V。它不是只在三点集合、某批枚举集合或最大 clique 中取最大。

L82–85 对每个真实 mp Finset 给 card≤mpNumber，理由是 Finset.card_le_univ 和 Nat.le_findGreatest。L87–96 显式提供空集满足 k=0，消除了 findGreatest 在无候选时默认零但不必满足谓词的漏洞；再用 findGreatest_spec 得到一个基数恰为 mpNumber 的实际集合，并通过上述 iff 转成 OriginalMonophonicPosition。Find.lean L165–167、L210–220 的实际定义/引理支持这两步。在 Fintype V 上所有 Set 都有限且对应某个 Finset，因此这里上界和达到覆盖原定义的全体选点集；没有另加选择范围。**PASS。**

## 5. 两个一般结构障碍：不依赖路径搜索

L99–112 的 chordless_adj_indices：若路径上两个顶点相邻，则 chordlessness 使它们的无向边在 p.edges；Traversal 给某个相邻索引 t,t+1，Sym2.eq_iff 的两个方向连同索引注入性得到 i+1=j 或 j+1=i。没有漏掉逆向无向边，也没有假定整条路径最短。

L114–126 对任意 pairwise-adjacent 集合 S，若路径出现三个选点 i<j<k，首末相邻却隔着 j，违反上面的相邻索引结论。L142–151 只是把三角形具体代入；三条边和 SimpleGraph.loopless 自动给三个不同顶点。任意三角形都是原 mp 集。**PASS。**

L130–140 是任意 open-twin 类的一般论证，不是判定某一长度的路径。设三个选点出现在 i<j<k。于是 j≥1；路径上 j−1 与 j 相邻，而 open-twin 的完整邻接等价让同一个 predecessor 也与 k 相邻。因为 k≥j+1，j−1 与 k 至少相隔两个索引，产生弦，矛盾。源码确实检验 predecessor 的存在和长度界，没有把 middle=端点漏掉：i<j 已排除 j=0。

这里 hS 要求对于全图任意 w 的开放邻接等价，未用 closed-neighborhood twins 冒充。简单性还迫使两个不同 open twins 不相邻：代入 w=y，否则会推出 y 的自环。即使 predecessor 恰好是第一个选点，所得到第三点的弦仍成立。L153–165 从 a,b 与 a,c 的两组邻接等价，用对称/传递覆盖三点集合内所有有序对；L167–173 用三点互异得到 Finset.card=3 和 3≤mpNumber。**PASS。**

## 6. 128 个 connection choices 的全称 kernel 命题

L176 的 Choices 是任意函数 Fin 7→Bool；L179–182 的 cyclicAdj 选位 k 对应步长 k+1∈{1,…,7}，允许正向或反向模 15 步，另排除 u=v。L188–195 直接构造对称、无自环的 SimpleGraph。未要求生成整个循环群，也未先筛选连通性或 triangle-free；空集和非连通 choices 同样在量词内。

L203–208 的 FiniteObstruction 明确是以下三项的析取：

1. 0 所在三角形；
2. 某 v 从 0 无法在 0、1 或 2 步内达到；
3. 0、5、10 对全体 w 的邻接完全相同。

第二项 ReachTwo 在 L200–201 包括 u=v、直接边和任意中间点的两条边，是真实长度≤2 reachability 的局部表达，不是只检查指定邻点或给定路径。

L218–221 的命题量化全部七个独立 Bool，由普通 decide 给出证明。全部 2^7=128 个 assignments 均在 theorem 中；不存在从日志样本数量推全称，也没有借作者先前的 19-set reduction 或两张 survivor 作前提。L223–228 再以 Fin 7 extensionality/fin_cases 证明任意函数 P 等于七个取值的向量，从而把该全称位命题覆盖到全部 Choices。

本审查不另跑 128 遍决定过程；完整读实际命题、所用 adjacency 和全部 Decidable 实例，并核对该 decide theorem 已由 ROOT 的实际 kernel 运行和标准公理输出接受。decide 与 native_decide 的信任边界不同：本源码没有本地机器 oracle 或验图脚本作为公理。分类得出的每个证据如何排除原两等式在后续一般定理中证明，因而其意义不是“有限检查一个替代性质便宣布反例”。**PASS。**

## 7. 无遗漏的距离、标签和原始 S 桥

### 7.1 真实距离消除 far 分支

L231–245 的 reachTwo_of_edist_le_two 没有连接性前提。若不是同点或直接边且无共同邻点，实际 Metric L163–174 的 two_lt_edist_iff 给 edist>2，包括不可达时的 ⊤；这与 edist≤2 冲突。得到的 commonNeighbors 证据经邻接对称性提供两步 walk。

L247–258 将 classifier 三分支分别转换为：三角形使 mp≥3；far 证据与 edist≤ediam≤2 冲突；三点 open twins 使 mp≥3。L260–264 因而排除全部七位 P 的 ediam=2、mp=2。它实际证明更强的 ediam≤2 ⇒ mp≥3，但不声称所有 15 阶图都如此。**PASS。**

### 7.2 任意原顶点标签

L268–269 的 IsCirculant15 暂以与某 circulant P 的图同构表示；后面还有独立的 raw Cayley coverage，故此定义没有独自充当“所有 circulant 已分类”的假设。

L271–278 从目标图 H 的 ReachTwo 沿图同构反向运到源图：同点用 injective，边用 map_adj_iff，中间点用 e.symm。L280–306 的任意 V 上定理直接运输三种结构证据；三角形边和互异性保持，far 通过该 ReachTwo 桥，open-twin 邻接等价则先用 e.surjective 覆盖目标图任意 w。最后再次应用目标图上一般的全长度 monophonic 论证。

因此没有只运输某条 witness path、只运输有限长度 paths 或默默假设 mpNumber 同构不变。没有单列一般 mp 同构定理是允许的，因为本链使用了足够强且可运输的结构障碍。L308–312 排除任意标签图的原两等式。**PASS。**

### 7.3 全部原始 connection sets

L315 的 difference=(v.val+15−u.val)%15 恰是循环群差 v−u；由于 u.val≤14，先加 15 后的 Nat 减法不会发生截断。L318 的 positiveGenerator 是 1,…,7。L320、L322、L326 是分别关于所有 v、所有不同 u,v、所有 u,v,k 的有限 kernel 算术引理，非图搜索：difference 0 v=v；每个非零差在七个正负逆对中；模步条件等价于对应的正差或逆差条件。15 为奇数，七对涵盖全部十四个非零元素，无遗漏的自逆非零元素。

L335–337 的 HasCayleyPresentation15 允许任意 Equiv Fin 15≃V 和任意 Set S，要求对所有 u,v 的实际 G.Adj(eu)(ev) 等价于 difference u v∈S。没有加入逆封闭、零排除、连通、固定首点等额外假设。原简单无向图通过 u=v 和邻接对称性自动迫使零排除及逆封闭；不合格原 S 无法呈现一张 SimpleGraph。L339–342 得出 Fintype.card V=15，而非把一个更大图的 15 个点误当全图。

L351–354 由 raw S 证明全部两点邻接可归一为 e0 与 e(difference u v) 的邻接。然后 L355 用实际 G.Adj(e0)(e(k+1)) 决定位 P。

正向：一条任意原边给 u≠v；inverse_pair_cover 找到 k。若 difference u v=k+1，归一化直接给 Pk=true；若逆差为 k+1，先用原边的对称性，再归一化。反向：位为真且模步成立，按正差或逆差代入归一化，逆差分支最后再用邻接对称性。L358 由此构造整个图的同构，而非局部同态或子图嵌入。

所以原 S 的所有可能、任意 cyclic labeling、换 generator 的标签和非循环原标签都已涵盖。即使将 circulant 定义为存在一个 regular cyclic automorphism，选一个 orbit 的循环编号后得到此 difference presentation；这与原文通常 Cayley 定义一致，不增加数学限制。L381–383 的 no_cayley15 确实由已证明的 coverage 接入任意标签排除。**PASS。**

### 7.4 Nat diameter 与最终原量词

L387–395 从 diam=2 首先用 ediam_ne_top_of_diam_ne_zero 得 ediam≠⊤，再用 natCast_diam_eq_ediam_iff 得 ediam=2。该过程中没有把 disconnected 图的有限成分直径 2 当成整个图直径 2；源码注释与实际 Mathlib Diam L278–287 一致。对原有限连通且直径 2 的对象，两种直径恰相同。**PASS。**

L399–402 的 CyclicConnectionPresentation 先独立定义任意正阶 n 的 raw connection presentation，与 n=15 classifier 无关。L407–409 的 OriginalConjecture45 是“所有 n≥11，存在 Fin n 上的 circulant 图，diam=mpNumber=2”，次序和量词匹配原文。给一个抽象 circulant 存在见证时选择其循环编号即可置于 Fin n，故它不是只排除某个特殊预设 labeling 的弱原命题。

L411–418 假定这个全称命题，取 n=15，原 S 与恒等 Equiv 立即给 HasCayleyPresentation15，再调用上述 natural diameter 排除。它证明的是该公开全称猜想的否定，不只是证明某张 15 阶图不是见证。**PASS。**

## 8. 全部 theorem 的逐项覆盖

| 源码行 | 声明 | 判定及理由 |
| --- | --- | --- |
| 38 | monophonicPosition_iff_original | PASS，三点支持与有界互异索引的双向等价 |
| 82、87 | card_le_mpNumber、mpNumber_attained | PASS，全体 mp Finset 的上界和实际达到；空集处理默认零 |
| 99 | chordless_adj_indices | PASS，真实边集和路径注入性迫使连续索引 |
| 114、130 | monophonic_of_pairwise_adj、monophonic_of_open_twins | PASS，一般全长度路径论证 |
| 142、153、167 | triangle_monophonic、twins_monophonic、three_le_mpNumber_of_triple | PASS，三点专门化、完整邻接等价、互异基数三 |
| 218、223 | finite_classification、all_choices_classified | PASS，全七 Bool 的 kernel 命题并覆盖任意函数 P |
| 231、247、260 | reachTwo_of_edist_le_two、three_le_mpNumber_of_diameter、no_labeled_counterexample | PASS，真实 extended distance 和三障碍排除 |
| 271、280、308 | iso_reachTwo、three_le_mpNumber_of_circulant15、no_circulant15 | PASS，任意目标顶点标签的完整结构运输 |
| 320、322、326 | difference_zero、inverse_pair_cover、difference_step | PASS，全模差算术覆盖，普通 decide，无 oracle |
| 339、347 | cayleyPresentation_card、cayleyPresentation_isCirculant15 | PASS，全图基数和任意原 S 的覆盖桥 |
| 381、387 | no_cayley15、no_cayley15_nat_diameter | PASS，任意 raw presentation；处理不可达与 toNat |
| 411 | not_originalConjecture45 | PASS，n=15 排除取反原全称存在性 |

没有数学 must-fix。没有必须再跑枚举或 Lean 才能使上述语义正确的缺口。发布说明可以陈述“15 阶不存在满足这两个原参数的 circulant，原 Conjecture 4.5 因而为假；全称结构分类及原语义链已实际 Lean 编译并经独立源码审查”。本报告不验收其他 n 的精确存在性分类、最小反例阶、survivor 的准确 mp 值、全部 vertex-transitive 图的分类或 Theorem 4.4 的否定。
