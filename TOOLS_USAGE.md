# Discord ADK Agent Tools Usage Guide

## 🛠️ Available Tools

### ⏰ Time Tools

#### `get_current_time()`

- **Purpose**: Get current date and time
- **Usage**: "What time is it?" or "Quelle heure il est?"
- **Returns**: Current time in format: "2024-01-15 14:30:22 (Monday)"

#### `get_time_ago(hours, days, minutes)`

- **Purpose**: Calculate time from X hours/days/minutes ago
- **Usage**: "What time was it 2 hours ago?" or "Il était quelle heure il y a 3 jours?"
- **Examples**:
  - "2 hours ago" → uses `get_time_ago(hours=2)`
  - "yesterday" → uses `get_time_ago(days=1)`
  - "30 minutes ago" → uses `get_time_ago(minutes=30)`

### 💬 Message Search Tools

#### `search_user_messages(user_ids, channel_id, hours_back, limit)`

- **Purpose**: Search for messages from specific users in Discord
- **Status**: ✅ **FULLY IMPLEMENTED** - searches real Discord messages
- **Usage**: "Search for messages from user 221351940867620864 in the last 12 hours"
- **Parameters**:
  - `user_ids`: List of Discord user IDs (as strings)
  - `channel_id`: Optional channel to search in
  - `hours_back`: How far back to search (default: 24)
  - `limit`: Max messages to return (default: 50)
- **Features**:
  - Searches all accessible channels if no channel specified
  - Respects Discord permissions
  - Shows message content, author, timestamp, and channel
  - Sorts results by newest first

## 🎯 Example Conversations

### Time Queries

```
User: "What time is it?"
Agent: Uses get_current_time() → "Il est actuellement 2024-01-15 14:30:22 (Monday)"

User: "What was the time 3 hours ago?"
Agent: Uses get_time_ago(hours=3) → "Il y a 3 heures, c'était 2024-01-15 11:30:22 (Monday)"
```

### Message Searches

```
User: "Search for messages from user 221351940867620864 in the last 12 hours"
Agent: Uses search_user_messages() → Returns actual Discord messages from that user

User: "Find messages from users 186182405831262208 and 306827479484465172 from yesterday"
Agent: Searches multiple users, returns formatted results with timestamps and content
```

## 🧪 Testing

### Test the tools:

```bash
python test_agent.py
```

### Test individual tools:

```python
from src.agent.tools.tools import get_current_time, search_user_messages

print(get_current_time())
# search_user_messages requires Discord client to be set
```

## 🚀 Discord Usage

In Discord, mention your bot and ask:

- "Quelle heure il est?"
- "Search for messages from user 221351940867620864 yesterday"
- "What time was it 2 hours ago?"
- "Find messages from users 186182405831262208 and 306827479484465172 in the last 6 hours"

**Note**: The agent will handle name-to-ID mapping through its system prompt, so you can also ask with names like "Find messages from Younes" and the agent will convert it to the appropriate user ID.

## 🔧 Implementation Details

### Message Search Features

✅ **Real Discord Integration**: Uses actual Discord API
✅ **Multi-channel Search**: Searches all accessible channels
✅ **Permission Aware**: Respects Discord permissions
✅ **Time Filtering**: Searches within specified timeframes
✅ **Formatted Results**: Clean, readable message display
✅ **Error Handling**: Graceful handling of access errors

### Required Permissions

Your bot needs these Discord permissions:

- Read Message History
- View Channels
- Send Messages

### Discord Client Integration

- Bot automatically sets up Discord client access for tools
- Message search works immediately when bot starts
- No additional configuration needed

## 🎉 Ready to Use!

Your agent now has:

- ⏰ **Complete time management**
- 💬 **Real Discord message search**
- 🧠 **Per-user conversation memory**
- 🔍 **Multi-channel search capabilities**

The agent handles user name mapping automatically through its system prompt, making it easy for users to search by names rather than IDs!
