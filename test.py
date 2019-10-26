import unittest
from gameService import GameService
from player import Player
class TestGameService(unittest.TestCase):
  def testBlockChoice(self):
    service = GameService()
    player = Player('Vincent')
    service.pickChoice('NHL', 'Canadiens', player)
    service.blockChoice('NHL', 'Sharks')
    service.blockChoice('NHL', 'Capitals')
    service.blockChoice('Fifa', 'FC Barcelone')
    service.blockChoice('Madden', 'Rams')
    service.blockChoice('Fifa', 'Tottenham')
    self.assertTrue(service.getGame('Fifa').isBlocked('Tottenham'))
    print(service)
    print('\n\n')
    print(player.getChoice())
if __name__ == '__main__':
  unittest.main()