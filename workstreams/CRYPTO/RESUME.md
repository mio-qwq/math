# 恢复说明

更新日期：2026-10-11 UTC。本文件保存已完成研究与下一可执行目标；会话结束后没有未配置的后台研究进程。

## 仓库与版本定位

- 正式仓库：https://github.com/mio-qwq/math
- 唯一工作分支：`partner/dist-crypto`；全部写入仅限 `workstreams/CRYPTO/`。
- 当前工作区：`/workspace/scratch/5f0455e66649/math-crypto`。
- 启动及最近再次 fetch 的 main：`a8c3f22e26b08c2d294e2b0e6df2d9cfa430cda0`。
- 第一阶段远端提交：`b3b24135d0c71fae7a97f48a8e1c00c73496fffd`。
- 已发布 C001–C006 数学检查点：`59a24dc5c1afeaf481bb77ac7f2228465c821f3b`，tree `9d4058b6e7470f3bbb9a96df3ac7b1c60fbddf9c`。
- 本次后续检查点的源码/证据版本由 [CHECKPOINT3_SNAPSHOT.json](verification/CHECKPOINT3_SNAPSHOT.json) 与包含它的 Git commit 共同确定。为避免自引用，不把本文件所属提交的 SHA 预填进本文件。

恢复时先只读检查状态与历史，再 fetch main 和本分支。若出现其他人的修改或分支前进，保留并核对，不 reset、不强推、不替换其他 checkout。旧 A 成员工作区有自己的修改，从未写入。启动时的跨分支内容扫描并非穷尽审查；后续重复研究检查也应明确实际读取范围。

## 已完成，不从头重做

1. [15 项算法机会调查](RESEARCH_OPPORTUNITIES.md)及三份文献分工，含参数、模型、得分依据和全文缺口；§8 保留同日研究后的降级及转向。
2. ChaCha 指定 all-XOR 掩码：标准 32 个输出位有闭式；固定首字有 O(r) 算术公式及完整符号分类；任意合法位/旋转有四状态精确求和。适用域、输入分布和反例见 [CLAIMS.md](CLAIMS.md) 与 [阶段报告](projects/chacha-three-add/RESULTS.md)。
3. 既有矩阵方法已被具体重构。O(n) 精确有理算术、O(n) 核心辅助位的流式单输出基线已实现，1650 个冻结精确值全部匹配；独立规格核验和随后普通源码审读已通过。这里不是 O(n) 位时间，也不是公开最佳攻击改进。
4. 固定 a,b,c、仅 d 均匀的有界评估已完成。发现端 17 例；独立端 23 个原字输出位及 6 个标准实例对照通过。它是 L0 的模型澄清与常量核应用，已关闭扩大枚举路线。
5. ChaCha 成果后查重、具体方法重构和固定输入模型的八组近邻审查均完成。**目前没有通过原创性审查的 L2，没有 L3/L4。** 个别应用级公式的历史优先权仍不确定，不能因验证通过认定新颖。
6. 下一方向已经自主转到 Keccak。近期 SAC 2026 工作使宽泛秩优化、单纤维计数和调和平均校正均失去新贡献资格，已进一步收窄目标。

独立验证是有阅读边界记录的 Agent 推导和实现复核，不是人类同行评议，也没有证明助手认证。

## 下一项可执行研究

先读 [Keccak OBJECTIVE.md](projects/keccak-conditional-rank/OBJECTIVE.md)、[近期查重](projects/keccak-conditional-rank/RECENT_LITERATURE.md) 和 [来源获取记录](projects/keccak-conditional-rank/SOURCE_ACCESS.md)。只保留 **SAC 2026 同一 Table 6 实例的全局纤维二阶矩、投影大小或有效自由度的非平凡可检查界** 这个候选。

第一步是从原始 Keccak 定义、Table 5–6 与全部 padding 条件独立重建约束和局部有效集合。使用文献的 800 位内部差分坐标与 R=412、C=388，不能替换成 416/384。文献给出的投影核维数 28、分块秩和局部乘积分解都须实际验证后才能作为本项目事实。矩阵本身、一般 Cauchy–Schwarz 界、自相关展开与普通核枚举均属 L0 基线。

公开作者仓库固定 commit `259d33b3eebfb6c3777c2bbf6299a47335d5ed2a`、tree `4bad4b3fa12ee4f0639b2b4c1e335c3e65358d0e`。本阶段只读指定源码，没有编译或执行。已固定官方会议预印 PDF 的 SHA-256，但最新 2026-09-30 ePrint 正文尚未取得；两版本不能默认相同。

先分析普通枚举及候选证书的成本，再决定是否计算；不直接启动 2^28 核方向遍历，更不扩大随机攻击实验。若只有旧公式或不能改变同模型判断的数值，记录 L0 并换候选。具体成功/失败标准已在 OBJECTIVE 中给出。

## 完整性检查与复现

从仓库根目录可先执行只读检查：

```sh
git status --short --branch
git log -5 --oneline
git fetch origin main partner/dist-crypto
python workstreams/CRYPTO/verification/verify_snapshot.py workstreams/CRYPTO/verification/CHECKPOINT3_SNAPSHOT.json
```

旧检查点的 69 项哈希已实际在 59a24dc 上核验通过。需要复核历史版本时使用：

```sh
python workstreams/CRYPTO/verification/verify_snapshot.py workstreams/CRYPTO/verification/RESEARCH_SNAPSHOT.json --ref 59a24dc5c1afeaf481bb77ac7f2228465c821f3b
```

只有存在具体代码变更或验证风险时才重跑数学实验。先在独立临时复制件中运行会覆写结果文件的脚本，保留已提交历史记录。详细命令、解释器、退出码、计时范围与 SHA-256 见每个 RUN/verification 报告。没有随机采样的程序应标为“确定性，随机种子不适用”。流式复现可以显式写到忽略缓存：

```sh
python workstreams/CRYPTO/projects/chacha-three-add/experiments/streaming_prefix.py --output workstreams/CRYPTO/.local-cache/recheck-streaming.json
```

脚本读取的历史证据应先通过 manifest 核验。不要扩大到 32 位原始四字暴力枚举。第三方 PDF 缓存未入 Git；来源记录包含下载 URL、版本、字节数和哈希，可按原来源重新取得并比较，不把缓存不存在当作新颖性证据。

## 提交与权限

用户已授权正常理论、实验、独立复核及本分支 Git 检查点，不需要问“是否继续”。shell HTTPS push 曾因无凭据失败；已有授权 GitHub connector 可创建与本地 index 相同的 tree，再以 expected_sha、force=false 更新本分支。发布前核对目录范围与远端旧头，发布后 fetch、核 tree 并无损对齐本地分支。

不向 main 或其他成员目录写入，不强推。未经新的明确授权，不联系作者、不提交预印本、不注册 DOI、不投稿。下一阶段开始时先保存新目标、证明及复杂度，再运行有界实验。
