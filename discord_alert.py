import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import sys

# Add parent directory to path so we can import display_table
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from display_table import display_neat_table

# 1. Setup the bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

load_dotenv()

# 2. Define the "on_ready" event
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        # This "syncs" your slash commands so they show up in Discord
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)

# 3. Create a Slash Command (No class needed!)
@bot.tree.command(name='send_info', description='Bot will send data regarding current situation of network')
async def send_info(interaction: discord.Interaction):
    message = display_neat_table()
    await interaction.response.send_message(message)


@bot.event
async def send_alert(message):
    await bot.get_channel(1224673507208859711).send(message)


def run_bot():
    bot.run(os.getenv('API_KEY'))
    