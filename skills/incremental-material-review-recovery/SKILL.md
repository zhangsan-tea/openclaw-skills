---
name: incremental-material-review-recovery
description: Reconcile an incremental knowledge-base material ledger after disputed exclusions or failed extraction. Use when the review requires duplicate proof, archive unpacking, source recovery from WeCom Drive, OCR of scanned evidence, and a regenerated full HTML review ledger before any intake action.
description_zh: 增量材料复核恢复
description_en: Incremental material review recovery
disable: false
agent_created: true
---

# 增量材料复核恢复

## 何时使用

当用户要求复核增量材料的“排除/提取失败/扫描件/压缩包”结论，且必须先完成内容读取、去重、解包或 OCR，再更新全量审阅 HTML 和决策台账时使用。

## 工作步骤

1. **冻结入库动作**：先声明本轮仅做审阅修正；未获确认前，不转换、脱敏、入库、图谱挂接或上传。
2. **读取三类台账**：主入库台账、边界复核台账、当前全量审阅决策 CSV。以主台账全量数为准，建立唯一键 `relative_path`。
3. **用正文而非文件名做去重**：
   - 可读提取文本用 SHA-256 证明完全重复；
   - 近重复用段落级 diff 判断差异是否仅为日志、截图、标题或空行；
   - 规则主体有实质差异才保留平行候选。
4. **压缩包必须前置解包**：读取既有解包 manifest；先找回原压缩包，再用已知、显式标注的密码尝试解开。不得执行解出的可执行文件或样本。解包失败必须标为“待密码解包”，不能伪装成“已检查后排除”。
5. **修正“提取失败”**：按四类落位：已有规范/AI 可读版本覆盖、微盘已定位待下载、恢复后确为空表/空模板、仍需源件。不要继续使用笼统的“文件损坏/无内容”。
6. **扫描件先 OCR**：PDF 按页渲染后使用中文 OCR；图片直接 OCR。将一次性审批/登记台账与包含流程、审核、控制、评测、应急、治理规则的内容分开判定。
7. **重建四态审阅集**：`已入库`、`建议补充入库（待确认）`、`待复核`、`继续排除`。四态总数必须严格等于全量材料数。
8. **产出 HTML + CSV**：HTML 每条应有状态、子状态、理由、来源路径、摘要及可用的本地原文/OCR 链接；CSV 与 HTML 的材料数、状态计数、卡片数必须一致。
9. **等待确认**：用户确认后，才按已确认候选进入去重、脱敏、转换、正式 AI 语料入库、知识图谱智能消化和 iWiki 同步。

## 关键陷阱

- macOS 中文文件名须先做 NFC 标准化，避免“文件存在但查不到”。
- “人事/展示/宣传”不构成自动排除理由；正文中的制度、规则、方法才是判断对象。
- 压缩包的外层条目和其中解出的材料可能同时存在于台账，状态要一致且避免重复计数。
- OCR 未完成或源件暂不可读时，状态应为“待复核”，不要直接驳回。
- 对恶意样本或受控检查工具，仅查看清单/说明，不执行文件。

## 验证清单

- [ ] 全量 HTML 卡片数 = 决策 CSV 行数 = 主台账总数。
- [ ] 四态计数之和等于总数。
- [ ] 每个“重复”结论有 hash 或段落差异依据。
- [ ] 每个压缩包都有“已解开/待密码”的明确状态。
- [ ] 每个扫描件都已 OCR 或明确说明源件恢复阻碍。
- [ ] 未确认候选没有进入正式入库或图谱/ iWiki 流程。
