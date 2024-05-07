import discord
from discord.ext import commands

from keggy_api import KeggyApi
from dnd_utils import DndUtils

api = KeggyApi()
utils = DndUtils()

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
        embed.add_field(name='', value=f'STR: {util.get_stat_mod(monster_from_api["strength"])}', inline=True)
        embed.add_field(name='', value=f'DEX: {util.get_stat_mod(monster_from_api["dexterity"])}', inline=True)
        embed.add_field(name='', value=f'CON: {util.get_stat_mod(monster_from_api["constitution"])}', inline=True)
        embed.add_field(name='', value=f'INT: {util.get_stat_mod(monster_from_api["intelligence"])}', inline=True)
        embed.add_field(name='', value=f'WIS: {util.get_stat_mod(monster_from_api["wisdom"])}', inline=True)
        embed.add_field(name='', value=f'CHA: {util.get_stat_mod(monster_from_api["charisma"])}', inline=True)

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

async def setup(bot):
    await bot.add_cog(DungeonsAndDragons(bot))
    