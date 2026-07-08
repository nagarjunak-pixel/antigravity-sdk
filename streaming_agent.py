import asyncio
import os
import sys
from google.antigravity import Agent, LocalAgentConfig

# Helper to verify GEMINI_API_KEY
if not os.environ.get("GEMINI_API_KEY"):
    print("Warning: GEMINI_API_KEY environment variable is not set.")
    print("Please get an API key from: https://aistudio.google.com/app/api-keys")
    print("And set it using: export GEMINI_API_KEY=\"your_key\"\n")

async def main():
    config = LocalAgentConfig(
        system_instructions="You are a helpful assistant.",
    )
    
    async with Agent(config) as agent:
        print("--- 1. Streaming response text tokens ---")
        prompt1 = "Explain gravity in one sentence."
        print(f"User: {prompt1}")
        print("Agent: ", end="", flush=True)
        
        response1 = await agent.chat(prompt1)
        async for token in response1:
            sys.stdout.write(token)
            sys.stdout.flush()
        print("\n")

        print("--- 2. Streaming thoughts (reasoning process) ---")
        prompt2 = "What is 12345 * 6789? Show your thought process."
        print(f"User: {prompt2}")
        
        response2 = await agent.chat(prompt2)
        
        print("Thoughts: ", end="", flush=True)
        async for thought in response2.thoughts:
            sys.stdout.write(thought)
            sys.stdout.flush()
        print("\n")
        
        print("Final Answer: ", end="", flush=True)
        async for token in response2:
            sys.stdout.write(token)
            sys.stdout.flush()
        print("\n")

if __name__ == "__main__":
    asyncio.run(main())
