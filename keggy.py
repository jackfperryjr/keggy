import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load the .env file containing 
# the Discord Application (Keggy) token
load_dotenv()

# Grab the intents configured in the Discord Dev Portal
intents = discord.Intents.all()

# Create a client using the above intents
client = discord.Client(intents=intents)

# Create a bot using the above intents
bot = commands.Bot(command_prefix='/',intents=intents)

# Defining an array of random messages
random_messages = [
    'Here you go! 🍺',
    'Coming right up! 🍺',
    'Oh, uh, sorry... I\'m all out!',
    '🍺',
    'Sure! 🍺',
    'Did someone ask for a beer? 🍺',
    'One for you! And one for you! 🍺🍺'
    ]

# The client responds to events that happen,
# in this case, once Keggy is connected to Discord
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

# If Keggy hears mention of a beer, he offers one
@client.event
async def on_message(message):
    if 'beer' in message.content.lower():
        await message.channel.send(random.choice(random_messages))

# Using the bot we can define commands
# for Keggy, in this case: beer
@bot.command(name='beer')
async def beer(ctx):
    response = random.choice(random_messages)
    await ctx.send(response)

# Connect Keggy to Discord
try:
    client.run(os.getenv('DISCORD_TOKEN'))
except Exception as e:
    print(f"An error occurred: {e}")
