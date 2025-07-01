from __future__ import annotations

import os
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
            # Get or create session for this user
            if user_id not in self.sessions:
                # Await session creation if it's async
                session = await self.runner.session_service.create_session(
                    app_name=self.runner.app_name, user_id=user_id
                )
                self.sessions[user_id] = session
            else:
                session = self.sessions[user_id]

            # Create user content
            content = UserContent(parts=[Part(text=message)])

            # Get response from agent using async iterator
            response_parts = []
            async for event in self.runner.run_async(
                user_id=session.user_id, session_id=session.id, new_message=content
            ):
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        response_parts.append(part.text)

            # Combine all response parts
            full_response = "".join(response_parts)
            return full_response if full_response else "Desole chui occupe."

        except Exception as e:
            print(f"Error getting advice from agent: {e}")
            return "Oups ca marche pas."

    def clear_user_session(self, user_id: str):
        """Clear a user's session (useful for starting fresh)"""
        if user_id in self.sessions:
            del self.sessions[user_id]


# Create the global agent instance
discord_agent = DiscordAdvisoryAgent()
