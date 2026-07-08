import asyncio
import os
from google.antigravity import Agent, LocalAgentConfig, ToolContext

# Helper to verify GEMINI_API_KEY
if not os.environ.get("GEMINI_API_KEY"):
    print("Warning: GEMINI_API_KEY environment variable is not set.")
    print("Please get an API key from: https://aistudio.google.com/app/api-keys")
    print("And set it using: export GEMINI_API_KEY=\"your_key\"\n")

# A simple custom weather tool
def get_weather(city: str) -> str:
    """Gets the current weather for a city.

    Args:
        city: The name of the city, e.g. "Seattle" or "Tokyo".
    """
    # Simple mockup weather mapping
    weather_db = {
        "tokyo": "Sunny, 22°C",
        "london": "Rainy, 14°C",
        "seattle": "Cloudy, 16°C",
        "sydney": "Windy, 18°C"
    }
    key = city.lower().strip()
    return f"The current weather in {city} is {weather_db.get(key, 'unknown (assume 20°C and mild)')}."

# A stateful custom counter tool
def update_item_count(item_name: str, delta: int, ctx: ToolContext) -> str:
    """Updates the inventory count of an item.

    Args:
        item_name: The name of the item.
        delta: The number of items to add (positive) or remove (negative).
        ctx: The ToolContext object injected automatically.
    """
    inventory = ctx.get_state("inventory", {})
    current = inventory.get(item_name, 0)
    new_total = max(0, current + delta)
    inventory[item_name] = new_total
    ctx.set_state("inventory", inventory)
    return f"Updated {item_name} inventory. Delta: {delta:+d}. New total: {new_total}."

async def main():
    # Register both tools in the config
    config = LocalAgentConfig(
        system_instructions="You are an inventory and assistant agent equipped with weather and inventory tools.",
        tools=[get_weather, update_item_count],
    )

    async with Agent(config) as agent:
        print("--- 1. Calling weather tool ---")
        prompt1 = "What's the weather like in Tokyo right now?"
        print(f"User: {prompt1}")
        response1 = await agent.chat(prompt1)
        print(f"Agent: {await response1.text()}\n")

        print("--- 2. Calling stateful tool (Turn 1) ---")
        prompt2 = "Add 15 laptops to the inventory."
        print(f"User: {prompt2}")
        response2 = await agent.chat(prompt2)
        print(f"Agent: {await response2.text()}\n")

        print("--- 3. Calling stateful tool (Turn 2) ---")
        prompt3 = "Remove 5 laptops from the inventory."
        print(f"User: {prompt3}")
        response3 = await agent.chat(prompt3)
        print(f"Agent: {await response3.text()}\n")

if __name__ == "__main__":
    asyncio.run(main())
