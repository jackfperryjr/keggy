import os
import re
import random
import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)

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

def get_races(race=None):
    if race == None:
        r = requests.get(f'https://www.dnd5eapi.co/api/races')
        return r.json()
    if race != None:
        r = requests.get(f'https://www.dnd5eapi.co/api/races/{race}')
        return r.json()

def get_monsters(monster_name=None,monster_cr=None):
    if monster_name == None and monster_cr == None:
        r = requests.get(f'https://www.dnd5eapi.co/api/monsters')
        return r.json()
    if monster_name == None and monster_cr != None:
        r = requests.get(f'https://www.dnd5eapi.co/api/monsters?challenge_rating={monster_cr}')
        return r.json()
    if monster_name != None and monster_cr == None:
        m = monster_name.strip().replace(' ', '-').lower()
        r = requests.get(f'https://www.dnd5eapi.co/api/monsters/{m}')
        return r.json()

# def get_races():
#     r = requests.get('https://www.dnd5eapi.co/api/races')
#     return r.text

# def get_races():
#     r = requests.get('https://www.dnd5eapi.co/api/races')
#     return r.text

# def get_races():
#     r = requests.get('https://www.dnd5eapi.co/api/races')
#     return r.text

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
    if message.author == bot.user:
        return
    await bot.process_commands(message)

    # if bot.user.mentioned_in(message) and not 'help' in message.content.lower():
    #     await message.channel.send('Sure, boss! Did someone need a beer? 🍺')

    if bot.user.mentioned_in(message) and 'tell me about' in message.content.lower() and 'monster' in message.content.lower():
        await message.channel.send('Sure, boss!')
        monster_in_message = re.search(r'tell me about the(.*?)monster', message.content).group(1)
        monster_from_api = get_monsters(monster_name=monster_in_message)

        if 'error' in monster_from_api:
            await message.author.send('Oh, uh, I actually don\'t know that one!')
            return

        embed = discord.Embed(color = 0x303136, title=monster_in_message)
        embed.add_field(name='size', value=monster_from_api['size'], inline=True)
        embed.add_field(name='challenge_rating', value=monster_from_api['challenge_rating'], inline=True)
        embed.add_field(name='strength', value=monster_from_api['strength'], inline=True)
        embed.add_field(name='dexterity', value=monster_from_api['dexterity'], inline=True)
        embed.add_field(name='constitution', value=monster_from_api['constitution'], inline=True)
        embed.add_field(name='intelligence', value=monster_from_api['intelligence'], inline=True)
        embed.add_field(name='wisdom', value=monster_from_api['wisdom'], inline=True)
        embed.add_field(name='charisma', value=monster_from_api['charisma'], inline=True)
        embed.add_field(name='hit_points', value=monster_from_api['hit_points'], inline=True)
        embed.add_field(name='speed', value=monster_from_api['speed'], inline=False)
        embed.add_field(name='armor_class', value=monster_from_api['armor_class'], inline=False)
        embed.add_field(name='actions', value=monster_from_api['actions'], inline=False)
        embed.add_field(name='special_abilities', value=monster_from_api['special_abilities'], inline=False)
        await message.author.send(embed = embed)

    if 'make me a drink' in message.content.lower():
        emojis = ['🍸','🍷','🥃','🍹','☕']
        drink = get_drink()

        embed = discord.Embed(color = 0x303136, title="Here's a drink for you!")
        for item in drink:
            if (item == 'image'):
                continue
            embed.add_field(name=item, value=drink[item], inline=False)
        embed.set_image(url=drink['image'])

        message = await message.channel.send(embed = embed)
        for emoji in emojis:
            await message.add_reaction(emoji)

    if 'beer' in message.content.lower() and not '/' in message.content.lower():
        await message.add_reaction('🍺')

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
    response = random.choice(random_messages)
    await ctx.send(response)

@bot.command(name='celebrate',brief='Keggy gets beers for everyone.')
async def celebrate(ctx):
    response = 'Beers for everyone! 🍻 🍻 🍻'
    await ctx.send(response)

try:
    bot.run(os.getenv('DISCORD_TOKEN_DEV'))
except Exception as e:
    print(f"An error occurred: {e}")
