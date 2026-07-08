import asyncio
import os
from google.antigravity import Agent, LocalAgentConfig

# Helper to verify GEMINI_API_KEY
if not os.environ.get("GEMINI_API_KEY"):
    print("Warning: GEMINI_API_KEY environment variable is not set.")
    print("Please get an API key from: https://aistudio.google.com/app/api-keys")
    print("And set it using: export GEMINI_API_KEY=\"your_key\"\n")

async def main():
    # LocalAgentConfig will read GEMINI_API_KEY from the environment
    config = LocalAgentConfig(
        system_instructions="You are a helpful and concise AI assistant.",
    )
    
    print("Initializing Agent...")
    async with Agent(config) as agent:
        print("Sending message: 'Hello, Antigravity!'")
        response = await agent.chat("Hello, Antigravity!")
        
        print("\nAgent Response:")
        print(await response.text())

if __name__ == "__main__":
    asyncio.run(main())
