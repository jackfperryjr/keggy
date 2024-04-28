import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!',intents=intents)

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    random_messages = [
        'Here you go! 🍺',
        'Coming right up! 🍺',
        'Oh, uh, sorry... I\'m all out!',
        '🍺',
        'Sure! 🍺',
        'Did someone ask for a beer? 🍺',
        'One for you! And one for you! 🍺🍺'
    ]

    if 'beer' in message.content.lower():
        await message.channel.send(random.choice(random_messages))

@bot.command(name='beer')
async def beer(ctx):
    random_messages = [
        'Here you go! 🍺',
        'Coming right up! 🍺',
        'Oh, uh, sorry... I\'m all out!',
        '🍺',
        'Sure! 🍺',
        'Did someone ask for a beer? 🍺',
        'One for you! And one for you! 🍺🍺'
    ]

    response = random.choice(random_messages)
    await ctx.send(response)

try:
    client.run(os.getenv('DISCORD_TOKEN'))
except Exception as e:
    print(f"An error occurred: {e}")
