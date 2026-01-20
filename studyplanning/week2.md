# 第 2 周：工具系统与可扩展点

## 本周目标
- 读懂工具（Tool）的最小接口：schema、执行、结果回传
- 读懂工具集合（ToolCollection）如何调度工具并返回 ToolResult
- 能够新增一个“最小自定义工具”，挂到 Agent 上跑通一轮调用

## 推荐阅读顺序
- `app/tool/base.py`
- `app/tool/tool_collection.py`
- `app/tool/create_chat_completion.py`
- `app/llm.py`（重点看 ask_tool 的 tools/tool_choice 传递）

## 本周关键点（必须搞懂）
- `BaseTool.to_param()` 如何定义 function calling 的 schema
- `ToolCollection.execute()` 如何根据 name 找到具体工具实例并执行
- `ToolResult` 的 `output/error/base64_image` 如何影响最终写回 memory 的内容

## 实战练习（本周主线）
### 练习 A：写一个最小工具
目标：新增一个“纯文本/纯计算”的工具，避免环境依赖，方便你专注于工具协议。

建议功能（任选其一）：
- `string_reverse`：把输入字符串反转返回
- `json_pretty_print`：把传入 JSON 字符串格式化
- `workspace_path`：返回配置里的 workspace root（只读）

交付要求：
- 该工具具备清晰的 parameters schema
- 工具能被 `Manus.available_tools` 注册并被 LLM 正确调用
- 工具执行结果能以 tool_message 形式写回 memory

### 练习 B：故障注入
目标：理解错误如何回传。
- 让工具在特定输入下抛异常
- 观察 execute_tool 的错误包装格式，理解失败时 memory 会追加什么

## 每日安排（建议 1–2 小时/天）
- Day 1：精读 BaseTool/ToolResult，理解 schema 与返回值
- Day 2：精读 ToolCollection.execute，理解调度与错误封装
- Day 3–4：实现最小工具并接入 Manus
- Day 5：做故障注入与复盘

## 本周验收
- 能从源码解释：tool_call.arguments 如何变成工具函数参数
- 能独立新增一个工具并跑通一轮调用（含成功与失败两种路径）

