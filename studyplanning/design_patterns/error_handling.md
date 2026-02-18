# OpenManus 错误处理设计模式深度解析

本文档旨在分析 OpenManus 项目中的**分层错误处理 (Layered Error Handling)** 设计模式。这种模式在构建高鲁棒性的 Agent 系统时至关重要，它确保了系统即使在个别组件失效时也能继续运行并自我修复。

## 1. 核心设计理念：分层防御 (Layered Defense)

OpenManus 将错误处理分为了两个明确的层级，分别对应不同的职责和错误类型。

| 层级 | 负责组件 | 捕获目标 | 处理策略 | 目的 |
| :--- | :--- | :--- | :--- | :--- |
| **第一层** | `ToolCollection` | **业务逻辑错误** (`ToolError`) | 降级为 `ToolFailure` 对象返回 | 让 Agent 感知到“操作失败”，但认为是正常的业务反馈 |
| **第二层** | `ToolCallAgent` | **未预期的系统崩溃** (`Exception`) | 捕获异常，记录堆栈，返回错误文本 | 防止整个进程崩溃，给 LLM 一个“报错”反馈，尝试让 LLM 修复或重试 |

---

## 2. 第一层防御：业务逻辑错误处理

### 场景
工具内部逻辑判断失败，例如：文件不存在、API 返回 404、参数校验不通过。
**案例**：外卖系统中，用户点餐时发现商品售罄。

### 实现机制
1.  **定义异常**：在 `app/exceptions.py` 中定义 `ToolError`。
2.  **主动抛出**：工具开发者在代码中显式 `raise ToolError("原因")`。
3.  **捕获与转化**：`ToolCollection` 捕获该异常，并将其转化为 `ToolFailure` 对象。

### 代码赏析
**[app/tool/tool_collection.py](file:///c%3A/Users/96408/Desktop/%E7%BC%96%E7%A8%8B%E5%AD%A6%E4%B9%A0%E8%AE%B0%E5%BD%95/OpenManus/app/tool/tool_collection.py#L31-L35)**
```python
try:
    result = await tool(**tool_input)
    return result
except ToolError as e:
    # 优雅降级：将异常转化为数据对象
    return ToolFailure(error=e.message)
```

### 设计意图
*   **消除异常流**：对于上层调用者来说，`execute` 方法**永远不会抛出 ToolError**。它总是返回一个 `ToolResult`（要么是成功的 Result，要么是失败的 Failure）。
*   **统一接口**：上层不需要写 try-except 来处理业务逻辑，只需要检查 `result.error` 字段。

---

## 3. 第二层防御：系统崩溃兜底

### 场景
代码 Bug、空指针、依赖库内部崩溃、内存溢出等不可预知的错误。
**案例**：外卖系统中，扣款时数据库连接中断。

### 实现机制
1.  **全局捕获**：在 Agent 的执行入口处包裹巨大的 `try...except Exception`。
2.  **日志留痕**：使用 `logger.exception` 打印完整的堆栈跟踪，方便开发者排查。
3.  **反馈 LLM**：将错误信息格式化为字符串，作为 Observation 返回给 LLM。

### 代码赏析
**[app/agent/toolcall.py](file:///c%3A/Users/96408/Desktop/%E7%BC%96%E7%A8%8B%E5%AD%A6%E4%B9%A0%E8%AE%B0%E5%BD%95/OpenManus/app/agent/toolcall.py#L207-L210)**
```python
except Exception as e:
    error_msg = f"⚠️ Tool '{name}' encountered a problem: {str(e)}"
    # 关键：记录堆栈，但不让进程死掉
    logger.exception(error_msg)
    # 关键：将错误转化为自然语言，告诉 LLM
    return f"Error: {error_msg}"
```

### 设计意图
*   **保活 (Keep-Alive)**：Agent 是一个长运行进程，不能因为一个工具坏了就挂掉。
*   **自我修复 (Self-Healing)**：LLM 看到 "Error: ..." 后，可能会尝试：
    *   修改参数重试。
    *   调用另一个替代工具。
    *   告诉用户“我遇到了技术问题”。

---

## 4. 实践指南：如何在自定义项目中运用

### 步骤一：定义业务异常
创建一个基础异常类，用于标识所有预期的业务失败。
```python
class CodeGenError(Exception):
    """当代码生成失败、语法错误或测试不通过时抛出"""
    pass
```

### 步骤二：底层主动抛出 (Throw)
在具体工具实现中，当遇到业务规则阻碍时，抛出该异常。
```python
# WriteCodeTool.execute
if has_syntax_error(code):
    raise CodeGenError("Python syntax error: missing ':'")
```

### 步骤三：中间层优雅降级 (Catch & Wrap)
在调度器中捕获业务异常，转化为失败结果对象，供上层逻辑判断。
```python
# ToolManager.execute
try:
    return tool.run()
except CodeGenError as e:
    return Result(success=False, error_msg=str(e))
```

### 步骤四：顶层兜底与反馈 (Consume)
在主循环中捕获所有未预料的 `Exception`，防止程序崩溃，并将错误反馈给 LLM。
```python
# Agent Loop
try:
    step = llm.think()
    tool_result = manager.execute(step)
except Exception as e:
    logger.error(f"System Crash: {e}")
    memory.add(f"System Error: {e}. Please retry.")
```

---

## 5. 总结

在设计 Agent 或插件系统时，请遵循：

1.  **区分“失败”与“错误”**：
    *   **失败 (Failure)** 是业务预期内的一种结果（如登录失败），应该用返回值表达。
    *   **错误 (Error/Exception)** 是系统异常（如空指针），应该在最外层兜底。
2.  **不要让异常穿透边界**：模块之间的边界（如 ToolCollection 和 Agent 之间）应该有异常防火墙。
3.  **让 LLM 参与运维**：将错误信息转化为自然语言反馈给 LLM，往往能产生意想不到的自我修复效果。

---

*这份文档已保存在 `studyplanning/design_patterns/error_handling.md`，方便随时复习。*
