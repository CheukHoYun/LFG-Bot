import os
import discord

# Discord Intents
intents = discord.Intents.all()

# Version number
bot_version = "{BOT_VERSION}"

# Update log
update_log = "{UPDATE_LOG}"

config_env = os.getenv('DISCORD_BOT_ENV')

if config_env == "DEV":
    # Guild
    guild = discord.Object(id={GUILD_ID_DEV})

    # Default channel id for generic requests
    generic_channel = {GENERIC_CHANNEL_DEV}

    # Announcement channel for bot updates
    announcement_channel = {ANNOUNCEMENT_CHANNEL_DEV}

    # Link to the tutorial message
    tutorial_link = "{TUTORIAL_LINK_DEV}"

    # Channel id's for specific games
    overwatch = {OVERWATCH_CHANNEL_DEV}
    apex = {APEX_CHANNEL_DEV}
    league = generic_channel
    the_finals = generic_channel
    valorant = {VALORANT_CHANNEL_DEV}
    cs = {CS_CHANNEL_DEV}
    dota = generic_channel
    r6 = {R6_CHANNEL_DEV}

    # Moderator role id
    moderator_role_id = {MODERATOR_ROLE_ID_DEV}
else:
    # Guild
    guild = discord.Object(id={GUILD_ID_PROD})

    # Default channel id for generic requests
    generic_channel = {GENERIC_CHANNEL_PROD}

    # Announcement channel for bot updates
    announcement_channel = {ANNOUNCEMENT_CHANNEL_PROD}

    # Link to the tutorial message
    tutorial_link = "{TUTORIAL_LINK_PROD}"

    # Channel id's for specific games
    overwatch = {OVERWATCH_CHANNEL_PROD}
    apex = {APEX_CHANNEL_PROD}
    league = generic_channel
    the_finals = generic_channel
    valorant = {VALORANT_CHANNEL_PROD}
    cs = {CS_CHANNEL_PROD}
    dota = generic_channel
    r6 = {R6_CHANNEL_PROD}

    # Moderator role id
    moderator_role_id = {MODERATOR_ROLE_ID_PROD}