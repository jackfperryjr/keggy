import random

class Responses:
  def __init__(self):
    self.positiveMessages = [
      'Here you go! 🍺',
      'Coming right up! 🍺',
      'Oh, uh, sorry... I\'m all out!',
      '🍺',
      'Sure! 🍺',
      'Did someone ask for a beer? 🍺',
      'One for you! And one for you! 🍺🍺',
      'Beers all around! 🍺🍺🍺'
    ]

    self.emojis = {
      'base': '🍺',
      'random': ['🍺','🍸','🍷','🥃','🍹','☕']
    }

    self.fritzMessages = [

    ]

  def getRandomPositiveMessage(self):
    return random.choice(self.positiveMessages)

  def getRandomFritzMessage(self):
    return  random.choice(self.fritzMessages)
  
  def getRandomEmoji(self):
    return random.choice(self.emojis['random'])
  
  def getBeerEmoji(self):
    return self.emojis['base']