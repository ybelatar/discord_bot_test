# Discord ADK Agent

A sophisticated Discord bot powered by Google's Agent Development Kit (ADK) framework that combines AI agent capabilities with Discord message search functionality.

## Features

### Discord Message Search Tools

- **Time-based Search**: Search messages within specific time ranges (start time to end time)
- **User-based Search**: Search messages from specific users using friendly name mappings
- **Combined Search**: Search messages with both time and user filters simultaneously
- **Channel Information**: Retrieve Discord channel metadata and statistics

### AI Agent Capabilities

- **Natural Language Processing**: Powered by Google's Gemini models
- **Context Awareness**: Maintains conversation context and history
- **Tool Integration**: Seamlessly integrates search tools with AI responses
- **Multiple Deployment Options**: CLI testing, web interface, and Discord bot

### User-Friendly Features

- **Friendly Name Mapping**: Use simple names instead of Discord IDs
- **Time Range Flexibility**: Support for various time formats and ranges
- **Comprehensive Error Handling**: Robust error management and user feedback
- **Configurable Permissions**: Control access and usage limits

## Quick Start

### Prerequisites

- Python 3.9 or higher
- Poetry for dependency management
- Discord Bot Token
- Google API Key (AI Studio or Vertex AI)

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd discord_bot
   ```

2. **Install dependencies with Poetry**

   ```bash
   poetry install
   ```

3. **Set up environment variables**

   ```bash
   cp environment.example .env
   # Edit .env with your actual API keys and configuration
   ```

4. **Configure user mappings** (Optional)
   ```bash
   # Edit discord_agent/config/user_mapping.json
   # Or use USER_ID_MAPPING environment variable
   ```

### Configuration

#### Environment Variables

Copy `environment.example` to `.env` and configure:

```bash
# Required
DISCORD_BOT_TOKEN=your_discord_bot_token_here
GOOGLE_API_KEY=your_google_api_key_here

# Optional
GEMINI_MODEL=gemini-2.0-flash-experimental
USER_ID_MAPPING={"john": "123456789012345678", "alice": "234567890123456789"}
```

#### User ID Mapping

Map friendly names to Discord user IDs for easier searching:

**Method 1: Environment Variable**

```bash
USER_ID_MAPPING={"john": "123456789012345678", "alice": "234567890123456789"}
```

**Method 2: JSON Configuration File**
Create `discord_agent/config/user_mapping.json`:

```json
{
  "john": "123456789012345678",
  "alice": "234567890123456789",
  "admin": "456789012345678901"
}
```

### Usage

#### Running the Discord Bot

```bash
poetry run python -m discord_agent.main
```

#### CLI Testing

```bash
poetry run python run_adk_agent.py
```

#### Web Interface

```bash
# Start ADK development server
poetry run adk dev
```

### Discord Commands

Once the bot is running and invited to your server:

- `@bot search messages from john in the last 2 hours`
- `@bot find messages between 2025-01-15T10:00:00 and 2025-01-15T18:00:00`
- `@bot show channel information`
- `@bot help with message search`

### Search Tool Examples

The bot provides several search capabilities:

1. **Time Range Search**

   - "Find messages from the last 6 hours"
   - "Search messages between 2025-01-15T09:00:00 and 2025-01-15T17:00:00"

2. **User-based Search**

   - "Show messages from john"
   - "Find posts by alice"

3. **Combined Search**
   - "Messages from john in the last 2 hours"
   - "Posts by alice between 10 AM and 2 PM today"

## Project Structure

```
discord_bot/
├── discord_agent/
│   ├── __init__.py           # Main package
│   ├── agent.py              # ADK Agent implementation
│   ├── main.py               # Discord bot entry point
│   ├── tools/
│   │   ├── __init__.py
│   │   └── message_search.py # Discord search tools
│   └── config/
│       └── user_mapping.json # User ID mappings
├── .taskmaster/              # TaskMaster project management
├── pyproject.toml            # Poetry configuration
├── environment.example       # Environment template
└── README.md                 # This file
```

## Development

### Task Management

This project uses TaskMaster for structured development:

```bash
# View current tasks
poetry run taskmaster get-tasks

# Expand a task into subtasks
poetry run taskmaster expand-task --id 1

# Mark task as completed
poetry run taskmaster update-task --id 1.1 --status done
```

### Code Quality

The project includes development tools:

```bash
# Code formatting
poetry run black discord_agent/

# Linting
poetry run flake8 discord_agent/

# Type checking
poetry run mypy discord_agent/

# Testing
poetry run pytest
```

## Architecture

### Core Components

1. **DiscordAgent**: Main ADK agent with tool integration
2. **DiscordMessageSearcher**: Message search functionality
3. **Tool Functions**: ADK-compatible search functions
4. **Configuration System**: Environment and file-based config

### Google ADK Integration

The project leverages Google's ADK framework for:

- Agent creation and management
- Tool specification and integration
- Natural language understanding
- Context management and conversation flow

### Discord Integration

Built on discord.py for:

- Bot lifecycle management
- Event handling and message processing
- Discord API interaction
- Async/await patterns

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:

- Create an issue in the repository
- Check the TaskMaster documentation
- Review the Google ADK documentation
- Discord.py documentation for Discord-specific functionality
