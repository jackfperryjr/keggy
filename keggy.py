import os
import random
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='/',intents=intents)

channels = [
    '1117941300466045050', # general
    '1122709588442108034', # thundering-plains
    '1122709849558487171', # adventure-league
    '1233522005920452732', # the-cauldron
    '1233522085205250160'  # monday-fiasco
]

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

random_chatter = [
    'Did someone call me?',
    'Hi!',
    'Who\'s there!?'
]

@tasks.loop(minutes=random.randint(60, 100))
async def background_chatter():
    await client.wait_until_ready()
    while not client.is_closed:
        channel = client.get_channel(random.choice(channels))
        await channel.send(random.choice(random_messages))

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    background_chatter.start()

    for guild in client.guilds:
        if guild.name == os.getenv('DISCORD_GUILD'):
            break

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_member_join(member):
    await message.channel.send(
        f'Hi {member.name}, welcome to {os.getenv("DISCORD_GUILD")}! Want a beer? 🍺'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if client.user.mentioned_in(message) and 'help' in message.content.lower():
        await message.channel.send('Did someone need a beer? That\'s all I know how to do. If I hear someone mention a beer I\'ll be right there! (Or you can request a beer with `/beer`.)')
    if client.user.mentioned_in(message) and not 'help' in message.content.lower():
        await message.channel.send('Hi! Did someone need a beer? 🍺')
    if 'beer' in message.content.lower():
        await message.channel.send(random.choice(random_messages))

@bot.command(name='beer')
async def beer(ctx):
    response = random.choice(random_messages)
    await ctx.send(response)

try:
    client.run(os.getenv('DISCORD_TOKEN'))
except Exception as e:
    print(f"An error occurred: {e}")
