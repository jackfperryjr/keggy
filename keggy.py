import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='/',intents=intents)

random_messages = [
    'Here you go! 🍺',
    'Coming right up! 🍺',
    'Oh, uh, sorry... I\'m all out!',
    '🍺',
    'Sure! 🍺',
    'Did someone ask for a beer? 🍺',
    'One for you! And one for you! 🍺🍺',
    'Beers all around! 🍺🍺🍺'
]

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await message.channel.send(
        f'Hi {member.name}, welcome to {os.getenv("DISCORD_GUILD")}! Want a beer? 🍺'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if client.user.mentioned_in(message):
        await message.channel.send('Did someone need a beer? 🍺')
    if 'beer' in message.content.lower():
        await message.channel.send(random.choice(random_messages))

# Not working. Need to investigate.
@bot.command(name='keggy')
async def keggy(ctx):
    response = 'Did someone need a beer? That\'s all I know how to do. If I hear chatter about beer I\'ll be right there! (Or you can request a beer with `/beer`.)'
    await ctx.send(response)

@bot.command(name='beer')
async def beer(ctx):
    response = random.choice(random_messages)
    await ctx.send(response)

try:
    client.run(os.getenv('DISCORD_TOKEN'))
except Exception as e:
    print(f"An error occurred: {e}")
