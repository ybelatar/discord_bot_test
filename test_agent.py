#!/usr/bin/env python3
"""
Simple test script for the Discord ADK Agent
Run this to test if the agent works correctly before using it in Discord
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


async def test_agent():
    """Test the Discord agent functionality"""
    try:
        print("🧪 Testing Discord ADK Agent...")
        print("=" * 50)

        # Import after loading env vars
        from src.agent.agent import discord_agent

        # Test cases
        test_cases = [
            ("test_user_1", "Hello! How are you?"),
            ("test_user_1", "What's your favorite programming language?"),
            ("test_user_2", "Can you give me advice on time management?"),
            ("test_user_1", "Do you remember our previous conversation?"),
        ]

        for i, (user_id, message) in enumerate(test_cases, 1):
            print(f"\n📝 Test {i}: User {user_id}")
            print(f"   Message: {message}")
            print(f"   Response: ", end="", flush=True)

            try:
                response = await discord_agent.get_advice(user_id, message)
                print(f"✅ {response[:100]}{'...' if len(response) > 100 else ''}")
            except Exception as e:
                print(f"❌ ERROR: {e}")

        print(f"\n📊 Session Statistics:")
        print(f"   Active sessions: {discord_agent.get_session_count()}")

        print("\n🎉 Test completed!")

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    # Check for required environment variables
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ ERROR: GOOGLE_API_KEY not found in environment!")
        print("Please make sure you have a .env file with your Google API key.")
        exit(1)

    print("🚀 Starting agent test...")
    asyncio.run(test_agent())
