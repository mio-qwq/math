# Literature register

调查截止 2026-10-11，UTC。

- [Hash 与原始来源 H01–H30](literature/HASHES_SURVEY.md)。
- [Symmetric/ARX 与近邻原始来源](literature/SYMMETRIC_SURVEY.md)。
- [Public-key/PQC 与来源 S01–S29](literature/PUBLICKEY_SURVEY.md)。

三份文件由独立文献分工生成，数值均有模型与读取范围；没有把所有摘要当成已全文核验。

主线新增先行：Bellini、Grados、Makarim、Sanna，Finding differential trails on ChaCha by means of state functions，作者稿 https://iris.polito.it/retrieve/handle/11583/2987931/707706 。包含 half-quarter XDP/ADP O(n) 公式与 quarter 独立性启发式。主 Agent URL取403，Research Agent已读作者稿；正式元数据和具体定理进一步核对。普通状态函数不能视为新方法。

选题前、成果后、投稿前三级查重；每个项目独立 NOVELTY_REVIEW。全文缺口和等价推广未排除时保持未定。

正式书目已核：International Journal of Applied Cryptography 4(3/4):156–175，2024，DOI https://doi.org/10.1504/IJACT.2024.138416；出版社列四位作者Bellini、Grados、Makarim、Sanna。作者稿与正式版编号/作者表需分别引用。

## 成果后近邻审查

[项目NOVELTY_REVIEW](projects/chacha-three-add/NOVELTY_REVIEW.md)列十组最近邻、确切版本、等价掩码和获取缺口；[检索日志](projects/chacha-three-add/literature/SEARCH_LOG.md)记录检索范围；[抓取清单](projects/chacha-three-add/literature/retrieval_manifest.json)记录公开PDF哈希与失败状态。第三方完整论文保留在忽略缓存内，不纳入本项目成果提交。

新增关键原始来源：

- [Sarkar 2009/047](https://eprint.iacr.org/2009/047)：多字加法/XOR有限位置相关，M0属于该旧问题；文中承认CRYPTO1990先行。
- [Niu等2026/1193](https://eprint.iacr.org/2026/1193)，[CRYPTO2026正式版](https://link.springer.com/chapter/10.1007/978-3-032-35412-9_13)：Mealy机器的线性及条件相关，通用状态精确求和已知。
- [Okada等2025/2128](https://eprint.iacr.org/2025/2128)，[INDOCRYPT2025正式版](https://link.springer.com/chapter/10.1007/978-3-032-13301-4_4)：两加法三变量精确线性分析，与本项目变换后的对象特别接近；正式全文未得。

选择性重检确认：Bellini等作者上传PDF/元数据列`10.1504/IJACT.2024.10063705`，但[出版社页面](https://www.inderscience.com/info/inarticle.php?artid=138416)主DOI为`10.1504/IJACT.2024.138416`，2024-05-03上线、2023-03-08接受。不得把稿件中的2023页眉与实际出版日期混同。

## 已有方法的具体重构与下一主线

[METHOD_COMPARISON](projects/chacha-three-add/literature/METHOD_COMPARISON.md)已写出普通两进位核与短行向量恒等式，重构特殊位和上位关键矩；通用方法的新颖性主张据此被否定。同目标的可逆前缀基线已独立重建，不能把初版O(n²)逐矩计算当作最好公开基线。

固定a,b,c模型的近邻补入Flórez-Gutiérrez–Todo，[EUROCRYPT2025正式版](https://link.springer.com/chapter/10.1007/978-3-031-91107-1_15)，pp427–457，2025-04-27；[ePrint2025/437](https://eprint.iacr.org/2025/437)当前明确标major revision。本文关于密钥条件化的具体内容仍需全文比较，不能用摘要给出未核验的定理。研究模型和逐项差异见该scout的NOVELTY_REVIEW。

下一方向的[Keccak选题前查重](projects/keccak-conditional-rank/NOVELTY_REVIEW.md)已经登记2024概率线性化、2025内部差分/VDDT与2025线性抵消三组直接近邻。公开全文、附录与实例是否可获得另行记录；这不是原创性通过。


近期补充：[Yan–Bao–Li，ePrint2026/2090](https://eprint.iacr.org/2026/2090)，SAC2026已确认接收/报告，metadata为minor revision，received2026-09-18/revised2026-09-30。已固定的35页[官方会议稿](https://www.sacworkshop.org/SAC26/preproceedings/SAC2026_2-final50.pdf)文件内制作日期为07-24，与未取得的09-30全文分开引用。它已覆盖SA-PIDS联合秩/自由度优化、投影重数、调和平均校正和精确单纤维计数。最终会议录卷页/DOI未核验。

[RECENT_LITERATURE](projects/keccak-conditional-rank/RECENT_LITERATURE.md)记录§5–6、Table5–6及作者代码的实际读取范围；[SOURCE_ACCESS](projects/keccak-conditional-rank/SOURCE_ACCESS.md)固定三份公开PDF的SHA-256。作者仓库commit259d33b3eebfb6c3777c2bbf6299a47335d5ed2a/tree4bad4b3fa12ee4f0639b2b4c1e335c3e65358d0e仅只读，未编译执行。新候选先核R412/C388、投影核及局部有效集合，不能把旧二阶矩或自相关恒等式作为新方法。
