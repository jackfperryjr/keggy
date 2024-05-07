import re

class Utils:
    def __init__(self):
        self.conversion_rates = {
        'pp': 1000,
        'gp': 100,
        'ep': 50,
        'sp': 10,
        'cp': 1
        }

    def get_stat_mod(stat_value):
        mod = (stat_value-10) // 2
        if mod >= 0:
            return f'{stat_value} (+{mod})'
        else:
            return f'{stat_value} ({mod})'

    async def is_message_blocked(message):
    # Blocks the bot from responding to itself
    if message.author == bot.user:
        return True

    # Blocks on Fritz
    if bot.user.mentioned_in(message) and keggy_store.checkFritz():
        keggy_store.resetFrtiz()
        await message.add_reaction("❌")
        await message.channel.send(responses.getRandomFritzMessage())
        return True

    return False

    def convert_to_copper(self, currency_string):
    matches = re.findall(r'(\d+)(pp|gp|ep|sp|cp)', currency_string)
    if not matches:
        return int(currency_string)

    # Convert each match to copper and sum them up
    total_copper = sum(int(number) * self.conversion_rates[currency] for number, currency in matches)
    return total_copper

    def split_copper(self, copper, shares):
    split = copper // shares
    remainder = copper % shares
    return split, remainder

    def convert_to_currency(self, copper):
    currency = {}
    for key, value in self.conversion_rates.items():
        currency[key] = copper // value
        copper %= value
    return currency
