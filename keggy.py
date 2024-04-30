import os
import random
import discord
import requests
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='/', intents=intents)

random_messages = [
    'Here you go! 🍺',
    'Coming right up! 🍺',
    'Oh, uh, sorry... I\'m all out!',
    '🍺',
    'Sure! 🍺',
    'Did someone ask for a beer? 🍺',
    'One for you! And one for you! 🍺🍺',
    'Beers all around! 🍺🍺🍺',
    'Beers for everyone! 🍻 🍻 🍻'
]

def get_drink():
    r = requests.get('https://www.thecocktaildb.com/api/json/v1/1/random.php')
    drink = r.json()['drinks'][0]

    ingredients = []
    for key in drink:
        if 'strIngredient' in key and drink[key] != None:
            strMeasure = key.replace('Ingredient', 'Measure')
            if drink[strMeasure] != None:
                ingredients.append(drink[strMeasure] + drink[key])
            else:
                ingredients.append(drink[key])
    
    return {
        'name': drink['strDrink'],
        'ingredients': ', '.join(ingredients[:-1]) + ' and ' + ingredients[-1],
        'instructions': drink['strInstructions'],
        'image': drink['strDrinkThumb']
    }

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

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
    if 'celebrate' in message.content.lower():
        await message.channel.send(random_messages[8])
    if client.user.mentioned_in(message) and 'help' in message.content.lower():
        await message.channel.send('Did someone need a beer? That\'s all I know how to do. If I hear someone mention a beer I\'ll be right there! (Or you can request a beer with `/beer`.)')
    if client.user.mentioned_in(message) and not 'help' in message.content.lower():
        await message.channel.send('Hi! Did someone need a beer? 🍺')
    if 'make me a drink' in message.content.lower():
        drink = get_drink()

        embed = discord.Embed(color = 0x303136, title="Here's a drink for you!")
        for item in drink:
            if (item == 'image'):
                continue
            embed.add_field(name=item, value=drink[item], inline=False)
        embed.set_image(url=drink['image'])

        await message.channel.send(embed = embed)
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
