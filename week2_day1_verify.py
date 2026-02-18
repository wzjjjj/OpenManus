import asyncio
from app.agent.manus import Manus
from app.logger import logger

async def main():
    agent = await Manus.create()

    # Verify tool registration
    tool_names = [t.name for t in agent.available_tools.tools]
    print(f"Available tools: {tool_names}")

    if "string_reverse" in tool_names:
        print("✅ StringReverseTool successfully registered!")
    else:
        print("❌ StringReverseTool NOT found!")
        return

    # Run a simple task
    print("\n🚀 Running agent with task: 'Reverse the string 'OpenManus rocks''")
    try:
        await agent.run("Please reverse the string 'OpenManus rocks'")
    except Exception as e:
        print(f"Error running agent: {e}")

if __name__ == "__main__":
    asyncio.run(main())
