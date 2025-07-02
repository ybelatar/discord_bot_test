"""
Discord ADK Agent Tools
Tools for time management and Discord message searching
"""

from __future__ import annotations

import discord
from datetime import datetime, timedelta
from typing import List, Optional

# Global Discord client reference (will be set by the bot)
_discord_client = None


def set_discord_client(client):
    """Set the Discord client for use in tools"""
    global _discord_client
    _discord_client = client


def get_current_time() -> str:
    """
    Get the current date and time in a readable format.

    Returns:
        Current date and time as a formatted string
    """
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S (%A)")


def get_time_ago(hours: int = 0, days: int = 0, minutes: int = 0) -> str:
    """
    Calculate time that was X hours/days/minutes ago.

    Args:
        hours: Number of hours ago (default: 0)
        days: Number of days ago (default: 0)
        minutes: Number of minutes ago (default: 0)

    Returns:
        Date and time from the specified time ago
    """
    time_ago = datetime.now() - timedelta(hours=hours, days=days, minutes=minutes)
    return time_ago.strftime("%Y-%m-%d %H:%M:%S (%A)")


async def search_user_messages(
    user_ids: List[str],
    channel_id: Optional[str] = "173025825942142977",
    hours_back: int = 240,
    limit: int = 50,
) -> str:
    """
    Search for recent messages from specific users in Discord.

    Args:
        user_ids: List of Discord user IDs to search for
        channel_id: Specific channel ID to search in (optional)
        hours_back: How many hours back to search (default: 24)
        limit: Maximum number of messages to return (default: 50)

    Returns:
        Formatted string containing found messages
    """
    if not _discord_client:
        return "❌ Discord client not available. Make sure the bot is running."

    try:
        # Calculate search timeframe
        search_time = datetime.now() - timedelta(hours=hours_back)

        # Convert string user_ids to integers for comparison
        target_user_ids = [int(uid) for uid in user_ids]

        result = f"🔍 Recherche de messages de {len(user_ids)} utilisateur(s)\n"
        result += f"📅 Période: dernières {hours_back} heures\n"
        result += f"⏰ Depuis: {search_time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        found_messages = []
        channels_searched = 0

        # If specific channel provided, search only that channel
        if channel_id:
            try:
                channel = _discord_client.get_channel(int(channel_id))
                if channel:
                    messages = await _search_channel_messages(
                        channel, target_user_ids, search_time, limit
                    )
                    found_messages.extend(messages)
                    channels_searched = 1
                else:
                    return f"❌ Channel {channel_id} not found or not accessible."
            except Exception as e:
                return f"❌ Erreur accessing channel {channel_id}: {str(e)}"
        else:
            # Search all accessible channels
            for guild in _discord_client.guilds:
                for channel in guild.text_channels:
                    try:
                        # Check if bot has permission to read message history
                        if channel.permissions_for(guild.me).read_message_history:
                            messages = await _search_channel_messages(
                                channel, target_user_ids, search_time, limit // 10
                            )
                            found_messages.extend(messages)
                            channels_searched += 1

                            # Stop if we've found enough messages
                            if len(found_messages) >= limit:
                                break
                    except discord.Forbidden:
                        continue  # Skip channels we can't access
                    except Exception as e:
                        print(f"Error searching channel {channel.name}: {e}")
                        continue

                if len(found_messages) >= limit:
                    break

        # Format results
        if found_messages:
            result += f"✅ Trouvé {len(found_messages)} message(s) dans {channels_searched} canal/canaux:\n\n"

            # Sort messages by timestamp (newest first)
            found_messages.sort(key=lambda x: x["timestamp"], reverse=True)

            for i, msg in enumerate(found_messages[:limit], 1):
                result += f"**{i}.** `{msg['author']}` dans #{msg['channel']} "
                result += f"({msg['timestamp'].strftime('%d/%m %H:%M')}):\n"
                result += f"   {msg['content'][:100]}{'...' if len(msg['content']) > 100 else ''}\n\n"
        else:
            result += f"❌ Aucun message trouvé pour les utilisateurs spécifiés dans les dernières {hours_back} heures.\n"
            result += f"Canaux recherchés: {channels_searched}\n"

        return result

    except Exception as e:
        return f"❌ Erreur lors de la recherche de messages: {str(e)}"


async def _search_channel_messages(channel, target_user_ids, search_time, limit):
    """Helper function to search messages in a specific channel"""
    found_messages = []

    try:
        async for message in channel.history(limit=1000, after=search_time):
            if message.author.id in target_user_ids:
                found_messages.append(
                    {
                        "author": message.author.display_name,
                        "content": message.content,
                        "timestamp": message.created_at,
                        "channel": channel.name,
                        "message_id": message.id,
                    }
                )

                if len(found_messages) >= limit:
                    break
    except discord.Forbidden:
        pass  # Skip channels we can't access
    except Exception as e:
        print(f"Error in _search_channel_messages: {e}")

    return found_messages


# Tool registry for easy import
DISCORD_TOOLS = [
    get_current_time,
    get_time_ago,
    search_user_messages,
]
