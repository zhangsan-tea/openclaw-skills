---
tags:
  - 自建skill
  - 平台集成
  - figma
  - 设计
  - design-to-code
created: 2025-07-12
updated: 2025-07-12
status: 有效
maintainer: WorkBuddy
source: skills/figma-connector/
---

# figma-connector

> Figma API 连接器 — 获取设计数据、导出图片、生成 React/Tailwind 代码

## 基本信息

| 属性 | 值 |
|------|-----|
| 版本 | 2.1.0 |
| 作者 | CodeBuddy AI |
| 创建日期 | 2026-02-01 |
| 最后更新 | 2026-02-05 |
| 触发关键词 | Figma、设计稿、design-to-code |

## 核心能力

1. **获取设计数据** — 通过 Nodes API 获取节点 JSON
2. **导出图片/SVG** — 通过 Images API 导出图标和素材
3. **获取样式** — 获取颜色、文本样式
4. **Design-to-Code** — Figma → React / Tailwind 代码生成

## 认证方式

使用 OAuth Token（`Authorization: Bearer` header），**非** Personal Access Token（`X-Figma-Token`）：

```bash
source <skill-directory>/scripts/get_token.sh figma && export FIGMA_TOKEN && \
  curl -H "Authorization: Bearer ${FIGMA_TOKEN}" \
  "https://api.figma.com/v1/files/{file_key}/nodes?ids={node_id}"
```

> ⚠️ Token 获取和 API 调用必须在**同一条命令**中完成。

## URL 解析

```
https://www.figma.com/design/JcHJusqhdcLvTpayC8MwXq/文件名?node-id=1348-168
                             ↑ file_key                      ↑ node_id
```

## 核心 API

| 操作 | API |
|------|-----|
| 获取文件 | `GET /v1/files/{file_key}` |
| 获取节点 | `GET /v1/files/{file_key}/nodes?ids={ids}` |
| 导出图片 | `GET /v1/images/{file_key}?ids={ids}&format=svg` |
| 获取样式 | `GET /v1/files/{file_key}/styles` |
| 获取组件 | `GET /v1/files/{file_key}/components` |
| 获取变量 | `GET /v1/files/{file_key}/variables/local` |

## Design-to-Code 流程

```
1. 解析 URL → file_key + node_id
2. 调用 Nodes API → 获取 JSON
3. 保存 JSON → 分析结构
4. 找 VECTOR 节点 → 收集图标 ID
5. 调用 Images API → 下载 SVG
6. 生成代码 → HTML/CSS/React
```

## 重要提示

### 1. JSON 数据量大
Figma 返回的 JSON 非常详细，单个组件可能 5000+ 行。建议保存到文件。

### 2. 图标必须单独下载
`VECTOR` 类型节点不包含 SVG 路径数据，必须通过 Images API 导出。

### 3. 颜色值转换
Figma 颜色是 0-1 浮点数，需转换为 hex：
```js
// { r: 0.772549, g: 0.772549, b: 0.772549 } => #C5C5C5
function rgbaToHex({ r, g, b }) {
  const toHex = n => Math.round(n * 255).toString(16).padStart(2, '0');
  return `#${toHex(r)}${toHex(g)}${toHex(b)}`;
}
```

### 4. Auto Layout → Flexbox

| Figma | CSS |
|-------|-----|
| `layoutMode: "HORIZONTAL"` | `flex-direction: row` |
| `layoutMode: "VERTICAL"` | `flex-direction: column` |
| `itemSpacing` | `gap` |
| `primaryAxisAlignItems: "CENTER"` | `justify-content: center` |
| `counterAxisAlignItems: "CENTER"` | `align-items: center` |

## 错误处理

- **偶发 403**：重试 2-3 次，通常是临时性问题
- **持续 401/403**：提示用户重新授权 Figma

## 源码文件

```
figma-connector/
├── SKILL.md                 # Skill 定义
└── scripts/
    ├── figma_api.sh         # API 调用脚本
    └── get_token.sh         # Token 获取
```
