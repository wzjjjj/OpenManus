from app.tool.base import BaseTool, ToolResult






class StringReverseTool(BaseTool):
    name:str = "string_reverse"
    description:str = "Reverse the input string"
    parameters:dict = {
        "type": "object",
        "properties": {
            "input": {
                "type": "string",
                "description": "The string to be reversed",
            }
        },
        "required": ["input"],
    }
    async def execute(self,input:str) -> ToolResult:
        result = input[::-1]
        return self.success_response(result)
