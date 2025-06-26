import discord
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Set up Discord client with necessary intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    """Prints a message to the console when the bot is connected to Discord."""
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    """
    Handles incoming messages.

    If the bot is mentioned, it sends a processing message,
    sends the message content to the Gemini API,
    and then edits the processing message with the response.
    """
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        # Get the message content without the bot mention
        prompt = message.content.replace(f'<@!{client.user.id}>', '').strip()

        # Send a processing message
        processing_message = await message.channel.send("I got your query! Processing...")

        try:
            # Send the prompt to the Gemini API
            response = model.generate_content(prompt)

            # Edit the processing message with the final response
            await processing_message.edit(content=response.text)

        except Exception as e:
            print(f"Error communicating with Gemini API: {e}")
            await processing_message.edit(content="I am sorry, I am having trouble connecting to my brain.")

# Run the bot
client.run(DISCORD_BOT_TOKEN)
