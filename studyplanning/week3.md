# 第 3 周：Flow（规划与多 Agent 编排）

## 本周目标
- 跑通 Planning Flow，理解“先计划、再执行、再标记状态”的闭环
- 读懂 Flow 与 Agent 的职责边界：Flow 负责 orchestration，Agent 负责执行能力
- 能做一个小改动：让不同类型 step 选择不同 executor agent

## 推荐阅读顺序
- `run_flow.py`
- `app/flow/base.py`
- `app/flow/planning.py`
- `app/tool/planning.py`

## 本周关键点（必须搞懂）
- PlanningFlow 如何创建 plan（LLM + PlanningTool）
- 如何找到当前待执行 step，并标记 step_status
- executor 的选择策略在哪里扩展（get_executor）

## 实战练习（本周主线）
### 练习 A：改造 executor 选择
目标：让计划 step 的类型（例如 `[SWE]`、`[SEARCH]`）映射到不同 agent 执行。

建议路径：
- 在 plan step 文本中用 `[AGENT_NAME]` 或 `[TYPE]` 标记
- 在 `get_executor(step_type=...)` 增加选择规则
- 观察：不同 agent 的 available_tools 与 system_prompt 会如何影响执行风格

### 练习 B：输出可追踪的执行结果
目标：让你能从最终输出反向追踪每个 step 的执行过程。
- 每个 step 的输出包含：step 文本、选择的 executor、执行结果摘要

## 每日安排（建议 1–2 小时/天）
- Day 1：跑通 `python run_flow.py`，观察计划生成与执行循环
- Day 2：精读 PlanningFlow.execute 与 step 状态机
- Day 3–4：实现 executor 选择改造并跑通
- Day 5：复盘：Flow 与 Agent 的边界与扩展点

## 本周验收
- 能解释：为什么需要 Flow（而不是只靠一个 Agent 步进）
- 能完成一次“多 agent 分工”的端到端执行并可回放

