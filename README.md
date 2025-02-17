# Discord LFG Bot

A Discord bot designed for **Looking For Group (LFG)** matchmaking across multiple games. Users can quickly post LFG requests and join voice channels. 

## Features
- **Game Selection Menu**: Users choose a game, rank, and mode through an interactive UI.
- **LFG Request Management**: Users can create, update, and delete LFG requests.
- **Game ID Storage**: The bot remembers the users' game ID's for future LFG requests they make. 
- **Voice Channel Integration**: Automatically tracks user counts in voice channels.

## Installation & Setup
### Prerequisites
- Python 3.11+
- `discord.py`
- `mysql.connector`
- A MySQL database

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/CheukHoYun/LFG-Bot.git
   ```
2. Install dependencies:
   ```bash
   pip install discord
   pip install mysql.connector
   ```
3. Set up environment variables:
   ```
   DISCORD_BOT_TOKEN=YOUR_BOT_TOKEN
   DISCORD_BOT_ENV=DEV # Or PROD
   ```
4. Configure `config.py`. You will need to set up your guild ID, the ID of a moderator role, and the ID's of channels to which the bot's messages will be sent. There's one set of config for DEV and a separate one for PROD. 
5. Set up your command name in `commands.py`, which is `lfg` by default. It must match the slash command you set up for your bot in your Discord dev portal. 
6. Configure **MySQL database** in `data_handler.py`. This database feature is for the bot to remember users' in-game ID's so they won't have to repeatedly type them in when they create future LFG requests. 
7. Run the bot:
   ```bash
   cd discord-lfg-bot
   python bot.py
   ```
   A "bot rebooted" message will be sent to the designated channel. If you don't want it, you can run the bot in silent mode:
   ```bash
   python bot.py -s
   ```

## File Overview
### `bot.py`
- Main entry point.
- Initializes the bot and loads configurations.
- Connects event handlers, command trees, and data handlers.

### `commands.py`
- Defines Discord slash commands (e.g., `/lfg` for LFG requests).
- Ensures users follow LFG rules (one request at a time, must be in a voice channel).

### `config.py`
- Stores **environment settings**, **guild/channel IDs**, and **moderator role IDs**.
- Supports switching between **DEV** and **PROD** environments.

### `data_handler.py`
- Handles MySQL database connections.
- Manages **game ID storage** (retrieval, addition, and modification).

### `embed_creator.py`
- Creates **rich Discord embeds** for LFG messages.
- Displays **game details, rank, mode, and player count**.

### `events.py`
- Handles bot lifecycle events (`on_ready()`, `on_voice_state_update()`).
- Updates LFG messages when users join/leave voice channels.

### `game.py`
- Defines supported **games** (e.g., Overwatch, Apex, Valorant).
- Stores **rank tiers, game modes, and channel IDs**.

### `lfg_request.py`
- Manages **active LFG requests**.
- Prevents duplicate requests.
- Provides an **interactive delete button**.

### `tasks.py`
- Runs background tasks (e.g., logging active requests every 60 seconds).

### `ui_main_menu.py`
- Implements **interactive UI elements** (dropdowns, modals, buttons).
- Collects user input for **game, rank, mode, and custom message**.

## Usage Guide
1. Join a voice channel.
2. **Use `/lfg` to start an LFG request.**
3. **Select a game, rank, and mode.**
4. **Provide your game ID (optional).**
5. **Post the LFG request.**
6. **Other users can join your voice channel using the interactive buttons.**

## Contribution
Feel free to **fork** and **submit pull requests**! If you find issues, report them via GitHub.

## License
[MIT License](LICENSE)

