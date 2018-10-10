"""Various events that may happen in a poker round.
"""

class PlayerEvent(object):
  """Base class for an event triggered by a player
  """

  def __init__(self, player):
    """

      Args:
        player: (Player) the player who triggered the event

    """
    self._player = player


class FoldEvent(object):
  """Event for when a player folds.
  """
  pass

#TODO

