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
