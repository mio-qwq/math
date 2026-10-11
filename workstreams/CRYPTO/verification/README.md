# 证据与版本完整性

这些清单核验源码和记录的字节身份，不替代数学证明、独立实现或原创性审查。执行命令均从仓库根目录开始。

## 两个快照

- `RESEARCH_SNAPSHOT.json` 是 C001–C006 检查点的历史清单，69 项。对应提交 `59a24dc5c1afeaf481bb77ac7f2228465c821f3b`。核心文档后来已更新，因此应在该精确提交下核对历史清单。
- `CHECKPOINT3_SNAPSHOT.json` 覆盖后续流式基线、固定输入模型、近期查重和恢复说明。它记录生成时的父提交；所属新 Git tree 绑定它的最终版本。
- `CHECKPOINT3_AUDIT_RUN.json` 保存三个独立冻结清单、七个额外冻结文件的核对结果，以及新快照验证程序的实际返回码和输出。

```sh
python workstreams/CRYPTO/verification/verify_snapshot.py workstreams/CRYPTO/verification/RESEARCH_SNAPSHOT.json --ref 59a24dc5c1afeaf481bb77ac7f2228465c821f3b
python workstreams/CRYPTO/verification/verify_snapshot.py workstreams/CRYPTO/verification/CHECKPOINT3_SNAPSHOT.json
```

第二条检查当前工作区；后续版本有修改时，可将 `--ref` 指向包含该快照的历史提交。脚本检查所有列入文件的字节数、SHA-256、重复路径和目录边界，不自动判定未列入的新文件是否经过审阅。

## 独立冻结边界

本次核对三个清单的 22+6+7=35 个条目。它们分别属于早期独立证明/计数、流式矩阵审查、固定 a,b,c 模型审查。各清单另由 SHA-256 固定；盲实现与披露后的普通审读有单独记录，不能统称为全部盲复现。

所有数学实验已有完整源码及 RUN/JSON 记录。此处没有重新执行大范围枚举，只有读取与哈希检查。实际计时仅适用于原报告明确列出的工作量，不能从这些校验耗时推导密码分析加速。

## 自引用与缓存

新快照排除自身及其后生成的审计回执，避免自引用；这两个文件由包含它们的 Git tree 固定。旧快照保持原样并作为新快照中的普通历史文件保存。

第三方全文 PDF、逐页提取文本和临时二进制保留在已忽略缓存，不计作本项目源码或论文成果。来源获取报告给出 URL、版本、页数、字节数和 SHA-256。缓存消失时可按原来源取回并核验；获取失败只说明访问缺口。
