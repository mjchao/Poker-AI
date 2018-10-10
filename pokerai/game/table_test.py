import unittest
import pokerai.game.player
import pokerai.game.table
import pokerai.mocks.player

class TableTest(unittest.TestCase):

  def _CreateTable(self, players):
    """Creates a generic table to be tested. 0 is always the dealer.

    Args:
      players: (list of MockPlayer) Mock players for testing
    """
    return pokerai.game.table.Table(players, 0)

  def testConstruction(self):
    actions = [[("bet", 10)], ["fold"]]
    players = pokerai.mocks.player.CreateMockPlayers(actions)
    self._CreateTable(players)


if __name__ == "__main__":
  unittest.main()

