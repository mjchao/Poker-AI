"""Contains logic for everything going on at a poker table.
"""
import pokerai.game.deal
import random

class Table(object):
  """Represents a poker table:
    * Dealer logic
    * Pot logic
    * Player logic
    * Determining a winner
  """

  def __init__(self, players, dealer_idx):
    """Creates a new poker table.

    Args:
      players: (list of Player) The players at the poker table
      dealer_idx: (int) The player who should begin as the dealer.
    """
    self._players = players
    self._round = pokerai.game.deal.Deal(dealer_idx)

