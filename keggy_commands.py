import numbers
import discord
from discord.ext import commands

from keggy_api import KeggyApi
from kegerator import Kegerator
from responses import Responses
from utils import Utils

api = KeggyApi()
keggy_store = Kegerator()
utils = Utils()
response = Responses()

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
        keggy_store.update_last_command('drink', None)
        drink = api.get_drink()
        embed = discord.Embed(color=0x303136, title="Here's a drink for you!")
        for item in drink:
            if (item == 'image'):
                continue
            embed.add_field(name=item, value=drink[item], inline=False)
        embed.set_image(url=drink['image'])

        await ctx.send(embed = embed)

class KeggyUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.command_names = {
            'drink': None,
            'help': 'help',
            'item': 'item',
            'monster': 'monster_name',
            'convert': 'string_currency',
            'split': ['copper_pieces', 'party_quantity']
        }

    @commands.command(name='rerun', brief='Keggy will rerun the last command issued.')
    async def rerun(self, ctx):
        if keggy_store.get_store_value('last_command') == '':
            await ctx.send('I don\'t have a command to rerun!')
            return
        
        command_to_rerun = self.bot.get_command(keggy_store.get_store_value('last_command'))

        await ctx.send('Rerunning command...')
        if keggy_store.get_store_value('last_command') == 'split':
            copper_pieces, party_quantity = keggy_store.get_store_value("last_command_args").values()
            await ctx.invoke(command_to_rerun, copper_pieces, party_quantity)
        elif keggy_store.get_store_value('last_command') == 'drink':
            await ctx.invoke(command_to_rerun)
        else:
            args = { self.command_names[keggy_store.get_store_value('last_command')]: keggy_store.get_store_value('last_command_args')}
            await ctx.invoke(command_to_rerun, **args)

