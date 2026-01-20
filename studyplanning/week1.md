# 第 1 周：跑通与读懂最小闭环

## 本周目标
- 跑通项目最小可用入口，知道一次请求从哪里进、在哪里循环、在哪里退出
- 读懂 Agent 的“状态机 + step-loop + memory”三件套
- 读懂 ToolCall 模式的 think/act：LLM 产出 tool_calls → 执行工具 → 写回 memory

## 推荐阅读顺序（只读这一条链）
- `main.py`
- `app/agent/manus.py`
- `app/agent/base.py`
- `app/agent/react.py`
- `app/agent/toolcall.py`

## 每日安排（建议 1–2 小时/天）
### Day 1：跑起来
- 运行：`python main.py --prompt "用一句话自我介绍并结束"`
- 观察：日志、是否进入多步循环、是否正常退出并 cleanup
- 记录：max_steps、AgentState 变化、memory 增长点

### Day 2：精读 BaseAgent.run
- 精读 `BaseAgent.run()` 的 while 循环、状态切换、stuck 检测
- 画图：`run -> step -> (think/act) -> memory` 的时序

### Day 3：精读 ToolCallAgent.think
- 搞清楚什么时候追加 `next_step_prompt` 到 messages
- 搞清楚 tool_choice 不同模式下的行为差异

### Day 4：精读 ToolCallAgent.act + execute_tool
- 搞清楚 tool_call.arguments 如何解析为 JSON
- 搞清楚工具执行结果如何被包装为 tool_message 写回 memory

### Day 5：复盘与输出
- 输出一页纸总结：
  - Agent 的核心循环是什么
  - memory 的结构与增长规律是什么
  - tool call 的输入/输出契约是什么

## 本周必做练习（最重要）
- 写一段“伪日志复盘”：
  - Step 1 到 Step N，每一步发生了什么（think/act/记忆写入）
  - 如果没有工具调用，act 返回什么

## 本周验收（做到即过）
- 能从源码解释：一次 prompt 如何进入 `BaseAgent.run()` 并终止
- 能从源码指出：assistant/tool 消息分别在哪里写入 memory
- 能用 5 句话讲清：ToolCallAgent 的 think/act 如何驱动工具执行

