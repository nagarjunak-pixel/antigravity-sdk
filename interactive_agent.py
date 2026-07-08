import asyncio
import os
from google.antigravity import Agent, LocalAgentConfig, CapabilitiesConfig

# Helper to verify GEMINI_API_KEY
if not os.environ.get("GEMINI_API_KEY"):
    print("Warning: GEMINI_API_KEY environment variable is not set.")
    print("Please get an API key from: https://aistudio.google.com/app/api-keys")
    print("And set it using: export GEMINI_API_KEY=\"your_key\"\n")

async def main():
    config = LocalAgentConfig(
        system_instructions="You are a friendly agent ready to help the user in the console.",
        capabilities=CapabilitiesConfig(),  # Enables write tools if needed
    )
    
    print("Starting interactive chat loop...")
    print("Type 'exit' or 'quit' to end the loop.\n")
    
    async with Agent(config) as agent:
        await agent.run_interactive_loop()

if __name__ == "__main__":
    asyncio.run(main())