class DungeonsAndDragons(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='item', brief='Keggy will look inside himself and try to deliever information about the item you requested.')
    async def item(self, ctx, *, item=None):
        keggy_store.update_last_command('item', item)
        await ctx.send('Sure, boss! Coming right up!')

        if item == None:
            await ctx.send('What item were you looking for?')
            return

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
    async def monster(self, ctx, *, monster_name=None):
        keggy_store.update_last_command('monster', monster_name)
        await ctx.send('Sure, boss! Coming right up!')

        if monster_name == None:
            await ctx.send('What monster were you looking for?')
            return

        monster_from_api = api.get_monsters(monster_name=monster_name)

        if 'error' in monster_from_api:
            await ctx.send('Oh, uh, sorry boss... I actually don\'t know that one!')
            return

        if 'detail' in monster_from_api:
            await ctx.send('Oh, uh, sorry boss... I actually don\'t know that one!')
            return

        embed = discord.Embed(color=0x303136, title=monster_name.upper())
        embed.add_field(name='', value="---", inline=False)
        embed.add_field(name='', value=f'The **{monster_name}** is a *{monster_from_api["size"].lower()}* CR *{monster_from_api["challenge_rating"]}* *{monster_from_api["type"]}* type with *{monster_from_api["hit_points"]}* hit points. It can take the following actions and has the below stats:', inline=False)
        embed.add_field(name='*STATS*', value=f'**STR**: {utils.get_stat_mod(monster_from_api["strength"])}\u1CBC\u1CBC\u1CBC\u1CBC\u1CBC\u1CBC**DEX**: {utils.get_stat_mod(monster_from_api["dexterity"])}\u1CBC\u1CBC\u1CBC\u1CBC\u1CBC\u1CBC**CON**: {utils.get_stat_mod(monster_from_api["constitution"])}\n**INT**: {utils.get_stat_mod(monster_from_api["intelligence"])}\u1CBC\u1CBC\u1CBC\u1CBC\u1CBC\u1CBC\u1CBC\u1CBC**WIS**: {utils.get_stat_mod(monster_from_api["wisdom"])}\u1CBC\u1CBC\u1CBC\u1CBC\u1CBC\u1CBC**CHA**: {utils.get_stat_mod(monster_from_api["charisma"])}', inline=True)
        embed.add_field(name="", value=f'**AC**: {monster_from_api['armor_class']}, {monster_from_api['armor_desc']}', inline=False)

        embed.add_field(name='*SPEED*', value="", inline=False)
        for obj in monster_from_api['speed']:
            key = obj
            value = monster_from_api['speed'][obj]
            embed.add_field(name="", value=f'{value} {key}', inline=True)

        embed.add_field(name='*ACTIONS*', value="", inline=False)
        for obj in monster_from_api['actions']:
            name = obj['name']
            desc = obj['desc']
            if name == 'Multiattack':
                embed.add_field(name="", value=f'**{name}**: {desc}', inline=False)
                continue
            embed.add_field(name="", value=f'**{name}**: {desc}', inline=False)

        embed.add_field(name='*SPECIAL*', value="", inline=False)
        for obj in monster_from_api['special_abilities']:
            key = obj['name']
            value = obj['desc']
            embed.add_field(name="", value=f'**{key}**: {value}', inline=False)

        damage_vulnerabilities = monster_from_api['damage_vulnerabilities']
        damage_vulnerabilities = 'N/a' if len(damage_vulnerabilities) == 0 else damage_vulnerabilities
        embed.add_field(name='*DMG VULNERABILITIES*', value=f'{damage_vulnerabilities}', inline=True)

        damage_resistances = monster_from_api['damage_resistances']
        damage_resistances = 'N/a' if len(damage_resistances) == 0 else damage_resistances
        embed.add_field(name='*DMG RESISTANCES*', value=f'{damage_resistances}', inline=True)

        damage_immunities = monster_from_api['damage_immunities']
        damage_immunities = 'N/a' if len(damage_immunities) == 0 else damage_immunities
        embed.add_field(name='*DMG IMMUNITIES*', value=f'{damage_immunities}', inline=True)

        condition_immunities = monster_from_api['condition_immunities']
        condition_immunities = 'N/a' if len(condition_immunities) == 0 else condition_immunities
        embed.add_field(name='*CONTITON IMMUNITIES*', value=f'{condition_immunities}', inline=True)

        senses = monster_from_api['senses']
        senses = 'N/a' if len(senses) == 0 else senses
        embed.add_field(name='*SENSES*', value=f'{senses.lower()}', inline=True)

        await ctx.send(embed = embed)

    @commands.command(name='convert', brief='Keggy can convert coin denominations to coppers (cp) using this format: 12pp34gp56sp78cp.')
    async def convert(self, ctx, string_currency=None):
        keggy_store.update_last_command('convert', string_currency)
        if (keggy_store.check_fritz()):
            response = response.get_random_fritz_message()
            await ctx.send(response)
            return
        
        if string_currency == None:
            await ctx.send('Convert what?')
            return

        copper = utils.convert_to_copper(string_currency)
        response = f'That\'s {copper} copper pieces!'
        await ctx.send(response)

    @commands.command(name='split', brief='Keggy can split up copper piece shares for each party member (default = 3). You can use `/convert` to convert a variety of pieces into copper pieces.')
    async def split(self, ctx, copper_pieces=None, party_quantity=None):
        default_party_quantity = 3
        keggy_store.update_last_command('split', { "copper_pieces": copper_pieces, "party_quantity": party_quantity or default_party_quantity })

        if (keggy_store.check_fritz()):
            response = response.get_random_fritz_message()
            await ctx.send(response)
            return

        if copper_pieces == None:
            await ctx.send('I can\'t count! You have to tell me how many copper pieces to split!')
            return

        if party_quantity == None:
            party_quantity = default_party_quantity
            await ctx.send('I don\'t know how many of you there are! I\'ll just guess (using default of 3)!')

        if not str(copper_pieces).isnumeric():
            await ctx.send(f'**{copper_pieces}** is gibberish! Try `/convert` first.')
            return

        if not str(party_quantity).isnumeric():
            await ctx.send(f'You have **{party_quantity}** in your party? Is that a real number?')
            return

        copper = utils.convert_to_copper(copper_pieces)
        split, remainder = utils.split_copper(copper, party_quantity)
        split_currency = utils.convert_to_currency(split)
        split_currency_filtered = {k: v for k, v in split_currency.items() if v != 0}
        split_currency_string = ', '.join(['{}{}'.format(v,k) for k,v in split_currency_filtered.items()])

        remainder_currency = utils.convert_to_currency(remainder)
        remainder_currency_filtered = {k: v for k, v in remainder_currency.items() if v != 0}
        remainder_currency_string = ', '.join(['{}{}'.format(v,k) for k,v in remainder_currency_filtered.items()])
        if len(remainder_currency_string) == 0:
            remainder_currency_string = '0'

        response = f'All **{party_quantity}** of you gets **{split_currency_string}**. There was a remainder of **{remainder_currency_string}** for me?'
        await ctx.send(response)

async def setup(bot):
    await bot.add_cog(KeggyHelp(bot))
    await bot.add_cog(KeggyFun(bot))
    await bot.add_cog(KeggyUtils(bot))
    await bot.add_cog(DungeonsAndDragons(bot))
    