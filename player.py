class Player:
  MIN_NAME_LENGTH = 2
  MAX_NAME_LENGTH = 16

  @staticmethod
  def validateName(name):
    return 'Player\'s name length must be between ' + str(Player.MIN_NAME_LENGTH) + ' and ' + str(Player.MAX_NAME_LENGTH)\
      if (len(name) < Player.MIN_NAME_LENGTH or len(name) > Player.MAX_NAME_LENGTH) else True

  def __init__(self, name):
    self._name = name
    self._choice = None

  def __str__(self):
    s = self._name
    if self._choice is not None:
      s += ' (' + self._choice.getName() + ')'
    return s

  def pickChoice(self, choice):
    self._choice = choice
    choice.pick()

  def getChoice(self):
    if self._choice is None:
      return ''
    return self._choice.getName()
  
  def getName(self):
    return self._name