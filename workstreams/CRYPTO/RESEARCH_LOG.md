# Research log

## 2026-10-11 — 启动与选题

基线 a8c3f22e26b08c2d294e2b0e6df2d9cfa430cda0。已有 A checkout 含未提交/未推送工作，未编辑；新 clone 上创建 partner/dist-crypto。git fetch origin 返回0。远端 workstream 文件名检查完成；广泛 git-grep 引发逐 blob 下载，数分钟后中断，不声称穷尽分支内容。

用户目录隔离要求优先；本目录承载检查点，不改共享 coordination 或主 README。

先行文献已经包含连续模加依赖、half-quarter 精确差分和 toy 相关性偏差。首项具体目标缩小到三加法输出的有符号相关公式、重叠位区和固定常量分布。证明、程序正确性与历史原创性分开验收。

初始化记录生成曾因相对父路径指向错误返回1；已改用绝对路径重建来源文件。这是文件准备错误，不涉及数学实验。
