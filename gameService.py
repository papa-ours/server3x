from game import Game
from PyInquirer import prompt
from games import GAMES
import random
from termcolor import cprint

class GameService:
  def __init__(self, games = []):
    self._games = games if len(games) is not 0 else\
      [Game(g['name'], g['choices'], g['max']) for g in GAMES]

  def __str__(self):
    s = ''
    for game in self._games:
      s += str(game)

    return s + '\n'

  def getGamesInfo(self):
    return list(map(self.getGameInfo, self._games))

  def getGameInfo(self, game):
    return {
      'name': game.getName(),
      'maxPlayers': game.getMaxPlayers()
    }

  def getNames(self):
    return list(map(lambda game: game.getName(), self._games))

  def getNamesLower(self):
    return list(map(lambda game: game.getName().lower(), self._games))

  def hasGame(self, name):
    return self.getNamesLower().count(name.lower()) > 0

  def getGame(self, name):
    if not self.hasGame(name):
      return None
    return self._games[self.getGameIndex(name)]

  def getGameIndex(self, name):
    if not self.hasGame(name):
      return -1
    return self.getNamesLower().index(name.lower())

  def blockChoice(self, gameName, choiceName):
    if self.hasGame(gameName):
      self.getGame(gameName).blockChoice(choiceName)
 
  def getGames(self):
    return self._games

  def pickChoice(self, gameName, choiceName, player):
    if self.hasGame(gameName):
      player.pickChoice(self.getGame(gameName).getChoice(choiceName))

  def askGame(self):
    questions = [
      {
        'type': 'list',
        'message': 'Select a game',
        'name': 'game',
        'choices': self.getNames()
      }
    ]
    return self.getGame(prompt(questions)['game'])

  def formatChoices(self, game, choices):
    formatted = []
    for choiceName in choices:
      choice = game.getChoice(choiceName)
      if choice.isBlocked():
        formatted.append({
          'name': choiceName,
          'disabled': 'Blocked'
        })
      else:
        formatted.append(choiceName)
    return formatted

  def formatBlocks(self, game, choices):
    choices = self.formatChoices(game, choices)
    blocks = []
    for choice in choices:
      if type(choice) == dict:
        blocks.append(choice)
      else:
        blocks.append({'name': choice})
    return blocks

  def askPickChoice(self, game, choices, player):
    questions = [
      {
        'type': 'list',
        'message': player.getName() + ', pick a choice',
        'name': 'choice',
        'choices': self.formatChoices(game, choices)
      }
    ]
    return prompt(questions)['choice']

  def blockRandomChoice(self, game, choices):
    while True:
      index = random.randint(0, len(choices) - 1)
      if game.getChoice(choices[index]).isAvailable():
        return choices[index]

  def askBlockChoice(self, game, choices, blockingPlayer, pickingPlayer, numberOfBlocks):
    if blockingPlayer is None:
      return [self.blockRandomChoice(game, choices) for _ in range(numberOfBlocks)]

    while True:
      questions = [
        {
          'type': 'checkbox',
          'message': blockingPlayer.getName() + ', block ' + str(numberOfBlocks) +\
            (' choice' if numberOfBlocks == 1 else ' choices') + ' to ' + pickingPlayer.getName(),
          'name': 'choice',
          'choices': self.formatBlocks(game, choices)
        }
      ]
      blocks = prompt(questions)['choice']

      if len(blocks) is not numberOfBlocks:
        cprint('You must block exactly ' + str(numberOfBlocks) +\
          (' choice' if numberOfBlocks == 1 else ' choices'), 'red')
        continue

      return blocks