# 公开原文可获得性检查

检查日期：2026-10-11 UTC。执行者：`survey_symmetric`。本记录只回答来源能否取得、版本能否固定、实例在哪里；不产生新的密码分析结论。

## 结论与研究边界

三项优先来源中，两篇 ePrint 的摘要和版本说明可读，但 PDF 均一次返回 403。对应的 Springer 正式主文均显示订阅预览，本轮没有取得主文全文。**两篇正式版本的官方补充 PDF 已公开取得，保存了字节哈希，且定位到实际差分路径和有限实例。** Qin 等人的公开副本可提供论文全文的 HTML 提取文本；其 PDF 下载入口一次失败，未能固定 PDF 字节版本。

检查临结束时，主 Agent 从作者仓库发现一个新的 SAC 2026 官方预印论文链接，并明确追加一次访问任务。**该 35 页完整论文 PDF 已成功取得并固定哈希**；这是额外来源，不改变前两篇主文仍未取得的事实，详见第 4 节。

这些材料使后续能够从实际公布的实例开始准备复现。取得补充材料、定位章节、验证文件哈希，均不等于复现攻击或审定其数学论证。尚未启动路径搜索、χ-DDT 枚举、秩优化或代码执行。

| 来源 | 正文状态 | 已固定的公开材料 | 当前可操作程度 |
|---|---|---|---|
| ePrint 2024/1136 / CRYPTO 2024 | 主文未取得、未通读 | 正式版补充 PDF，10 页 | 有 GreedyPIDS 伪代码、路径及小状态碰撞实例；主文定义仍需补齐 |
| ePrint 2025/439 / EUROCRYPT 2025 | 主文未取得、未通读 | 正式版补充 PDF，24 页 | 有 PIDS、具体路径与小状态原像实例；与 ePrint 修订版的差异未核 |
| Qin 等，ToSC 2025(3) | 可读公开全文提取文本；本轮只核相关章节，未通读 | PDF 未取得；无 PDF 哈希 | 已知实际章节、图表、匹配方程与作者代码入口；图形和版本冻结仍不足 |
| Yan–Bao–Li，SAC 2026 官方预印版本 | 完整 PDF 已取得；本轮只做目录与实例定位，未通读 | 完整 PDF，35 页 | 有实际路径、逐 Sbox 方程选择、算法与源码链接；尚未复现或独立审查 |

## 1. CRYPTO 2024：概率线性化

Zhongyi Zhang、Chengan Hou、Meicheng Liu，*Probabilistic Linearization: Internal Differential Collisions in up to 6 Rounds of SHA-3*。

