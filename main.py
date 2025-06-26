import discord
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OLLAMA_ENDPOINT = os.getenv("OLLAMA_ENDPOINT", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")

print(DISCORD_BOT_TOKEN)
print(OLLAMA_ENDPOINT)
print(OLLAMA_MODEL)

# Set up Discord client with necessary intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    """Prints a message to the console when the bot is connected to Discord."""
    print(f"{client.user} has connected to Discord!")


@client.event
async def on_message(message):
    """
    Handles incoming messages.

    If the bot is mentioned, it sends a processing message,
    sends the message content to the Ollama endpoint,
    and then edits the processing message with the response.
    """
    print(f"Received message: {message.content}")

    if message.author == client.user:
        return

    print(f"Client user: {client.user}")
    if client.user.mentioned_in(message):
        # Get the message content without the bot mention
        prompt = message.content.replace(f"<@!{client.user.id}>", "").strip()

        # Send a processing message
        processing_message = await message.channel.send(
            "I got your query! Processing..."
        )

        # Prepare the data for the Ollama API
        data = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}

        try:
            # Send the request to the Ollama endpoint
            response = requests.post(OLLAMA_ENDPOINT, json=data)
            response.raise_for_status()  # Raise an exception for bad status codes

            # Parse the JSON response
            response_json = response.json()
            bot_response = response_json.get(
                "response", "I am sorry, I could not generate a response."
            )

            # Edit the processing message with the final response
            await processing_message.edit(content=bot_response)

        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Ollama: {e}")
            await processing_message.edit(
                content="I am sorry, I am having trouble connecting to my brain."
            )


# Run the bot
client.run(DISCORD_BOT_TOKEN)
