import discord
from discord.ext import commands

from keggy_api import KeggyApi
from kegerator import Kegerator
from utils import Utils

api = KeggyApi()
keggy_store = Kegerator()
utils = Utils()

class KeggyHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def help(self, ctx, args=None):
        help_embed = discord.Embed(color = 0x303136, title='Hi, I\'m Keggy! Did you want a beer?')
        command_list = [c.name for c in self.bot.commands]

        if not args:
            help_embed.add_field(
                name="Available commands:",
                value="\n".join([c.name for i, c in enumerate(self.bot.commands)]),
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
                value=self.bot.get_command(args).brief
            )

        else:
            help_embed.add_field(
                name="",
                value="Sorry, boss! Is that a new kind of beer?"
            )

        await ctx.send(embed=help_embed)

class KeggyFun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='drink', brief='Keggy will make you a cocktail! (Or at least find you a cocktail recipe.)')
    async def drink(self, ctx):
        drink = api.get_drink()
        embed = discord.Embed(color=0x303136, title="Here's a drink for you!")
        for item in drink:
            if (item == 'image'):
                continue
            embed.add_field(name=item, value=drink[item], inline=False)
        embed.set_image(url=drink['image'])

        await ctx.send(embed = embed)

class DungeonsAndDragons(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='item', brief='Keggy will look inside himself and try to deliever information about the item you requested.')
    async def item(self, ctx, *, item):
        await ctx.send('Sure, boss! Coming right up!')
        item_from_api = api.get_magic_item(item=item)

        if 'error' in item_from_api:
            await ctx.send('Oh, uh, sorry boss... I actually don\'t know that one!')
            return

        embed = discord.Embed(color = 0x303136, title=item.upper())
        embed.add_field(name='', value="---", inline=False)
        for obj in item_from_api['desc']:
            value = obj
            embed.add_field(name='', value=f'{value}', inline=False)
        
        await ctx.send(embed = embed)

    @commands.command(name='monster', brief='Keggy will look inside himself and try to deliver information about the monster you requested.')
    async def monster(self, ctx, *, monster_name):
        await ctx.send('Sure, boss! I\'ll send you a private message with details.')
        monster_from_api = api.get_monsters(monster_name=monster_name)

        if 'error' in monster_from_api:
            await ctx.send('Oh, uh, sorry boss... I actually don\'t know that one!')
            return

        embed = discord.Embed(color=0x303136, title=monster_name.upper())
        embed.add_field(name='', value="---", inline=False)
        embed.add_field(name='', value=f'The **{monster_name}** is a *{monster_from_api["size"].lower()}* CR *{monster_from_api["challenge_rating"]}* *{monster_from_api["type"]}* type with *{monster_from_api["hit_points"]}* hit points. It can take the following actions and has the below stats:', inline=False)
        embed.add_field(name='STATS', value="", inline=False)
        embed.add_field(name='', value=f'STR: {utils.get_stat_mod(monster_from_api["strength"])}', inline=True)
        embed.add_field(name='', value=f'DEX: {utils.get_stat_mod(monster_from_api["dexterity"])}', inline=True)
        embed.add_field(name='', value=f'CON: {utils.get_stat_mod(monster_from_api["constitution"])}', inline=True)
        embed.add_field(name='', value=f'INT: {utils.get_stat_mod(monster_from_api["intelligence"])}', inline=True)
        embed.add_field(name='', value=f'WIS: {utils.get_stat_mod(monster_from_api["wisdom"])}', inline=True)
        embed.add_field(name='', value=f'CHA: {utils.get_stat_mod(monster_from_api["charisma"])}', inline=True)

        embed.add_field(name='SPEED', value="", inline=False)
        for obj in monster_from_api['speed']:
            key = obj
            value = monster_from_api['speed'][obj]
            embed.add_field(name="", value=f'{value} {key}', inline=True)

        embed.add_field(name='AC', value="", inline=False)
        for obj in monster_from_api['armor_class']:
                armor_type = obj['type']
                value = obj['value']
                embed.add_field(name="", value=f'{value}, {armor_type}', inline=True)

        embed.add_field(name='ACTIONS', value="", inline=False)
        for obj in monster_from_api['actions']:
            name = obj['name']
            desc = obj['desc']
            if name == 'Multiattack':
                embed.add_field(name="", value=f'**{name}**: {desc}', inline=False)
                continue
            embed.add_field(name="", value=f'**{name}**: {desc}', inline=False)

        embed.add_field(name='SPECIAL', value="", inline=False)
        for obj in monster_from_api['special_abilities']:
            key = obj['name']
            value = obj['desc']
            embed.add_field(name="", value=f'**{key}**: {value}', inline=False)

        await ctx.send(embed = embed)

    @commands.command(name='convert', brief='Keggy can convert coin denominations to coppers (cp) using this format: 12pp34gp56sp78cp.')
    async def convert(self, ctx, arg):
        if (keggy_store.check_fritz()):
            response = responses.get_random_fritz_message()
            await ctx.send(response)
            return

        copper = utils.convert_to_copper(arg)
        response = f'That\'s {copper} copper pieces!'
        await ctx.send(response)

    @commands.command(name='split', brief='Keggy can split up copper pieces shares. You can use `/convert` to conver a variety of pieces into copper pieces.')
    async def split(self, ctx, arg=None):
        if arg == None:
            await ctx.send('You have to tell me how many copper pieces to split!')

        if (keggy_store.check_fritz()):
            response = responses.get_random_fritz_message()
            await ctx.send(response)
            return

        copper = utils.convert_to_copper(arg)
        split, remainder = utils.split_copper(copper, 3)
        split_currency = utils.convert_to_currency(split)
        remainder_currency = utils.convert_to_currency(remainder)

        response = f'Each person gets {split_currency["pp"]}pp {split_currency["gp"]}gp {split_currency["ep"]}ep {split_currency["sp"]}sp {split_currency["cp"]}cp. There are {remainder_currency["pp"]}pp {remainder_currency["gp"]}gp {remainder_currency["ep"]}ep {remainder_currency["sp"]}sp {remainder_currency["cp"]}cp left over.'
        await ctx.send(response)

async def setup(bot):
    await bot.add_cog(KeggyHelp(bot))
    await bot.add_cog(KeggyFun(bot))
    await bot.add_cog(DungeonsAndDragons(bot))
    