- [ePrint 2024/1136](https://eprint.iacr.org/2024/1136)：网页标为 CRYPTO 2024 正式论文的 **minor revision**；接收日期 2024-07-12，批准日期 2024-07-15。此为网页版本说明，不代表已核对全文修订差异。
- [正式发表页面](https://link.springer.com/chapter/10.1007/978-3-031-68385-5_8)：LNCS 14923，页 241–272，首次上线 2024-08-17。页面正文区域仅供订阅预览。
- [ePrint PDF](https://eprint.iacr.org/2024/1136.pdf)：一次 HTTP 403，停止该入口。
- [官方补充 PDF](https://media.springernature.com/original/springer-static/esm/chp:10.1007%2F978-3-031-68385-5_8/MediaObjects/635505_1_En_8_MOESM1_ESM.pdf)：从正式发表页面的补充材料链接发现，公开 HTTP 200。

### 固定版本

| 字段 | 实际值 |
|---|---|
| 缓存文件 | `workstreams/CRYPTO/.local-cache/keccak-source-access/supp2024.pdf` |
| 获取请求起始时间 | `2026-10-11T08:06:38.053641+00:00` |
| 大小 | 463,732 字节 |
| PDF 实测页数 | 10 |
| SHA-256 | `486ed9c6d706ac04214d978f04bc594f75060bc3e58708243910a1e904a12c7d` |
| PDF 内 CreationDate | `D:20240715045359Z` |
| PDF 内 ModDate | `D:20240715125547+08'00'` |

PDF 内日期只是文件元数据，不是独立认证的发布或修订日期。

### 实例精确位置

下列页码均为补充 PDF 的物理页序，从 1 开始；该 PDF 的印刷页码与物理页序一致。

- **附录 A，第 1 页**：GreedyPIDS 伪代码，包括方程系统分块和秩比较步骤。主文符号定义仍不可省略。
- **附录 B，第 2–4 页**：Characteristic 1–3。第 2 页对应 5 轮 SHA3-384 的路径，第 3 页对应 6 轮 SHAKE256 的路径，第 4 页为较小状态 `Keccak[240,160]` 的路径。路径给出与端到端攻击轮数不是同一口径，应沿用各自图注。
- **附录 E，第 7 页**：给出 `Keccak[r=240,c=160,nr=5,d=96]` 的两块消息碰撞实例及中间状态。它是公开既有实例，可作为将来的复现输入；本轮未验证碰撞。第 2 页明确了十六进制、小端和 `-` 代表零半字节的记法。

## 2. EUROCRYPT 2025：内部差分原像攻击

同三位作者，*Preimage Attacks on up to 5 Rounds of SHA-3 Using Internal Differentials*。

- [ePrint 2025/439](https://eprint.iacr.org/2025/439)：网页标为 EUROCRYPT 2025 正式论文的 **major revision**；接收日期 2025-03-07，批准日期 2025-03-10。
- [正式发表页面](https://link.springer.com/chapter/10.1007/978-3-031-91107-1_12)：LNCS 15601，页 333–363，首次上线 2025-04-27；主文为订阅预览。
- [ePrint PDF](https://eprint.iacr.org/2025/439.pdf)：一次 HTTP 403，停止该入口。
- [官方补充 PDF](https://media.springernature.com/original/springer-static/esm/chp:10.1007%2F978-3-031-91107-1_12/MediaObjects/646527_1_En_12_MOESM1_ESM.pdf)：从正式发表页面补充材料链接发现，公开 HTTP 200。

### 固定版本

| 字段 | 实际值 |
|---|---|
| 缓存文件 | `workstreams/CRYPTO/.local-cache/keccak-source-access/supp2025.pdf` |
| 获取请求起始时间 | `2026-10-11T08:06:52.295238+00:00` |
| 大小 | 839,635 字节 |
| PDF 实测页数 | 24 |
| SHA-256 | `377684a9fa1809f217c4bd4930dff9d623b482b92b58f15b4cb9d7f406c6147f` |
| PDF 内 CreationDate | `D:20250402163713+05'30'` |
| PDF 内 ModDate | `D:20250402163714+05'30'` |

### 实例精确位置

物理第 1 页对应印刷页 31，之后顺延；不要与 Springer 主文章节的卷内页码混用。

- **附录 C，物理第 3–4 页／印刷页 33–34**：`Keccak[r=704,c=96,nr=4]` 的实际原像实验说明；第 4 页列出五个消息块与全 1 目标摘要。这是 800 位状态实例，不能称为标准 1600 位 SHA-3 的同参数实验。
- **附录 E，物理第 6 页／印刷页 36**：PIDS 伪代码。
- **附录 G，物理第 8–14 页／印刷页 38–44**：Characteristic 1–7。其中 **Characteristic 6 在物理第 13 页／印刷页 43**，对应上述 800 位实例。

执行前须核对原图而不是直接信任 PDF 文本提取。附录 C 参数列表末项提取为 128，而 Characteristic 6 图注末项提取为 125；本轮没有判定它是版本、符号、提取问题或原文差异。不得自行择一补全实验，更不得据此宣布发现论文错误。正式补充文件也不能自动当作 ePrint major revision 的同字节附录。

## 3. Qin 等：ToSC 2025 线性抵消

Lingyue Qin、Boxin Zhao、Qingliang Hou、Keting Jia、Gaoli Wang、Xiaoyang Dong，*Linear Cancellations in the MitM Attacks on Sponge Functions*。

- [DOI](https://doi.org/10.46586/tosc.v2025.i3.633-692)：本轮一次返回工具不可访问错误，未重试。针对 ToSC 的定向搜索还报告 `tosc.iacr.org` 被 robots.txt 阻止；没有枚举或猜测数字下载端点。
- [作者机构记录](https://pure.ecnu.edu.cn/zh/publications/linear-cancellations-in-the-mitm-attacks-on-sponge-functions/)：可读；发表日期 2025-09-25，卷 2025、期 3、页 633–692，共 60 页。该页数来自书目信息，**未通过 PDF 页对象实测**。
- [公开全文副本页面](https://www.researchgate.net/publication/395901860_Linear_Cancellations_in_the_MitM_Attacks_on_Sponge_Functions)：可读论文全文的 HTML 提取文本，标注 CC BY 4.0，包含主文章节与补充材料。本轮只定位相关部分；不是通读审查。页面“Download full-text PDF”入口一次内部错误，未尝试另一重复下载按钮。

正文所示 DOI 与作者列表和机构记录一致；上传身份及 PDF 字节版本未独立固定。**PDF SHA-256：不可提供，因为未取得 PDF 字节。** 不以摘要哈希、HTML 片段哈希或题名相同替代论文版本哈希。

### 已定位的后续入口

- **第 6.1 节、图 10、补充材料 A.1 的图 13 与式 (18)**：4 轮 `Keccak[1024]` 的具体状态设置与 12 个匹配方程。
- **补充材料 B.3、图 19–20**：`Keccak[768]` 的低内存配置。
- **补充材料 C、表 5**：3 轮 Ascon-Xof 的 32 位部分目标原像实例；属于跨算法的方法复现候选，不是本 Keccak 主线的新结果。
- 论文第 6 节及实验段明确给出作者代码入口：[qly14/Sponge_MitM_Linear_Cancellation](https://github.com/qly14/Sponge_MitM_Linear_Cancellation)。本轮未取得可审读源码及其 Commit SHA，未克隆、未执行。

提取文本丢失若干着色符号，不能据它重建位归属或彩色路径图。以上是章节定位，不是可立即运行的已审查复现包。

## 4. 新发现并成功取得的 SAC 2026 官方全文

Luhan Yan、Zhenzhen Bao、Huina Li，*Refining Probabilistic-Linearization TIDA for 5-Round SHA3-384 Collision Attacks*。

- [SAC 2026 官方预印论文 PDF](https://www.sacworkshop.org/SAC26/preproceedings/SAC2026_2-final50.pdf)：主 Agent 从作者仓库 README 发现后交给本 Agent，仅进行一次原始字节请求，成功 HTTP 200。
- [SAC 2026 官方演讲](https://sacworkshop.org/SAC26/talks/50-2.pdf)：主 Agent 报告共 27 张幻灯片，本 Agent 未重新取得或核计该演讲。
- [作者代码仓库](https://github.com/KeccakInternalDiff/keccak-internal-differential)：主 Agent 通过只读连接器检查为 public、MIT、main，并分别核对 `/git/ref/heads/main` 与 `/commits/main`：**Commit SHA** 为 `259d33b3eebfb6c3777c2bbf6299a47335d5ed2a`，该 commit 的 **tree SHA** 为 `4bad4b3fa12ee4f0639b2b4c1e335c3e65358d0e`。两者均为主 Agent 提供的已核对象信息，本 Agent 未独立访问 API、下载或执行代码；它们不是论文哈希。

版本范围仅认定为官方 `preproceedings` 路径所提供的 PDF；没有把它当成已核对的 Springer 最终排印版，也未进行与 ePrint 2026/2090 的字节比对。

| 字段 | 实际值 |
|---|---|
| 缓存文件 | `workstreams/CRYPTO/.local-cache/keccak-source-access/sac2026_2-final50.pdf` |
| 获取请求起始时间 | `2026-10-11T08:11:10.077171+00:00` |
| 大小 | 821,976 字节 |
| PDF 实测页数 | 35 |
| SHA-256 | `da997847e94e3c6fda942af56956d101c17a3dfcaa7ddd25d5b573d4b9292645` |
| PDF 内 CreationDate 与 ModDate | `D:20260724135645Z` |

### 可操作位置

页码为 PDF 物理页序，从 1 开始；与本文印刷页码相同。

- **第 4.2 节，第 15–18 页，算法 1–2**：评价过程与 SA-PIDS；**第 4.3 节，第 18–19 页，表 3**：实验设置与比较。
- **第 5.3 节，第 23–25 页**：抽样与概率评估过程；不据标题或摘要改写其概率公式。
- **第 6 节，第 25–27 页，表 4**：实际攻击配置及比较；第 26 页给出作者代码链接。
- **附录 A，第 30 页，表 5**：文中使用的既有路径；**第 31 页，表 6**：逐活跃 Sbox 的方程选择，足以作为下一轮原文核对的明确入口。
- **第 33–34 页，算法 3–4**：文中列出的既有 TIDA／Greedy-PIDS 基线。

完整 PDF 已存入忽略缓存，已逐页提取文本。本轮只确认可获得性及上述位置，未审定其定理、数值、代码或攻击复杂度。当前项目的秩优化和投影想法与该论文高度接近，应由 Literature Agent 对照全文，不能将其已给出的内容重复认领为原创。

## 5. 缓存、执行证据与复核命令

### 存储与范围

唯一新增的可跟踪研究文档为本文件。第三方 PDF 和逐页提取文本均放在既有忽略目录 `workstreams/CRYPTO/.local-cache/keccak-source-access/`。下载前实际执行：

```text
git check-ignore -v workstreams/CRYPTO/.local-cache/keccak-source-access/supp2024.pdf
workstreams/CRYPTO/.gitignore:5:.local-cache/  workstreams/CRYPTO/.local-cache/keccak-source-access/supp2024.pdf
exit_code=0
```

未修改 `.gitignore`、ChaCha 文件、共享协调文件或 Git 历史。父 Agent 决定文档提交；缓存不应加入 Git。

### 实际执行

前两份文件各用 Python `urllib.request.urlopen(url, timeout=20)` 获取一次原始字节，要求 `%PDF-` 文件头，读取上限为 5,000,000 字节；然后用 `hashlib.sha256` 和 `pypdf.PdfReader` 计算哈希与页数。网页工具此前通过出版社明确链接成功解析相同 PDF。下载过程实际结束码为 0；两个响应都是 HTTP 200、`application/pdf`。随后的本地再哈希和下列断言命令均得到相同结果，结束码为 0。

追加的 SAC 官方全文采用相同获取与解析方法，读取上限为 8,000,000 字节，实际 HTTP 200、`application/pdf`，进程结束码为 0。每个成功文件只有一次 Python 网络获取；本地页数、哈希复核不请求网络。两次不同获取途径不构成独立数学验证。

环境实测于 `2026-10-11T08:08:43.320532+00:00`：Python 3.12.14，pypdf 6.10.0，Linux 6.18.44 x86_64、glibc 2.39。检查时仓库 HEAD 为 `59a24dc5c1afeaf481bb77ac7f2228465c821f3b`；这只是本次访问检查的工作树基点，不是任何第三方论文或代码的版本号。

以下只验证已有缓存，不重新请求失败来源，也不执行第三方代码：

```bash
python - <<'PY'
from pathlib import Path
from hashlib import sha256
from pypdf import PdfReader

base = Path('workstreams/CRYPTO/.local-cache/keccak-source-access')
expected = {
    'supp2024.pdf': (10, 463732,
        '486ed9c6d706ac04214d978f04bc594f75060bc3e58708243910a1e904a12c7d'),
    'supp2025.pdf': (24, 839635,
        '377684a9fa1809f217c4bd4930dff9d623b482b92b58f15b4cb9d7f406c6147f'),
    'sac2026_2-final50.pdf': (35, 821976,
        'da997847e94e3c6fda942af56956d101c17a3dfcaa7ddd25d5b573d4b9292645'),
}
for name, wanted in expected.items():
    path = base / name
    data = path.read_bytes()
    found = (len(PdfReader(path).pages), len(data), sha256(data).hexdigest())
    assert found == wanted, (name, found, wanted)
    print(name, found)
PY
```

## 6. 有界检查停止条件

已完成三项优先来源的公开入口检查、两份补充 PDF 和一份追加官方完整论文的版本固定，以及实际实例位置的移交。所有失败入口都已停止，不登录、不付费、不联系作者、不重复请求失败 PDF。

**本轮结束，不启动新的数学目标。** 后续若使用具体实例，应首先补齐主文定义、核对原图与版本差异，并完成已有结果查重；不能把材料可获得性记录当成数学研究增量。
