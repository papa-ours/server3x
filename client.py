from playerService import PlayerService
from gameService import GameService
from choiceService import ChoiceService

class Client():
  def __init__(self, game, names):
    self._playerService = PlayerService(names = names)
    self._gameName = game.getName()
    self._gameService = GameService([game])
    self._choiceService = ChoiceService(game.count() / 2)
    self._pickedPlayers = []
    self._playerChoices = {}

  def getGame(self):
    return self._gameService.getGame(self._gameName)

  def validateParameters(self, numberOfChoices, numberOfBlocks):
    validation = self._choiceService.setNumberOfChoices(numberOfChoices)
    if type(validation) is str:
      return validation
    validation = self._choiceService.setNumberOfBlocks(numberOfBlocks)
    if type(validation) is str:
      return validation
    return True

  def getRandomPlayer(self, players):
    return self._playerService.randomPlayer(players)
    
  def getNextTurn(self):
    pickingPlayer = self.getRandomPlayer(self._pickedPlayers)
    if pickingPlayer is None:
      return None

    self._pickedPlayers.append(pickingPlayer)
    blockingPlayer = self.getRandomPlayer([pickingPlayer])
    game = self.getGame()
    game.unblockAll()
    choices = game.getRandomChoices(self._choiceService.getNumberOfChoices())
    self._playerChoices[pickingPlayer.getName()] = choices

    return {
      'picking': pickingPlayer.getName(),
      'blocking': blockingPlayer.getName(),
      'choices': self.formatChoices(choices),
      'numberOfBlocks': self._choiceService.getNumberOfBlocks(),
    }

  def formatChoices(self, choices):
    return list(map(lambda c: {'name': c, 'blocked': self.getGame().isBlocked(c)}, choices))
  
  def blockChoices(self, choiceNames):
    for choiceName in choiceNames:
      self._gameService.blockChoice(self.getGame().getName(), choiceName)

  def pickChoice(self, playerName, choiceName):
    player = self._playerService.getPlayer(playerName)
    self._gameService.pickChoice(self.getGame().getName(), choiceName, player)
    print(self._playerService)

  def getChoicesForPlayer(self, playerName):
    if playerName not in self._playerChoices:
      return []
    return self.formatChoices(self._playerChoices[playerName])

  def getResults(self):
    results = {}
    for playerName in self._playerChoices:
      results[playerName] = self._playerService.getPlayer(playerName).getChoice()
    return results