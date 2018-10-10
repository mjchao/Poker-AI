"""Contains logic for players at a poker table
"""

class Action(object):
  """Enum for actions a player can make.
  """
  FOLD = 1
  CHECK = 2
  CALL = 3
  BET = 4
  RAISE = 5


class Player(object):
  """Base class representing a player:
    * The cards the player has.
    * The money the player has.
    * Hooks for events where another player folds, checks, calls, bets, raises,
      and for requesting the player to make a decision and for notifying when
      the round is over.

    The player always folds.
  """

  def __init__(self):
    pass

  def OnFolded(self, round_data, event):
    """Callback for when another player folds.

    Args:
      round_data: (RoundData) Details of the current round after the player
        folded.
      event: (Event) Details about the fold.
    """
    pass

  def OnChecked(self, round_data, event):
    """Callback for when another player checks.

    Args:
      round_data: (RoundData) Details of the current round after the player
        checked.
      event: (Event) Details about the check.
    """
    pass

  def OnCalled(self, round_data, event):
    """Callback for when another player calls.

    Args:
      round_data: (RoundData) Details of the current round after the player
        called.
      event: (Event) Details about the call.
    """
    pass

  def OnBet(self, round_data, event):
    """Callback for when another player bet.

    Args:
      round_data: (RoundData) Details of the current round after the player
        bet.
      event: (Event) Details about the bet.
    """
    pass

  def OnRaised(self, round_data, event):
    """Callback for when another player makes a decision.

    Args:
      round_data: (RoundData) Details of the current round after the player
        raised.
      event: (Event) Details about the raise.
    """
    pass

  def MakeDecision(self, round_data):
    """Callback for when it's time for the player to make a decision.

    Args:
      round_data: (RoundData) Details of the current round.

    Return:
      (Action) FOLD, CALL, CHECK, BET, or RAISE.
    """
    return Action.FOLD

  def OnRoundOver(self, round_data, event):
    """Callback for when the round is over.

    Args:
      round_data: (RoundData) Details of the current round.
      event: (Event) Details about the ending of the round (i.e. who won)
    """
    pass

