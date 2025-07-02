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
        print("🧪 Testing Discord ADK Agent with Tools...")
        print("=" * 60)

        # Import after loading env vars
        from src.agent.agent import discord_agent

        # Test cases including tool usage
        test_cases = [
            ("test_user_1", "Hello! How are you?"),
            ("test_user_1", "What time is it right now?"),
            ("test_user_2", "What was the time 2 hours ago?"),
            (
                "test_user_1",
                "Can you search for messages from Younes in the last 24 hours?",
            ),
            ("test_user_1", "Find me messages from momo and idris from yesterday"),
            ("test_user_1", "Do you remember our previous conversation?"),
            ("test_user_3", "Quelle heure il était il y a 1 jour et 3 heures?"),
        ]

        for i, (user_id, message) in enumerate(test_cases, 1):
            print(f"\n📝 Test {i}: User {user_id}")
            print(f"   Message: {message}")
            print(f"   Response: ", end="", flush=True)

            try:
                response = await discord_agent.get_advice(user_id, message)
                # Show first 150 chars for readability
                display_response = (
                    response[:150] + "..." if len(response) > 150 else response
                )
                print(f"✅ {display_response}")

                # Add a small delay between tests
                await asyncio.sleep(0.5)

            except Exception as e:
                print(f"❌ ERROR: {e}")

        print(f"\n📊 Session Statistics:")
        print(f"   Active sessions: {discord_agent.get_session_count()}")

        print("\n🔧 Testing Tools Directly:")
        print("-" * 40)

        # Test tools directly
        try:
            from src.agent.tools.tools import (
                get_current_time,
                get_time_ago,
            )

            print(f"⏰ Current time: {get_current_time()}")
            print(f"⏰ 2 hours ago: {get_time_ago(hours=2)}")
            print(f"⏰ Yesterday: {get_time_ago(days=1)}")

        except Exception as tool_error:
            print(f"❌ Tool test error: {tool_error}")

        print("\n🎉 All tests completed!")

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()


async def test_tools_only():
    """Test just the tools without the agent"""
    print("\n🔧 Testing Tools Only...")
    print("=" * 40)

    try:
        from src.agent.tools.tools import (
            get_current_time,
            get_time_ago,
            search_user_messages,
        )

        print("1. Testing time functions:")
        print(f"   Current time: {get_current_time()}")
        print(f"   5 minutes ago: {get_time_ago(minutes=5)}")
        print(f"   2 days ago: {get_time_ago(days=2)}")

        print("\n2. Testing message search (requires Discord client):")
        result = await search_user_messages(
            user_ids=["221351940867620864", "306827479484465172"], hours_back=12
        )
        print(f"   Search result:\n{result}")

    except Exception as e:
        print(f"❌ Tools test error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    # Check for required environment variables
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ ERROR: GOOGLE_API_KEY not found in environment!")
        print("Please make sure you have a .env file with your Google API key.")
        exit(1)

    print("🚀 Starting comprehensive agent and tools test...")

    # Run both tests
    asyncio.run(test_tools_only())
    asyncio.run(test_agent())
