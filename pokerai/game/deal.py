"""Contains logic for a deal, i.e. the entire sequence of four betting rounds.
"""
import deuces.deck

class Deal(object):
  """Contains logic about one deal of poker.
  """

  def __init__(self, players, dealer_idx, blind=1):
    self._players = players
    self._dealer_idx = dealer_idx
    self._deck = deuces.deck.Deck()
    self._blind = blind


  def Execute(self):
    """Executes the deal by dealing hole cards, requesting bets, dealing the
    flop, requesting bets, etc. until somebody wins.
    """
    # deal out hole cards
    for p in self._players:
      p.SetHoleCards(self._deck.draw(2))

    # preflop betting
    # TODO


