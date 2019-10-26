from choice import Choice
import random

class Game:
  def __init__(self, name, names, maxPlayers):
    self._name = name
    self._choices = list(map(lambda n: Choice(n), names))
    self._maxPlayers = maxPlayers

  def __str__(self):
    s = self._name + ':\n'
    for choice in self._choices:
      s += '\t - ' + choice.getName()
      if choice.isBlocked():
        s += ' [BLOCKED]'
      elif choice.isPicked():
        s += ' [PICKED]'
      s += '\n'

    return s

  def getMaxPlayers(self):
    return self._maxPlayers

  def count(self):
    return len(self._choices)

  def getChoices(self):
    return list(map(lambda c:c.getName(), self._choices))

  def getRandomChoices(self, n):
    choices = []
    availableChoices = list(filter(lambda c: c.isAvailable(), self._choices))
    while len(choices) < n:
      index = random.randint(0, len(availableChoices) - 1)
      name = availableChoices[index].getName()
      if choices.count(name) > 0:
        continue
      choices.append(availableChoices[index].getName())
    return choices
  
  def getMaxPlayers(self):
    return self._maxPlayers

  def hasChoice(self, name):
    return self.getChoices().count(name) > 0

  def addChoice(self, name):
    if not self.hasChoice(name):
      self._choices.append(Choice(name))

  def getChoice(self, name):
    if not self.hasChoice(name):
      return None
    return self._choices[self.getChoices().index(name)]

  def getName(self):
    return self._name

  def isBlocked(self, name):
    if not self.hasChoice(name):
      return True  
    return self.getChoice(name).isBlocked()
  
  def getChoiceIndex(self, name):
    if not self.hasChoice(name):
      return -1
    return self.getChoices().index(name)

  def blockChoice(self, name):
    if self.hasChoice(name):
      self._choices[self.getChoiceIndex(name)].block()

  def unblockAll(self):
    for choice in self._choices:
      choice.unblock()