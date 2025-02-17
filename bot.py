import os
import discord
import config
import events
import commands
import data_handler
import lfg_request
import argparse

# Set up argument parsing
parser = argparse.ArgumentParser()

# Starting the program in silent mode won't send a message to the announcement channel
parser.add_argument('-s', '--silent', action='store_true', help="Enable silent mode")
args = parser.parse_args()

silent = False
if args.silent:
    silent = True


intents = config.intents  # Ensure you have the necessary intents
client = discord.Client(intents=intents)
guild = config.guild
command_tree = commands.setup(client, guild)
events.setup(client, command_tree, guild, silent)
data_handler = data_handler.DataHandler()
request_manager = lfg_request.RequestManager()

# Set up your bot token as an OS environment variable,
# or hardcode it if you don't care about security.
token = os.getenv('DISCORD_BOT_TOKEN')
client.run(token)
