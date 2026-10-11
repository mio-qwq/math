# 恢复说明

本文件记录可恢复的研究状态，不是后台运行承诺。当前会话结束后，未配置的研究进程不会自行继续。

## 仓库和隔离约束

- 仓库：https://github.com/mio-qwq/math
- 工作分支：`partner/dist-crypto`；所有写入仅限`workstreams/CRYPTO/`。
- 原始main基线：`a8c3f22e26b08c2d294e2b0e6df2d9cfa430cda0`。
- 第一阶段已核实远端提交：`b3b24135d0c71fae7a97f48a8e1c00c73496fffd`。
- 本地工作区：`/workspace/scratch/5f0455e66649/math-crypto`。旧A成员工作区有自己的未提交工作，不得修改。
- 以当前`git log`、远端ref及`verification/RESEARCH_SNAPSHOT.json`确定后续数学检查点；文件哈希与Git对象共同绑定版本。

恢复时先运行只读`git status --short --branch`、`git log -5 --oneline`，再fetch主分支和本分支。若发现别人修改，保留并核对，不reset、不强推、不替换其他工作目录。用户只授权本分支的研究检查点，未授权学术投稿或共享协调文件改动。

## 已完成，勿从头重做

1. 15算法机会调查：[RESEARCH_OPPORTUNITIES.md](RESEARCH_OPPORTUNITIES.md)。
2. ChaCha指定all-XOR掩码：标准32个输出位有闭式；固定首字有O(r)公式和完整符号分类；任意合法位/旋转有四状态精确求和。
3. 独立原字枚举、两份基本证明、后续文稿审读、标准160个有理数双实现对照已经完成。状态以[CLAIMS.md](CLAIMS.md)、[PROGRESS.md](PROGRESS.md)和[RESULTS.md](projects/chacha-three-add/RESULTS.md)为准。
4. 原创性没有通过。M0与普通状态法已有先行；不能把正确性当新颖性。没有L3/L4或完整ChaCha20攻击。

## 当前剩余工作

先完成基于既有Mealy矩阵的更强计算基线。Literature Agent推导可逆前缀流式算法；Research Agent实现和Verification Agent审查分别只追加新文件。当前已保存的逐矩重算程序成本为O(n²)算术，新前缀目标是O(n)算术与O(n)辅助位；在新代码/证明实证完成前只能称目标，不声称已改进。

对照`literature/METHOD_COMPARISON.md`（若已在后续检查点中出现）评估该模型是否只是旧定理的直接应用。缺失Okada、Li等近邻全文时，保留未定，不重复宣称“首次”。随后按[ROADMAP.md](ROADMAP.md)进行固定输入分布的必要性评估或转向；先写具体数学目标、现有基线和失败标准，再投入计算。

## 复现命令

进入`workstreams/CRYPTO/projects/chacha-three-add/`：

```sh
python experiments/exact_signed.py --max-n 5 --output experiments/results/exact_signed_max5.json
python verification/independent_verify.py
python verification/general_independent_verify.py
python tooling/exact_dp.py --check --standard-table --output tooling/results/dp_all_bits.json
python tooling/cross_check_standard.py
python tooling/check_upper_formula.py
```

这些命令会生成新的时间戳与记录。先检查保存的SHA与证据，只有存在具体复核风险或代码变更时才重复运行。源码无采样；不要把小参数穷举扩大到32位。文稿与记录中的旧绝对路径标明实际历史执行环境；脚本本身一般按自身文件位置定位附件。

## 发表与权限

允许正常理论、实验、独立审查和本研究分支提交，不需要再问“是否继续”。不向主分支、他人成员分支或其他目录写入。未经用户另行明确授权，不联系作者、不发布学术预印本、不注册DOI、不投稿。记录可以推送到用户已明确授权的研究分支。
