# 第 3 周：记忆系统 (Memory System) 🧠

## 本周目标
- 理解 Agent 的“大脑”是如何存储对话历史的。
- 掌握 `Message` 的四种角色 (`system`, `user`, `assistant`, `tool`) 及其数据结构。
- 理解 `Memory` 类如何管理上下文窗口 (Context Window)。
- 动手验证：手动构建 Memory 并观察 LLM 的反应。

## 推荐阅读顺序
1. `app/schema.py` (重点关注 `Message` 类和 `Memory` 类)
2. `app/agent/toolcall.py` (看 `act` 方法是如何往 memory 里写 `tool_message` 的)
3. `app/llm.py` (看 `ask_tool` 是如何把 memory 转换成 LLM 请求的)

## 本周关键点 (必须搞懂)
- **Message 的多态性**: 为什么 `tool_calls` 和 `content` 可以同时存在？
- **ToolMessage 的闭环**: 为什么 `tool_message` 必须包含 `tool_call_id`？
- **上下文管理**: 当对话太长时，OpenManus 是怎么处理的？(查看 `Memory.add_message` 的截断逻辑)

## 实战练习 (本周主线)

### 练习 A: 手搓一段对话
目标：不启动 Agent，直接使用 `Memory` 和 `LLM` 类来完成一次“伪造”的对话历史回放。
1. 创建一个 `Memory` 实例。
2. 手动塞入：
   - System: "You are a calculator."
   - User: "1+1=?"
   - Assistant: (ToolCall: python_execute("1+1"))
   - Tool: (Result: "2")
3. 调用 `llm.ask_tool(memory.messages)`，看看 LLM 会不会回答 "The result is 2."

### 练习 B: 记忆压缩 (进阶)
目标：给 Memory 增加一个 `summarize` 功能。
- 当消息超过 10 条时，把前 5 条总结成一句话 "Previous summary: ..." 放在开头。

## 每日安排
- **Day 1**: 精读 `app/schema.py`，理解 Message 和 Memory 的定义。
- **Day 2**: 实战练习 A，手动构建对话链。
- **Day 3-4**: 深入研究 `ToolCallAgent` 里的记忆读写逻辑。
- **Day 5**: 总结与复盘。
