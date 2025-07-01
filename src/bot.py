import discord
import os
from dotenv import load_dotenv
from .agent.agent import discord_agent

# Load environment variables
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Set up Discord client with necessary intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    """Prints a message to the console when the bot is connected to Discord."""
    print(f"{client.user} has connected to Discord!")
    print("ADK Advisory Agent is ready to help!")


@client.event
async def on_message(message):
    """
    Handles incoming messages.

    If the bot is mentioned, it sends the message content to the ADK agent
    and responds with the agent's advice.
    """
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        # Special handling for specific users (keeping the original functionality)
        if (
            message.author.id == 306827479484465172
            or message.author.id == 280098879293095936
        ):
            await message.channel.send("ftg sale merde a la niche")
            return

        # Get the message content without the bot mention
        message_content = message.content.replace(f"<@{client.user.id}>", "").strip()

        # If no content after removing mention, provide a helpful message
        if not message_content:
            message_content = "Hello! How can I help you today?"

        # Send a "thinking" message to show the bot is processing
        thinking_message = await message.channel.send("🤔 Let me think about that...")

        try:
            # Get advice from the ADK agent
            user_id = str(message.author.id)
            advice = await discord_agent.get_advice(user_id, message_content)

            # Edit the thinking message with the agent's response
            await thinking_message.edit(content=advice)

        except Exception as e:
            print(f"Error getting advice from agent: {e}")
            await thinking_message.edit(
                content="Sorry, I'm having trouble processing your request right now. Please try again later."
            )


def main():
    """Main function to run the Discord bot"""
    if not DISCORD_BOT_TOKEN:
        print("Error: DISCORD_BOT_TOKEN not found in environment variables!")
        print("Please make sure you have a .env file with your Discord bot token.")
        return

    print("Starting Discord ADK Bot...")
    try:
        # Run the bot
        client.run(DISCORD_BOT_TOKEN)
    except Exception as e:
        print(f"Error running bot: {e}")


if __name__ == "__main__":
    main()
