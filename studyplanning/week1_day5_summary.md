# Week 1 / Day 5：复盘与 Memory 机制深度解析

对应学习计划：[week1.md](week1.md)

Day 5 的核心任务是把前 4 天的碎片拼成完整的 Agent 运行时图景，特别是通过“伪日志复盘”练习，彻底搞懂了 Memory 的生长规律和 Role 的接力机制。

## 核心对话复盘

### 1. 伪日志填空挑战 (Mental Sandbox)

我们通过模拟“查文件”场景，还原了 Memory 的真实变化过程：

-   **Step 1 Think**: LLM 决定调工具。
    -   Role: `assistant`
    -   Content: `null` (或思考过程)
    -   **ToolCalls**: `[{"name": "bash", ...}]`
-   **Step 1 Act**: 工具执行完毕。
    -   Role: **`tool`** (你的答案：Tool，正确！)
    -   Content: `result` (你的答案：result，正确！)
    -   ToolCallId: `command.id` (必须与 Think 阶段的 ID 对应)
-   **Step 2 Think**: LLM 总结回答。
    -   Role: `assistant`
    -   Content: "当前目录下有..."
-   **Terminate 场景**:
    -   Role: `tool` (因为 terminate 也是工具)
    -   State: `FINISHED` (触发主循环退出)

### 2. Memory 与 Role 的深度解析 (Q&A)

你提出了两个非常关键的疑问：

-   **Q1**: 用户提示词进来，会变成 `user` 格式吗？
    -   **A**: 是的。`BaseAgent.run` 会调用 `update_memory("user", request)`，底层封装为 `{"role": "user", "content": ...}`。
-   **Q2**: 每次大模型反馈、Tool 回答，角色是怎么样的？
    -   **A**: 这是一个“接力赛”：
        1.  **User**: 提问 (Start)
        2.  **Assistant**: 想招/调工具 (Call)
        3.  **Tool**: 干活/反馈结果 (Result)
        4.  **Assistant**: 总结/回答 (Response)

## 关键知识点总结

### 1. Memory Snapshot (记忆快照)
一个标准的工具调用闭环在 Memory 中长这样：

```json
[
  {"role": "user", "content": "查文件"},
  {"role": "assistant", "tool_calls": [...]},  // 发起调用
  {"role": "tool", "tool_call_id": "...", "content": "file1.txt"}, // 工具结果
  {"role": "assistant", "content": "有 file1.txt"} // 最终回复
]
```

### 2. Stuck 检测的盲区
-   **检测逻辑**: `is_stuck` 检查最后一条消息内容是否与历史 `assistant` 消息重复。
-   **安全区**: 在 `Act` 阶段结束后，最后一条消息是 `tool` 角色。此时通常不会触发 Stuck（因为代码只统计 `assistant` 重复）。Stuck 更多发生在 LLM 连续输出重复文本且不调工具时。

### 3. Week 1 毕业总结
-   **Run Loop**: `IDLE` -> `RUNNING` -> `FINISHED`。
-   **Think**: 决定是否 Act，生成 `tool_calls`。
-   **Act**: 串行执行工具，捕获结果，写回 `tool` 消息。
-   **Tool**: 独立的类，通过 `ToolCollection` 查表调用，返回 `ToolResult`。

## 下周展望 (Week 2)
恭喜完成 Week 1！既然你已经掌握了 Agent 的“单兵作战”能力（Think/Act/Memory），下一周我们将挑战更复杂的场景：
-   **Planning**: 如何拆解复杂任务？
-   **Custom Tools**: 如何手写一个新工具？
-   **Browser Agent**: 它是怎么操控浏览器的？
