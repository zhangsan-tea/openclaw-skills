---
name: openclaw-local-noauth-switch
description: 将 OpenClaw 网关切换为“仅本机可访问 + 免鉴权”的标准流程。适用于用户明确要求本机浏览器直接连网关且不想输入
  token/密码的场景；自动处理与 Tailscale 暴露冲突的配置并重启网关验证。
description_zh: OpenClaw 本机免鉴权
description_en: OpenClaw Local NoAuth
agent_created: true
---

# openclaw-local-noauth-switch

## When to use
- 用户明确说“改为本机免鉴权 / 不要 token / 不要密码”。
- 网关运行在本机（loopback），希望浏览器直接访问 `http://127.0.0.1:18789/`。
- 当前配置是 `gateway.auth.mode=token/password`，导致控制台要求令牌或密码。

## Steps
1. 先备份配置：
   - `cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak_noauth_$(date +%Y%m%d_%H%M%S)`
2. 编辑 `~/.openclaw/openclaw.json`：
   - 设置 `gateway.auth.mode` 为 `none`
3. 处理冲突（关键）：
   - 如果 `gateway.tailscale.mode` 是 `serve` 或 `funnel`，必须改为 `off`，否则配置校验会失败。
4. 重启网关：
   - `launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway`
5. 校验生效：
   - `openclaw config validate`
   - `openclaw dashboard --no-open`
   - 预期无 token 要求，输出普通本地 URL。

## Pitfalls
- `gateway.auth.mode=none` 与 `gateway.tailscale.mode=serve/funnel` 不兼容，会报：
  - `gateway.auth.mode=none cannot be used with gateway.tailscale.mode=serve ...`
- 免鉴权仅建议用于 `gateway.bind=loopback` 的本机场景；不要用于公网或 tailnet 暴露。
- 改完不重启网关通常不会立即生效。

## Verification
- `openclaw config validate` 显示 `Config valid`
- `openclaw dashboard --no-open` 正常输出 URL 且不提示 token auto-auth
- 浏览器打开 `http://127.0.0.1:18789/` 不再出现“需要身份验证”