import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.schema import Function, Memory, Message, Role, ToolCall


def main() -> None:
    mem = Memory(max_messages=100)

    mem.add_message(Message.system_message("You are a calculator."))
    mem.add_message(Message.user_message("1+1=?"))

    args = json.dumps({"code": "print(1+1)"})
    tool_call = ToolCall(
        id="call_1",
        function=Function(name="python_execute", arguments=args),
    )

    assistant = Message.from_tool_calls(tool_calls=[tool_call], content="")
    mem.add_message(assistant)

    tool_msg = Message.tool_message(
        content="2",
        name="python_execute",
        tool_call_id="call_1",
    )
    mem.add_message(tool_msg)

    print("=== Memory.messages (Message objects) ===")
    for i, m in enumerate(mem.messages, 1):
        print(
            i,
            m.role,
            "tool_call_id=",
            m.tool_call_id,
            "has_tool_calls=",
            bool(m.tool_calls),
        )

    print("\n=== Serialized for LLM (Message.to_dict) ===")
    for i, d in enumerate(mem.to_dict_list(), 1):
        print(i, d)

    print("\n=== Bad tool message (missing tool_call_id) ===")
    bad_tool = Message(role=Role.TOOL, content="2", name="python_execute")
    print(bad_tool.to_dict())

    try:
        from app.llm import LLM

        print("\n=== LLM.format_messages(mem.messages) ===")
        for i, d in enumerate(LLM.format_messages(mem.messages), 1):
            print(i, d)
    except Exception as e:
        print("\n=== LLM.format_messages skipped (import failed) ===")
        print(type(e).__name__, str(e))


if __name__ == "__main__":
    main()
