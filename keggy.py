import os
import random
import discord
import re
import requests
from discord.ext import commands
from dotenv import load_dotenv

from kegerator import Kegerator
from responses import Responses
from currency_utils import CurrencyUtils

keggy_store = Kegerator()
responses = Responses()
currency_utils = CurrencyUtils()

load_dotenv()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)

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

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

    for guild in bot.guilds:
        if guild.name == os.getenv('DISCORD_GUILD'):
            break

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@bot.event
async def on_member_join(member):
    await message.channel.send(
        f'Hi {member.name}, welcome to {os.getenv("DISCORD_GUILD")}! Want a beer? 🍺'
    )

@bot.event
async def on_message(message):
    # Blocks the bot from responding to itself
    if message.author == bot.user:
        return
    
    # Process Bot Commands
    await bot.process_commands(message)

    # Blocks on Fritz
    if keggy_store.checkFritz():
        await message.channel.send(responses.getRandomFritzMessage())
        return

    if bot.user.mentioned_in(message) and 'help' in message.content.lower():
        await message.channel.send('Did someone need a beer? That\'s all I know how to do. If I hear someone mention a beer I\'ll be right there! (Or you can request a beer with `/beer`.)')
    
    if bot.user.mentioned_in(message) and not 'help' in message.content.lower():
        await message.channel.send('Sure, boss! Did someone need a beer? 🍺')

    if 'make me a drink' in message.content.lower():
        await message.add_reaction(responses.getRandomEmoji())
        drink = get_drink()
        embed = discord.Embed(color = 0x303136, title="Here's a drink for you!")
        for item in drink:
            if (item == 'image'):
                continue
            embed.add_field(name=item, value=drink[item], inline=False)
        embed.set_image(url=drink['image'])

        message = await message.channel.send(embed = embed)

    if 'beer' in message.content.lower() and not '/' in message.content.lower():
        await message.add_reaction(responses.getBeerEmoji())
        await message.channel.send(responses.getRandomPositiveMessage())

@bot.command()
async def help(ctx, args=None):
    help_embed = discord.Embed(color = 0x303136, title='Hi, I\'m Keggy! Did you want a beer?')
    command_list = [c.name for c in bot.commands]

    if not args:
        help_embed.add_field(
            name="Available commands:",
            value="\n".join([c.name for i, c in enumerate(bot.commands)]),
            inline=False
        )
        help_embed.add_field(
            name="",
            value="Type `/help <command name>` for more details about each command.",
            inline=False
        )

    elif args in command_list:
        help_embed.add_field(
            name=args,
            value=bot.get_command(args).brief
        )

    else:
        help_embed.add_field(
            name="",
            value="Sorry, boss! Is that a new kind of beer?"
        )

    message = await ctx.send(embed=help_embed)
    await message.add_reaction('🍻')

@bot.command(name='beer',brief='Keggy gets you a beer.')
async def beer(ctx):
    if (keggy_store.checkFritz()):
        response = responses.getRandomFritzMessage()
        await ctx.send(response)
        return
    response = responses.getRandomPositiveMessage()
    await ctx.send(response)

@bot.command()
async def convert(ctx, arg):
    if (keggy_store.checkFritz()):
        response = responses.getRandomFritzMessage()
        await ctx.send(response)
        return

    copper = currency_utils.convert_to_copper(arg)
    response = f'That\'s {copper} copper pieces!'
    await ctx.send(response)

@bot.command()
async def split_shares(ctx, arg):
    if (keggy_store.checkFritz()):
        response = responses.getRandomFritzMessage()
        await ctx.send(response)
        return

    copper = currency_utils.convert_to_copper(arg)
    split, remainder = currency_utils.split_copper(copper, 3)
    split_currency = currency_utils.convert_to_currency(split)
    remainder_currency = currency_utils.convert_to_currency(remainder)

    response = f'Each person gets {split_currency["pp"]}pp {split_currency["gp"]}gp {split_currency["ep"]}ep {split_currency["sp"]}sp {split_currency["cp"]}cp. There are {remainder_currency["pp"]}pp {remainder_currency["gp"]}gp {remainder_currency["ep"]}ep {remainder_currency["sp"]}sp {remainder_currency["cp"]}cp left over.'
    await ctx.send(response)

@bot.command(name='celebrate',brief='Keggy gets beers for everyone.')
async def celebrate(ctx):
    if (keggy_store.checkFritz()):
        response = responses.getRandomFritzMessage()
        await ctx.send(response)
        return
    response = 'Beers for everyone! 🍻 🍻 🍻'
    await ctx.send(response)

try:
    bot.run(os.getenv('DISCORD_TOKEN'))
except Exception as e:
    print(f"An error occurred: {e}")
