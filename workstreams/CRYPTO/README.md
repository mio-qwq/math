# CRYPTO：密码分析研究

独立分支 `partner/dist-crypto`，全部改动只在本目录。基线 `a8c3f22e26b08c2d294e2b0e6df2d9cfa430cda0`。

2026-10-11：完成15项算法/问题机会调查，并连续推进 **ChaCha 季轮第一输出字的精确有符号相关**。均匀标准32个输出位闭式、固定首字符号分类与任意位计数已有书面证明和独立实现证据。当前没有超越公开最佳攻击的结果，也没有通过原创性审查的L2结论。

- [机会报告](RESEARCH_OPPORTUNITIES.md)：排序、模型、资源与首个目标。
- [文献台账](LITERATURE.md)、[全局查重](NOVELTY_REVIEW.md)。
- [路线图](ROADMAP.md)、[实际进度](PROGRESS.md)、[研究日志](RESEARCH_LOG.md)、[命题状态](CLAIMS.md)。
- [ChaCha项目](projects/chacha-three-add/README.md)：精确模型、公式、独立验证和项目级NOVELTY_REVIEW。
- [阶段研究报告](projects/chacha-three-add/RESULTS.md)：已经核验的数学结论、证据和安全意义。
- [具体旧方法比较](projects/chacha-three-add/literature/METHOD_COMPARISON.md)：关键矩的先行框架重构及已实现的O(n)算术基线。
- [下一主线](projects/keccak-conditional-rank/OBJECTIVE.md)：Keccak同一公开实例的全局投影计数界；近期先行已排除宽泛秩优化目标，实例待独立重建。
- [恢复说明](RESUME.md)：已有检查点、无需重跑的证据和下一动作。
- [完整性核验](verification/README.md)：历史版本、源码哈希清单和本次审计回执。
- `verification/STARTUP.json`：基线、分支、环境和检查范围。

Agent 内部复核不是人类同行评议；分支记录不等于主分支验收或历史原创性。未经用户授权不提交学术平台、申请 DOI 或联系第三方。
