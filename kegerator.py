import random

class Kegerator:
  def __init__(self):
    self.store = {
      "fritz": 0,
      "last_command": "",
      "last_command_args": None
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

  ### Update Last Command for Rerun
  def update_last_command(self, command, args):
    self.update_store("last_command", command)
    self.update_store("last_command_args", args)

  ### Generic Operations: Read, Write, Update
  def update_store(self, key, value):
    self.store[key] = value

  def get_store(self):
    return self.store
  
  def get_store_value(self, key):
    return self.store[key]
  