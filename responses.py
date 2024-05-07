import random

class Responses:
  def __init__(self):
    self.positive_messages = [
      "`Here you go! 🍺`",
      "`Coming right up! 🍺`",
      "`Oh, uh, sorry... I'm all out!`",
      "`🍺`",
      "`Sure! 🍺`",
      "`Did someone ask for a beer? 🍺`",
      "`One for you! And one for you! 🍺🍺`",
      "`Beers all around! 🍺🍺🍺`"
    ]

    self.emojis = {
      "base": "🍺",
      "random": ["🍺","🍸","🍷","🥃","🍹","☕"]
    }

    self.fritz_messages = [
      "`101 Error: Drink Overflow...`",
      "`404 Error: Drink Not Found...`",
      "`500 Error: Internal Server Error.  I will try to serve you later...`",
      "`I'm sorry, Dave, but I'm afraid I can't do that...`",
      "`Leak detected 💦💦💦`",
      "`Laughter logic board misfiring on pin 4: Sorting out brew-haha.`",
    ]

  def get_random_positive_message(self):
    return random.choice(self.positive_messages)

  def get_random_fritz_message(self):
    return  random.choice(self.fritz_messages)
  
  def get_random_emoji(self):
    return random.choice(self.emojis["random"])
  
  def get_beer_emoji(self):
    return self.emojis["base"]