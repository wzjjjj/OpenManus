# 第 4 周：Sandbox / MCP（把 Agent 接到真实世界）

## 本周目标
- 理解并跑通隔离执行（Sandbox）或远程工具（MCP）中的一种
- 能解释三类工具接入方式的差异：本地工具 / Sandbox 工具 / MCP 工具
- 能做一个小扩展：新增一个只读工具并验证其可用性

## 路线选择（选其一优先做深）
### 路线 A：Sandbox（隔离执行）
- 入口：`sandbox_main.py`
- Agent：`app/agent/sandbox_agent.py`
- 重点理解：环境隔离、文件映射、网络权限、清理资源

### 路线 B：MCP（远程工具）
- 入口：`run_mcp.py`
- Agent：`app/agent/mcp.py`
- 重点理解：远程 tool schema 注册/刷新、调用与错误处理、网络边界

## 推荐阅读顺序
- Sandbox：`sandbox_main.py` → `app/agent/sandbox_agent.py` → `app/sandbox/*`
- MCP：`run_mcp.py` → `app/agent/mcp.py` → `app/mcp/*`

## 实战练习（本周主线）
### 练习 A：新增一个“只读信息工具”
目标：体验从 schema → 调用 → observation 回传的完整链路，同时避免写入与破坏性操作。

建议功能：
- 返回运行环境信息（例如 python 版本、工作目录、已启用的工具列表）

验证标准：
- 该工具能在你选择的路线中被调用（Sandbox 或 MCP）
- 失败路径能清晰回传错误信息，并且不会导致 agent 崩溃

### 练习 B：对比总结（写下来）
- 本地工具：最简单、最灵活，但权限边界需要你自己控制
- Sandbox：安全边界强，但引入环境复杂度与资源管理成本
- MCP：工具可服务化与复用，但有网络与协议复杂度

## 每日安排（建议 1–2 小时/天）
- Day 1：选路线并跑通入口脚本
- Day 2：精读关键 Agent（SandboxManus 或 MCPAgent）
- Day 3–4：实现“只读信息工具”并做成功/失败验证
- Day 5：写对比总结与下一步改进清单

## 本周验收
- 能说清：为什么要引入 Sandbox/MCP，它们解决了什么问题
- 能完成一个在 Sandbox 或 MCP 中可用的工具扩展

