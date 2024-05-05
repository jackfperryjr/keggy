import random

class Kegerator:
  def __init__(self):
    self.store = {
      "fritz": 0
    }

  ### Fritz Mechanics
  def addFritz(self):
    print("Fritz: ", self.getStoreValue("fritz"))
    self.updateStore("fritz", self.getStoreValue("fritz") + 0.01)

  def checkFritz(self):
    self.addFritz()
    return self.getStoreValue("fritz") >= random.random()

  def resetFrtiz(self):
    self.updateStore("fritz", 0)

  ### Generic Operations: Read, Write, Update
  def updateStore(self, key, value):
    self.store[key] = value

  def getStore(self):
    return self.store
  
  def getStoreValue(self, key):
    return self.store[key]
