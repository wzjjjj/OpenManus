import asyncio
from app.agent.manus import Manus
from app.logger import logger

async def main():
    agent = await Manus.create()
    
    print("\n🧪 Test Case 1: Expected ToolError")
    try:
        # 我们直接调用 tool_collection.execute 来模拟 Agent 的行为
        # 这样可以避开 LLM 思考，直接测试底层逻辑
        print("Executing faulty_tool with error_type='tool_error'...")
        result = await agent.available_tools.execute(
            name="faulty_tool", 
            tool_input={"error_type": "tool_error"}
        )
        print(f"👉 Result Type: {type(result)}")
        print(f"👉 Result Content: {result}")
        if result.error:
            print("✅ Successfully caught ToolError!")
        else:
            print("❌ Failed to catch ToolError (unexpected success)")
            
    except Exception as e:
        print(f"❌ Unexpected exception caught outside: {e}")

    print("\n" + "="*50 + "\n")

    print("🧪 Test Case 2: Unexpected RuntimeError")
    try:
        print("Executing faulty_tool with error_type='runtime_error'...")
        result = await agent.available_tools.execute(
            name="faulty_tool", 
            tool_input={"error_type": "runtime_error"}
        )
        print(f"👉 Result: {result}")
    except RuntimeError as e:
        print(f"✅ Successfully caught expected RuntimeError outside: {e}")
    except Exception as e:
        print(f"❓ Caught other exception: {type(e)}: {e}")

if __name__ == "__main__":
    asyncio.run(main())
