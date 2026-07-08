import asyncio
import os
import logging
from google.antigravity import Agent, LocalAgentConfig, types
from google.antigravity.hooks import hooks, policy
from google.antigravity.triggers import every, TriggerContext

# Helper to verify GEMINI_API_KEY
if not os.environ.get("GEMINI_API_KEY"):
    print("Warning: GEMINI_API_KEY environment variable is not set.")
    print("Please get an API key from: https://aistudio.google.com/app/api-keys")
    print("And set it using: export GEMINI_API_KEY=\"your_key\"\n")

# Configure logging to see hook outputs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Define hooks
@hooks.on_session_start
async def my_session_start():
    logging.info("[HOOK] Session started!")

@hooks.on_session_end
async def my_session_end():
    logging.info("[HOOK] Session ended!")

@hooks.pre_turn
async def my_pre_turn(data: str) -> types.HookResult:
    logging.info(f"[HOOK] Intercepted user prompt: {data}")
    return types.HookResult(allow=True)

@hooks.post_turn
async def my_post_turn(data: str):
    logging.info(f"[HOOK] Final agent response: {data}")

# Define a periodic trigger (runs every 5 seconds for demonstration)
async def health_check_trigger(ctx: TriggerContext):
    logging.info("[TRIGGER] Background task check: System online and healthy.")

# Create the config with policies, hooks, and triggers
policies = [
    policy.confirm_run_command(), # Default: deny run_command, allow other tools
]

config = LocalAgentConfig(
    system_instructions="You are a status reporting agent.",
    policies=policies,
    hooks=[my_session_start, my_session_end, my_pre_turn, my_post_turn],
    triggers=[every(5, health_check_trigger)],
)

async def main():
    print("Initializing Agent with hooks and triggers...")
    async with Agent(config) as agent:
        print("\n--- Sending chat turn ---")
        response = await agent.chat("Print a quick status message.")
        print(f"Agent text output: {await response.text()}\n")
        
        print("Sleeping for 11 seconds to let the background trigger run twice...")
        await asyncio.sleep(11)
        print("Exiting...")

if __name__ == "__main__":
    asyncio.run(main())
