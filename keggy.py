import os
import random
import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

from kegerator import Kegerator
from responses import Responses
from utils import Utils

keggy_store = Kegerator()
responses = Responses()
utils = Utils()

load_dotenv()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)

async def is_message_blocked(message):
    # Blocks the bot from responding to itself
    if message.author == bot.user:
        return True

    # Blocks on Fritz
    if bot.user.mentioned_in(message) and keggy_store.check_fritz():
        keggy_store.resetFrtiz()
        await message.add_reaction("❌")
        await message.channel.send(responses.get_random_fritz_message())
        return True

    return False

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

    for guild in bot.guilds:
        if guild.name == os.getenv('DISCORD_GUILD'):
            break

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

    await bot.load_extension('keggy_commands')
    print('Keggy comands loaded!')

@bot.event
async def on_member_join(member):
    await message.channel.send(
        f'Hi {member.name}, welcome to {os.getenv("DISCORD_GUILD")}! Want a beer? 🍺'
    )

@bot.event
async def on_message(message):
    # Process Bot Commands
    await bot.process_commands(message)
    # Blocks the bot from responding to itself

    if await is_message_blocked(message):
        return

    if 'beer' in message.content.lower():
        await message.add_reaction(responses.get_beer_emoji())

try:
    bot.run(os.getenv('DISCORD_TOKEN'))
except Exception as e:
    print(f"An error occurred: {e}")
