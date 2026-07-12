---
tags:
  - 自建skill
  - web
  - 预览
  - 部署
  - supervisord
created: 2025-07-12
updated: 2025-07-12
status: 有效
maintainer: WorkBuddy
source: skills/preview/
---

# preview

> Web 项目预览 — 在沙箱中启动 Web 服务器并生成可访问的预览 URL

## 基本信息

| 属性 | 值 |
|------|-----|
| 作者 | CodeBuddy AI |
| 触发关键词 | 预览、preview、看效果、跑起来、deploy、give me a URL、show me the page |

## 核心原则

> ⛔ **绝对禁止自行构造预览 URL**。URL 必须通过 `notify` 脚本获取，域名和查询参数由运行时环境动态生成。

## 触发条件

- 用户要求预览页面或项目
- 用户要求部署并查看效果
- 创建/修改网页后用户想要查看
- 用户要求获取可访问的链接

## 服务策略

| 项目类型 | 方法 |
|----------|------|
| 静态 HTML | `python3 -m http.server <port>` |
| Vite / CRA / Vue CLI | `build` → 静态服务 `dist/` |
| Next.js | `next build && next start` |
| 自定义服务 | 生产模式 (`node server.js`) |

**重要**：WebSocket 不被代理，禁止使用开发服务器（`vite dev` / `next dev` / `webpack-dev-server`）。

## 关键流程

### 1. 启动服务（带休眠恢复）

使用 supervisord 管理服务进程，确保沙箱休眠/恢复后自动重启：

```bash
# 写入 program conf
cat > /usr/local/share/supervisor/preview-${PORT}.conf <<EOF
[program:preview-${PORT}]
command=<start-command>
directory=<project-dir>
autostart=true
autorestart=true
startsecs=2
startretries=3
stopsignal=INT
stopwaitsecs=10
stdout_logfile=/tmp/preview-${PORT}.log
stderr_logfile=/tmp/preview-${PORT}.log
redirect_stderr=true
environment=PATH="%(ENV_PATH)s",NODE_OPTIONS=""
EOF

# 应用配置
supervisord ctl reread
supervisord ctl update
supervisord ctl start preview-${PORT}
```

### 2. 获取预览 URL

```bash
<skill-directory>/notify <port>
```

`notify` 会输出包含正确 URL 的 JSON，必须直接使用该 URL。

### 3. 回复用户

使用 `notify` 输出的 URL，不要修改域名、scheme 或查询参数。

## 常见错误

| # | 错误 | 后果 |
|---|------|------|
| 1 | 忘记调用 `notify`，自行构造 URL | 域名错误 → 404 或 SSL 错误 |
| 2 | 使用 `localhost:8000` 回复 | 仅沙箱内可访问 |
| 3 | URL 路径放在 `?` 查询参数之后 | 路径被当作查询字符串 |
| 4 | 追加了不存在的文件路径 | 404 错误 |
| 5 | 双斜杠路径 (`//index.html`) | 路径解析错误 |
| 6 | 使用 `vite dev` / `next dev` | HMR WebSocket 失败 |
| 7 | BrowserRouter 无 fallback | 路径匹配失败 → 空白页 |

## 服务状态检查

| 状态 | 含义 | 处理 |
|------|------|------|
| `RUNNING` + `HTTP 2xx/3xx` | 服务健康 | ✅ 正常 |
| `RUNNING` 但 curl 失败 | 端口未监听或绑定错误 | 检查是否绑定 `0.0.0.0` |
| `STARTING`（超过 10s） | startsecs 未到 | 等待 2-3s 或查日志 |
| `BACKOFF` | 崩溃重试耗尽 | 查 `/tmp/preview-{port}.log` |
| `FATAL` | Supervisor 放弃 | 同 BACKOFF |

## 源码文件

```
preview/
├── SKILL.md          # Skill 定义
├── notify            # URL 生成工具（二进制）
└── notify.go         # notify 源码
```
