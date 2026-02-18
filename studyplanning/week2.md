# 第 2 周：工具系统架构与设计模式深度解析

## 本周目标
- **架构视角**：理解 OpenManus 统一工具系统（Unified Tool System）的设计思想，掌握 **BaseTool**（标准化）、**ToolCollection**（调度器）与 **ToolResult**（结果封装）的交互机制。
- **代码能力**：深入 Python 的 **Pydantic** 高级用法（Schema 生成）、**Async/Await** 异步执行流、以及 **Magic Methods**（如 `__add__` 实现结果聚合）。
- **实战落地**：从 0 到 1 实现一个生产级工具，并验证其在 Agent "Think-Act-Observe" 闭环中的行为。

## 核心阅读材料（基于源码与技术解读）
1. **基础协议层**：
   - `app/tool/base.py`：**核心必读**。关注 `BaseTool` 如何利用 Pydantic 自动生成 JSON Schema；关注 `ToolResult` 的 `__add__` 方法如何实现多模态结果（Text + Image + System）的聚合。
2. **调度管理层**：
   - `app/tool/tool_collection.py`：关注 `to_params()`（Think 阶段：提供工具描述）与 `execute()`（Act 阶段：分发执行与错误兜底）。
3. **实现参考层**（对比不同类型的工具实现）：
   - `app/tool/bash.py`：系统命令执行工具（有副作用、流式输出）。
   - `app/tool/browser_use_tool.py`：浏览器操作工具（复杂依赖、多模态返回）。

## 架构设计关键点（深度思考）
在阅读源码时，请带着以下问题进行“代码审查”式学习：
1. **接口标准化**：`BaseTool` 如何通过 `ABC` (Abstract Base Class) 和 `Pydantic` 强制规范所有工具的输入输出？这种设计对扩展新工具有什么好处？
2. **结果封装模式**：`ToolResult` 为什么要区分 `output` (LLM 可见)、`error` (异常信息)、`base64_image` (视觉信息) 和 `system` (系统隐式信息)？
   - *思考*：当一个工具同时产生文本和截图时，Agent 是如何感知的？（参考 `ToolResult.__add__`）
3. **容错与防御**：在 `ToolCollection.execute` 中，是如何处理工具内部异常的？这种“沙箱化”执行对 Agent 的稳定性有何意义？

## 实战练习（由浅入深）

### 练习 A：复刻标准工具架构（基础）
目标：实现一个符合 OpenManus 标准的自定义工具 `SystemInfoTool`。
- **功能**：获取当前系统信息（OS 版本、Python 版本、内存占用）。
- **要求**：
  1. 继承 `BaseTool`。
  2. 使用 `Field` 定义清晰的参数 Schema（即使没有参数也要定义空 Schema）。
  3. 返回 `ToolResult`，尝试同时填充 `output`（给 LLM 看的总结）和 `system`（详细 JSON 数据）。

### 练习 B：探索 ToolResult 的组合逻辑（进阶）
目标：验证 `ToolResult` 的运算符重载特性。
- **操作**：编写一段测试代码，手动创建两个 `ToolResult` 对象（一个含文本，一个含图片或系统信息），将它们相加 `result1 + result2`。
- **观察**：检查合并后的 `ToolResult` 内容，理解源码中 `__add__` 的实现逻辑。这对于理解 Agent 如何处理多步操作的复合结果至关重要。

### 练习 C：故障注入与防御机制（架构健壮性）
目标：测试系统的鲁棒性。
- **操作**：修改你的工具，使其在特定参数下抛出 `RuntimeError`。
- **验证**：通过 `ToolCollection.execute` 调用该工具，观察异常是否被主程序崩溃，还是被封装为包含 `error` 字段的 `ToolResult`。
- *思考*：这种“错误即结果”的设计模式在分布式系统中不仅用于 Agent，还常见于哪些场景？

## 每日安排建议
- **Day 1 (架构认知)**：阅读 `app/tool/base.py`，画出 `BaseTool` 与 `ToolResult` 的类图，理解字段含义。
- **Day 2 (调度逻辑)**：阅读 `app/tool/tool_collection.py`，梳理 "LLM 决定调用 -> ToolCollection 查找 -> 执行 -> 结果回传" 的时序图。
- **Day 3 (代码实战)**：完成 **练习 A** 和 **练习 B**，体验 Pydantic 在工具定义中的强大作用。
- **Day 4 (系统健壮性)**：完成 **练习 C**，并对比 `bash.py` 的实现，看官方工具如何处理执行错误。
- **Day 5 (复盘与扩展)**：总结 OpenManus 工具系统的优缺点。如果让你设计支持“撤销”操作的工具系统，你会怎么改？

## 验收标准
1. 能脱稿画出 Agent 调用工具的完整时序图（从 `to_params` 到 `execute` 再到 `ToolResult`）。
2. 能够解释为什么 OpenManus 选择用 Pydantic 模型来定义工具参数，而不是普通的 Python 字典。
3. 成功运行自定义工具，并看到它在 Agent 的思考过程（Memory）中留下的记录。
