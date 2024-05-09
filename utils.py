import re
import discord

class Utils:
    def __init__(self):
        self.conversion_rates = {
        'pp': 1000,
        'gp': 100,
        'ep': 50,
        'sp': 10,
        'cp': 1
        }

    def get_stat_mod(self, stat_value):
        mod = (stat_value-10) // 2
        if mod >= 0:
            return f'{stat_value} (+{mod})'
        else:
            return f'{stat_value} ({mod})'

    def convert_to_copper(self, currency_string):
        matches = re.findall(r'(\d+)(pp|gp|ep|sp|cp)', currency_string)
        if not matches:
            return int(currency_string)

        # Convert each match to copper and sum them up
        total_copper = sum(int(number) * self.conversion_rates[currency] for number, currency in matches)
        return total_copper

    def split_copper(self, copper, shares):
        split = int(copper) // int(shares)
        remainder = int(copper) % int(shares)
        return split, remainder

    def convert_to_currency(self, copper):
        currency = {}
        for key, value in self.conversion_rates.items():
            currency[key] = copper // value
            copper %= value
        return currency

    def embed_subrace(self, subrace):
        embed = discord.Embed(color = 0x303136, title=subrace['name'].upper())
        embed.add_field(name='', value="---", inline=False)
        embed.add_field(name='', value=f'{subrace["desc"]}', inline=False)
        embed.add_field(name='*ABILITY BONUSES*', value="", inline=False)
        for obj in subrace['ability_bonuses']:
            bonus = obj['bonus']
            name = obj['ability_score']['name']
            embed.add_field(name="", value=f'**{name}**: +{bonus}', inline=True)
        if len(subrace['starting_proficiencies']) > 0:
            proficiencies = ', '.join([s['name'] for s in subrace['starting_proficiencies']])
            embed.add_field(name='*PROFICIENCIES*', value=f'{proficiencies.lower()}', inline=False)
        if len(subrace['racial_traits']) > 0:
            racial_traits = ', '.join([t['name'] for t in subrace['racial_traits']])
            embed.add_field(name='*TRAITS*', value=f'{racial_traits.lower()}', inline=False)
        
        return embed

    def embed_race(self, race):
        embed = discord.Embed(color = 0x303136, title=race['name'].upper())
        embed.add_field(name='', value="---", inline=False)
        embed.add_field(name='', value=f'{race["size_description"]} {race["language_desc"]} {race["age"].replace(".", ",")} {race["alignment"].replace("Humans", "and")}', inline=False)
        embed.add_field(name='*ABILITY BONUSES*', value="", inline=False)
        for obj in race['ability_bonuses']:
            bonus = obj['bonus']
            name = obj['ability_score']['name']
            embed.add_field(name="", value=f'**{name}**: +{bonus}', inline=True)
        if len(race['starting_proficiencies']) > 0:
            proficiencies = ', '.join([s['name'] for s in race['starting_proficiencies']])
            embed.add_field(name='*PROFICIENCIES*', value=f'{proficiencies.lower()}', inline=False)
        if len(race['traits']) > 0:
            traits = ', '.join([t['name'] for t in race['traits']])
            embed.add_field(name='*TRAITS*', value=f'{traits.lower()}', inline=False)
        if len(race['subraces']) > 0:
            subraces = ', '.join([s['name'] for s in race['subraces']])
            embed.add_field(name='*SUBRACES*', value=f'{subraces.lower()}', inline=False)

        return embed
