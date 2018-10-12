import unittest
import pokerai.game.player
import pokerai.game.deal
import pokerai.mocks.player

class DealTest(unittest.TestCase):

  def _CreateDeal(self, players):
    """Creates a generic deal to be tested. 0 is always the dealer.

    Args:
      players: (list of MockPlayer) Mock players for testing
    """
    return pokerai.game.deal.Deal(players, 0)

  def testConstruction(self):
    actions = [[("raise", 10)], ["fold"]]
    players = pokerai.mocks.player.CreateMockPlayers(actions)
    deal = self._CreateDeal(players)
    deal.Execute()


if __name__ == "__main__":
  unittest.main()

