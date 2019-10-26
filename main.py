from playerService import PlayerService
from gameService import GameService
from choiceService import ChoiceService
from termcolor import cprint

def main():
  try:
    gameService = GameService()
    game = gameService.askGame()

    # Create players
    playerService = PlayerService(game.getMaxPlayers())
    playerService.askNumberOfPlayers()
    playerService.askPlayersName()

    # Ask game parameters
    choiceService = ChoiceService(game.count() / 2)
    choiceService.askNumberOfChoices()
    choiceService.askNumberOfBlocks()

    # Picking process for every player
    players = []
    pickingPlayer = playerService.randomPlayer(players)
    while pickingPlayer is not None:
      # Generate random choices
      game.unblockAll()
      choices = game.getRandomChoices(choiceService.getNumberOfChoices())

      # Pick a blocking player and ask him to block a choice
      blockingPlayer = playerService.randomPlayer([pickingPlayer])
      blocks = gameService.askBlockChoice(game, choices, blockingPlayer, pickingPlayer, choiceService.getNumberOfBlocks())
      for block in blocks:
        gameService.blockChoice(game.getName(), block)

      # Ask picking player to select a choice
      choice = gameService.askPickChoice(game, choices, pickingPlayer)
      gameService.pickChoice(game.getName(), choice, pickingPlayer)

      # Pick a new picking player
      players.append(pickingPlayer)
      pickingPlayer = playerService.randomPlayer(players)

    cprint('\n\033[1mChoices are locked in\033[0;0m', 'green')
    print(playerService)
  except KeyError:
    exit(0)

if __name__ == "__main__":
  main()