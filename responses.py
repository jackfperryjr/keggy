import random

class Responses:
  def __init__(self):
    self.positiveMessages = [
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

    self.fritzMessages = [
      "`101 Error: Drink Overflow...`",
      "`404 Error: Drink Not Found...`",
      "`500 Error: Internal Server Error.  I will try to serve you later...`",
      "`I'm sorry, Dave, but I'm afraid I can't do that...`",
      "`Leak detected 💦💦💦`",
      "`Laughter logic board misfiring on pin 4: Sorting out brew-haha.`",
    ]

  def getRandomPositiveMessage(self):
    return random.choice(self.positiveMessages)

  def getRandomFritzMessage(self):
    return  random.choice(self.fritzMessages)
  
  def getRandomEmoji(self):
    return random.choice(self.emojis["random"])
  
  def getBeerEmoji(self):
    return self.emojis["base"]