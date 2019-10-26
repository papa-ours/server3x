from termcolor import cprint
from player import Player
from PyInquirer import prompt
import random

class PlayerService:
  @staticmethod
  def asNameSet(players):
    return set(map(lambda p: p.getName(), players))

  def __init__(self, maxPlayers = -1, names = []):
    self._maxPlayers = maxPlayers
    self._numberOfPlayers = 0
    self._players = list(map(lambda name: Player(name), names))

  def __str__(self):
    s = ''
    i = 0
    for player in self._players:
      s += str(player) + '\n'
      i += 1
    return s

  def getNames(self):
    return list(map(lambda p: p.getName(), self._players))

  def validateNumberOfPlayers(self, n):
    try:
      n = int(n)
      if n <= 0:
        return 'Must have at least one player'
      elif n > self._maxPlayers:
        return 'Number of players must be less or equal to ' + str(self._maxPlayers)
      return True        
    except ValueError:
      return 'Number of players must be a number'

  def askNumberOfPlayers(self):
    questions = [
      {
        'type': 'input',
        'message': 'Number of players',
        'name': 'n_players',
        'validate': self.validateNumberOfPlayers
      }
    ]
    answers = prompt(questions)
    self._numberOfPlayers = int(answers['n_players'])

  def askPlayersName(self):
    while len(self._players) < self._numberOfPlayers:
      try:
        name = self.askPlayerName(len(self._players) + 1)
        self._players.append(Player(name))
      except ValueError:
        continue

  def hasPlayer(self, name):
    return self.getNames().count(name) > 0

  def validatePlayerName(self, name):
    playerValidation = Player.validateName(name)
    if type(playerValidation) is str:
      return playerValidation
    return 'Player\'s name must be unique' if self.hasPlayer(name) else True

  def askPlayerName(self, n):
    questions = [
      {
        'type': 'input',
        'message': 'Name for player ' + str(n),
        'name': 'name',
        'validate': self.validatePlayerName
      }
    ]
    return prompt(questions)['name']

  def getPlayer(self, name):
    if self.hasPlayer:
      return self._players[self.getNames().index(name)]
    return None

  def randomPlayer(self, players):
    names = PlayerService.asNameSet(self._players) - PlayerService.asNameSet(players)
    if len(names) is 0:
      return None
    index = random.randint(0, len(names) - 1)
    return self.getPlayer(list(names)[index])

  def getPlayers(self):
    return list(map(lambda player: player.getName(), self._players))