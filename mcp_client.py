import mcp
from mcp.client.stdio import stdio_client
from mcp import StdioServerParameters
import json
import asyncio
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True)

params = StdioServerParameters(command="uv", args=["run", "date_server.py"], env=None)


class MCPOpenAIClient:
    """Client connecting MCP (Model Context Protocol) with OpenAI API"""

    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.mcp_tools = []

    async def connect_to_mcp_server(self):
        """Connects to MCP server and retrieves available tools"""
        async with stdio_client(params) as (read, write):
            async with mcp.ClientSession(read, write) as session:
                await session.initialize()

                tools_list = await session.list_tools()
                print(f"Available MCP tools: {[tool.name for tool in tools_list.tools]}")

                for tool in tools_list.tools:
                    openai_tool = {
                        "type": "function",
                        "function": {
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": tool.inputSchema
                        }
                    }
                    self.mcp_tools.append(openai_tool)

                return session

    async def run_agent(self, user_message: str):
        """Runs agent with ability to call MCP tools"""
        async with stdio_client(params) as (read, write):
            async with mcp.ClientSession(read, write) as session:
                await session.initialize()

                messages = [{"role": "user", "content": user_message}]

                response = self.openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=messages,
                    tools=self.mcp_tools if self.mcp_tools else None
                )

                assistant_message = response.choices[0].message

                if assistant_message.tool_calls:
                    for tool_call in assistant_message.tool_calls:
                        tool_name = tool_call.function.name
                        tool_args = json.loads(tool_call.function.arguments)

                        print(f"Calling tool: {tool_name} with arguments: {tool_args}")

                        result = await session.call_tool(tool_name, tool_args)
                        print(f"Result from tool: {result.content}")

                        messages.append({
                            "role": "assistant",
                            "content": assistant_message.content,
                            "tool_calls": [tool_call.model_dump()]
                        })
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": str(result.content)
                        })

                        final_response = self.openai_client.chat.completions.create(
                            model="gpt-4",
                            messages=messages
                        )

                        return final_response.choices[0].message.content
                else:
                    return assistant_message.content


async def main():
    """Main demo function"""
    client = MCPOpenAIClient()

    print("Connecting to MCP server...")
    await client.connect_to_mcp_server()

    user_query = "What is today's date in YYYY-MM-DD format?"
    print(f"\nUser query: {user_query}")

    result = await client.run_agent(user_query)
    print(f"\nResponse: {result}")


if __name__ == "__main__":
    asyncio.run(main())
