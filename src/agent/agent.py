from __future__ import annotations

import os
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.genai.types import Part, UserContent

# Load environment variables
load_dotenv()

# Create the advisory agent
advisory_agent = Agent(
    name="discord_advisory_agent",
    model="gemini-2.5-flash-lite-preview-06-17",
    instruction="""
    You are a helpful advisory agent for Discord users. Your role is to provide thoughtful, 
    constructive advice on any topic users ask about. Be concise but informative, friendly 
    but professional. Always aim to be helpful and supportive.
    
    Guidelines:
    - Keep responses conversational and engaging
    - Provide actionable advice when possible
    - Be empathetic and understanding
    - If you don't know something, admit it and suggest ways to find out
    - Keep responses reasonably short for Discord chat
    """,
    description="An advisory agent that provides helpful advice and guidance to Discord users on various topics.",
    tools=[],  # Starting with no tools, just basic conversation
)

# Create a runner for the agent
runner = InMemoryRunner(agent=advisory_agent)


class DiscordAdvisoryAgent:
    """Wrapper class for the ADK agent to handle Discord interactions"""

    def __init__(self):
        self.runner = runner
        self.sessions = {}  # Store user sessions
        self.session_lock = asyncio.Lock()  # Prevent race conditions

    async def get_advice(self, user_id: str, message: str) -> str:
        """
        Get advice from the agent for a user's message

        Args:
            user_id: Discord user ID
            message: The user's message/query

        Returns:
            The agent's response as a string
        """
        try:
            print(f"[DEBUG] Processing message for user {user_id}: {message[:50]}...")

            # Use lock to prevent race conditions on session creation
            async with self.session_lock:
                # Get or create session for this user
                if user_id not in self.sessions:
                    print(f"[DEBUG] Creating new session for user {user_id}")
                    try:
                        # Try to create session - this might not be async in all ADK versions
                        session = self.runner.session_service.create_session(
                            app_name=self.runner.app_name, user_id=user_id
                        )
                        # If it returns a coroutine, await it
                        if hasattr(session, "__await__"):
                            session = await session
                        self.sessions[user_id] = session
                        print(
                            f"[DEBUG] Session created successfully for user {user_id}"
                        )
                    except Exception as session_error:
                        print(f"[ERROR] Failed to create session: {session_error}")
                        return "Desole, je n'arrive pas a initialiser une session."
                else:
                    session = self.sessions[user_id]
                    print(f"[DEBUG] Using existing session for user {user_id}")

            # Create user content
            content = UserContent(parts=[Part(text=message)])
            print(f"[DEBUG] Created UserContent, starting ADK processing...")

            # Get response from agent using proper async pattern
            response_parts = []
            try:
                # Use async iteration pattern as shown in ADK docs
                async for event in self.runner.run_async(
                    user_id=session.user_id, session_id=session.id, new_message=content
                ):
                    print(f"[DEBUG] Received event from ADK runner")
                    for part in event.content.parts:
                        if hasattr(part, "text") and part.text:
                            response_parts.append(part.text)
                            print(f"[DEBUG] Added response part: {part.text[:30]}...")
            except AttributeError as attr_error:
                print(f"[ERROR] AttributeError in run_async: {attr_error}")
                # Fallback to synchronous method if async not available
                print("[DEBUG] Falling back to synchronous runner.run()")
                for event in self.runner.run(
                    user_id=session.user_id, session_id=session.id, new_message=content
                ):
                    for part in event.content.parts:
                        if hasattr(part, "text") and part.text:
                            response_parts.append(part.text)

            # Combine all response parts
            full_response = "".join(response_parts)
            print(f"[DEBUG] Final response length: {len(full_response)} characters")

            return full_response if full_response else "Desole chui occupe."

        except Exception as e:
            print(f"[ERROR] Unexpected error in get_advice: {e}")
            print(f"[ERROR] Error type: {type(e)}")
            import traceback

            traceback.print_exc()
            return "Oups ca marche pas."

    def clear_user_session(self, user_id: str):
        """Clear a user's session (useful for starting fresh)"""
        if user_id in self.sessions:
            print(f"[DEBUG] Clearing session for user {user_id}")
            del self.sessions[user_id]

    def get_session_count(self) -> int:
        """Get the number of active sessions"""
        return len(self.sessions)

    async def cleanup_old_sessions(self, max_age_hours: int = 24):
        """Clean up old sessions to prevent memory leaks"""
        # This is a placeholder - in production you'd track session creation times
        print(f"[DEBUG] Current active sessions: {len(self.sessions)}")


# Create the global agent instance
discord_agent = DiscordAdvisoryAgent()
