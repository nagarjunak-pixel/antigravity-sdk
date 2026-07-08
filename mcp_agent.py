import asyncio
import os
from google.antigravity import Agent, LocalAgentConfig, types

# Helper to verify GEMINI_API_KEY
if not os.environ.get("GEMINI_API_KEY"):
    print("Warning: GEMINI_API_KEY environment variable is not set.")
    print("Please get an API key from: https://aistudio.google.com/app/api-keys")
    print("And set it using: export GEMINI_API_KEY=\"your_key\"\n")

async def main():
    # Configure the MCP server to run via the same virtual environment python interpreter
    # using stdio transport.
    mcp_servers = [
        types.McpStdioServer(
            name="math_server",  # Name to identify the server
            command=".venv/bin/python",
            args=["simple_mcp_server.py"],
        )
    ]

    config = LocalAgentConfig(
        system_instructions="You are an assistant equipped with an external MathServer MCP tool. Use the tools to multiply numbers or format messages.",
        mcp_servers=mcp_servers,
    )

    print("Initializing Agent with MCP math_server...")
    async with Agent(config) as agent:
        print("\n--- 1. Calling MCP multiply_numbers tool ---")
        prompt1 = "What is 765 * 432? Use the math_server multiply_numbers tool."
        print(f"User: {prompt1}")
        response1 = await agent.chat(prompt1)
        print(f"Agent: {await response1.text()}\n")

        print("--- 2. Calling MCP format_message tool ---")
        prompt2 = "Can you format the word 'antigravity' in uppercase using the math_server format_message tool?"
        print(f"User: {prompt2}")
        response2 = await agent.chat(prompt2)
        print(f"Agent: {await response2.text()}\n")

if __name__ == "__main__":
    asyncio.run(main())
