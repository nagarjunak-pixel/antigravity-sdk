import asyncio
import os
from google.antigravity import Agent, LocalAgentConfig
from google.antigravity.types import Document, CapabilitiesConfig, BuiltinTools

# Helper to verify GEMINI_API_KEY
if not os.environ.get("GEMINI_API_KEY"):
    print("Warning: GEMINI_API_KEY environment variable is not set.")
    print("Please get an API key from: https://aistudio.google.com/app/api-keys")
    print("And set it using: export GEMINI_API_KEY=\"your_key\"\n")

async def create_dummy_files():
    # Create a simple dummy text document to analyze
    with open("sample_doc.txt", "w") as f:
        f.write("Project Antigravity: The goal of this project is to build autonomous, resilient, and multi-turn AI agents that interact seamlessly with systems.")

async def main():
    await create_dummy_files()

    # Configure the agent to enable the generate_image tool
    config = LocalAgentConfig(
        system_instructions=f"You are a helpful assistant with access to the '{BuiltinTools.GENERATE_IMAGE.value}' tool to generate images when requested.",
        capabilities=CapabilitiesConfig(
            enabled_tools=[BuiltinTools.GENERATE_IMAGE]
        )
    )

    async with Agent(config) as agent:
        print("--- 1. Attaching a Document ---")
        # Load the sample document
        doc = Document.from_file("sample_doc.txt")
        prompt1 = ["What is the main goal of Project Antigravity described in this document?", doc]
        print("User: [sample_doc.txt] What is the main goal of Project Antigravity described in this document?")
        
        response1 = await agent.chat(prompt1)
        print(f"Agent: {await response1.text()}\n")

        print("--- 2. Generating an Image ---")
        prompt2 = "Generate an image of a red apple on a wooden table."
        print(f"User: {prompt2}")
        
        response2 = await agent.chat(prompt2)
        print(f"Agent: {await response2.text()}\n")

    # Cleanup the dummy file
    if os.path.exists("sample_doc.txt"):
        os.remove("sample_doc.txt")

if __name__ == "__main__":
    asyncio.run(main())
