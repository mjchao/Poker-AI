"""Contains logic for everything going on at a poker table.
"""
import game.round

class Table(object):
  """Represents a poker table:
    * Dealer logic
    * Pot logic
    * Player logic
    * Determining a winner
  """

  def __init__(self):
    self._round = Round()

