# Week 1 / Day 1：最小闭环问答总结（本次对话）

对应学习计划：[week1.md]

## 最小闭环（你跑通的那次 terminate）

- 入口：`main.py` 创建并运行 agent：`agent = await Manus.create()` → `await agent.run(prompt)`
- 主循环：`BaseAgent.run()` while：每轮 `current_step += 1` → `await self.step()`
- step 骨架：`ReActAgent.step()`：先 `think()`，`think()` 返回 True 才 `act()`
- think（Manus → ToolCallAgent）：`Manus.think()` 做一层上下文处理，然后 `super().think()` 进入 `ToolCallAgent.think()` 调 LLM 产出 `content/tool_calls`，并把 assistant 消息写入 memory
- act：消费 `self.tool_calls`，逐个执行 `execute_tool()`，把 tool 结果写成 tool_message 回 memory，返回本 step 的文本结果
- 终止：`execute_tool()` 内部执行到特殊工具 terminate 时把 `state=FINISHED`，run 的 while 条件失效 → run 结束
- 清理：`main.py` finally 里总会 `await agent.cleanup()`；`ToolCallAgent.run()` 自己也用 `finally` 确保 cleanup

## 关键知识点（按你问的问题整理）

### 1）要不要学 agent 是怎么创建的？

- 第一周不必深挖到能改造；但要知道 `Manus.create()` 有副作用（例如连接 MCP、标记初始化完成），影响“是否准备好”，不影响“方法派发走哪一个实现”。

### 2）run() 进 while 后执行哪个 step()？为什么我跳到基类 step？

- `BaseAgent.run()` 调用的是 `self.step()`（动态派发）。
- `BaseAgent.step` 是抽象方法（接口），IDE 容易先跳到接口定义；实际运行会落到继承链上最近的具体实现：`ReActAgent.step()`。

### 3）走哪个 step，是看怎么实例化 agent 吗？

- 不是看 `Manus()` vs `Manus.create()`，而是看实例真实类型（MRO）。创建方式通常只影响初始化是否做完，不改变方法解析顺序。

### 4）继承链与动态派发（你总结的那条）

- 继承链：`Manus` → `ToolCallAgent` → `ReActAgent` → `BaseAgent`
- `Manus.step()` 实际走 `ReActAgent.step()`，但 `think/act` 仍按动态派发：`think` 命中 `Manus.think`，`act` 命中 `ToolCallAgent.act`

### 5）为什么是 super().run()？如果本身也有 run 呢？

- `ToolCallAgent.run()` 的目的：复用父类的主循环（最终是 `BaseAgent.run()` 的 while），自己只额外包一层 `finally cleanup` 保障资源清理。
- 在 `ToolCallAgent.run` 内部调用 `super().run()` 是“跳过当前类”，调用继承链上下一个类提供的 `run` 实现，不会递归调用自己。

### 6）think：只返回 bool 吗？后面用什么信息？

- 返回值是 bool（控制 step 是否进入 act）。
- 但 think 还会“产出后续要用的信息”，主要靠副作用：
  - 更新 `self.tool_calls`，供 act 消费
  - 把 assistant 消息写入 memory，供下一轮 think 当上下文
  - 在 messages 里追加 next_step_prompt（作为 user message）
  - 某些异常路径会设置 `state=FINISHED` 终止执行

### 7）Token usage 日志在哪里打印？是不是 act？

- 不是 act，是 think 阶段 `llm.ask_tool()` 调用 LLM 返回后，`LLM.update_token_count()` 打印的。

### 8）act 的逻辑分支分别是什么？

- 分支 A：没有 tool_calls
  - `tool_choices == REQUIRED` → 抛错
  - 否则 → 直接返回最后一条 message 的 content（当作本 step 输出）
- 分支 B：有 tool_calls
  - 循环执行每个 tool_call：`execute_tool` →（可截断 max_observe）→ 写 tool_message 回 memory → 收集 result → join 返回

### 9）terminate 参数解析报错那段日志是怎么走到的？

- act → execute_tool → `json.loads(arguments)` 抛 `JSONDecodeError` → 捕获后返回 `Error: ...Invalid JSON format` 字符串 → act 仍把它写回 tool_message。
- terminate schema 期望 `{"status": "success"|"failure"}`（字符串枚举），缺引号就会触发 JSON 解析失败。

### 10）act 结束是不是第一轮循环也结束？

- act 结束 = 这一轮 step 结束，控制权回到 `BaseAgent.run()` 的 while。
- run 是否继续取决于 while 条件：`current_step < max_steps` 且 `state != FINISHED`；terminate 会把 `state=FINISHED`，所以通常一轮就结束整个 run。
