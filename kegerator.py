import random

class Kegerator:
  def __init__(self):
    self.store = {
      "fritz": 0
    }

  ### Fritz Mechanics
  def add_fritz(self):
    self.update_store("fritz", self.get_store_value("fritz") + 1)
    print("Fritz chance at", self.get_store_value("fritz"), "percent.")

  def check_fritz(self):
    self.add_fritz()
    return self.get_store_value("fritz") >= random.randint(1, 100)

  def reset_frtiz(self):
    self.update_store("fritz", 0)

  ### Generic Operations: Read, Write, Update
  def update_store(self, key, value):
    self.store[key] = value

  def get_store(self):
    return self.store
  
  def get_store_value(self, key):
    return self.store[key]
